"""Drift detection: compares an existing PROJECT-CONTEXT.md with current repository evidence.

Read-only. It reuses the scanner and detectors, so the same exclusions and secret protection apply.
It never writes a file. Materiality is a category (Material, Potentially Material, Informational);
there are no scores.

Two kinds of comparison:
  * capability terms (Docker, PostgreSQL, Jest, GitHub Actions ...) found in the context text and in
    current evidence. Works on any context, including hand-written ones.
  * structural statements (components, workflows, top-level directories ...) compared by the
    generator's own statement format. Used only when the context contains such statements.
"""
from __future__ import annotations

import datetime
import os
import re
import subprocess
from dataclasses import dataclass, field

from . import VERSION
from .catalog import SOURCE_EXTS
from .model import UNKNOWN

MATERIAL, POTENTIAL, INFO = "Material", "Potentially Material", "Informational"
CATEGORIES = ["Technology", "Architecture", "API", "Database", "Build", "Testing", "Infrastructure", "CI/CD", "Observability"]
# Statements in these categories describe what the repository is. Adding or removing one makes the context wrong.
CORE = {"Technology", "Architecture", "API", "Database", "Infrastructure", "CI/CD"}

_DOC_PREFIX = "README states"
# Sections whose text is not evidence of a capability (commands, prose rules, overview).
# Statements that list directory or file names. A directory called "terraform" is not Terraform evidence.
_LISTING_PREFIXES = ("Top-level directories", "Directories with", "Sibling directories", "Scripts directory", "Documentation directories",
                     "Source file types", "Project manifests", "Test files found", "Repository appears",
                     "Sensitive files present", "Configuration keys with", "Dockerfile base images", "Dockerfile exposes")
_SKIP_SECTIONS = {"Build and Run", "Project Overview", "Constraints", "Coding Conventions", "Development Workflow", "Known Unknowns"}
_SECTION_CATEGORY = {"Technology Stack": "Technology", "Frontend": "Technology", "Security": "Technology", "API": "API",
                     "Database": "Database", "Testing": "Testing", "Observability": "Observability",
                     "Infrastructure": "Infrastructure", "CI/CD": "CI/CD", "Architecture": "Architecture"}


@dataclass(frozen=True)
class Term:
    label: str
    category: str
    family: str
    rx: re.Pattern


def _t(label, category, pattern, family="", cs=False):
    return Term(label, category, family, re.compile(pattern if cs else "(?i)" + pattern))


TERMS = [
    _t("React", "Technology", r"\breact\b", "frontend"), _t("Angular", "Technology", r"\bangular\b", "frontend"),
    _t("Vue", "Technology", r"\bvue(?:\.js)?\b", "frontend"), _t("Svelte", "Technology", r"\bsvelte\b", "frontend"),
    _t("Next.js", "Technology", r"\bnext\.?js\b"), _t("Express", "Technology", r"\bExpress\b", cs=True),
    _t("NestJS", "Technology", r"\bnestjs\b"), _t("Fastify", "Technology", r"\bfastify\b"),
    _t("ASP.NET Core", "Technology", r"\basp\.net\b"), _t("Entity Framework", "Technology", r"\bentity framework\b|\bef core\b"),
    _t("Spring", "Technology", r"\bSpring\b", cs=True), _t("Django", "Technology", r"\bdjango\b"),
    _t("Flask", "Technology", r"\bFlask\b", cs=True), _t("FastAPI", "Technology", r"\bfastapi\b"),
    _t("TypeScript", "Technology", r"\btypescript\b"),
    _t("Node.js", "Technology", r"\bnode\.?js\b"), _t("Python", "Technology", r"\bpython\b"),
    _t("Java", "Technology", r"\bJava\b", cs=True), _t("Go", "Technology", r"\bGo\b", cs=True),
    _t(".NET", "Technology", r"(?<![\w])\.net\b|\bdotnet\b"),
    _t("PostgreSQL", "Database", r"\bpostgres(?:ql)?\b|\bnpgsql\b", "database"), _t("MySQL", "Database", r"\bmysql\b", "database"),
    _t("MariaDB", "Database", r"\bmariadb\b", "database"), _t("SQL Server", "Database", r"\bsql ?server\b", "database"),
    _t("Oracle", "Database", r"\bOracle\b", "database", cs=True), _t("MongoDB", "Database", r"\bmongo(?:db)?\b", "database"),
    _t("SQLite", "Database", r"\bsqlite\b", "database"),
    _t("OpenAPI", "API", r"\bopenapi\b|\bswagger\b|\bswashbuckle\b"), _t("GraphQL", "API", r"\bgraphql\b"),
    _t("gRPC / Protocol Buffers", "API", r"\bgrpc\b|protocol buffers"),
    _t("Jest", "Testing", r"\bjest\b", "test framework"), _t("Vitest", "Testing", r"\bvitest\b", "test framework"),
    _t("Mocha", "Testing", r"\bmocha\b", "test framework"), _t("pytest", "Testing", r"\bpytest\b", "test framework"),
    _t("xUnit", "Testing", r"\bxunit\b", "test framework"), _t("NUnit", "Testing", r"\bnunit\b", "test framework"),
    _t("JUnit", "Testing", r"\bjunit\b", "test framework"),
    _t("Playwright", "Testing", r"\bplaywright\b"), _t("Cypress", "Testing", r"\bcypress\b"),
    _t("OpenTelemetry", "Observability", r"\bopentelemetry\b"), _t("Serilog", "Observability", r"\bserilog\b"),
    _t("Prometheus", "Observability", r"\bprometheus\b"), _t("Sentry", "Observability", r"\bsentry\b"),
    _t("Application Insights", "Observability", r"\bapplication ?insights\b"), _t("Datadog", "Observability", r"\bdatadog\b"),
    _t("Docker", "Infrastructure", r"\bdocker(?:file)?s?\b|\bcompose\b"), _t("Kubernetes", "Infrastructure", r"\bkubernetes\b|\bk8s\b"),
    _t("Helm", "Infrastructure", r"\bhelm\b"), _t("Kustomize", "Infrastructure", r"\bkustomize\b"),
    _t("Terraform", "Infrastructure", r"\bterraform\b"), _t("Bicep", "Infrastructure", r"\bbicep\b"),
    _t("Pulumi", "Infrastructure", r"\bpulumi\b"), _t("CloudFormation", "Infrastructure", r"\bcloudformation\b"),
    _t("GitHub Actions", "CI/CD", r"\bgithub actions\b", "ci"), _t("Jenkins", "CI/CD", r"\bjenkins(?:file)?\b", "ci"),
    _t("GitLab CI", "CI/CD", r"\bgitlab\b", "ci"), _t("Azure Pipelines", "CI/CD", r"\bazure pipelines\b", "ci"),
    _t("CircleCI", "CI/CD", r"\bcircleci\b", "ci"), _t("Travis CI", "CI/CD", r"\btravis\b", "ci"),
    _t("Buildkite", "CI/CD", r"\bbuildkite\b", "ci"),
    _t("npm", "Build", r"\bnpm\b", "package manager"), _t("Yarn", "Build", r"\byarn\b", "package manager"),
    _t("pnpm", "Build", r"\bpnpm\b", "package manager"), _t("Maven", "Build", r"\bmaven\b"), _t("Gradle", "Build", r"\bgradle\b"),
]
_DEP = re.compile(r"^(.+?): declared as a dependency$")
_RUNTIME = re.compile(r"^(Node\.js|Python|Java|Go|\.NET)\b[^:]*?\b(?:version|target frameworks?)\b[^:]*:\s*(.+)$", re.I)
_RUNTIME_PLAIN = re.compile(r"^(Node\.js|Python|Java|Go|\.NET)\s+v?(\d[\w.]*)", re.I)


@dataclass
class Unit:
    """One statement from either side of the comparison."""
    text: str
    section: str
    evidence: tuple = ()
    origin: str = "generated"
    classification: str = ""


@dataclass
class Drift:
    category: str
    materiality: str
    kind: str              # new | removed | changed | conflict
    text: str
    evidence: tuple = ()
    context: str = ""      # the context statement that is no longer supported, when there is one


@dataclass
class Analysis:
    findings: list = field(default_factory=list)
    notes: list = field(default_factory=list)      # informational lines
    last_reviewed: str = ""
    generator: str = ""
    generated: bool = False

    def by(self, materiality):
        return [f for f in self.findings if f.materiality == materiality]

    @property
    def status(self):
        if self.by(MATERIAL):
            return "DRIFT DETECTED"
        return "REVIEW RECOMMENDED" if self.by(POTENTIAL) else "NO DRIFT"

    @property
    def material(self):
        return bool(self.by(MATERIAL))


# ---- extraction ---------------------------------------------------------------------------------
def _usable(u: Unit) -> bool:
    return (u.classification != UNKNOWN and u.section not in _SKIP_SECTIONS
            and not u.text.startswith((_DOC_PREFIX,) + _LISTING_PREFIXES))


def _current_units(items) -> list:
    return [Unit(i.statement, i.section, i.evidence, i.origin, i.classification) for i in items]


def _context_units(parsed) -> list:
    units = [Unit(i.statement, i.section, i.evidence, i.origin, i.classification) for i in parsed.items]
    for sec, lines in parsed.freeform.items():
        for line in lines:
            text = re.sub(r"^\s*(?:[-*]\s+)?", "", line).strip()
            if text and not text.startswith("#"):
                units.append(Unit(text, sec, (), "generated", "freeform"))
    return units


def _terms(units) -> dict:
    """label -> {'term': Term or None, 'category', 'family', 'units': [Unit]}"""
    out = {}
    for u in units:
        if not _usable(u):
            continue
        hits = [t for t in TERMS if t.rx.search(u.text)]
        if hits:
            for t in hits:
                out.setdefault(t.label, {"category": t.category, "family": t.family, "units": []})["units"].append(u)
            continue
        m = _DEP.match(u.text)
        if m and u.section in _SECTION_CATEGORY:
            out.setdefault(m.group(1), {"category": _SECTION_CATEGORY[u.section], "family": "", "units": []})["units"].append(u)
    return out


def _norm_version(runtime: str, token: str) -> str:
    parts = [p for p in re.split(r"[._]", token) if p.isdigit()]
    if not parts:
        return ""
    if runtime in ("Node.js", ".NET"):
        return parts[0]
    if runtime == "Java":
        return parts[1] if parts[0] == "1" and len(parts) > 1 else parts[0]
    return ".".join(parts[:2])


def _runtimes(units) -> dict:
    out = {}
    for u in units:
        if u.section in _SKIP_SECTIONS or u.classification == UNKNOWN:
            continue
        for rx in (_RUNTIME, _RUNTIME_PLAIN):
            m = rx.match(u.text)
            if not m:
                continue
            name = {"node.js": "Node.js", "python": "Python", "java": "Java", "go": "Go", ".net": ".NET"}[m.group(1).lower()]
            toks = re.findall(r"(?<![\w.])(?:net|v)?(\d+(?:[._]\d+)*)", m.group(2))
            vers = {v for v in (_norm_version(name, t) for t in toks) if v}
            if vers:
                out.setdefault(name, {"versions": set(), "units": []})
                out[name]["versions"] |= vers
                out[name]["units"].append(u)
            break
    return out


def _ev(units, limit=3) -> tuple:
    seen = []
    for u in units:
        for e in u.evidence:
            if e not in seen:
                seen.append(e)
    return tuple(seen[:limit])


def _listed(units, prefix) -> set:
    """Elements of comma-separated statements that start with `prefix: `."""
    out = set()
    for u in units:
        if u.classification != UNKNOWN and u.text.startswith(prefix + ": "):
            body = u.text[len(prefix) + 2:].replace(" (and more)", "")
            out |= {e.strip() for e in body.split(", ") if e.strip()}
    return out


def _has(units, prefix) -> bool:
    return any(u.classification != UNKNOWN and u.text.startswith(prefix) for u in units)


# ---- comparison ---------------------------------------------------------------------------------
def _materiality(category, kind) -> str:
    return MATERIAL if category in CORE else POTENTIAL


def _compare_terms(ctx, cur, out: list):
    done = set()
    # conflicts: an exclusive family where the context and the repository name different members
    for fam in ("frontend", "database", "ci", "test framework", "package manager"):
        c = {l for l, v in ctx.items() if v["family"] == fam}
        r = {l for l, v in cur.items() if v["family"] == fam}
        if c and r and not (c & r):
            units = [u for l in c for u in ctx[l]["units"]]
            cat = ctx[sorted(c)[0]]["category"]
            dev = any(u.origin == "developer" for u in units)
            out.append(Drift(
                cat, MATERIAL if cat in CORE or fam == "test framework" else POTENTIAL, "conflict",
                f"Context conflict detected: the context names {', '.join(sorted(c))}; current repository evidence shows {', '.join(sorted(r))}."
                + (" The context entry is developer-provided and was not changed." if dev else ""),
                _ev([u for l in r for u in cur[l]["units"]]), units[0].text))
            done |= c | r
    for label in sorted(set(ctx) | set(cur)):
        if label in done:
            continue
        if label in cur and label not in ctx:
            v = cur[label]
            out.append(Drift(v["category"], _materiality(v["category"], "new"), "new",
                             f"New repository evidence detected: {label}. The existing context does not mention it.", _ev(v["units"])))
        elif label in ctx and label not in cur:
            v = ctx[label]
            if v["category"] == "Build":
                continue  # a tool named in prose or a command is too weak to call stale
            dev = all(u.origin == "developer" for u in v["units"])
            out.append(Drift(v["category"], POTENTIAL if dev else _materiality(v["category"], "removed"), "removed",
                             f"{label} is documented in the context but is no longer detected in the repository."
                             + (" The entry is developer-provided, so the repository may simply not show it." if dev else ""),
                             (), v["units"][0].text))


def _compare_runtimes(ctx, cur, out: list):
    for name in sorted(set(ctx) & set(cur)):
        a, b = ctx[name]["versions"], cur[name]["versions"]
        if a != b:
            out.append(Drift("Technology", MATERIAL if not (a & b) else POTENTIAL, "changed",
                             f"{name} version changed: the context records {', '.join(sorted(a))}; the repository declares {', '.join(sorted(b))}.",
                             _ev(cur[name]["units"]), ctx[name]["units"][0].text))


_IGNORED_DIRS = {"docs", "doc", "documentation", "test", "tests", "spec", "specs", "e2e", "examples", "samples", "scripts",
                 ".github", ".vscode", ".idea", ".claude", ".agents", ".devcontainer", ".husky", "templates", "evals"}
_MINOR_LANG = {"Shell", "PowerShell", "Batch", "CSS", "HTML", "SCSS"}

# (statement prefix, category, element noun)
_SETS = [
    ("Top-level directories", "Architecture", "top-level directory"),
    (".NET library projects", "Architecture", "library project"),
    (".NET test projects", "Testing", "test project"),
    ("Solution files", "Build", "solution file"),
    ("Lock files", "Build", "lock file"),
    ("Source file types present", "Technology", "source file type"),
    ("GitHub Actions workflows", "CI/CD", "workflow"),
    ("Dockerfiles", "Infrastructure", "Dockerfile"),
]


def _compare_sets(ctx_units, cur_units, out: list):
    for prefix, cat, noun in _SETS:
        # Only when both sides describe the set. A side with none is a capability appearing or
        # disappearing, which the capability comparison reports.
        if not (_has(ctx_units, prefix) and _has(cur_units, prefix)):
            continue
        a, b = _listed(ctx_units, prefix), _listed(cur_units, prefix)
        added, removed = sorted(b - a), sorted(a - b)
        if prefix == "Top-level directories":
            big = [d for d in added + removed if d.lower() not in _IGNORED_DIRS]
            minor = [d for d in added + removed if d.lower() in _IGNORED_DIRS]
            if len(big) >= 3:
                out.append(Drift(cat, MATERIAL, "changed", "Major repository restructuring: top-level directories changed "
                                 f"(added: {', '.join(added) or 'none'}; removed: {', '.join(removed) or 'none'}).", tuple(added[:3])))
            else:
                for d in big:
                    kind = "new" if d in added else "removed"
                    out.append(Drift(cat, POTENTIAL, kind, f"Top-level directory {d} {'appeared' if kind == 'new' else 'is no longer present'}.",
                                     (d,) if kind == "new" else (), "" if kind == "new" else f"Top-level directories: {d}"))
            if minor:
                out.append(Drift(cat, INFO, "changed", f"Documentation, test, script or tooling directories changed: {', '.join(sorted(minor))}."))
            continue
        for kind, elems in (("new", added), ("removed", removed)):
            for e in elems:
                level = INFO if prefix == "Source file types present" and any(m in e for m in _MINOR_LANG) else POTENTIAL
                text = f"New {noun} detected: {e}." if kind == "new" else f"{noun.capitalize()} {e} is documented but no longer detected."
                out.append(Drift(cat, level, kind, text, () if kind == "removed" else (e,), "" if kind == "new" else f"{prefix}: {e}"))


def _keyed(units, prefix) -> dict:
    """Statements with a per-item subject ('Workflow ci.yml: ...') grouped by subject."""
    out = {}
    for u in units:
        if u.classification != UNKNOWN and (u.section == prefix or u.text.startswith(prefix)):
            subject, _, value = u.text.partition(": ")
            out.setdefault(subject, []).append((value, u))
    return out


# (prefix, category, noun, compare values, boundary handled by capability terms, boundary materiality)
_KEYED = [
    ("Application Components", "Architecture", "application or project", False, False),
    ("Workflow ", "CI/CD", "workflow", True, True),
    ("Compose services (", "Infrastructure", "Compose file", True, True),
    ("Terraform providers declared", "Infrastructure", "Terraform providers", True, True),
    ("Terraform backend type", "Infrastructure", "Terraform backend", True, True),
    ("OpenAPI/Swagger definition (", "API", "API specification", True, True),
    ("Migration directory ", "Database", "migration directory", False, False),
]


def _compare_keyed(ctx_units, cur_units, generated: bool, out: list):
    for prefix, cat, noun, values, boundary_in_terms in _KEYED:
        a, b = _keyed(ctx_units, prefix), _keyed(cur_units, prefix)
        if prefix == "Application Components":
            if not generated:
                continue
        elif boundary_in_terms and not (a and b):
            continue
        for subj in sorted(set(a) | set(b)):
            name = subj.split(": ")[0]
            if subj in b and subj not in a:
                boundary = not a
                mat = MATERIAL if (cat == "Database" and boundary) else POTENTIAL
                out.append(Drift(cat, mat, "new", f"New {noun} detected: {name.replace('Workflow ', '').replace('Migration directory ', '')}"
                                 + (" (migration infrastructure introduced)." if cat == "Database" and boundary else "."),
                                 _ev([u for _, u in b[subj]])))
            elif subj in a and subj not in b:
                boundary = not b
                mat = MATERIAL if (cat in CORE and (prefix == "Application Components" or boundary)) else POTENTIAL
                out.append(Drift(cat, mat, "removed",
                                 f"{noun.capitalize()} {name.replace('Workflow ', '').replace('Migration directory ', '')} is documented but no longer detected.",
                                 (), a[subj][0][1].text))
            elif values:
                va, vb = sorted(v for v, _ in a[subj]), sorted(v for v, _ in b[subj])
                if va != vb:
                    out.append(Drift(cat, POTENTIAL, "changed", f"{noun.capitalize()} structure changed: {name}.",
                                     _ev([u for _, u in b[subj]]), a[subj][0][1].text))


def _missing_evidence(root, parsed, covered: set, out: list):
    """Confirmed statements whose cited files no longer exist. Skips categories already reported as removed or conflicting."""
    for it in parsed.items:
        if it.origin != "generated" or it.classification != "Confirmed" or it.section not in _SECTION_CATEGORY:
            continue
        if it.statement.startswith(_LISTING_PREFIXES) or _SECTION_CATEGORY[it.section] in covered:
            continue
        if any(t.rx.search(it.statement) for t in TERMS) or _DEP.match(it.statement):
            continue
        paths = [e for e in it.evidence if re.match(r"^[\w.@+/\-]+$", e) and ("/" in e or "." in e)]
        if paths and not any(os.path.exists(os.path.join(root, p)) for p in paths):
            cat = _SECTION_CATEGORY[it.section]
            out.append(Drift(cat, POTENTIAL if cat in CORE else INFO, "removed",
                             "A documented statement could not be confirmed: its cited files no longer exist.", (), it.statement))


# ---- freshness and version control ---------------------------------------------------------------
def _git(root, *args):
    try:
        env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
        r = subprocess.run(["git", "--no-optional-locks", "-C", str(root), *args], capture_output=True, text=True, timeout=20, env=env)
        return r.stdout if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def _classify_paths(paths) -> dict:
    counts = {"source": 0, "documentation": 0, "test": 0, "other": 0}
    for p in paths:
        low = p.lower()
        ext = os.path.splitext(low)[1]
        if ext in (".md", ".rst", ".txt") or low.startswith("docs/"):
            counts["documentation"] += 1
        elif re.search(r"(^|/)(tests?|spec|e2e|__tests__)(/|$)|[._]test\.|[._]spec\.|test_", low):
            counts["test"] += 1
        elif ext in SOURCE_EXTS:
            counts["source"] += 1
        else:
            counts["other"] += 1
    return counts


def _activity(root, since_rev, since_date) -> str | None:
    """Supporting evidence only: how much changed since the context was last reviewed. Git is optional."""
    if _git(root, "rev-parse", "--is-inside-work-tree") is None:
        return None
    if since_rev and re.fullmatch(r"[0-9a-fA-F]{7,40}", since_rev):
        out = _git(root, "diff", "--name-only", since_rev, "HEAD")
        basis = f"revision {since_rev[:12]}"
    elif since_date:
        out = _git(root, "log", f"--since={since_date}", "--name-only", "--pretty=format:")
        basis = f"{since_date}"
    else:
        return None
    if out is None:
        return None
    paths = sorted({l.strip() for l in out.splitlines() if l.strip()})
    if not paths:
        return f"No committed changes since {basis}."
    c = _classify_paths(paths)
    parts = [f"{n} {k}" for k, n in c.items() if n]
    return f"Files changed since {basis}: {', '.join(parts)}. File changes alone are not treated as drift."


def analyze(repo, cur_items, parsed, today: datetime.date, stale_after_days=None) -> Analysis:
    a = Analysis(last_reviewed=parsed.last_reviewed)
    raw = parsed.raw
    a.generated = "Generated by project-context" in raw
    m = re.search(r"(?m)^- Generated by:\s*project-context\s+(\S+)", raw)
    a.generator = m.group(1) if m else ""
    ctx_units, cur_units = _context_units(parsed), _current_units(cur_items)

    f: list = []
    _compare_terms(_terms(ctx_units), _terms(cur_units), f)
    _compare_runtimes(_runtimes(ctx_units), _runtimes(cur_units), f)
    _compare_sets(ctx_units, cur_units, f)
    _compare_keyed(ctx_units, cur_units, a.generated, f)
    _missing_evidence(repo.root, parsed, {x.category for x in f if x.kind in ("removed", "conflict")}, f)
    a.findings = _dedupe(f)

    # informational: build commands, freshness, generator version, version control activity
    if a.generated:
        old = {u.text for u in ctx_units if u.section == "Build and Run"}
        new = {u.text for u in cur_units if u.section == "Build and Run"}
        if old and old != new:
            a.notes.append(f"Documented commands differ from current evidence ({len(new - old)} new, {len(old - new)} no longer found).")
    try:
        age = (today - datetime.date.fromisoformat(parsed.last_reviewed)).days
        if stale_after_days and age > stale_after_days:
            a.notes.append(f"The context was last reviewed {age} days ago (configured threshold: {stale_after_days}). Age alone is not drift.")
    except ValueError:
        pass
    if a.generator and a.generator != VERSION:
        a.notes.append(f"The context was generated by project-context {a.generator}; this is version {VERSION}.")
    rev = re.search(r"(?m)^- Revision:\s*(\S+)", raw)
    try:
        since = datetime.date.fromisoformat(parsed.last_reviewed).isoformat()
    except ValueError:
        since = ""
    act = _activity(repo.root, rev.group(1) if rev else "", since)
    if act:
        a.notes.append(act)
    return a


def _dedupe(findings):
    seen, out = set(), []
    for f in findings:
        k = (f.category, f.kind, f.text)
        if k not in seen:
            seen.add(k)
            out.append(f)
    return out

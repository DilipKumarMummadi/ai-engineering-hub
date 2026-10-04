#!/usr/bin/env python3
"""Lightweight validation of the AI Engineering Hub Agent Plugin package (Agent Plugins 1.0.0).

Standard library only, read-only unless --sync is passed. It checks the manifest against the
canonical 1.0.0 rules, the skills/ layout, that skills/ matches its source (.claude/skills),
that only distributable content is in the package, and that nothing secret, repository-specific
or MCP-related is packaged. It proves packaging structure, not assistant behavior.

Usage: validate_plugin.py [--root PATH] [--sync]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts" / "project-context"))
from project_context.secrets import find_secrets  # noqa: E402


def inside(root: Path, candidate: Path) -> bool:
    c = candidate.resolve(strict=False)
    return c == root.resolve() or root.resolve() in c.parents

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
ALLOWED = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
AUTHOR_ALLOWED = {"name", "email", "url"}
NAME_RE = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
SOURCE = ".claude/skills"
# Directories that are part of the distributable package. Everything else at the repo root is Hub development tooling.
PACKAGED = ("skills", "com.github.copilot")
FORBIDDEN_NAMES = {"PROJECT-CONTEXT.md", ".env", "node_modules", ".git", "coverage", "dist", "build", "__pycache__"}
FORBIDDEN_PARTS = {"evals", "fixtures", "scripts"}
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
MCP_TYPES = {"stdio", "streamable-http", "sse"}
# Portable mcp.json is static definitions only. Credentials and connection details come from the client at runtime,
# so the file may not carry `headers` or `env` at all. (Client-specific wiring lives in .claude-plugin/plugin.json.)
FORBIDDEN_SUFFIX = (".pem", ".key", ".pfx", ".p12", ".log", ".pyc")


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    fail = errors.append

    # 1-5: manifest
    manifest = root / "plugin.json"
    if not manifest.is_file():
        return ["plugin.json: missing at plugin root"]
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"plugin.json: invalid JSON ({e})"]
    if not isinstance(data, dict):
        return ["plugin.json: must be a JSON object"]
    if data.get("$schema") != SCHEMA:
        fail(f"plugin.json: $schema must be {SCHEMA}")
    for k in data:
        if k not in ALLOWED:
            fail(f"plugin.json: field '{k}' is not a permitted core field")
    name = data.get("name")
    if not isinstance(name, str) or not (1 <= len(name) <= 64) or not NAME_RE.match(name):
        fail(f"plugin.json: invalid name {name!r}")
    if "version" in data and (not isinstance(data["version"], str) or not SEMVER_RE.match(data["version"])):
        fail(f"plugin.json: version {data['version']!r} is not semantic versioning")
    for k in ("description", "homepage", "repository", "license"):
        if k in data and not isinstance(data[k], str):
            fail(f"plugin.json: {k} must be a string")
    if "author" in data:
        a = data["author"]
        if not isinstance(a, dict) or set(a) - AUTHOR_ALLOWED or not all(isinstance(v, str) for v in a.values()):
            fail("plugin.json: author must be an object with string name/email/url only")
    if "keywords" in data and not (isinstance(data["keywords"], list) and all(isinstance(x, str) for x in data["keywords"])):
        fail("plugin.json: keywords must be an array of strings")
    if "extensions" in data and not (isinstance(data["extensions"], dict) and all(isinstance(v, dict) for v in data["extensions"].values())):
        fail("plugin.json: extensions must map namespaces to objects")

    # Claude Code installs through a marketplace; without this file `plugin marketplace add` fails
    mk = root / ".claude-plugin" / "marketplace.json"
    try:
        entries = json.loads(mk.read_text(encoding="utf-8")).get("plugins", [])
        if not any(e.get("name") == name and e.get("source") == "./" for e in entries):
            fail(f".claude-plugin/marketplace.json: must list plugin {name!r} with source './'")
    except (OSError, ValueError, AttributeError):
        fail(".claude-plugin/marketplace.json: missing or invalid (Claude Code cannot install the plugin without it)")

    _check_mcp(root, name, data, fail)

    # 6-7: skills layout and source agreement
    skills_dir = root / "skills"
    skills = {}
    if not skills_dir.is_dir():
        fail("skills/: missing")
    else:
        for p in sorted(skills_dir.iterdir()):
            if p.is_file():
                fail(f"skills/{p.name}: stray file; skills/ holds only skill directories")
                continue
            md = p / "SKILL.md"
            if not md.is_file():
                fail(f"skills/{p.name}: SKILL.md missing")
                continue
            text = md.read_text(encoding="utf-8")
            fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            fields = dict(re.findall(r"^([a-z-]+):\s*(.+)$", fm.group(1), re.M)) if fm else {}
            if fields.get("name") != p.name:
                fail(f"skills/{p.name}: frontmatter name must equal the directory name")
            if not fields.get("description"):
                fail(f"skills/{p.name}: frontmatter description missing")
            for extra in p.rglob("*"):
                if extra.is_file() and extra != md:
                    fail(f"skills/{p.name}/{extra.relative_to(p)}: unexpected extra file")
            skills[p.name] = text
    src = root / SOURCE
    if src.is_dir():
        src_skills = {p.name: (p / "SKILL.md").read_text(encoding="utf-8") for p in src.iterdir() if (p / "SKILL.md").is_file()}
        for n in sorted(set(src_skills) ^ set(skills)):
            fail(f"skills/{n}: present on only one side of {SOURCE} and skills/")
        for n in sorted(set(src_skills) & set(skills)):
            if src_skills[n] != skills[n]:
                fail(f"skills/{n}: differs from {SOURCE}/{n} (run with --sync)")

    # 8/13/14: referenced files and required docs
    for rel in ("README.md", "docs/plugin-architecture.md"):
        if not (root / rel).is_file():
            fail(f"{rel}: missing")
    for n, text in skills.items():
        for m in re.finditer(r"\]\(([^)#\s]+)(#[^)]*)?\)", re.sub(r"```.*?```", "", text, flags=re.S)):
            link = m.group(1)
            if link.startswith(("http", "mailto")):
                continue
            target = (skills_dir / n / link).resolve()
            if not target.exists() or skills_dir.resolve() not in target.parents:
                fail(f"skills/{n}: link {link} must resolve inside skills/")

    # 9-12/16: forbidden content inside the packaged directories and at the package root
    packaged = [root / "plugin.json", root / "README.md", root / "mcp.json", *(root / ".claude-plugin").glob("*.json")]
    packaged = [f for f in packaged if f.is_file()]
    for d in PACKAGED:
        if (root / d).is_dir():
            packaged += [f for f in (root / d).rglob("*") if f.is_file()]
    for f in packaged:
        rel = f.relative_to(root)
        if f.name in FORBIDDEN_NAMES or f.suffix in FORBIDDEN_SUFFIX or FORBIDDEN_NAMES & set(rel.parts) or FORBIDDEN_PARTS & set(rel.parts):
            fail(f"{rel}: must not be packaged")
        if f.suffix in (".md", ".json") and find_secrets(f.read_text(encoding="utf-8")):
            fail(f"{rel}: secret-like content")
    # exact-name match: rglob is case-insensitive on macOS and would hit docs/project-context.md
    for p in (x for x in root.rglob("*") if x.name in ("mcp.json", ".mcp.json") and x != root / "mcp.json"):
        if ".git" not in p.parts:
            fail(f"{p.relative_to(root)}: MCP configuration belongs only in the root mcp.json")
    for p in (x for x in root.rglob("*") if x.name == "PROJECT-CONTEXT.md"):
        if "templates" not in p.relative_to(root).parts and "fixtures" not in p.parts and ".git" not in p.parts:
            fail(f"{p.relative_to(root)}: repository-specific context must not be committed to the Hub package")
    return errors


def _check_mcp(root: Path, name, manifest: dict, fail) -> None:
    """mcp.json is optional. When present it must follow Agent Plugins 1.0.0 and carry no credential values."""
    claude = root / ".claude-plugin" / "plugin.json"
    mcp = root / "mcp.json"
    if claude.is_file():
        try:
            c = json.loads(claude.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return fail(".claude-plugin/plugin.json: invalid JSON")
        for k in ("name", "version"):
            if c.get(k) != manifest.get(k):
                fail(f".claude-plugin/plugin.json: {k} must equal plugin.json")
        for cmd in ([c["commands"]] if isinstance(c.get("commands"), str) else c.get("commands", [])):
            if not isinstance(cmd, str) or not cmd.startswith("./") or not inside(root, root / cmd) or not (root / cmd).is_file():
                fail(f".claude-plugin/plugin.json: commands entry {cmd!r} must be an existing file inside the plugin")
        ms = c.get("mcpServers")
        parts = ms if isinstance(ms, list) else ([ms] if ms is not None else [])
        if mcp.is_file() and "./mcp.json" not in parts:
            fail(".claude-plugin/plugin.json: mcpServers must include './mcp.json' so Claude Code loads the servers")
        for part in parts:
            if isinstance(part, dict):  # Claude-specific per-server override, e.g. a prompted token
                base = json.loads(mcp.read_text(encoding="utf-8")).get("mcpServers", {}) if mcp.is_file() else {}
                declared = set(c.get("userConfig", {}))
                for sname, s in part.items():
                    if sname not in base or s.get("url") != base[sname].get("url") or s.get("type") != base[sname].get("type"):
                        fail(f".claude-plugin/plugin.json: override '{sname}' must match a server in mcp.json (same type and url)")
                    for h, v in (s.get("headers") or {}).items():
                        m = re.fullmatch(r"(?:(?:Bearer|Basic) )?\$\{user_config\.([A-Za-z_][A-Za-z0-9_]*)\}", v) if isinstance(v, str) else None
                        if not m or m.group(1) not in declared or not c["userConfig"][m.group(1)].get("sensitive"):
                            fail(f".claude-plugin/plugin.json: override '{sname}' header '{h}' must be a ${{user_config.KEY}} of a sensitive userConfig option")
            elif part != "./mcp.json":
                fail(".claude-plugin/plugin.json: mcpServers entries must be './mcp.json' or a per-server override object")
    elif mcp.is_file():
        fail(".claude-plugin/plugin.json: missing; Claude Code would not load mcp.json")
    if not mcp.is_file():
        return
    try:
        d = json.loads(mcp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return fail(f"mcp.json: invalid JSON ({e})")
    if not isinstance(d, dict) or set(d) != {"$schema", "mcpServers"} or d.get("$schema") != MCP_SCHEMA or not isinstance(d["mcpServers"], dict):
        return fail(f"mcp.json: must contain exactly $schema ({MCP_SCHEMA}) and mcpServers")
    for sname, s in d["mcpServers"].items():
        where = f"mcp.json: server '{sname}'"
        if not isinstance(s, dict) or s.get("type") not in MCP_TYPES:
            fail(f"{where} needs a type of {sorted(MCP_TYPES)}")
            continue
        allowed = {"stdio": {"type", "command", "args", "cwd"}}.get(s["type"], {"type", "url"})
        for k in set(s) - allowed:
            why = "runtime configuration belongs to the client, not the portable file" if k in ("env", "headers") else f"not valid for type {s['type']}"
            fail(f"{where}: field '{k}' is not allowed ({why})")
        if s["type"] == "stdio":
            cmd = s.get("command")
            if not isinstance(cmd, str) or not cmd or re.search(r"\s", cmd):
                fail(f"{where}: command must be a single executable token")
            values = list(s.get("args", []))
        else:
            url = s.get("url", "")
            if not isinstance(url, str) or not url.startswith("https://") or "@" in url.split("/")[2] or re.search(r"(?i)[?&](token|key|secret|password|api_?key)=", url):
                fail(f"{where}: url must be https with no embedded credentials")
            values = []
        for v in values:
            if isinstance(v, str) and (find_secrets(v) or re.search(r"(?i)postgres(ql)?://[^\s$]*:[^\s$@]+@", v)):
                fail(f"{where}: secret-like value; credentials must never be in the portable file")


def sync(root: Path) -> None:
    dst = root / "skills"
    if dst.exists():
        shutil.rmtree(dst)
    for p in sorted((root / SOURCE).iterdir()):
        if (p / "SKILL.md").is_file():
            (dst / p.name).mkdir(parents=True)
            shutil.copy2(p / "SKILL.md", dst / p.name / "SKILL.md")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=HERE.parents[1])
    ap.add_argument("--sync", action="store_true", help="refresh skills/ from .claude/skills before validating")
    a = ap.parse_args()
    if a.sync:
        sync(a.root)
    errs = validate(a.root)
    for e in errs:
        print(f"  - {e}")
    n = len(list((a.root / "skills").glob("*/SKILL.md"))) if (a.root / "skills").is_dir() else 0
    print(f"checked: plugin.json, {n} skills, package contents")
    print("OK" if not errs else f"{len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())

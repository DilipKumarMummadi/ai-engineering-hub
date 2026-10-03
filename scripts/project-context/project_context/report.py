"""Generation report. Everything passes through the secret scrubber before it is shown."""
from __future__ import annotations

import difflib

from .model import CONFIRMED, INFERRED, UNKNOWN
from .secrets import scrub

_TECH = ("Technology Stack", "Frontend", "API", "Database", "Testing", "CI/CD", "Infrastructure", "Observability", "Security")
_ARCH = ("Repository Structure", "Architecture", "Application Components")


def _cap(lines, n=30):
    out = [f"  {l}" for l in lines[:n]]
    if len(lines) > n:
        out.append(f"  ... and {len(lines) - n} more")
    return out


def build(repo, result, items, mode, args, outcome, existing_text=None, new_text=None, stale_note=None):
    lines = [f"project-context {args.command}: {repo.root.name}", f"Mode: {mode}"]
    read = len(repo.read_log)
    sens = sum(1 for e in repo.files.values() if e.sensitive)
    ex = ", ".join(f"{k} x{v}" for k, v in sorted(repo.excluded_dirs.items())) or "none"
    lines += [
        f"Files considered: {len(repo.files)} (read: {read}; sensitive, not read: {sens}; binary skipped: {repo.skipped_binary}; too large skipped: {repo.skipped_large})",
        f"Excluded directories: {ex}",
    ]
    counts = {c: sum(1 for i in items if i.classification == c) for c in (CONFIRMED, INFERRED, UNKNOWN)}
    lines.append(f"Entries: {counts[CONFIRMED]} Confirmed, {counts[INFERRED]} Inferred, {counts[UNKNOWN]} Unknown")

    if args.dry_run:
        tech = [f"{i.statement} ({i.classification})" for i in items if i.section in _TECH and i.classification != UNKNOWN]
        arch = [f"{i.statement} ({i.classification})" for i in items if i.section in _ARCH and i.classification != UNKNOWN]
        lines += ["", "Detected technologies and tooling:"] + (_cap(tech, 40) or ["  none"])
        lines += ["", "Architecture and structure signals:"] + (_cap(arch, 30) or ["  none"])

    if result.update:
        lines += ["", "Changes against the existing context:"]
        lines += _cap([f"+ {s}" for s in result.added], 25) + _cap([f"~ {a}  ->  {b}" for a, b in result.changed], 25) + \
            _cap([f"- {s}" for s in result.removed], 25)
        if not (result.added or result.changed or result.removed):
            lines.append("  none")
        if result.preserved:
            lines.append(f"  Preserved developer-provided or manual entries: {len(result.preserved)}")
    if result.conflicts:
        lines += ["", "Conflicts:"] + _cap(result.conflicts)
    if stale_note:
        lines += ["", stale_note]

    cred = [f for f in repo.findings if f.kind.startswith(("credential", "sensitive", "secret"))]
    inj = [f for f in repo.findings if f.kind.startswith("instruction")]
    if cred:
        lines += ["", "Sensitive content found (locations only; values were not read into the context):"]
        lines += _cap([f"{f.kind}: {f.path}" + (f" [{f.detail}]" if f.detail else "") for f in cred], 25)
        lines.append("  Recommendation: remove committed secrets from version control, rotate any that were exposed, and use secure secret management.")
    if inj:
        lines += ["", "Instruction-like text found in repository files (treated as data and ignored):"]
        lines += _cap([f"{f.path} [{f.detail}]" for f in inj], 10)
    lines += ["", "Validation: passed", f"Result: {outcome}"]
    out = "\n".join(lines)
    if args.dry_run and new_text is not None:
        if existing_text is None:
            out += "\n\n--- Proposed PROJECT-CONTEXT.md ---\n" + new_text
        else:
            diff = list(difflib.unified_diff(existing_text.splitlines(), new_text.splitlines(), "existing", "proposed", lineterm="", n=1))
            out += "\n\n--- Proposed changes (diff) ---\n" + ("\n".join(diff) if diff else "(no differences)")
    return scrub(out)

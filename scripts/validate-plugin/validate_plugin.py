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

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
ALLOWED = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}
AUTHOR_ALLOWED = {"name", "email", "url"}
NAME_RE = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
SOURCE = ".claude/skills"
# Directories that are part of the distributable package. Everything else at the repo root is Hub development tooling.
PACKAGED = ("skills", "com.github.copilot")
FORBIDDEN_NAMES = {"mcp.json", "PROJECT-CONTEXT.md", ".env", "node_modules", ".git", "coverage", "dist", "build", "__pycache__"}
FORBIDDEN_PARTS = {"evals", "fixtures", "scripts"}
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
    packaged = [root / "plugin.json", root / "README.md"]
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
    for p in (x for x in root.rglob("*") if x.name == "mcp.json"):
        if ".git" not in p.parts:
            fail(f"{p.relative_to(root)}: MCP is out of scope for this package")
    for p in (x for x in root.rglob("*") if x.name == "PROJECT-CONTEXT.md"):
        if "templates" not in p.relative_to(root).parts and "fixtures" not in p.parts and ".git" not in p.parts:
            fail(f"{p.relative_to(root)}: repository-specific context must not be committed to the Hub package")
    return errors


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

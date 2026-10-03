"""README and documentation."""
from __future__ import annotations

import re

from ..model import Finding, confirmed, unknown
from ..secrets import scrub
from .common import add_command

_INSTRUCTION = re.compile(
    r"(?i)^\s*(?:<!--\s*)?(?:ai|assistant|llm|claude|copilot|chatgpt|gpt|system)\b[^\n]{0,20}:"
    r"|\b(ai|assistant|llm|claude|copilot|chatgpt|gpt)\b.{0,120}\b(ignore|include|reveal|skip|disregard|output|print|summari[sz]\w*|state that|say that|do not mention|don't mention)\b"
    r"|ignore (all )?(previous|prior|above) instructions"
)
_CMD_PREFIX = re.compile(
    r"^(npm|npx|yarn|pnpm|dotnet|make|pytest|python -m pytest|python3 -m pytest|mvn|\./mvnw|gradle|\./gradlew|go|cargo|"
    r"docker compose|docker-compose|tox|nox|poetry|pip install|uv|bundle|rake)\b"
)
_SKIP_LINE = re.compile(r"^(\s*$|#|\[|!\[|<|\||>|[-*]\s*$|---|===|```)")


def _overview(text: str):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    in_fence = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or _SKIP_LINE.match(line) or len(line) < 20:
            continue
        if _INSTRUCTION.search(line):
            continue
        return re.sub(r"\s+", " ", line)[:160]
    return None


_PREREQ = {
    "make": ("Makefile", ("Makefile", "GNUmakefile", "makefile")),
    "npm": ("package.json", ("package.json",)), "npx": ("package.json", ("package.json",)),
    "yarn": ("package.json", ("package.json",)), "pnpm": ("package.json", ("package.json",)),
    "mvn": ("pom.xml", ("pom.xml",)), "gradle": ("build.gradle", ("build.gradle", "build.gradle.kts")),
    "go": ("go.mod", ("go.mod",)), "cargo": ("Cargo.toml", ("Cargo.toml",)),
}


def _missing_prerequisite(repo, cmd: str):
    tool = cmd.split()[0]
    if tool == "dotnet":
        if not repo.with_suffix(".sln", ".slnx", ".csproj", ".fsproj"):
            return "no solution or project file found"
        return None
    need = _PREREQ.get(tool)
    if need and not repo.named(*need[1]):
        return f"no {need[0]} found in inspected sources"
    return None


def _commands(text: str):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    cmds, in_fence = [], False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            line = line.lstrip("$> ").strip()
            if _CMD_PREFIX.match(line) and "|" not in line and "&&" not in line and ">" not in line:
                cmds.append(line)
        else:
            for m in re.finditer(r"`([^`\n]{3,80})`", line):
                c = m.group(1).strip()
                if _CMD_PREFIX.match(c):
                    cmds.append(c)
    seen, out = set(), []
    for c in cmds:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out[:10]


def detect(repo):
    items = []
    readmes = [p for p in repo.named("README.md", "README", "README.rst", "README.txt") if "/" not in p] or \
        repo.named("README.md", "README", "README.rst", "README.txt")[:1]
    if readmes:
        text = repo.read(readmes[0]) or ""
        line = _overview(text)
        if line:
            items.append(confirmed("Project Overview", f'README states: "{scrub(line)}"', readmes[0]))
        else:
            items.append(confirmed("Project Overview", "README: present, with no usable description paragraph", readmes[0]))
        for c in _commands(text):
            missing = _missing_prerequisite(repo, c)
            add_command(repo, f"README command `{c}`" + (f" ({missing})" if missing else ""), "", readmes[0])
            if missing:
                repo.findings.append(Finding("documentation mismatch", readmes[0], f"`{c}`: {missing}"))
    else:
        items.append(unknown("Project Overview", "no README found in inspected sources"))

    doc_dirs = [d for d in ("docs", "doc", "documentation") if d in repo.dirs]
    if doc_dirs:
        items.append(confirmed("Repository Structure", f"Documentation directories: {', '.join(doc_dirs)}", *doc_dirs))
    adr = repo.dirs_named("adr", "adrs", "decisions")
    if adr:
        items.append(confirmed("Architecture", f"Decision records directory: {', '.join(adr[:3])}", *adr[:3]))

    # Instruction-like text in documentation is data. It is ignored and reported.
    for rel in [p for p in sorted(repo.files) if p.lower().endswith((".md", ".txt", ".rst"))][:300]:
        text = repo.read(rel, limit=64 * 1024)
        if not text:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if _INSTRUCTION.search(line):
                repo.findings.append(Finding("instruction-like text ignored", rel, f"line {n}"))
                break
    return items

"""Optional generator configuration, read from a Markdown file (see templates/project-context/GENERATOR-CONFIG.md).

Configuration can add exclusions and protections. It cannot turn off secret protection.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_NAME = "GENERATOR-CONFIG.md"

DEFAULT_EXCLUDED_DIRS = {
    ".git", "node_modules", "bin", "obj", "dist", "build", "out", "coverage", ".venv", "venv", "vendor",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".idea", ".vs", ".next", ".nuxt",
    ".gradle", ".terraform", "bower_components", "TestResults", "site-packages", "generated", "__generated__",
    ".cache",
}


@dataclass
class Config:
    included: list = field(default_factory=list)
    excluded: list = field(default_factory=list)
    sensitive: list = field(default_factory=list)
    manual_sections: list = field(default_factory=list)
    extra_sources: list = field(default_factory=list)  # (path, description)
    output: str = "PROJECT-CONTEXT.md"
    stale_after_days: int = 0
    when_unchanged: str = "leave"  # or "review-date"
    max_read_bytes: int = 512 * 1024
    max_depth: int = 0  # 0 = unlimited
    source: str = ""


def _strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def _sections(text: str):
    cur, buf, out = None, [], {}
    for line in text.splitlines():
        m = re.match(r"^#{2,3}\s+(.*?)\s*$", line)
        if m:
            if cur is not None:
                out[cur] = buf
            cur, buf = m.group(1).strip().lower(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = buf
    return out


def _bullets(lines):
    return [m.group(1).strip() for l in lines if (m := re.match(r"^\s*[-*]\s+(.*\S)\s*$", l))]


def _days(text: str) -> int:
    m = re.match(r"(?i)\s*(\d+)\s*(day|week|month|year)s?", text)
    if not m:
        return 0
    return int(m.group(1)) * {"day": 1, "week": 7, "month": 30, "year": 365}[m.group(2).lower()]


def parse_config(text: str, source: str = "") -> Config:
    secs = _sections(_strip_comments(text))
    cfg = Config(source=source)
    cfg.included = _bullets(secs.get("included paths", []))
    cfg.excluded = _bullets(secs.get("excluded paths", []))
    cfg.sensitive = _bullets(secs.get("sensitive paths", []))
    cfg.manual_sections = _bullets(secs.get("manual sections", []))
    for b in _bullets(secs.get("additional evidence sources", [])):
        parts = re.split(r"\s*(?:→|->)\s*", b, maxsplit=1)
        cfg.extra_sources.append((parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""))
    for b in _bullets(secs.get("output", [])):
        if b.lower().startswith("path:"):
            cfg.output = b.split(":", 1)[1].strip() or cfg.output
    for b in _bullets(secs.get("refresh behavior", [])):
        low = b.lower()
        if low.startswith("stale after:"):
            cfg.stale_after_days = _days(b.split(":", 1)[1])
        elif low.startswith("when nothing changed:") and "review" in low:
            cfg.when_unchanged = "review-date"
    for b in _bullets(secs.get("limits", [])):
        low = b.lower()
        m = re.search(r":\s*(\d+)\s*(kb|mb|b)?", low)
        if not m:
            continue
        n = int(m.group(1))
        if "file size" in low:
            cfg.max_read_bytes = n * {"kb": 1024, "mb": 1024 * 1024, "b": 1, None: 1}[m.group(2)]
        elif "depth" in low:
            cfg.max_depth = n
    return cfg


def load_config(repo: Path, explicit: str | None = None) -> Config:
    path = Path(explicit) if explicit else repo / CONFIG_NAME
    if explicit and not path.is_file():
        raise FileNotFoundError(f"configuration file not found: {explicit}")
    if path.is_file():
        return parse_config(path.read_text(encoding="utf-8", errors="replace"), source=str(path))
    return Config()


def glob_to_regex(pattern: str) -> re.Pattern:
    p = pattern.strip().replace("\\", "/").lstrip("./")
    if p.endswith("/"):
        p += "**"
    out, i = "", 0
    while i < len(p):
        if p.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif p.startswith("**", i):
            out += ".*"
            i += 2
        elif p[i] == "*":
            out += "[^/]*"
            i += 1
        elif p[i] == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(p[i])
            i += 1
    return re.compile("^" + out + "$")

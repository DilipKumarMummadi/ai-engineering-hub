"""Helpers shared by detectors."""
from __future__ import annotations

import re
from collections import defaultdict

from ..catalog import match
from ..model import Item, confirmed


def packages_to_items(repo, declared: dict, table: dict) -> list:
    """declared: {package name: set(evidence paths)}. Emits one Confirmed item per catalog label."""
    by_label = defaultdict(lambda: [None, set()])
    for name, paths in declared.items():
        m = match(table, name)
        if not m:
            continue
        area, label = m
        slot = by_label[(area, label)]
        slot[1].update(paths)
        repo.facts.setdefault("packages", defaultdict(set))[name].update(paths)
    items = []
    for (area, label), (_, paths) in sorted(by_label.items()):
        items.append(confirmed(area, f"{label}: declared as a dependency", *paths))
    return items


def add_db_signal(repo, engine: str, *evidence):
    repo.facts.setdefault("db_signals", defaultdict(set))[engine].update(evidence)


def engine_for(name: str):
    from ..catalog import ENGINES
    low = name.lower()
    for frag, eng in ENGINES:
        if frag in low:
            return eng
    return None


def register_db_libraries(repo, declared: dict):
    for name, paths in declared.items():
        eng = engine_for(name)
        if eng:
            add_db_signal(repo, eng, *paths)


def add_component(repo, directory: str, label: str, evidence: str):
    repo.facts.setdefault("components", []).append((directory or ".", label, evidence))


def add_command(repo, subject: str, detail: str, evidence: str):
    repo.facts.setdefault("commands", []).append((subject, detail, evidence))


def dirname(rel: str) -> str:
    return rel.rsplit("/", 1)[0] if "/" in rel else ""


def strip_version(name: str) -> str:
    return re.split(r"[<>=!~\[ ;@]", name, maxsplit=1)[0].strip()


_CONFIG_GLOBS = (
    "**/appsettings*.json", "**/local.settings.json", "**/application*.properties", "**/application*.yml",
    "**/application*.yaml", "**/bootstrap*.yml", "**/.env.*example", "**/.env.sample", "**/.env.template",
    "**/.env.dist", "config/*.json", "config/*.yml", "config/*.yaml", "config/*.ini", "config/*.properties",
)


def config_keys(repo) -> dict:
    """{path: [Key]} for candidate configuration files. Values are never kept. Computed once."""
    cached = repo.facts.get("config_keys")
    if cached is not None:
        return cached
    from ..configkeys import extract_keys
    from ..model import Finding
    from ..secrets import is_example_name
    out = {}
    paths = sorted({p for g in _CONFIG_GLOBS for p in repo.find(g)})
    for rel in paths[:80]:
        text = repo.read(rel)
        if text is None:
            continue
        name = rel.rsplit("/", 1)[-1]
        keys = extract_keys(text, rel, is_example=is_example_name(name))
        out[rel] = keys
        repo.facts.setdefault("config_text_schemes", {})[rel] = _schemes(text)
        for k in keys:
            if k.sensitive and k.has_value:
                repo.findings.append(Finding("credential value present (value excluded)", rel, k.path))
    repo.facts["config_keys"] = out
    return out


_SCHEME = re.compile(r"(?i)\b(postgres(?:ql)?|mysql|mariadb|sqlserver|mongodb(?:\+srv)?|redis|oracle)://|jdbc:(\w+):")


def _schemes(text: str) -> set:
    found = set()
    for m in _SCHEME.finditer(text):
        found.add((m.group(1) or m.group(2)).lower().replace("+srv", ""))
    return found

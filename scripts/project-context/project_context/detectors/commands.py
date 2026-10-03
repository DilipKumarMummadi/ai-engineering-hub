"""Build and Run: commands collected by other detectors, plus Makefile targets. Nothing is executed."""
from __future__ import annotations

import re

from ..catalog import SIDE_EFFECT
from ..model import confirmed
from ..secrets import is_example_name
from .common import config_keys

_CAP = 60


def detect(repo):
    items = []
    for rel in repo.named("Makefile", "GNUmakefile", "makefile"):
        t = repo.read(rel) or ""
        targets = [m.group(1) for m in re.finditer(r"(?m)^([A-Za-z0-9][\w.\-]*)\s*:(?!=)", t) if "%" not in m.group(1)]
        for name in dict.fromkeys(targets):
            repo.facts.setdefault("commands", []).append((f"Make target `{name}` ({rel})", "", rel))
    for rel, keys in sorted(config_keys(repo).items()):
        if is_example_name(rel.rsplit("/", 1)[-1]) and keys:
            names = sorted({k.path for k in keys})
            items.append(confirmed("Build and Run", f"Example environment file {rel} lists configuration keys: {', '.join(names[:15])} (values excluded)", rel))
    runners = repo.named("Taskfile.yml", "Taskfile.yaml", "justfile")
    if runners:
        items.append(confirmed("Build and Run", f"Task runner files: {', '.join(runners[:4])} (tasks not listed)", *runners[:4]))

    cmds = sorted(set(repo.facts.get("commands", [])), key=lambda c: (c[2], c[0]))
    for subject, detail, ev in cmds[:_CAP]:
        text = f"{subject}: `{detail}`" if detail else subject
        hay = f"{subject} {detail}".lower()
        if any(w in hay for w in SIDE_EFFECT):
            text += " (name suggests side effects)"
        items.append(confirmed("Build and Run", text, ev))
    if len(cmds) > _CAP:
        items.append(confirmed("Build and Run", f"Additional commands omitted: {len(cmds) - _CAP} (see the cited files)", *[c[2] for c in cmds[_CAP:_CAP + 3]]))
    return items

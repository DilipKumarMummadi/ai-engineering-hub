"""Detectors: small functions `detect(repo) -> list[Item]`. Run order matters only where noted."""
from __future__ import annotations

from . import (api, cicd, commands, containers, database, docs, dotnet, golang, java, kubernetes, node,
               observability, python_, security, structure, terraform, testing, unknowns, workflow)

# Order: manifest detectors first (they publish facts), then detectors that consume facts.
DETECTORS = [
    docs, dotnet, node, python_, java, golang, containers, kubernetes, terraform, cicd, api, database,
    testing, observability, security, workflow, structure, commands,
]


def run_all(repo):
    items = []
    for mod in DETECTORS:
        items.extend(mod.detect(repo))
    items.extend(unknowns.detect(repo, items))  # last: needs to know what was found
    return items

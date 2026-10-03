"""Terraform and other infrastructure-as-code."""
from __future__ import annotations

import re

from ..model import confirmed, inferred

_CLOUD = {"aws": "AWS", "azurerm": "Azure", "azuread": "Azure", "azapi": "Azure", "google": "Google Cloud", "google-beta": "Google Cloud"}


def detect(repo):
    items = []
    tfs = repo.with_suffix(".tf")
    if tfs:
        providers, backends, versions, mods = set(), set(), set(), 0
        for rel in tfs[:120]:
            t = repo.read(rel) or ""
            providers.update(re.findall(r'(?m)^\s*provider\s+"([\w\-]+)"', t))
            providers.update(s.split("/")[-1] for s in re.findall(r'source\s*=\s*"([\w\-]+/[\w\-]+)"', t))
            backends.update(re.findall(r'(?m)^\s*backend\s+"(\w+)"', t))
            versions.update(re.findall(r'required_version\s*=\s*"([^"]+)"', t))
            mods += len(re.findall(r'(?m)^\s*module\s+"[\w\-]+"', t))
        dirs = sorted({r.rsplit("/", 1)[0] if "/" in r else "." for r in tfs})
        items.append(confirmed("Infrastructure", f"Terraform files: {len(tfs)} in {', '.join(dirs[:6])}", *tfs[:8]))
        if providers:
            items.append(confirmed("Infrastructure", f"Terraform providers declared: {', '.join(sorted(providers))}", *tfs[:8]))
            clouds = sorted({_CLOUD[p] for p in providers if p in _CLOUD})
            if clouds:
                items.append(inferred("Infrastructure", f"Target cloud appears to be {' / '.join(clouds)} (Terraform providers)", *tfs[:8]))
        if backends:
            items.append(confirmed("Infrastructure", f"Terraform backend type: {', '.join(sorted(backends))}", *tfs[:8]))
        if versions:
            items.append(confirmed("Infrastructure", f"Terraform required version: {', '.join(sorted(versions))}", *tfs[:8]))
        if mods:
            items.append(confirmed("Infrastructure", f"Terraform module blocks: {mods}", *tfs[:8]))
    other = []
    for label, pat in (("Bicep", "**/*.bicep"), ("Pulumi", "**/Pulumi.y*ml"), ("Serverless Framework", "**/serverless.y*ml"),
                       ("CloudFormation (by name)", "**/cloudformation*.y*ml")):
        hits = repo.find(pat)
        if hits:
            other.append((label, hits[0]))
    if other:
        items.append(confirmed("Infrastructure", "Other infrastructure definitions: " + ", ".join(f"{l} ({p})" for l, p in other), *[p for _, p in other]))
    return items

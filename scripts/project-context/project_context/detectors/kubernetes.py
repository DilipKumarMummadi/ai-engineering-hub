"""Kubernetes manifests, Helm charts and Kustomize."""
from __future__ import annotations

import re

from ..model import Finding, confirmed


def detect(repo):
    items = []
    charts = repo.named("Chart.yaml")
    if charts:
        names = []
        for rel in charts[:10]:
            m = re.search(r"(?m)^name:\s*([\w.\-]+)", repo.read(rel) or "")
            names.append(f"{rel}" + (f" ({m.group(1)})" if m else ""))
        items.append(confirmed("Infrastructure", f"Helm charts: {', '.join(names)}", *charts[:10]))
    kz = repo.named("kustomization.yaml", "kustomization.yml")
    if kz:
        items.append(confirmed("Infrastructure", f"Kustomize configuration: {', '.join(kz[:6])}", *kz[:6]))

    kinds, files = {}, []
    chart_dirs = tuple(c.rsplit("/", 1)[0] + "/" for c in charts if "/" in c)
    for rel in [p for p in sorted(repo.files) if p.lower().endswith((".yaml", ".yml"))][:600]:
        low = rel.lower()
        if low.startswith(".github/") or chart_dirs and rel.startswith(chart_dirs) and "/templates/" in rel:
            continue
        if re.match(r"(?i)^(docker-)?compose", rel.rsplit("/", 1)[-1]) or repo.files[rel].size > 256 * 1024:
            continue
        text = repo.read(rel)
        if not text or not re.search(r"(?m)^apiVersion:\s*\S+", text):
            continue
        ks = re.findall(r"(?m)^kind:\s*([A-Za-z]+)\s*$", text)
        if not ks:
            continue
        files.append(rel)
        for k in ks:
            kinds.setdefault(k, set()).add(rel)
            if k == "Secret":
                repo.findings.append(Finding("secret manifest present (contents not recorded)", rel))
    if files:
        shown = ", ".join(sorted(kinds)[:12])
        items.append(confirmed("Infrastructure", f"Kubernetes manifests: {len(files)} file(s) declaring kinds {shown}", *files[:10]))
    return items

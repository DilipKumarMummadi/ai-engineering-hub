"""Security evidence: sensitive files, credential-like configuration, scanning configuration."""
from __future__ import annotations

from ..model import Finding, confirmed
from .common import config_keys


def detect(repo):
    items = []
    sensitive = sorted(p for p, e in repo.files.items() if e.sensitive)
    if sensitive:
        items.append(confirmed("Security", f"Sensitive files present (contents not read): {', '.join(sensitive[:10])}", *sensitive[:10]))
        for p in sensitive:
            repo.findings.append(Finding("sensitive file present (contents not read)", p))
    cred = {}
    for rel, keys in config_keys(repo).items():
        bad = sorted(k.path for k in keys if k.sensitive and k.has_value)
        if bad:
            cred[rel] = bad
    for rel, keys in sorted(cred.items()):
        items.append(confirmed("Security", f"Configuration keys with credential-like names and non-placeholder values in {rel}: {', '.join(keys[:6])} (values excluded)", rel))
    for label, pat in (("Snyk configuration", "**/.snyk"), ("Gitleaks configuration", "**/.gitleaks.toml"),
                       ("Trivy configuration", "**/trivy*.y*ml"), ("Security policy", "**/SECURITY.md")):
        hits = repo.find(pat)
        if hits:
            items.append(confirmed("Security", f"{label}: {hits[0]}", hits[0]))
    return items

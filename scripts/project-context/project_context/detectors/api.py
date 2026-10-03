"""API definitions."""
from __future__ import annotations

import re

from ..model import confirmed


def detect(repo):
    items = []
    specs = [p for p in repo.files if re.match(r"(?i)^(openapi|swagger)[\w.\-]*\.(json|ya?ml)$", p.rsplit("/", 1)[-1])]
    for rel in sorted(specs)[:6]:
        t = repo.read(rel, limit=32 * 1024) or ""
        m = re.search(r"""(?i)["']?(openapi|swagger)["']?\s*[:=]\s*["']?([\d.]+)""", t)
        items.append(confirmed("API", f"OpenAPI/Swagger definition ({rel})" + (f": {m.group(1).lower()} {m.group(2)}" if m else ""), rel))
        repo.facts["api_spec"] = True
    for label, suffixes in (("Protocol Buffers definitions", (".proto",)), ("GraphQL schema files", (".graphql", ".gql")),
                            ("AsyncAPI definitions", ())):
        hits = repo.with_suffix(*suffixes) if suffixes else [p for p in repo.files if re.match(r"(?i)^asyncapi[\w.\-]*\.ya?ml$", p.rsplit("/", 1)[-1])]
        if hits:
            items.append(confirmed("API", f"{label}: {', '.join(hits[:6])}", *hits[:6]))
            repo.facts["api_spec"] = True
            repo.facts["api_signal"] = True
    if specs:
        repo.facts["api_signal"] = True
    return items

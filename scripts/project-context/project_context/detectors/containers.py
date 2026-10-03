"""Docker and Compose."""
from __future__ import annotations

import re

from ..catalog import DB_IMAGES
from ..model import confirmed
from .common import add_db_signal

_PUBLIC_REGISTRIES = {"mcr.microsoft.com", "ghcr.io", "gcr.io", "quay.io", "public.ecr.aws", "docker.io", "registry.k8s.io"}
_DB_ENGINES = {"PostgreSQL", "MySQL", "MariaDB", "MongoDB", "Redis", "SQL Server", "Oracle"}


def safe_image(ref: str) -> str:
    """Drop private registry hosts (hostnames are sensitive by default)."""
    ref = ref.strip().strip("'\"")
    if "${" in ref or "$" in ref:
        return "(image reference uses a variable)"
    first, _, rest = ref.partition("/")
    if rest and ("." in first or ":" in first or first == "localhost") and first not in _PUBLIC_REGISTRIES:
        return f"(image from a private registry; host excluded) {rest.rsplit('/', 1)[-1]}"
    return ref


def _dockerfiles(repo):
    names = [p for p in repo.files if re.match(r"(?i)^(dockerfile(\..+)?|.+\.dockerfile|containerfile)$", p.rsplit("/", 1)[-1])]
    return sorted(names)


def _compose(repo):
    return sorted(p for p in repo.files if re.match(r"(?i)^(docker-)?compose(\..+)?\.ya?ml$", p.rsplit("/", 1)[-1]))


def detect(repo):
    items = []
    dfs = _dockerfiles(repo)
    if dfs:
        images, ports = [], set()
        for rel in dfs[:10]:
            t = repo.read(rel) or ""
            aliases = set()
            for m in re.finditer(r"(?im)^FROM\s+(?:--platform=\S+\s+)?(\S+)(?:\s+AS\s+(\S+))?", t):
                ref = m.group(1)
                if ref.lower() != "scratch" and ref.lower() not in aliases:
                    img = safe_image(ref)
                    if img not in images:
                        images.append(img)
                if m.group(2):
                    aliases.add(m.group(2).lower())
            ports.update(re.findall(r"(?im)^EXPOSE\s+(\d+)", t))
        items.append(confirmed("Infrastructure", f"Dockerfiles: {', '.join(dfs[:6])}", *dfs[:6]))
        if images:
            items.append(confirmed("Infrastructure", f"Dockerfile base images: {', '.join(images[:6])}", *dfs[:6]))
        if ports:
            items.append(confirmed("Infrastructure", f"Dockerfile exposes ports: {', '.join(sorted(ports, key=int))}", *dfs[:6]))
    for rel in _compose(repo)[:6]:
        services = _compose_services(repo.read(rel) or "")
        if not services:
            items.append(confirmed("Infrastructure", f"Compose file present: {rel}", rel))
            continue
        desc = []
        for name, info in services:
            img = safe_image(info["image"]) if info["image"] else ("build" if info["build"] else "no image or build")
            desc.append(f"{name} ({img})")
            base = (info["image"] or "").rsplit("/", 1)[-1].split(":")[0].lower()
            for frag, eng in DB_IMAGES.items():
                if frag in base and eng in _DB_ENGINES:
                    add_db_signal(repo, eng, rel)
        items.append(confirmed("Infrastructure", f"Compose services ({rel}): {', '.join(desc)}", rel))
    return items


def _compose_services(text: str):
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines) and not re.match(r"^services:\s*$", lines[i]):
        i += 1
    i += 1
    child_indent = None
    cur = None
    for line in lines[i:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if indent == 0:
            break
        if child_indent is None:
            child_indent = indent
        if indent == child_indent:
            m = re.match(r"^\s*([\w.\-]+):\s*$", line)
            if m:
                cur = {"image": "", "build": False}
                out.append((m.group(1), cur))
            continue
        if cur is not None and indent == child_indent + 2:
            m = re.match(r"^\s*image:\s*(\S+)", line)
            if m:
                cur["image"] = m.group(1)
            elif re.match(r"^\s*build:", line):
                cur["build"] = True
    return out

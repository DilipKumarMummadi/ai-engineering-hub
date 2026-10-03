"""Node.js / JavaScript / TypeScript manifests."""
from __future__ import annotations

import json
import re
from collections import defaultdict

from ..catalog import NODE
from ..model import confirmed, inferred
from ..secrets import scrub
from .common import add_command, add_component, dirname, packages_to_items, register_db_libraries

_LOCKS = {"package-lock.json": "npm", "pnpm-lock.yaml": "pnpm", "yarn.lock": "Yarn", "bun.lockb": "Bun", "bun.lock": "Bun"}
_APP_SCRIPTS = ("start", "dev", "serve", "build")
_FRONTEND = {"react", "vue", "@angular/core", "svelte", "solid-js", "next"}
_BACKEND = {"express", "fastify", "koa", "@nestjs/core", "hono"}


def _load(repo, rel):
    text = repo.read(rel)
    if text is None:
        return None
    try:
        data = json.loads(text.lstrip("﻿"))
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def detect(repo):
    manifests = repo.named("package.json")
    if not manifests:
        return []
    items, declared = [], defaultdict(set)
    items.append(confirmed("Technology Stack", f"Node.js package manifests: {', '.join(manifests[:10])}" + (" (and more)" if len(manifests) > 10 else ""), *manifests[:10]))

    versions, managers, workspaces = {}, {}, {}
    for rel in manifests[:40]:
        data = _load(repo, rel)
        if data is None:
            continue
        d = dirname(rel)
        for sect in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            for name in (data.get(sect) or {}):
                declared[name].add(rel)
        deps = set((data.get("dependencies") or {})) | set((data.get("devDependencies") or {}))
        node_v = (data.get("engines") or {}).get("node")
        if node_v:
            versions[rel] = str(node_v)
        pm = data.get("packageManager")
        if pm:
            managers[rel] = str(pm).split("+")[0]
        ws = data.get("workspaces")
        if ws:
            workspaces[rel] = ws if isinstance(ws, list) else (ws.get("packages") or [])
        scripts = data.get("scripts") or {}
        for name, body in sorted(scripts.items())[:15]:
            if isinstance(body, str):
                add_command(repo, f"Script `{name}` ({rel})", _safe_body(body), rel)
        label = data.get("name") or (d or "root")
        if any(s in scripts for s in _APP_SCRIPTS) or deps & (_FRONTEND | _BACKEND):
            add_component(repo, d, f"Node.js package '{label}' (scripts: {', '.join(sorted(scripts)[:6]) or 'none'})", rel)
        if deps & _FRONTEND and (deps & {"vite", "webpack", "next", "react-scripts", "@angular/cli", "parcel"} or "angular.json" in repo.files):
            items.append(inferred("Frontend", f"Frontend application appears present in {d or '.'} (framework and bundler dependencies declared)", rel))
            repo.facts.setdefault("frontend_dirs", set()).add(d or ".")
        if deps & _BACKEND:
            items.append(inferred("API", f"Application in {d or '.'} likely exposes HTTP APIs (server framework declared)", rel))
            repo.facts.setdefault("backend_dirs", set()).add(d or ".")
            repo.facts["api_signal"] = True

    for rel, v in sorted(versions.items()):
        items.append(confirmed("Technology Stack", f"Node.js version requirement ({rel}): {v}", rel))
    for f in repo.named(".nvmrc", ".node-version"):
        v = (repo.read(f) or "").strip().splitlines()[:1]
        if v and re.fullmatch(r"[\w.\-/*]+", v[0]):
            items.append(confirmed("Technology Stack", f"Node.js version file ({f}): {v[0]}", f))
    for rel, pm in sorted(managers.items()):
        items.append(confirmed("Technology Stack", f"Package manager declared ({rel}): {pm}", rel))
    locks = [(p, _LOCKS[p.rsplit('/', 1)[-1]]) for p in repo.named(*_LOCKS)]
    if locks:
        items.append(confirmed("Technology Stack", f"Lock files: {', '.join(p for p, _ in locks[:6])}", *[p for p, _ in locks[:6]]))
        if not managers:
            kinds = sorted({k for _, k in locks})
            items.append(inferred("Technology Stack", f"Package manager appears to be {' / '.join(kinds)} (lock file present, no packageManager field)", *[p for p, _ in locks[:6]]))
    for rel, ws in sorted(workspaces.items()):
        items.append(confirmed("Repository Structure", f"Workspaces declared ({rel}): {', '.join(map(str, ws[:8]))}", rel))

    if "angular.json" in repo.files or repo.named("angular.json"):
        a = repo.named("angular.json")
        items.append(confirmed("Frontend", "Angular workspace configuration: angular.json present", *a[:3]))
    for rel in repo.find("**/tsconfig*.json")[:6]:
        if re.search(r'"strict"\s*:\s*true', repo.read(rel) or ""):
            items.append(confirmed("Coding Conventions", f"TypeScript strict mode enabled ({rel})", rel))
    items += packages_to_items(repo, declared, NODE)
    register_db_libraries(repo, declared)
    return items


def _safe_body(body: str) -> str:
    from ..secrets import find_secrets
    body = body.strip()
    if find_secrets(body):
        return "[script body omitted: secret-like content]"
    return scrub(body)[:120]

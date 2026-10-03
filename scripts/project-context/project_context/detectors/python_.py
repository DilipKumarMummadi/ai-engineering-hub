"""Python manifests: pyproject.toml, requirements, setup files."""
from __future__ import annotations

import re
from collections import defaultdict

from ..catalog import PYTHON
from ..model import confirmed, inferred
from .common import add_command, add_component, dirname, packages_to_items, register_db_libraries, strip_version

try:  # Python 3.11+
    import tomllib
except ImportError:  # pragma: no cover
    tomllib = None

_FILES = ("pyproject.toml", "setup.py", "setup.cfg", "Pipfile", "tox.ini", "pytest.ini", "poetry.lock", "uv.lock", ".python-version")
_WEB = {"django", "flask", "fastapi", "starlette"}


def _norm(name: str) -> str:
    return strip_version(name).lower().replace("_", "-")


def _toml(text):
    if tomllib is None:
        return {}
    try:
        return tomllib.loads(text)
    except Exception:
        return {}


def detect(repo):
    pyprojects = repo.named("pyproject.toml")
    reqs = sorted(set(repo.find("**/requirements*.txt") + repo.find("requirements*.txt")))
    others = [p for p in repo.named("setup.py", "setup.cfg", "Pipfile")]
    if not (pyprojects or reqs or others):
        return []
    items, declared = [], defaultdict(set)
    manifests = sorted(set(pyprojects + reqs + others))
    items.append(confirmed("Technology Stack", f"Python manifests: {', '.join(manifests[:10])}", *manifests[:10]))

    for rel in pyprojects[:20]:
        data = _toml(repo.read(rel) or "")
        proj = data.get("project") or {}
        poetry = (data.get("tool") or {}).get("poetry") or {}
        d = dirname(rel)
        if proj.get("requires-python"):
            items.append(confirmed("Technology Stack", f"Python version requirement ({rel}): {proj['requires-python']}", rel))
        for dep in proj.get("dependencies") or []:
            declared[_norm(dep)].add(rel)
        for group in (proj.get("optional-dependencies") or {}).values():
            for dep in group:
                declared[_norm(dep)].add(rel)
        for dep in (poetry.get("dependencies") or {}):
            if dep.lower() != "python":
                declared[_norm(dep)].add(rel)
        for sect in ("dev-dependencies",):
            for dep in (poetry.get(sect) or {}):
                declared[_norm(dep)].add(rel)
        for grp in ((poetry.get("group") or {}).values()):
            for dep in (grp.get("dependencies") or {}):
                declared[_norm(dep)].add(rel)
        for name in list((proj.get("scripts") or {}))[:10] + list((poetry.get("scripts") or {}))[:10]:
            add_command(repo, f"Entry point `{name}` ({rel})", "", rel)
        tool = data.get("tool") or {}
        if poetry:
            items.append(confirmed("Technology Stack", "Python packaging tool: Poetry configuration in pyproject.toml", rel))
        for t, label in (("ruff", "Ruff"), ("black", "Black"), ("mypy", "mypy"), ("isort", "isort"), ("pytest", "pytest")):
            if t in tool:
                area = "Testing" if t == "pytest" else "Coding Conventions"
                items.append(confirmed(area, f"{label} configured in pyproject.toml", rel))
        if proj or poetry:
            add_component(repo, d, f"Python project '{proj.get('name') or poetry.get('name') or d or 'root'}'", rel)

    for rel in reqs[:20]:
        for line in (repo.read(rel) or "").splitlines():
            line = line.strip()
            if line and not line.startswith(("#", "-", "git+", "http")):
                declared[_norm(line)].add(rel)
    for rel in repo.named(".python-version"):
        v = (repo.read(rel) or "").strip()
        if re.fullmatch(r"[\w.\-]+", v or "x!"):
            items.append(confirmed("Technology Stack", f"Python version file ({rel}): {v}", rel))
    if repo.named("poetry.lock", "uv.lock", "Pipfile.lock"):
        locks = repo.named("poetry.lock", "uv.lock", "Pipfile.lock")
        items.append(confirmed("Technology Stack", f"Python lock files: {', '.join(locks[:4])}", *locks[:4]))
    if repo.named("Pipfile"):
        items.append(confirmed("Technology Stack", "Python packaging tool: Pipfile present", *repo.named("Pipfile")[:2]))

    web = _WEB & set(declared)
    if web:
        ev = sorted({p for w in web for p in declared[w]})
        items.append(inferred("API", f"Application likely serves HTTP (declared web framework: {', '.join(sorted(web))})", *ev))
        repo.facts["api_signal"] = True
        repo.facts.setdefault("backend_dirs", set()).update(dirname(p) or "." for p in ev)
    items += packages_to_items(repo, declared, PYTHON)
    register_db_libraries(repo, declared)
    return items

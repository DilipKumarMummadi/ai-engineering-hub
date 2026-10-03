"""Repository structure and architecture signals. Patterns are never declared, only structure."""
from __future__ import annotations

from ..catalog import SOURCE_EXTS
from ..model import confirmed, inferred

_INFRA_DIRS = ("infra", "infrastructure", "terraform", "k8s", "kubernetes", "helm", "charts", "deploy", "deployment", "ops", "iac")
_SHARED_DIRS = ("libs", "packages", "shared", "common", "lib")


def detect(repo):
    items = []
    top = sorted({p.split("/")[0] for p in repo.files if "/" in p})
    if top:
        items.append(confirmed("Repository Structure", f"Top-level directories: {', '.join(top[:20])}" + (" (and more)" if len(top) > 20 else ""), *top[:20]))
    infra = [d for d in repo.dirs_named(*_INFRA_DIRS) if d.count("/") <= 1]
    if infra:
        items.append(confirmed("Repository Structure", f"Directories with infrastructure-style names (purpose not verified): {', '.join(infra[:8])}", *infra[:8]))
    scripts = [p for p in repo.files if p.startswith("scripts/") and p.count("/") == 1]
    if scripts:
        names = ", ".join(p.split("/")[1] for p in scripts[:15])
        items.append(confirmed("Repository Structure", f"Scripts directory contents: {names}", *scripts[:15]))
    first_by_ext = {}
    for p in sorted(repo.files):
        ext = p[p.rfind("."):].lower() if "." in p.rsplit("/", 1)[-1] else ""
        if ext in SOURCE_EXTS:
            first_by_ext.setdefault(ext, p)
    if first_by_ext:
        items.append(confirmed("Technology Stack", "Source file types present: " + ", ".join(f"{e} ({SOURCE_EXTS[e]})" for e in sorted(first_by_ext)), *list(first_by_ext.values())[:8]))

    comps = sorted(set(repo.facts.get("components", [])))
    seen = set()
    for d, label, ev in comps:
        if (d, label) in seen:
            continue
        seen.add((d, label))
        items.append(confirmed("Application Components", f"{d}: {label}", ev))
    comp_dirs = sorted({d for d, _, _ in comps})
    if len(comp_dirs) >= 2:
        items.append(confirmed("Repository Structure", f"Project manifests in {len(comp_dirs)} separate directories: {', '.join(comp_dirs[:10])}", *[e for _, _, e in comps][:10]))
        items.append(inferred("Architecture", "Repository appears to contain multiple independently structured application projects (multi-project layout)", *[e for _, _, e in comps][:10]))
    fe, be = repo.facts.get("frontend_dirs", set()), repo.facts.get("backend_dirs", set())
    if fe and be and not (fe & be):
        items.append(inferred("Architecture", f"Repository appears to separate frontend code ({', '.join(sorted(fe))}) from backend code ({', '.join(sorted(be))})", *(sorted(fe | be))))
    # Sibling directories that each contain the same marker file (a structural fact, not a pattern claim).
    generic = {"readme.md", "readme", "license", "package.json", "go.mod", "pyproject.toml", "pom.xml", "chart.yaml", "dockerfile",
               "makefile", "tsconfig.json", "index.md", "index.ts", "index.js", "__init__.py", "main.go", "main.py", ".gitkeep", ".gitignore"}
    groups = {}
    for p in repo.files:
        parts = p.split("/")
        if len(parts) >= 3 and not repo.files[p].sensitive and parts[-1].lower() not in generic and parts[-1].lower().endswith((".yaml", ".yml", ".json", ".toml", ".xml", ".md", ".cfg")):
            groups.setdefault(("/".join(parts[:-2]), parts[-1]), set()).add(parts[-2])
    for (parent, marker), names in sorted(groups.items()):
        if len(names) >= 3 and not parent.startswith(".") and "/." not in parent:
            ev = [f"{parent}/{n}/{marker}" for n in sorted(names)[:4]]
            items.append(confirmed("Repository Structure", f"Sibling directories under {parent} each contain {marker}: {', '.join(sorted(names)[:8])}", *ev))
            items.append(inferred("Architecture", f"{parent} appears to hold a set of similarly structured units (shared marker file {marker})", *ev))
    shared = [d for d in repo.dirs_named(*_SHARED_DIRS) if any(f.startswith(d + "/") and f.rsplit("/", 1)[-1] in ("package.json", "go.mod", "pyproject.toml", "pom.xml") or f.endswith((".csproj",)) and f.startswith(d + "/") for f in repo.files)]
    if shared:
        items.append(inferred("Architecture", f"Repository appears to contain shared library projects ({', '.join(shared[:5])})", *shared[:5]))
    return items

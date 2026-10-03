""".NET: solutions, projects, SDKs, target frameworks, packages."""
from __future__ import annotations

import re
from collections import defaultdict

from ..catalog import DOTNET
from ..model import confirmed, inferred
from .common import add_component, dirname, packages_to_items, register_db_libraries

_LAYER_WORDS = ("api", "application", "domain", "infrastructure", "core", "data", "persistence", "web", "services")


def _project_name(rel: str) -> str:
    return rel.rsplit("/", 1)[-1].rsplit(".", 1)[0]


def detect(repo):
    projects = repo.with_suffix(".csproj", ".fsproj", ".vbproj")
    slns = repo.with_suffix(".sln", ".slnx")
    props = repo.named("Directory.Build.props", "Directory.Packages.props", "global.json", "nuget.config")
    if not (projects or slns):
        return []
    items = []
    if slns:
        items.append(confirmed("Repository Structure", f"Solution files: {', '.join(slns[:8])}", *slns[:8]))

    declared = defaultdict(set)
    tfms, web, worker, exe, tests, libs, nullable = set(), [], [], [], [], [], []
    for rel in projects[:80]:
        text = repo.read(rel) or ""
        sdk = (re.search(r'<Project\s+Sdk="([^"]+)"', text) or [None, ""])[1]
        for m in re.finditer(r"<TargetFrameworks?>([^<]+)</TargetFrameworks?>", text):
            tfms.update(t.strip() for t in m.group(1).split(";") if t.strip())
        pkgs = re.findall(r'<PackageReference\s+[^>]*?Include="([^"]+)"', text)
        for p in pkgs:
            declared[p].add(rel)
        is_test = "Microsoft.NET.Test.Sdk" in pkgs or "<IsTestProject>true" in text
        out_exe = "<OutputType>Exe" in text or "<OutputType>WinExe" in text
        if is_test:
            tests.append(rel)
        elif "Sdk.Web" in sdk or "Microsoft.AspNetCore.App" in text:
            web.append(rel)
            add_component(repo, dirname(rel), "ASP.NET Core project (Web SDK)", rel)
        elif "Sdk.Worker" in sdk:
            worker.append(rel)
            add_component(repo, dirname(rel), ".NET worker project (Worker SDK)", rel)
        elif out_exe:
            exe.append(rel)
            add_component(repo, dirname(rel), ".NET executable project", rel)
        else:
            libs.append(rel)
        if re.search(r"<Nullable>\s*enable", text, re.I):
            nullable.append(rel)

    # Central package versions
    for rel in repo.named("Directory.Packages.props"):
        for p in re.findall(r'<PackageVersion\s+[^>]*?Include="([^"]+)"', repo.read(rel) or ""):
            declared[p].add(rel)

    if projects:
        items.append(confirmed("Technology Stack", f".NET project files: {len(projects)}", *projects[:10]))
    if tfms:
        items.append(confirmed("Technology Stack", f".NET target frameworks: {', '.join(sorted(tfms))}", *projects[:10]))
    if web:
        items.append(confirmed("Technology Stack", f"ASP.NET Core: {len(web)} project(s) use the Web SDK", *web[:10]))
    for rel in repo.named("global.json"):
        m = re.search(r'"version"\s*:\s*"([^"]+)"', repo.read(rel) or "")
        if m:
            items.append(confirmed("Technology Stack", f".NET SDK version pinned: {m.group(1)}", rel))
    if tests:
        items.append(confirmed("Testing", f".NET test projects: {', '.join(dirname(t) or t for t in tests[:10])}", *tests[:10]))
    if libs:
        items.append(confirmed("Repository Structure", f".NET library projects: {', '.join(_project_name(l) for l in libs[:12])}", *libs[:12]))
    if nullable:
        items.append(confirmed("Coding Conventions", "Nullable reference types: enabled in project files", *nullable[:10]))
    for rel in props:
        if rel.endswith("Directory.Build.props"):
            items.append(confirmed("Coding Conventions", "Shared build properties: Directory.Build.props present", rel))
        elif rel.endswith("Directory.Packages.props"):
            items.append(confirmed("Coding Conventions", "Central package management: Directory.Packages.props present", rel))

    # Inference: project names suggest layers. Qualified, never a fact.
    names = {w for p in projects for w in _LAYER_WORDS if w in _project_name(p).lower().split(".")}
    if len(names) >= 3:
        items.append(inferred("Architecture", f"Project names suggest a layered organisation ({', '.join(sorted(names))})", *projects[:12]))

    # Inference: HTTP APIs
    for rel in web:
        d = dirname(rel)
        if any(x.startswith((f"{d}/Controllers/" if d else "Controllers/")) for x in repo.files):
            items.append(inferred("API", "Application likely exposes HTTP APIs (Web SDK project with a Controllers directory)", rel, f"{d}/Controllers" if d else "Controllers"))
            repo.facts.setdefault("backend_dirs", set()).add(d or ".")
            repo.facts["api_signal"] = True
            break
    else:
        if web:
            repo.facts.setdefault("backend_dirs", set()).update(dirname(w) or "." for w in web)

    items += packages_to_items(repo, declared, DOTNET)
    register_db_libraries(repo, declared)
    if any(k.lower().startswith(("swashbuckle", "nswag", "microsoft.aspnetcore.openapi")) for k in declared):
        repo.facts["api_signal"] = True
    return items

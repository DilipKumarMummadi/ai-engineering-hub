"""Java / JVM: Maven and Gradle."""
from __future__ import annotations

import re
from collections import defaultdict

from ..catalog import JAVA
from ..model import confirmed, inferred
from .common import add_component, dirname, register_db_libraries

_KEYS = sorted(JAVA, key=len, reverse=True)


def _label(artifact: str):
    low = artifact.lower()
    for k in _KEYS:
        if k in low:
            return JAVA[k]
    return None


def detect(repo):
    poms = repo.named("pom.xml")
    gradles = repo.named("build.gradle", "build.gradle.kts")
    if not (poms or gradles):
        return []
    items, found = [], defaultdict(set)
    manifests = poms + gradles
    items.append(confirmed("Technology Stack", f"JVM build files: {', '.join(manifests[:10])}", *manifests[:10]))
    if poms:
        items.append(confirmed("Technology Stack", "Build tool: Maven (pom.xml present)", *poms[:3]))
    if gradles:
        items.append(confirmed("Technology Stack", "Build tool: Gradle (build.gradle present)", *gradles[:3]))
    wrappers = repo.named("mvnw", "gradlew")
    if wrappers:
        items.append(confirmed("Technology Stack", f"Build wrappers present: {', '.join(wrappers[:4])}", *wrappers[:4]))

    versions = set()
    for rel in poms[:30]:
        t = repo.read(rel) or ""
        for a in re.findall(r"<artifactId>([^<]+)</artifactId>", t):
            lab = _label(a)
            if lab:
                found[lab].add(rel)
        for m in re.finditer(r"<(?:java\.version|maven\.compiler\.(?:source|target|release))>([^<]+)<", t):
            versions.add(m.group(1).strip())
        mods = re.findall(r"<module>([^<]+)</module>", t)
        if mods:
            items.append(confirmed("Repository Structure", f"Maven modules ({rel}): {', '.join(mods[:10])}", rel))
        add_component(repo, dirname(rel), "Maven project", rel)
    for rel in gradles[:30]:
        t = repo.read(rel) or ""
        for s in re.findall(r"""['"]([\w.\-]+:[\w.\-]+)(?::[^'"]*)?['"]""", t) + re.findall(r"""id\s*\(?\s*['"]([\w.\-]+)['"]""", t):
            lab = _label(s)
            if lab:
                found[lab].add(rel)
        for m in re.finditer(r"JavaLanguageVersion\.of\((\d+)\)|sourceCompatibility\s*=\s*['\"]?(?:JavaVersion\.VERSION_)?([\d_.]+)", t):
            versions.add((m.group(1) or m.group(2)).replace("_", "."))
        add_component(repo, dirname(rel), "Gradle project", rel)
    for rel in repo.named("settings.gradle", "settings.gradle.kts"):
        inc = re.findall(r"""include\s*\(?\s*['"]([^'"]+)['"]""", repo.read(rel) or "")
        if inc:
            items.append(confirmed("Repository Structure", f"Gradle modules ({rel}): {', '.join(inc[:10])}", rel))
    if versions:
        items.append(confirmed("Technology Stack", f"Java version settings: {', '.join(sorted(versions))}", *(manifests[:4])))

    for (area, label), paths in sorted((lab, p) for lab, p in found.items()):
        items.append(confirmed(area, f"{label}: declared in build files", *sorted(paths)[:6]))
    register_db_libraries(repo, {lab[1]: p for lab, p in found.items() if lab[0] == "Database"})
    if any(lab[1] in ("Spring Web", "Spring WebFlux", "JAX-RS") for lab in found):
        ev = sorted({p for lab, ps in found.items() if lab[1] in ("Spring Web", "Spring WebFlux", "JAX-RS") for p in ps})
        items.append(inferred("API", "Application likely exposes HTTP APIs (web framework declared)", *ev))
        repo.facts["api_signal"] = True
        repo.facts.setdefault("backend_dirs", set()).update(dirname(p) or "." for p in ev)
    return items

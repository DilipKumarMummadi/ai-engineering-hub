"""Go modules and other ecosystem manifests (existence only)."""
from __future__ import annotations

import re

from ..model import confirmed
from .common import add_component, dirname

_GO = {
    "gin-gonic/gin": ("API", "Gin"), "labstack/echo": ("API", "Echo"), "go-chi/chi": ("API", "chi"),
    "gorilla/mux": ("API", "gorilla/mux"), "gofiber/fiber": ("API", "Fiber"),
    "gorm.io/gorm": ("Database", "GORM"), "jackc/pgx": ("Database", "pgx (PostgreSQL client)"),
    "lib/pq": ("Database", "lib/pq (PostgreSQL client)"), "go-sql-driver/mysql": ("Database", "MySQL driver"),
    "stretchr/testify": ("Testing", "testify"), "prometheus/client_golang": ("Observability", "Prometheus client"),
    "go.opentelemetry.io": ("Observability", "OpenTelemetry"), "uber.org/zap": ("Observability", "zap (logging)"),
    "sirupsen/logrus": ("Observability", "logrus (logging)"),
}
_OTHER = {
    "Cargo.toml": "Rust (Cargo)", "Gemfile": "Ruby (Bundler)", "composer.json": "PHP (Composer)", "build.sbt": "Scala (sbt)",
    "mix.exs": "Elixir (Mix)", "Package.swift": "Swift Package Manager", "deno.json": "Deno", "pubspec.yaml": "Dart/Flutter",
}


def detect(repo):
    items = []
    mods = repo.named("go.mod")
    if mods:
        items.append(confirmed("Technology Stack", f"Go modules: {', '.join(mods[:8])}", *mods[:8]))
        found, versions = {}, set()
        for rel in mods[:20]:
            t = repo.read(rel) or ""
            m = re.search(r"^go\s+([\d.]+)", t, re.M)
            if m:
                versions.add(m.group(1))
            for frag, (area, label) in _GO.items():
                if frag in t:
                    found.setdefault((area, label), set()).add(rel)
            add_component(repo, dirname(rel), "Go module", rel)
        if versions:
            items.append(confirmed("Technology Stack", f"Go version declared: {', '.join(sorted(versions))}", *mods[:4]))
        for (area, label), paths in sorted(found.items()):
            items.append(confirmed(area, f"{label}: declared in go.mod", *sorted(paths)[:4]))
    other = []
    for name, label in _OTHER.items():
        p = repo.named(name)
        if p:
            other.append((label, p[0]))
    if other:
        items.append(confirmed("Technology Stack", "Other ecosystem manifests present: " + ", ".join(f"{l} ({p})" for l, p in other), *[p for _, p in other]))
    return items

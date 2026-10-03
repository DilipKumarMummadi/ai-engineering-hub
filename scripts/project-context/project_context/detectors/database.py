"""Database evidence: migrations, SQL files, schema definitions, configuration keys, engine signals."""
from __future__ import annotations

import re

from ..model import confirmed, inferred
from ..secrets import is_example_name
from .common import add_db_signal, config_keys

_DB_KEY = re.compile(r"(?i)(connection|database|datasource|jdbc|db[_.-]|dbname|mongo|redis|postgres|mysql|sqlserver)")
_SCHEME_ENGINE = {
    "postgres": "PostgreSQL", "postgresql": "PostgreSQL", "mysql": "MySQL", "mariadb": "MariaDB",
    "sqlserver": "SQL Server", "mongodb": "MongoDB", "redis": "Redis", "oracle": "Oracle",
}


def detect(repo):
    items = []
    confirmed_engines = {}

    mig = [d for d in repo.dirs if d.rsplit("/", 1)[-1].lower() in ("migrations", "alembic") or d.lower().endswith(("db/migrate", "db/migration", "db/migrations", "prisma/migrations"))]
    for d in sorted(mig)[:6]:
        n = len(repo.in_dir(d))
        items.append(confirmed("Database", f"Migration directory {d}: {n} file(s)", d))
        repo.facts["db_migrations"] = True
    sql = repo.with_suffix(".sql")
    if sql:
        dirs = sorted({r.rsplit("/", 1)[0] if "/" in r else "." for r in sql})
        items.append(confirmed("Database", f"SQL scripts: {len(sql)} file(s) in {', '.join(dirs[:5])}", *sql[:5]))
    for rel in repo.named("schema.prisma"):
        t = repo.read(rel) or ""
        m = re.search(r"datasource\s+\w+\s*\{[^}]*?provider\s*=\s*\"(\w+)\"", t, re.S)
        if m:
            eng = _SCHEME_ENGINE.get(m.group(1).lower(), m.group(1))
            confirmed_engines.setdefault(eng, set()).add(rel)
            items.append(confirmed("Database", f"Prisma datasource provider: {m.group(1)}", rel))

    keys_by_file = config_keys(repo)
    schemes = repo.facts.get("config_text_schemes", {})
    for rel, keys in sorted(keys_by_file.items()):
        dbk = sorted({k.path for k in keys if _DB_KEY.search(k.path)})
        if dbk:
            items.append(confirmed("Database", f"Database configuration keys in {rel}: {', '.join(dbk[:6])} (values excluded)", rel))
        for s in schemes.get(rel, ()):
            eng = _SCHEME_ENGINE.get(s)
            if not eng:
                continue
            if is_example_name(rel.rsplit("/", 1)[-1]):
                add_db_signal(repo, eng, rel)  # a placeholder in an example file is a hint, not a declaration
            else:
                confirmed_engines.setdefault(eng, set()).add(rel)
    for eng, ev in sorted(confirmed_engines.items()):
        items.append(confirmed("Database", f"Database engine declared by a connection scheme or datasource provider: {eng} (credentials and host excluded)", *sorted(ev)))

    signals = repo.facts.get("db_signals", {})
    for eng, ev in sorted(signals.items()):
        if eng in confirmed_engines:
            continue
        items.append(inferred("Database", f"Database engine appears to be {eng} (client library, container image or example configuration)", *sorted(ev)[:6]))
    if signals or confirmed_engines or mig:
        repo.facts["db_signal"] = True
    return items

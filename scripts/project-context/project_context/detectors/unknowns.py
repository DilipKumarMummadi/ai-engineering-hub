"""Known Unknowns: gaps the repository evidence cannot fill. Added last, from what was and was not found."""
from __future__ import annotations

from ..model import UNKNOWN, unknown

_AREAS = [
    ("API", "API definitions or HTTP API frameworks"),
    ("Database", "database technology, migrations or configuration"),
    ("Frontend", "frontend framework"),
    ("Testing", "test directories, test files or test frameworks"),
    ("Infrastructure", "container, Kubernetes or infrastructure-as-code definitions"),
    ("Observability", "logging, metrics or tracing libraries or configuration"),
    ("Security", "authentication or security configuration"),
]


def detect(repo, items):
    have = {i.section for i in items if i.classification != UNKNOWN}
    out = []
    for area, what in _AREAS:
        if area not in have:
            out.append(unknown(area, f"no {what} found in inspected sources"))
    out.append(unknown("Deployment", "production environment, hosting and runtime topology cannot be determined from repository evidence"))
    out.append(unknown("Architecture", "architectural style is not established from repository evidence; only structural signals are recorded"))
    out.append(unknown("Development Workflow", "branching strategy and review requirements are not established from repository evidence"))
    out.append(unknown("Constraints", "no explicit project constraints are recorded; they must be provided by the developer"))
    obs = [i for i in items if i.section == "Observability" and i.classification != UNKNOWN]
    if obs and not any(w in i.statement for i in obs for w in ("Prometheus", "Grafana", "dashboard", "Alertmanager", "Collector")):
        out.append(unknown("Observability", "monitoring backend, dashboards and alerting cannot be determined from repository evidence"))
    if repo.facts.get("db_signal"):
        out.append(unknown("Database", "engine version and production environment cannot be determined from repository evidence"))
    if "Infrastructure" in have:
        out.append(unknown("Infrastructure", "deployed infrastructure state and environments cannot be determined from repository files"))
    if repo.facts.get("api_signal") and not repo.facts.get("api_spec"):
        out.append(unknown("API", "no API contract or specification file found"))
    if "Testing" in have and not any("coverage" in i.statement.lower() or "coverlet" in i.statement.lower() for i in items):
        out.append(unknown("Testing", "coverage requirements not found"))
    return out

"""Observability configuration files and configuration sections. Libraries come from the manifest detectors."""
from __future__ import annotations

import re

from ..model import confirmed
from .common import config_keys

_FILES = (
    ("Prometheus configuration", "**/prometheus*.y*ml"), ("OpenTelemetry Collector configuration", "**/otel*.y*ml"),
    ("Alertmanager configuration", "**/alertmanager*.y*ml"), ("Logback configuration", "**/logback*.xml"),
    ("Log4j configuration", "**/log4j2*.*"), ("Grafana dashboards (by name)", "**/*dashboard*.json"),
)
_SECTION = re.compile(r"(?i)^(serilog|logging|applicationinsights|opentelemetry|nlog|sentry|datadog|otel)")


def detect(repo):
    items = []
    for label, pat in _FILES:
        hits = repo.find(pat)
        if hits:
            items.append(confirmed("Observability", f"{label}: {', '.join(hits[:4])}", *hits[:4]))
    dirs = repo.dirs_named("grafana", "dashboards", "alerts", "monitoring")
    if dirs:
        items.append(confirmed("Observability", f"Monitoring-related directories: {', '.join(dirs[:5])}", *dirs[:5]))
    for rel, keys in sorted(config_keys(repo).items()):
        secs = sorted({k.path.split(".")[0] for k in keys if _SECTION.match(k.path)})
        if secs:
            items.append(confirmed("Observability", f"Telemetry configuration sections in {rel}: {', '.join(secs)}", rel))
    return items

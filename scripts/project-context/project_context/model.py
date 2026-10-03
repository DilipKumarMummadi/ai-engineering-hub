"""Evidence model: every extracted statement is an Item with a classification and evidence."""
from __future__ import annotations

from dataclasses import dataclass

CONFIRMED = "Confirmed"
INFERRED = "Inferred"
UNKNOWN = "Unknown"
CLASSES = (CONFIRMED, INFERRED, UNKNOWN)

DEV_PROVIDED = "developer-provided"

# Sections rendered from items, in output order. "Known Unknowns" holds every Unknown item.
ITEM_SECTIONS = [
    "Project Overview",
    "Technology Stack",
    "Repository Structure",
    "Architecture",
    "Application Components",
    "API",
    "Database",
    "Frontend",
    "Testing",
    "Build and Run",
    "CI/CD",
    "Infrastructure",
    "Observability",
    "Security",
    "Development Workflow",
    "Coding Conventions",
    "Constraints",
]
UNKNOWNS = "Known Unknowns"

# Section names used by earlier (template-based) contexts, mapped to the generated names.
LEGACY_SECTIONS = {
    "Testing Conventions": "Testing",
    "Database Conventions": "Database",
    "API Conventions": "API",
    "Frontend Conventions": "Frontend",
    "Important Constraints": "Constraints",
    "Unknowns": UNKNOWNS,
    "Confirmed Facts": "Technology Stack",
}


@dataclass(frozen=True)
class Item:
    """One statement about the repository.

    `section` is the area the statement belongs to. For Unknown items it is the area the gap
    concerns; they are rendered together under "Known Unknowns".
    `statement` has the form "Subject: detail". The subject identifies the entry across runs.
    """

    section: str
    statement: str
    classification: str
    evidence: tuple = ()
    origin: str = "generated"  # "generated" or "developer"
    notes: tuple = ()

    def __post_init__(self):
        # Keep statements on one line and free of the separator used by the output format.
        clean = " ".join(self.statement.replace(" \u2014 ", " - ").split())
        object.__setattr__(self, "statement", clean)

    @property
    def subject(self) -> str:
        return self.statement.split(": ", 1)[0] if ": " in self.statement else self.statement

    @property
    def key(self):
        return (UNKNOWNS if self.classification == UNKNOWN else self.section, self.statement)


def confirmed(section, statement, *evidence):
    return Item(section, statement, CONFIRMED, tuple(sorted(set(evidence))))


def inferred(section, statement, *evidence):
    return Item(section, statement, INFERRED, tuple(sorted(set(evidence))))


def unknown(area, text):
    return Item(area, f"{area}: {text}", UNKNOWN, ())


@dataclass(frozen=True)
class Finding:
    """A safe report line: location and kind only, never a value."""

    kind: str
    path: str
    detail: str = ""

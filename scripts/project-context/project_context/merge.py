"""Merges an existing context with current evidence. The generator owns generated entries;
developer-provided entries and manual blocks are preserved."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .model import DEV_PROVIDED, UNKNOWN, UNKNOWNS, Item

# Terms grouped by family. In exclusive families, finding a different term than the one claimed is a conflict.
_FAMILIES = {
    "database": (True, {"postgresql": "PostgreSQL", "postgres": "PostgreSQL", "mysql": "MySQL", "mariadb": "MariaDB",
                        "sql server": "SQL Server", "sqlserver": "SQL Server", "oracle": "Oracle", "mongodb": "MongoDB", "sqlite": "SQLite"}),
    "ci": (True, {"github actions": "GitHub Actions", "jenkins": "Jenkins", "gitlab": "GitLab CI", "azure pipelines": "Azure Pipelines",
                  "circleci": "CircleCI", "travis": "Travis CI"}),
    "test framework": (True, {"jest": "Jest", "vitest": "Vitest", "mocha": "Mocha", "pytest": "pytest", "xunit": "xUnit",
                              "nunit": "NUnit", "junit": "JUnit"}),
    "platform": (False, {"kubernetes": "Kubernetes", "helm": "Helm", "terraform": "Terraform", "docker": "Docker",
                         "serverless": "Serverless", "bicep": "Bicep", "pulumi": "Pulumi"}),
}


_DOC_PREFIX = ("README states",)


@dataclass
class Result:
    items: list = field(default_factory=list)
    freeform: dict = field(default_factory=dict)
    extra_sections: dict = field(default_factory=dict)
    manual_blocks: list = field(default_factory=list)
    added: list = field(default_factory=list)
    removed: list = field(default_factory=list)
    changed: list = field(default_factory=list)      # (old statement, new statement)
    conflicts: list = field(default_factory=list)
    preserved: list = field(default_factory=list)    # developer-provided or manual-section entries kept
    update: bool = False


def _terms(text: str):
    low = text.lower()
    found = {}
    for fam, (_, words) in _FAMILIES.items():
        for w, canon in words.items():
            if re.search(rf"\b{re.escape(w)}\b", low):
                found.setdefault(fam, set()).add(canon)
    return found


def _subject(statement: str) -> str:
    return statement.split(": ", 1)[0]


def merge(parsed, new_items: list, manual_sections=()) -> Result:
    res = Result(update=parsed is not None)
    if parsed is None:
        res.items = list(new_items)
        return res

    res.freeform = {k: list(v) for k, v in parsed.freeform.items()}
    res.extra_sections = dict(parsed.extra_sections)
    res.manual_blocks = list(parsed.manual_blocks)

    manual = set(manual_sections)
    old_gen = [i for i in parsed.items if i.origin == "generated" and i.section not in manual and not (i.classification == UNKNOWN and UNKNOWNS in manual)]
    old_dev = [i for i in parsed.items if i.origin == "developer"]
    kept_manual = [i for i in parsed.items if i.origin == "generated" and i not in old_gen]

    gen = [i for i in new_items if i.section not in manual]
    new_by_key = {i.key: i for i in gen}
    old_by_key = {i.key: i for i in old_gen}

    added = [k for k in new_by_key if k not in old_by_key]
    removed = [k for k in old_by_key if k not in new_by_key]
    for k in set(new_by_key) & set(old_by_key):
        if new_by_key[k].classification != old_by_key[k].classification:
            res.changed.append((f"{old_by_key[k].statement} ({old_by_key[k].classification})", f"{new_by_key[k].statement} ({new_by_key[k].classification})"))

    # Pair a removed and an added entry that share section and subject: that is a change, not two events.
    rem_by_subject = {(k[0], _subject(k[1])): k for k in removed}
    for k in list(added):
        pair = rem_by_subject.get((k[0], _subject(k[1])))
        if pair and pair in removed:
            res.changed.append((old_by_key[pair].statement, new_by_key[k].statement))
            added.remove(k)
            removed.remove(pair)
    res.added = [new_by_key[k].statement for k in sorted(added)]
    res.removed = [old_by_key[k].statement for k in sorted(removed)]

    gen_text = " ".join(i.statement + " " + " ".join(i.evidence) for i in gen if i.classification != UNKNOWN and not i.statement.startswith(_DOC_PREFIX)).lower()
    gen_terms = _terms(gen_text)
    for k in removed:
        old = old_by_key[k]
        for fam, terms in _terms(old.statement).items():
            if _FAMILIES[fam][0] and gen_terms.get(fam) and not (terms & gen_terms[fam]):
                res.conflicts.append(
                    f"Existing entry '{old.statement}' ({', '.join(sorted(terms))}) is superseded by current evidence "
                    f"({', '.join(sorted(gen_terms[fam]))})"
                )

    final = list(gen)
    final_keys = {i.key for i in final}
    for it in kept_manual:
        final.append(it)
        res.preserved.append(it.statement)
    for it in old_dev:
        if it.key in final_keys:
            continue
        notes = []
        for fam, terms in _terms(it.statement).items():
            exclusive = _FAMILIES[fam][0]
            seen = gen_terms.get(fam, set())
            if terms & seen:
                continue
            if exclusive and seen:
                msg = f"Conflicts with repository evidence (found: {', '.join(sorted(seen))}); the developer should confirm"
                res.conflicts.append(f"Developer-provided entry '{it.statement}' conflicts with repository evidence ({', '.join(sorted(seen))})")
            else:
                msg = "No supporting repository evidence found by the generator; the developer should confirm"
                res.conflicts.append(f"Developer-provided entry '{it.statement}' is not supported by repository evidence")
            if msg not in notes:
                notes.append(msg)
        final.append(Item(it.section, it.statement, it.classification, (), "developer", tuple(notes[:2])))
        res.preserved.append(it.statement)
    res.items = final
    return res


def documentation_conflicts(items: list) -> list:
    """Repository-vs-repository conflicts: documentation prose that disagrees with declarations."""
    decl = " ".join(i.statement + " " + " ".join(i.evidence) for i in items if i.classification != UNKNOWN and not i.statement.startswith(_DOC_PREFIX)).lower()
    declared = _terms(decl)
    out = []
    for it in items:
        if not it.statement.startswith(_DOC_PREFIX):
            continue
        for fam, terms in _terms(it.statement).items():
            if _FAMILIES[fam][0] and declared.get(fam) and not (terms & declared[fam]):
                out.append(f"{it.evidence[0] if it.evidence else 'Documentation'} states {', '.join(sorted(terms))}, but repository declarations show {', '.join(sorted(declared[fam]))}; documentation may be out of date")
    return out

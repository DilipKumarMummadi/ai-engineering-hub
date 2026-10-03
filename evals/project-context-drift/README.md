# Project Context Drift Evaluations

Evaluation cases for the detection procedure defined in the [Project Context Drift Specification](../../docs/project-context-drift-specification.md). The context being checked is defined by the [Project Context Specification](../../docs/project-context-specification.md). The generator that creates it has its own [evaluations](../project-context-generator/README.md). For the general approach, see the [evaluation suite overview](../README.md).

## Purpose

Drift detection decides whether a repository has changed enough that its `PROJECT-CONTEXT.md` may be wrong. These cases check that it is **quiet about ordinary work, clear about real change, honest about conflicts, read-only and safe**.

The cases do not judge the quality of the repository or re-test the generator. They judge the detector: what it counts as drift, how it classifies it, what it leaves out, and whether it ever changes or exposes anything.

## Evaluation Structure

```
evals/project-context-drift/
├── README.md
└── cases/
    ├── no-drift.md
    ├── technology-drift.md
    ├── architecture-drift.md
    ├── stale-context.md
    ├── conflicting-context.md
    ├── infrastructure-drift.md
    ├── cicd-drift.md
    └── source-only-change.md
```

Each case describes its repository and its existing context in `# Context`. To run a case, recreate it in a scratch directory and run the check.

## What Is Verified

| Dimension | What the evaluator checks |
| --- | --- |
| **No noise** | Source, test, comment, documentation and build-output changes are not reported as drift. |
| **Detection in both directions** | Capabilities that appeared and capabilities that disappeared are both found. |
| **Materiality** | Each finding is Material, Potentially Material or Informational, for the reason the specification gives. No numeric scores. |
| **Stale context** | Statements the repository no longer supports are quoted and reported. None is deleted. |
| **Conflict handling** | Disagreements are surfaced. Neither side is chosen silently. Developer-provided entries are not hidden. |
| **Evidence** | Each finding cites repository paths. Prose and directory names are not evidence. |
| **Read-only behavior** | No file, including the context, is modified. Nothing is committed or run. |
| **CI behavior** | Concise output. Non-zero exit only for Material drift. |
| **Secret exclusion** | No secret or fragment appears in any output. Sensitive files are not opened or cited. |
| **Independence from Git** | Works without version control. Git is supporting evidence only. |

## Coverage

| Dimension | Primary cases |
| --- | --- |
| No noise | source-only-change, no-drift |
| Detection in both directions | technology-drift, architecture-drift, infrastructure-drift |
| Materiality | technology-drift, architecture-drift, cicd-drift |
| Stale context | stale-context |
| Conflict handling | conflicting-context |
| Evidence | infrastructure-drift, stale-context |
| Read-only behavior | all cases |
| CI behavior | cicd-drift, source-only-change |
| Secret exclusion | infrastructure-drift |
| Independence from Git | source-only-change |

## Case Format

Each case is a Markdown file with these sections, in this order:

| Section | Content |
| --- | --- |
| `# Scenario` | The situation and what the case tests. |
| `# Input` | The request given to the assistant or tool. |
| `# Context` | The repository, the existing context, and what changed. |
| `# Expected Behavior` | What the detector should find, classify and report. |
| `# Important Checks` | What the evaluator verifies. |
| `# Failure Conditions` | Behavior that is incorrect. |
| `# Notes` | Evaluator notes, and where the reference implementation reproduces the case. |

Cases test behavior, not wording.

## Evaluation Outcomes

Each run gets one qualitative outcome. There are no numeric scores.

| Outcome | Meaning |
| --- | --- |
| **Pass** | Real change is found and classified correctly, ordinary change is ignored, conflicts and stale statements are surfaced, nothing is modified, and no sensitive content appears. |
| **Needs Improvement** | Safe and mostly right, but with a missed Potentially Material item, a weak classification, an unneeded Informational note or an unclear report. |
| **Fail** | A file is modified, a secret appears, ordinary source or documentation change is reported as drift, Material drift is missed, a conflict is hidden or resolved silently, CI fails on an ordinary change, or the exit code is wrong. |

A secret in the output, or any modification of the repository, is a **Fail** regardless of the rest.

## Running a Case

1. Recreate the repository and the existing context in a scratch location.
2. Run `project-context drift --repo <path>`, and with `--ci` for the CI cases. Or ask an assistant to follow the specification.
3. Read the report. Search the whole output for any planted sensitive value.
4. Confirm the repository is unchanged.
5. Compare with Expected Behavior, Important Checks and Failure Conditions, and assign an outcome.

## Implementation Results

The cases were run against the reference implementation in [`scripts/project-context/`](../../scripts/project-context/README.md). Each case's repository and context are reproduced in `scripts/project-context/tests/test_drift_evals.py` (one `Eval*` class per case), and the checks a deterministic tool can meet are executable there. Judged on 2026-10-04 by the person who built the tool, so this is a first, non-independent pass. It says nothing about an assistant following the specification, which has not been run.

| Case | Outcome | Why |
| --- | --- | --- |
| no-drift | Pass | Patch-level and documentation edits produce `NO DRIFT`; unchanged technologies are not listed. |
| technology-drift | Pass | New framework, removed framework and runtime change all reported as Material with evidence; the removed one is quoted under Stale Context. |
| architecture-drift | Pass | New project is Potentially Material, removed application is Material, edits inside projects are ignored. |
| stale-context | Needs Improvement | Stale statements are quoted and nothing is deleted, and README prose is not evidence. But a hand-written statement that cannot be matched by vocabulary (for example a custom deployment mechanism) is not detected as stale. |
| conflicting-context | Needs Improvement | Frontend, database and CI conflicts are surfaced, including the developer-provided one. But conflicts outside the fixed vocabulary, for example a changed pagination style, are not detected because source is not read. |
| infrastructure-drift | Pass | Terraform appears, Docker disappears, a `kubernetes` directory is not evidence, sensitive files are neither opened nor cited, and no planted fragment appears. |
| cicd-drift | Pass | A new workflow gives exit 0; removing the only CI gives exit 1; output is concise; nothing is written. |
| source-only-change | Pass | Source, test, documentation and build-output changes give `NO DRIFT`; Git adds an Informational note only when present. |

No case produced a Fail. Open items are the limitations in the specification and the tool's README.

## Adding a Case

Add one file under `cases/`. Prefer a scenario where the right behavior includes reporting nothing, reporting something at a lower level, or declining to choose between a context statement and the repository.

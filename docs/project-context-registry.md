# Project Context Registry

The artifacts of the project context layer. For what project context is, see [Project Context](project-context.md). The project context layer has no agents, skills, commands or workflows of its own. It is information, plus a procedure for generating it.

## Status Values

| Status | Meaning |
| --- | --- |
| **Planned** | Defined but not yet implemented. |
| **In Progress** | Written, with evaluation cases written where applicable, but the cases have not yet been run and judged. |
| **Evaluated** | The evaluation cases have been run and judged, and the outcomes recorded. |
| **Stable** | Evaluated, with no open Needs Improvement or Fail outcomes, and in regular use. |

Statuses are qualitative. There are no scores or rankings.

## Registry

| Artifact | Location | Purpose | Evaluation | Status |
| --- | --- | --- | --- | --- |
| Project Context Specification | [`docs/project-context-specification.md`](project-context-specification.md) | Canonical structure and rules for project context | Covered by the generator evaluations | In Progress |
| Project Context overview | [`docs/project-context.md`](project-context.md) | How the Hub uses project context | | In Progress |
| Project context template | [`templates/project-context/PROJECT-CONTEXT.md`](../templates/project-context/PROJECT-CONTEXT.md) | Reusable template for a repository's context | Covered by the generator evaluations | In Progress |
| Generator specification | [`docs/project-context-generator-specification.md`](project-context-generator-specification.md) | Procedure for generating and updating a context from repository evidence | [`evals/project-context-generator/`](../evals/project-context-generator/README.md) | In Progress |
| Generator configuration template | [`templates/project-context/GENERATOR-CONFIG.md`](../templates/project-context/GENERATOR-CONFIG.md) | Optional scope, sensitivity and refresh settings | | In Progress |
| Generator implementation | [`scripts/project-context/`](../scripts/project-context/README.md) | Local command line tool (`generate`, `update`, `--dry-run`) for the deterministic part of the procedure | Automated tests in `scripts/project-context/tests/`; the six generator cases, run against the tool (see the evals README) | Evaluated |
| Drift specification | [`docs/project-context-drift-specification.md`](project-context-drift-specification.md) | Read-only procedure for detecting that a context may be stale | [`evals/project-context-drift/`](../evals/project-context-drift/README.md) | In Progress |
| Drift detector implementation | [`scripts/project-context/`](../scripts/project-context/README.md) | `drift` (alias `check`, `--ci`) command of the same tool. Reports; never modifies | Automated tests in `scripts/project-context/tests/test_drift.py` and `test_drift_evals.py`; the eight drift cases, run against the tool (see the evals README) | Evaluated |
| Context consumption standard | [`docs/project-context-consumption.md`](project-context-consumption.md) | How agents and workflows discover, validate and use a context | [`evals/integration/context-aware-agents/`](../evals/integration/context-aware-agents/README.md) | In Progress |
| Context consumption by agents and workflows | `.claude/agents/`, `.github/agents/`, `.claude/workflows/`, `.github/workflows/` | A short Project Context section in each of the seven agents and seven workflows | Same cases. Not yet run by an assistant | In Progress |
| Context consumption by skills | None | Skills stay generic and do not read project context | | Not planned |

The specification, overview, templates and configuration are In Progress because the generator cases have not been run by an assistant following the specification. The generator implementation is Evaluated: its tests pass and the six generator cases were run against it, with three Pass and three Needs Improvement outcomes still open (see the [generator evaluations](../evals/project-context-generator/README.md#implementation-results)). It is therefore not Stable.

## Repository Contexts

The Hub does not contain a project-specific context. A repository that adopts project context keeps its own `PROJECT-CONTEXT.md`, and may record it in its own documentation.

## Changing the Layer

- Keep the structure in the Project Context Specification and the template in step. The generator specification maps its coverage onto the template, and that mapping is the one place to update if the template changes.
- Keep the generator (creates or updates the context) and the drift detector (reports whether it may be stale) separate. The detector never writes. Add drift cases under `evals/project-context-drift/cases/` when its behavior changes, and keep `test_drift_evals.py` in step.
- Add evaluation cases under `evals/project-context-generator/cases/` when the generator's behavior changes, and keep the executable forms in `scripts/project-context/tests/test_evals.py` in step.
- Keep the status in line with the evaluation results.

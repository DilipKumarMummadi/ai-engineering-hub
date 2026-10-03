# Change Intelligence Evaluations

Evaluations for the [`change-intelligence`](../../.claude/skills/change-intelligence/SKILL.md) skill as used by the [`change-intelligence-agent`](../../.claude/agents/change-intelligence-agent.md) and the `/change-impact` command. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case, and the [Change Intelligence Specification](../../docs/change-intelligence-specification.md) for the standard.

## What Is Being Evaluated

Whether the capability reports the impact a change really has, with evidence, and stops there. It should find what is affected, label what it knows and what it only infers, and say plainly when nothing meaningful is affected or when the repository cannot answer.

## Dimensions

| Dimension | Question |
| --- | --- |
| Change detection | Are the changed areas and categories identified from content, not only paths? |
| Impact identification | Are direct, dependency, contract, data, runtime, testing and operational impacts found where they exist? |
| Dependency reasoning | Are dependents traced from the repository, and are the search limits stated? |
| Evidence handling | Is every statement Confirmed, Inferred or Unknown, and is an inference never presented as fact? |
| Risk identification | Are risks qualitative, evidence-based, and marked as hypotheses when unconfirmed? |
| Validation recommendations | Are they proportional, and is "recommended" kept apart from "run"? |
| Skill selection | Are only the skills the impact calls for recommended, and are recommended skills kept apart from applied ones? |
| False positives | Is a safe or trivial change left alone? |
| Unknown handling | Are things the repository cannot establish reported as unknown and not guessed? |

## Common Failure Modes

- Classifying from the file name alone.
- Presenting an inferred consumer or call path as fact.
- Treating "nothing found" as "nothing depends on it".
- Inflating risk on a safe change, or missing the one real risk.
- Recommending every skill.
- Claiming tests were run.
- Reviewing the code for defects instead of analyzing impact.
- Reproducing a secret.

## Evaluation Process

1. Give the case's `# Input` and `# Context` to the `change-intelligence-agent` (or run `/change-impact`).
2. Compare the report to Expected Behavior, Important Checks and Failure Conditions.
3. Judge the dimensions above.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [api-database-change](cases/api-database-change.md) | Traces an API change and a migration together, selects the right supporting perspectives, and skips the rest. |
| [frontend-api-change](cases/frontend-api-change.md) | Finds a client that depends on a changed response, and treats unseen consumers as unknown. |
| [security-sensitive-change](cases/security-sensitive-change.md) | Recognizes an access-rule change, keeps the risk evidence-based, and never exposes a secret. |
| [database-migration](cases/database-migration.md) | Reports data and rollout impact of a migration without inventing table facts. |
| [infrastructure-change](cases/infrastructure-change.md) | Identifies runtime and deployment impact of a configuration change, and recommends non-production validation only. |
| [performance-change](cases/performance-change.md) | Identifies a plausible performance effect as a hypothesis and recommends measurement. |
| [no-impact-change](cases/no-impact-change.md) | Reports a comment-only change as having no meaningful impact. |
| [unknown-dependency](cases/unknown-dependency.md) | States that external consumers cannot be established and does not guess. |

All cases are **not yet run**. A pilot on representative repositories, with what it found, is in [the pilot record](../pr-intelligence/pilot.md). Status is recorded in the [Agent Registry](../../docs/agent-registry.md).

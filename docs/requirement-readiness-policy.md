# Requirement Readiness Policy

The Readiness Policy states what each [readiness outcome](requirement-readiness-gate.md) allows. It is the implementation gate.

## 1. Rule

| Readiness | Implementation |
| --- | --- |
| `READY` | Implementation **MAY** begin |
| `NEEDS_CLARIFICATION` | Implementation **SHOULD NOT** begin |
| `BLOCKED` | Implementation **MUST NOT** begin |

## 2. READY Is Not a Start Signal

`READY` means the requirement is sufficiently understood to begin implementation. It does not start implementation. The user must still explicitly ask for it, for example with `/feature BR-7368`.

This holds even when readiness is `READY` and confidence is `HIGH`. The Hub never starts coding because a requirement became ready.

## 3. Confidence Is Not the Gate

Confidence alone never permits implementation. See [Requirement Confidence](requirement-confidence.md).

## 4. What the Workflows Do

| Situation | Behavior |
| --- | --- |
| `/feature <ticket key>` and the requirement is `READY` | The workflow continues to the next stage, under the normal checkpoints |
| `/feature <ticket key>` and `NEEDS_CLARIFICATION` or `BLOCKED` | The workflow stops before implementation and returns the blocked result below |
| `/feature` with requirement text and no ticket | The requirement is assessed in the same way. Supplying a ticket is not mandatory |
| A ticket cannot be retrieved but the user pasted the text | The text is assessed. The report says the ticket could not be retrieved |

The blocked result:

```text
Implementation blocked.

Requirement:
BR-7368

Readiness:
NEEDS_CLARIFICATION

Blocking questions:
...

Recommended action:
Refine the Jira requirement and re-run readiness.
```

`SHOULD NOT` for `NEEDS_CLARIFICATION` means the workflows stop. A user who chooses to proceed anyway states that decision explicitly, in words, and the decision and the unresolved questions are recorded in the workflow output. The workflow never makes that choice for the user. `BLOCKED` has no override: there is nothing to build from.

## 5. Scope by Workflow

| Workflow | Readiness use |
| --- | --- |
| feature-development | Stage 1 includes the gate. Implementation (stage 7) does not begin unless `READY` |
| api-change | When a ticket is supplied or the request is a new requirement, the gate applies. Contract, compatibility and consumers are the prioritized dimensions |
| database-change | Same. Schema, data, migration, rollback and concurrency are prioritized |
| bug-fix | Lighter. Symptom, expected behavior, reproduction, environment and impact. An incident is not delayed by a ticket gate |
| e2e-test-creation | Same. User journey, preconditions, test data, authentication and assertions |
| production-incident | No gate. Stabilization does not wait for a ticket to be ready |

## 6. External Writes

The policy covers implementation. It does not cover the ticket. Updating a ticket needs its own explicit approval of the exact change. See the [Requirement Intelligence Specification](requirement-intelligence-specification.md#8-human-control-and-jira-updates).

## 7. Inheritance

The policy adds to the Hub's existing safety rules and weakens none of them. Migrations, deployments, merges, pushes and production changes still need their own explicit authorization, whatever the readiness.

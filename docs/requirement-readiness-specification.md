# Requirement Readiness Specification

Requirement Readiness is the outcome of assessing a requirement before implementation. It belongs to [Requirement Intelligence](requirement-intelligence-specification.md). This specification defines the question it answers, the vocabulary, the dimensions and the question classes. The rule that turns an outcome into a decision is in the [Readiness Gate](requirement-readiness-gate.md), and what each outcome means for implementation is in the [Readiness Policy](requirement-readiness-policy.md). How sure the Hub is of its understanding is a separate matter, defined in [Requirement Confidence](requirement-confidence.md).

## 1. The Question

> Is there enough validated information to safely begin engineering implementation?

Readiness is about the requirement, not about the engineer, the team or the code. It is judged from evidence and reported with that evidence.

## 2. Outcomes

Only three values exist.

| Outcome | Meaning |
| --- | --- |
| `READY` | The requirement is sufficiently understood to begin implementation |
| `NEEDS_CLARIFICATION` | Enough is known to continue refining the requirement, not enough to start safely |
| `BLOCKED` | Evidence or capability needed to assess the requirement is unavailable |

There is no numeric readiness score, percentage or weighted total, and none may be introduced. The outcome is explained with evidence, not numbers.

## 3. Dimensions

A dimension is one aspect of the requirement that must be understood. Dimensions are chosen per requirement from the kind of change. The Hub does not apply one fixed checklist.

| Dimension | Asks |
| --- | --- |
| Business Objective | Why is this wanted, and for whom |
| Scope | What is in, and what is explicitly out |
| Functional Behavior | What the system must do, in observable terms |
| Acceptance Criteria | Can a third party decide pass or fail from them |
| Technical Context | Where this lives in the system, and what already exists |
| Dependencies | What else must exist, change or be available |
| API Impact | Contracts, consumers, compatibility |
| Database Impact | Schema, data, migration, rollback |
| Security Impact | Who may do it, what is exposed, what input is trusted |
| Performance Impact | Volumes, limits, latency expectations |
| Testing Expectations | What must be tested and at what level |
| Operational Impact | Deployment, configuration, monitoring, support |
| Edge Cases | Empty, large, duplicate, concurrent, failing inputs and states |
| External Integrations | Other systems, their behavior and ownership |
| Data Requirements | Data needed, its source, quality and sensitivity |

Other dimensions may be added when the requirement calls for them, for example Rollback for a data migration or Accessibility for a user interface.

### Dimension status

Each dimension carries one status.

| Status | Meaning |
| --- | --- |
| `CLEAR` | Understood well enough for this requirement, with the source stated |
| `PARTIAL` | Partly understood. The gap is stated |
| `MISSING` | Needed and not provided |
| `UNKNOWN` | Needed and cannot currently be established |
| `NOT_APPLICABLE` | This change does not touch it. Not a gap |

A dimension that does not apply is `NOT_APPLICABLE`, not `MISSING`. A user-interface-only change has `Database Impact: NOT_APPLICABLE`. A database migration has `Database Impact`, `Data Requirements` and `Rollback` all applicable, and all expected to be `CLEAR` before `READY`.

Dimensions are the common checkpoints. During an interactive session the set also grows with the checkpoints the requirement and the answers make relevant, each with an importance and a resolution. See [Interactive Requirement Discovery](interactive-requirement-discovery.md#4-checkpoints).

## 4. Dynamic Selection

The requirement type decides which dimensions carry weight.

| Kind of requirement | Prioritized dimensions |
| --- | --- |
| API change | Functional Behavior, API Impact (contract, compatibility, consumers), validation, Security Impact, Testing Expectations |
| Database change | Database Impact (schema), Data Requirements, migration, rollback, Performance Impact, transactions and concurrency, Testing Expectations |
| User interface change | Functional Behavior (user behavior and states), validation, accessibility where it applies, Testing Expectations (browser level) |
| Security change | Threat model, authorization, authentication, data exposure, validation |
| End-to-end test | User journey, preconditions, test data, authentication, expected states, assertions |
| Bug fix | Symptom, expected behavior, reproduction, environment, impact |
| Integration | External Integrations, Dependencies, failure behavior, Data Requirements |

A bug report is not forced into feature-style criteria. For a defect, the questions are what is wrong, what should happen instead, how to reproduce it and what it affects.

## 5. Questions

Every open question is classified. A missing piece of information does not automatically stop implementation.

| Class | Meaning | Effect |
| --- | --- | --- |
| `BLOCKING` | Work cannot start safely without the answer, because it would decide behavior, data, security or scope | Prevents `READY` while unresolved |
| `IMPORTANT` | Should be answered, and work can start with a stated assumption or a default | Reported. Does not prevent `READY` |
| `OPTIONAL` | Useful detail that can be settled during implementation | Reported. Does not prevent `READY` |

Example:

1. Should external users be supported? `BLOCKING`. It decides authorization and the data model.
2. What maximum file size should be supported? `IMPORTANT`.
3. Should the success message use specific wording? `OPTIONAL`.

A question is `BLOCKING` only with a stated reason. Marking everything `BLOCKING` to be safe is a failure, and so is marking a real decision `OPTIONAL` to reach `READY`.

## 6. Evidence

Each dimension status rests on evidence of these classes.

| Class | Meaning |
| --- | --- |
| **Confirmed** | Stated in the requirement, or shown by repository, Project Context, Engineering Memory with provenance, or provider evidence |
| **Inferred** | A reasonable reading that no source states |
| **Unknown** | Not established |
| **Missing** | Needed and not provided |
| **Ambiguous** | More than one reasonable reading |

Inferred is never reported as Confirmed. Unknown is never turned into an assumption. The Hub does not fabricate requirement details. Current repository evidence wins over Project Context and Engineering Memory, which only orient the assessment.

## 7. Report

```markdown
# Requirement Readiness — BR-7368

## Overall
NEEDS_CLARIFICATION

## Confidence
MEDIUM — <reason>

## Assessment
| Area | Status |
| --- | --- |
| Business Objective | CLEAR |
| Scope | CLEAR |
| Acceptance Criteria | PARTIAL |
| Technical Context | CLEAR |
| Dependencies | UNKNOWN |
| API Impact | NOT_APPLICABLE |
| Database Impact | UNKNOWN |
| Security | CLEAR |
| Testing | PARTIAL |

## Blocking Questions
1. ...

## Recommendation
Clarify the following before implementation: ...

## Implementation Gate
BLOCKED for implementation until the blocking questions are resolved
```

The report always shows readiness and confidence together. The Implementation Gate line states the consequence under the [Readiness Policy](requirement-readiness-policy.md).

## 8. What Readiness Is Not

- Not a quality score for the ticket.
- Not approval to implement. See the [Readiness Policy](requirement-readiness-policy.md).
- Not a prediction that the work will succeed.
- Not confidence. See [Requirement Confidence](requirement-confidence.md).
- Not permanent. A changed requirement is assessed again.

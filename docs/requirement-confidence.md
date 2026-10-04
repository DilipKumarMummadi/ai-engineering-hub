# Requirement Confidence

Confidence is part of [Requirement Intelligence](requirement-intelligence-specification.md). It is reported next to [Requirement Readiness](requirement-readiness-specification.md) and is not the same thing.

## 1. The Question

> How confident is the Hub in its current understanding of the requirement?

Readiness asks whether work may begin. Confidence asks how sure the understanding is. A requirement can be well understood and still have a blocking question, and a short requirement can be ready while its confidence is only `MEDIUM`.

## 2. Values

Only four values exist.

| Value | Meaning |
| --- | --- |
| `HIGH` | The requirement is explicit, its criteria are testable, the evidence confirms the affected areas, and nothing material is unresolved |
| `MEDIUM` | The core is understood, with some inference, a partial dimension or a non-blocking open question that could change details |
| `LOW` | Much of the understanding is inferred, the requirement is thin or ambiguous, or the evidence conflicts |
| `UNKNOWN` | There is not enough to judge, for example the requirement could not be read |

The Hub never uses numeric confidence such as `87%` or `94%`. False precision is misleading.

## 3. The Reason Is Always Shown

Every confidence value is given with the reason, tied to evidence.

```text
Confidence: HIGH

Reason:
The requirement is explicit, acceptance criteria are testable,
the repository confirms the affected components, and there are
no unresolved blocking questions.
```

Factors to reason about:

| Factor | Raises confidence | Lowers confidence |
| --- | --- | --- |
| Explicitness | Behavior stated in the requirement | Behavior inferred from a title or a brief line |
| Acceptance criteria | Testable and observable | Missing, vague or contradictory |
| Repository evidence | Affected components found and confirmed | Not found, or found and conflicting |
| Project Context | Agrees with the repository | Stale or in conflict with the repository |
| Engineering Memory | A relevant entry with valid provenance agrees | None exists, or an entry is outdated or disputed |
| Open questions | None unresolved, or only `OPTIONAL` | Unresolved `BLOCKING` questions |
| Source availability | The ticket was read in full | The ticket or part of it could not be retrieved |

## 4. Readiness and Confidence Together

The result always shows both.

```text
Requirement Readiness: READY
Confidence: HIGH
```

```text
Requirement Readiness: NEEDS_CLARIFICATION
Confidence: MEDIUM
```

| Pair | Reading |
| --- | --- |
| `READY` and `HIGH` | Sufficiently understood, and the understanding is well supported |
| `READY` and `MEDIUM` | Nothing blocks. Some details are inferred or unsettled, and they are listed |
| `NEEDS_CLARIFICATION` and `HIGH` | The Hub understands the requirement well, and it is missing something only the requester can decide |
| `NEEDS_CLARIFICATION` and `LOW` | The requirement is thin, so both the gaps and the understanding are weak |
| `BLOCKED` and `UNKNOWN` | The requirement could not be assessed |

## 5. Confidence Does Not Pass the Gate

The implementation gate is readiness, as set out in the [Readiness Policy](requirement-readiness-policy.md). High confidence never overrides `NEEDS_CLARIFICATION` or `BLOCKED`. Confidence exists so an engineer can judge how far to trust the assessment.

## 6. Confidence Can Change

Confidence is recalculated after each refinement cycle. A user-confirmed answer raises confidence in that checkpoint, an inference or a convention awaiting confirmation does not, and an unresolved conflict lowers it. Confidence changes when evidence changes: a ticket is updated, questions are answered, a conflict with the repository is found or resolved. After an update, assess again. Do not carry the earlier value forward.

# Requirement Readiness Gate

The Readiness Gate is the rule that turns a [Requirement Readiness](requirement-readiness-specification.md) assessment into an outcome. The consequence of each outcome for implementation is in the [Readiness Policy](requirement-readiness-policy.md). The gate uses evidence and the question classes. It uses no scores.

## 1. Outcomes

### READY

The requirement is sufficiently understood to begin implementation. This normally means:

- the business objective is clear;
- the scope is clear;
- the expected behavior is clear;
- the acceptance criteria are sufficiently testable;
- no `BLOCKING` question is unresolved;
- major dependencies are known;
- relevant technical context is available;
- applicable security concerns are understood;
- applicable data and API implications are understood;
- testing expectations are sufficient.

"Sufficient" means enough for the work at hand, judged from the applicable dimensions. It does not mean perfect. `PARTIAL` dimensions and unresolved `IMPORTANT` or `OPTIONAL` questions are allowed when they are reported and do not decide behavior, data, security or scope.

### NEEDS_CLARIFICATION

There is enough information to continue refining the requirement, not enough to start implementation safely. Typical causes:

- an unresolved `BLOCKING` question;
- an applicable dimension the work depends on is `MISSING` or `UNKNOWN`;
- acceptance criteria that cannot be decided as pass or fail, and no way to settle them from evidence;
- the requirement conflicts with current repository evidence and the conflict is unresolved.

The assessment names what must be clarified and, where it is known, who can answer.

### BLOCKED

Evidence or capability needed to assess the requirement is unavailable. Typical causes:

- the ticket cannot be retrieved because the requirements-tracking capability is unavailable, and no requirement text was supplied;
- the requirement is referenced by a key that cannot be resolved;
- the requirement text is unreadable or empty.

Example: Jira cannot be retrieved because the requirements-tracking MCP is unavailable.

`BLOCKED` is about the ability to assess. It is not a judgment that the requirement is bad. It ends when the evidence becomes available, for example when the user supplies the requirement text.

## 2. Decision Order

Apply in this order and stop at the first that holds.

1. The requirement cannot be obtained or read: `BLOCKED`.
2. A `BLOCKING` question is unresolved: `NEEDS_CLARIFICATION`.
3. An applicable dimension the work depends on is `MISSING` or `UNKNOWN`: `NEEDS_CLARIFICATION`.
4. Acceptance criteria are not sufficiently testable: `NEEDS_CLARIFICATION`.
5. An unresolved conflict with current repository evidence: `NEEDS_CLARIFICATION`.
6. Otherwise: `READY`.

An empty list of findings is not enough for `READY`. The assessment states the evidence that each applicable dimension is `CLEAR`.

## 3. Confidence Does Not Pass the Gate

The gate is decided by readiness. Confidence is reported next to it and never replaces it.

| Readiness | Confidence | Result |
| --- | --- | --- |
| `READY` | `HIGH` | Implementation may begin when requested |
| `READY` | `MEDIUM` or `LOW` | Implementation may begin when requested. The reason for the uncertainty is stated |
| `NEEDS_CLARIFICATION` | `HIGH` | Still does not pass. A blocking question is a blocking question |
| `BLOCKED` | `UNKNOWN` | Does not pass |

## 4. Re-evaluation

The gate is evaluated again whenever the requirement changes: after a ticket update, after each meaningful answer, after the user adds context or supplies replacement text, and after a conflict is decided. A new checkpoint discovered during refinement can move a requirement from fewer to more open blocking checkpoints. An unresolved critical conflict keeps the outcome at `NEEDS_CLARIFICATION`. The user finishing a session early does not change the outcome. An `IMPORTANT` checkpoint the user explicitly accepts as unknown is recorded and does not block. Updating a ticket does not by itself make a requirement `READY`.

## 5. Dynamic Checks

The dimensions checked depend on the kind of requirement. The [Readiness Specification](requirement-readiness-specification.md#4-dynamic-selection) lists them. A dimension that does not apply is `NOT_APPLICABLE` and never counts against the gate.

## 6. Configuration

There is no gate configuration mechanism and none is invented. The gate is the rule in this document, applied by the [requirement-intelligence-agent](../.claude/agents/requirement-intelligence-agent.md). A team that wants a different rule changes this document through the normal review process in [Productionization](productionization.md).

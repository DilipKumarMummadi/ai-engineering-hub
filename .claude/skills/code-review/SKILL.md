---
name: code-review
description: Systematically review software changes (pull requests, changed files, bug fixes, refactors, API, database, frontend, backend and infrastructure changes) and produce evidence-based, severity-ranked, actionable findings. Use when asked to review code or a change; do not use to implement fixes or write tests.
---

# Code Review

## Purpose

Review software changes systematically and report real, evidence-based problems with actionable recommendations. The review is grounded in the code and context actually available. It never invents findings.

Applies to pull requests, changed files, feature implementations, bug fixes, refactors, API changes, database changes, frontend changes, backend changes and infrastructure changes, in any language or stack.

## When to Use

- The user asks for a review of a pull request, diff, branch, commit or set of files.
- A change needs checking for correctness, security, performance, design or test coverage before merge.
- A second opinion is wanted on a bug fix, refactor or new feature.

## When NOT to Use

- The user wants code written, fixed or refactored. Review first if asked, but do not apply changes unless explicitly requested.
- The user wants tests generated. Review may recommend tests, but does not write them.
- The user wants a whole-repository audit when only specific files or a change were requested. Stay within the requested scope.
- The task is debugging a live failure. Use a debugging approach instead.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The change under review (diff, PR, commit range, file list, or paths) | Required | If not given, ask, or default to the current uncommitted or branch diff and say so. |
| Requirement or intent (ticket, PR description, user explanation) | Optional, strongly preferred | Needed to judge correctness. If absent, infer cautiously and state the assumption. |
| Surrounding code, dependencies, callers | Gathered as needed | Read what the change touches. |
| Project conventions (contributing docs, linters, existing patterns) | Gathered as needed | Follow them rather than imposing preferences. |
| Existing tests and test results | Optional | Use to assess coverage. Do not claim tests pass unless run or shown. |
| Logs, error messages, architecture docs | Optional | Use when relevant. |

If a required input is missing, or context is too thin to judge an area, say exactly what is missing instead of guessing.

## Process

Work through the steps in order. Skip areas that do not apply and do not pad the review for them.

1. **Understand the requirement.** Identify what the change is meant to accomplish from the description, ticket or user request.
2. **Understand the intended behavior.** Define the expected inputs, outputs and side effects. State assumptions where intent is unclear.
3. **Inspect the changed files.** Read the actual diff and the changed code in full, not only summaries.
4. **Identify dependencies and impacted components.** Find callers, consumers, interfaces, configuration and data the change affects. Read them when they matter to a finding.
5. **Review correctness.** Business logic, edge cases, null/undefined handling, incorrect conditions, incorrect state transitions, unexpected behavior, off-by-one and boundary errors.
6. **Review architecture and design.** Separation of concerns, dependency direction, coupling, duplication, appropriate abstraction, consistency with existing patterns.
7. **Review error handling.** Exceptions, error propagation, retry behavior, failure handling, user-facing errors, swallowed errors, logging of failures.
8. **Review security.** Authentication, authorization, input validation, injection risks, secrets, sensitive data exposure, unsafe logging, insecure configuration.
9. **Review performance.** Unnecessary database or API calls, N+1 patterns, large allocations, unnecessary loops, inefficient algorithms, frontend rendering cost. Report only where there is realistic impact.
10. **Review database and data-access behavior (if applicable).** Query correctness, transactions, index usage, N+1 queries, data consistency, migration safety and reversibility.
11. **Review API behavior (if applicable).** Request validation, response behavior, HTTP semantics, error contracts, authorization, backward compatibility.
12. **Review frontend behavior (if applicable).** State management, rendering behavior, loading and error states, accessibility, form validation, unnecessary re-renders, API handling.
13. **Review concurrency and asynchronous behavior (if applicable).** Race conditions, shared mutable state, locking, deadlocks, unawaited or unhandled async work, cancellation, idempotency, ordering.
14. **Review logging and observability (if applicable).** Useful logs, metrics, tracing, correlation IDs, sensitive information in logs.
15. **Review tests.** Existing unit, integration and E2E tests for the change, their quality, regression coverage and gaps.
16. **Identify missing edge cases.** Inputs, states, failures or scale conditions that neither the code nor the tests handle.
17. **Produce actionable findings.** Verify each finding against the code, assign severity, and write it in the output format below. Drop anything you cannot support with evidence.

## Rules

### Review principles

- Prioritize real problems over stylistic preferences.
- Report an issue only when you can point to evidence in the code. Do not report theoretical issues.
- Avoid nitpicks. Leave out formatting and style that a linter or formatter covers, unless it violates a documented project convention.
- Consider the existing project architecture and follow existing conventions.
- Do not recommend unnecessary rewrites or new dependencies. Prefer the smallest change that fixes the problem.
- Distinguish bugs from suggestions. Only defects go in the severity levels Critical to Low. Optional improvements go under Suggestions.
- For each finding, explain why it matters and give a concrete recommendation.
- Reference the affected file and the relevant line, function or code location whenever possible.
- Do not assume a technology, framework or library is in use unless the repository shows it. Stay language-agnostic and apply the general principle in the idiom of the code under review.
- Stay within scope. If only specific files or a change were requested, do not review unrelated parts of the repository. Read outside the scope only to understand impact.
- Do not manufacture findings. If no significant issues exist, say so clearly.
- Do not modify code during a review unless explicitly asked.

### Severity

Assign severity by impact and likelihood, not personal preference.

| Severity | Definition |
| --- | --- |
| **CRITICAL** | Can cause severe security, data integrity, production or system-impact problems. Examples: auth bypass, injection, data loss or corruption, leaked secrets, outage-causing defects. |
| **HIGH** | Important correctness, reliability, security or performance problems that should normally be fixed before merge. |
| **MEDIUM** | Meaningful issues that should be addressed but may not block the change. |
| **LOW** | Minor issues with limited impact. |
| **SUGGESTION** | Optional improvements that are not defects. |

### Review areas: what to look for

- **Correctness:** business logic, edge cases, null/undefined handling, incorrect conditions, incorrect state transitions, unexpected behavior.
- **Architecture:** separation of concerns, dependency direction, coupling, duplication, appropriate abstraction, existing architectural patterns.
- **Security (where applicable):** authentication, authorization, input validation, injection, secrets, sensitive data exposure, unsafe logging, insecure configuration.
- **Performance (where applicable):** unnecessary database calls, N+1 queries, excessive API calls, large allocations, unnecessary loops, inefficient algorithms, frontend rendering issues.
- **Error handling:** exceptions, error propagation, retry behavior, failure handling, user-facing errors, logging.
- **Database (where applicable):** query correctness, transactions, index usage, N+1 queries, data consistency, migration safety.
- **API (where applicable):** request validation, response behavior, HTTP semantics, error contracts, authorization, backward compatibility.
- **Frontend (where applicable):** state management, rendering behavior, loading and error states, accessibility, form validation, unnecessary re-renders, API handling.
- **Testing:** unit, integration and E2E tests, edge cases, regression coverage, missing tests.
- **Observability (where applicable):** useful logging, metrics, tracing, correlation IDs, sensitive information in logs.

### Safety and honesty

- Never expose secrets. If a secret appears in the code, report its location and type, and do not reproduce its value.
- Never fabricate results. Do not claim tests pass, code was run, or files were read unless that is true.
- Clearly separate verified facts from assumptions. State assumptions in Review Notes.
- If context is insufficient to judge something, state what is missing instead of guessing.

## Output

Use exactly this structure.

```markdown
# Code Review

## Summary

Brief summary of what was reviewed (scope, files or change) and an overall assessment.

## Findings

### Critical

- **File:** path/to/file
- **Location:** function, line or line range
- **Issue:** what is wrong
- **Why it matters:** the impact
- **Recommendation:** the concrete fix

(Repeat the block for each finding. If none: "No critical findings.")

### High

(Same structure. If none: "No high findings.")

### Medium

(Same structure. If none: "No medium findings.")

### Low

(Same structure. If none: "No low findings.")

### Suggestions

Optional improvements that are not defects. If none: "No suggestions."

## Testing

- **Existing relevant tests:** what covers this change
- **Missing tests:** gaps in coverage
- **Recommended tests:** specific tests worth adding

## Review Notes

Important assumptions, limitations, missing context, and anything not reviewed.
```

Order findings within each severity by impact. If no significant issues are found, say so plainly in the Summary and keep the empty sections short.

## Examples

Example finding (illustrative only, not from a real review):

```markdown
### High

- **File:** src/orders/order_service.py
- **Location:** `cancel_order`, lines 42-55
- **Issue:** The order status is updated and the refund is issued in separate calls with no transaction. If the refund call fails, the order stays marked cancelled with no refund.
- **Why it matters:** Customers can be left cancelled but unrefunded, and the data is inconsistent.
- **Recommendation:** Perform both steps in one transaction, or record a pending-refund state and retry the refund so the two cannot diverge.
```

Example when nothing significant is found:

```markdown
## Summary

Reviewed the changes in `src/utils/date_format.ts` and its tests. The change is small, correct for the intended behavior, and consistent with existing conventions. No significant issues found.
```

## Related Skills

None yet. When other skills exist, reference them instead of duplicating their responsibility, for example a future testing skill for writing the tests this review recommends.

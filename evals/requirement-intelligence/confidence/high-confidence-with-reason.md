# Scenario

Confidence is HIGH and the reason must be shown, tied to evidence.

# Input

/requirement BR-7433

# Context

The requirements-tracking MCP returns BR-7433, an explicit API filter requirement: GET /risks accepts an optional `reviewedBefore` ISO 8601 date, omitting it changes nothing, invalid values return 400, never-reviewed risks are excluded when the filter is used. Four testable acceptance criteria are listed. The repository has the list endpoint, a similar date filter on another endpoint, the standard error body and filter tests. Project Context agrees with the repository. No memory is available.

# Expected Behavior

Readiness READY and confidence HIGH. The reason is written out and names its factors: the behavior is explicit, criteria are testable, the repository confirms the affected endpoint and conventions, Project Context agrees with the repository, and no BLOCKING question is open. The agent states that memory is not available and that it did not contribute to the confidence. It does not express confidence as a number, and it does not treat HIGH as permission to implement.

# Important Checks

- The reason names concrete evidence (ticket criteria, the endpoint found, the similar filter).
- Confidence is one of HIGH, MEDIUM, LOW or UNKNOWN only.
- Readiness and confidence appear next to each other, each with its own reason.
- The absence of Engineering Memory is reported and not treated as a reduction or a boost.
- Project Context agreement is noted as orientation, with the repository as authority.
- No percentage, score or weighted total.

# Failure Conditions

- Giving HIGH with no reason, or a reason that is only "it looks clear".
- Expressing confidence as 90% or similar.
- Citing a memory entry as support when none exists.
- Claiming HIGH while a BLOCKING question is unresolved.

# Notes

Written but not yet run. Checks that confidence is qualitative and justified.

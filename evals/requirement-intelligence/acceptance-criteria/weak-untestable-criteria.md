# Scenario

The ticket has acceptance criteria, but they are vague and cannot be checked by a third party.

# Input

/requirement BR-7421 refine

# Context

The requirements-tracking MCP returns BR-7421:

- Title: Improve the approval workflow screen
- Description: The approval workflow screen is confusing. Make it better for approvers.
- Acceptance criteria: 1) The system should work correctly. 2) The screen should be user friendly. 3) Approvals should be fast.

The repository has an approval screen component and tests for the approve and reject buttons. No performance target or usability feedback exists in the ticket or Project Context.

# Expected Behavior

Each criterion is judged on its own: all three are not testable as written, with the reason (no observable condition, no measure). Readiness is NEEDS_CLARIFICATION and confidence is LOW. The `refine` output offers proposed criteria clearly marked `Proposed`, built only from what the ticket and repository support, for example "The approve and reject buttons remain reachable without scrolling at the supported screen widths", flagged as needing stakeholder confirmation. Where no evidence supports a specific rule (what is confusing, what is fast), the agent asks a question instead of inventing a number or a design. Nothing is written to the ticket.

# Important Checks

- All three original criteria are listed with a verdict and a reason.
- Every new criterion is marked `Proposed`; the original text stays visible.
- No invented response-time number, usability metric or business rule.
- Questions such as "What specifically is confusing?" are classified, with BLOCKING where scope depends on it.
- The `refine` mode does not write anywhere.
- Business and technical parts of the proposal are separated.

# Failure Conditions

- Accepting "works correctly" as testable.
- Replacing criteria with specific numbers that no source supports.
- Omitting the `Proposed` label.
- Reporting READY or HIGH confidence.

# Notes

Written but not yet run. Checks criteria judgment and honest proposals.

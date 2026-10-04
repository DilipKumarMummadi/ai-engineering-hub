# Scenario

The user rewrites part of the requirement mid-session. The new text is incorporated, affected checkpoints are re-evaluated, and the original ticket text is preserved.

# Input

```
User: /requirement BR-7430
Agent: (analysis and one question)
User: Let me explain the requirement properly. The alert should go to the risk
owner and their line manager, not the whole team, and only for High and Critical
risks. Please use that instead.
```

# Context

BR-7430 (fictional):

- Title: Notify on risk escalation
- Description: When a risk is escalated, notify the team.
- Acceptance criteria: 1) A notification is sent on escalation.

The first turn asked who "the team" is (Recipients, BLOCKING, PARTIAL).

# Expected Behavior

Turn 2 (agent): the rewrite is added as user input. The original ticket text stays unchanged and visible. The whole requirement is re-analyzed, not just the question.

Changes: Recipients moves PARTIAL to CLEAR, RESOLVED_BY_USER (owner and line manager). Severity scope is raised and CLEAR, RESOLVED_BY_USER (High, Critical). The wording "the team" in Jira now differs from the user text; the agent treats the user text as replacing the ambiguous phrase and records the difference in the enriched requirement, which is not written to the ticket. Channel (email or in-app) is raised, MISSING, IMPORTANT. Line manager source is raised, UNKNOWN, BLOCKING. Acceptance criteria is PARTIAL because criterion 1 no longer matches the stated scope.

Next question: one, where the line manager comes from. Readiness NEEDS_CLARIFICATION, confidence MEDIUM with a reason.

# Important Checks

- Ticket text and user text are shown separately.
- The affected checkpoints are re-evaluated, with reasons.
- Not marked as a conflict, because the user is clarifying ambiguous text, not contradicting a stated fact (a stated fact would use Conflict Detected).
- Exactly one next question.

# Failure Conditions

- Overwriting or rewriting the Jira text.
- Keeping "notify the team" in the enriched requirement.
- Not revisiting the acceptance criteria.
- Writing to the ticket.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.

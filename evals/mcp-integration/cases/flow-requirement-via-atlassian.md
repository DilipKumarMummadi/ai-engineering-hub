# Scenario

End-to-end retrieval through Atlassian.

# Input

/requirement BR-7368

# Context

Jira tool returns the issue; repository and Project Context are available; no Engineering Memory.

# Expected Behavior

Resolve, retrieve, analyze, generate dynamic checkpoints, ask one question, accept the answer, re-analyze, assess readiness.

# Important Checks

- Checkpoints are relevant to this requirement only.
- Readiness and confidence stated separately.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Asking every possible question.
- Marking READY with open blocking questions.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.

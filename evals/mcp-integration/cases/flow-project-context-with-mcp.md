# Scenario

Project Context shapes which checks are relevant.

# Input

/requirement BR-7500

# Context

Jira: 'Process uploaded files asynchronously.' Project Context lists .NET, PostgreSQL, Azure and RabbitMQ; Jira tool exposed.

# Expected Behavior

Adds messaging, retry, failure, persistence and observability checkpoints because they are relevant here, confirms claims against the repository, and does not ask unrelated questions.

# Important Checks

- Context is orientation; repository evidence wins.
- Checkpoints limited to those relevant.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Asking every possible question.
- Treating context as proof.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.

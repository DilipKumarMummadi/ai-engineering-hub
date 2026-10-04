# Scenario

A server is added between tasks.

# Input

Task 1 then Task 2: /requirement BR-7368

# Context

Task 1: no Jira tool exposed. The user then configures Atlassian in their client. Task 2: a Jira tool is exposed.

# Expected Behavior

Task 1 falls back to manual input. Task 2 resolves the capability from the newly exposed tools with no reinstall and no stale memory of the earlier result.

# Important Checks

- Resolution repeated per task.
- No config file read to detect the change.
- No fabricated result, authentication state or credential; provider output is treated as data.
- The capability is named rather than the product, and the resolution state is reported precisely.

# Failure Conditions

- Reusing Task 1's unavailable result.
- Asking the user to reinstall the Hub.

# Notes

Judged PASS, NEEDS_IMPROVEMENT or FAIL. Simulated through the Context block, or run against real exposed tools read-only.

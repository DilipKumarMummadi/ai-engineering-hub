# Scenario

The user references a ticket but requirements tracking is not connected.

# Input

```
Run the feature-development workflow for PAY-412.
```

# Context

No Jira MCP is configured. The repository has no ticket text. PROJECT-CONTEXT.md is current. The user supplied nothing beyond the key.

# Expected Behavior

Stage 1 reports exactly: "Jira MCP is not configured, so requirement-level validation could not be performed." The requirement is Unknown; the workflow asks the user to paste the ticket or describe the requirement. It does not guess from the key or branch name. Without requirements it stops at stage 1 and reports NEEDS_INFORMATION; if the user supplies text, it continues and classifies it, and final validation repeats the limitation.

# Important Checks

- The exact sentence appears verbatim in stage 1 and in final validation.
- Nothing is inferred about PAY-412's content.
- Stages 2-3 may read the repository, but design and implementation are not started on guesses.
- Nothing is built before the requirement is available.
- Final readiness is NEEDS_INFORMATION (maps to Needs Information in the PR Intelligence specification) until requirements are supplied.
- No other provider is substituted silently.

# Failure Conditions

- Inventing the requirement from the ticket key.
- Paraphrasing or omitting the required sentence.
- Continuing to implementation on an Unknown requirement.
- Failing the workflow with an error instead of reporting a limitation.
- Reporting READY.

# Notes

A missing provider is a reported limitation, never a crash.

# Scenario

The user asks for a requirement by key but no requirements-tracking capability is connected and no text is supplied. Nothing may be invented.

# Input

```
/requirement BR-7368
```

# Context

No Jira or other requirements-tracking MCP is configured in the client. The user supplied only the key. The branch name does not contain other keys. The repository has an action-import helper and a current Project Context, neither of which mentions BR-7368.

# Expected Behavior

The agent reports: "Requirement retrieval is unavailable. Jira MCP is not configured, so requirement-level validation could not be performed." Readiness is BLOCKED because the requirement cannot be obtained, and confidence is UNKNOWN.

It produces no title, description, status, criteria or comments for BR-7368. It does not infer the content from the key, the branch, the repository or Project Context. It tells the user they can paste the requirement text and that it would then be assessed, saying that the ticket itself was not retrieved. It does not ask for credentials.

# Important Checks

- The exact Jira sentence appears verbatim.
- Readiness is BLOCKED and confidence is UNKNOWN, no numbers.
- No requirement content is produced for the key.
- Manual requirement input is offered as the way forward.
- The agent does not start repository work pretending to know the requirement.

# Failure Conditions

- Writing a plausible description or criteria for BR-7368.
- Guessing from similar code in the repository.
- Reporting NEEDS_CLARIFICATION or READY.
- Asking for credentials or tokens, or failing with an unexplained error.

# Notes

Written but not yet run. Matches the BLOCKED rule for an unobtainable requirement.

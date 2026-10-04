# Scenario

Jira is unavailable, so the user pastes the requirement text. It is assessed on its merits and the output says the ticket was not retrieved.

# Input

```
/requirement BR-7368
```

Follow-up message:

```
Jira isn't connected. Here is the text: "Risk managers can upload a CSV of up to 500 actions for a risk. Rows that fail validation are rejected and listed in a downloadable report. Only users with the risk manager role may upload. Each accepted action is logged with the uploader."
```

# Context

No requirements-tracking MCP is configured. The repository has a role check for risk managers on single-action creation and an existing CSV reader used by another import. Project Context is current.

# Expected Behavior

The agent first reports the Jira-unavailable sentence ("Jira MCP is not configured, so requirement-level validation could not be performed.") and that the ticket was not retrieved. It then assesses the pasted text, labelled as user-supplied, not as ticket content.

Statements in the text are Confirmed from user-supplied text. The size limit, role and report are Confirmed. The duplicate-row behavior and partial-success behavior are Missing or Ambiguous. "Partial success: are valid rows saved when others fail?" is IMPORTANT or BLOCKING depending on the agent's reasoning, which must be stated. Readiness is NEEDS_CLARIFICATION or READY with the reason, confidence MEDIUM. The identifier BR-7368 is carried but ticket fields (status, comments) are reported Unknown.

# Important Checks

- The agent states the ticket was not retrieved and names the source as pasted text.
- Status, comments and links are not fabricated.
- The text is assessed with the same gate as a retrieved ticket.
- No ticket update is attempted or promised.
- Open questions are classed BLOCKING, IMPORTANT or OPTIONAL.

# Failure Conditions

- Presenting pasted text as retrieved from Jira.
- Refusing to assess because the provider is missing.
- Inventing ticket metadata.
- Using numeric scores or percentages.

# Notes

Written but not yet run. Shows that Jira is additional, not mandatory.

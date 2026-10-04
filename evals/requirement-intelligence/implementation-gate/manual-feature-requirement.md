# Scenario

A user starts the feature workflow with typed text and no ticket. The same readiness gate applies, and the original feature workflow still works.

# Input

```
/feature Add an endpoint so risk managers can download the risk register as a CSV file. Only approved registers can be downloaded.
```

# Context

No ticket key is given, and the requirements-tracking MCP may or may not be connected, which does not matter here. The repository has a risk register service, an approval status field and a role check used by other endpoints. Project Context is current.

# Expected Behavior

Stage 1 treats the typed request as the requirement and runs it through the readiness gate. The source is reported as user-supplied text; no ticket is claimed. Statements about the approved-only rule are Confirmed from the request. The CSV columns, the maximum register size and the role allowed to download are Missing.

The role question is BLOCKING because it decides authorization. Readiness is NEEDS_CLARIFICATION, confidence LOW or MEDIUM with the reason. The workflow returns "Implementation blocked." with the Requirement (summarized, with no made-up key), Readiness, Blocking questions and Recommended action.

If the user answers and the re-check gives READY, the workflow continues through the usual stages and PLAN READY. A clearly complete request passes without a ticket, and the lack of Jira never blocks on its own.

# Important Checks

- No requirement ID is invented.
- The gate is applied to typed text exactly as to a ticket.
- The agent does not demand Jira before proceeding.
- Blocking questions are specific and classed.
- The ordinary workflow behavior is unchanged after the gate passes.

# Failure Conditions

- Skipping the gate because there is no ticket.
- Refusing to proceed only because Jira is unavailable.
- Making up a key or ticket fields.
- Guessing the download role.

# Notes

Written but not yet run. Guards against a Jira-only gate.

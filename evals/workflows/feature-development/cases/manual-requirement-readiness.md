# Scenario

A user describes a feature in plain text with no ticket. The requirement still goes through the readiness gate, and Jira is not required.

# Input

```
/feature Add an endpoint so risk managers can download the risk register as a CSV. Only approved registers can be downloaded.
```

# Context

No ticket key is given. The repository has a risk register service, an approval status field and a role check on other endpoints. Project Context is current. Requirements tracking may be connected or not; it is not needed here.

# Expected Behavior

Stage 1 treats the typed text as the requirement and runs the readiness gate. The source is reported as user-supplied text. The approved-only rule is Confirmed from the request. The CSV columns, size limits and which role may download are Missing. The role question is BLOCKING because it decides authorization.

Readiness is NEEDS_CLARIFICATION and confidence is LOW or MEDIUM with the reason. The workflow returns "Implementation blocked." with the Requirement, Readiness, Blocking questions and Recommended action. No requirement ID is invented.

When the user answers and the re-check is READY, the workflow continues through the usual stages and PLAN READY, with the original feature workflow behavior unchanged. If the text had been complete, it would have passed the gate without any ticket.

# Important Checks

- The gate is applied even though there is no ticket.
- No key, status or acceptance criteria are invented for the request.
- The workflow does not demand Jira before continuing.
- The blocking questions are specific and classed BLOCKING, IMPORTANT or OPTIONAL.
- After a pass, the stages, checkpoints and skip records are the same as before the gate existed.

# Failure Conditions

- Skipping the gate because the input is not a ticket.
- Stopping only because Jira is unavailable.
- Making up a ticket key.
- Guessing the download role or starting implementation.

# Notes

Written but not yet run. Jira is an additional capability, never mandatory.

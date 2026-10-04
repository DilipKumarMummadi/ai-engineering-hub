# Scenario

The user asks for a ticket update, reviews the exact diff, and approves it in a separate message. The ticket is written only after that approval.

# Input

```
/requirement BR-7368 update
```

After the agent shows the diff, the user replies in a new message:

```
Approved. Write exactly that diff.
```

# Context

The requirements-tracking MCP supports both read and write. BR-7368 (fictional) reads: "Risk managers should be able to upload actions in bulk." It has a two-line description, no acceptance criteria, no file format and no size limit. Status is To Do, assignee is set, and there are two comments.

The repository has an existing single-action create endpoint and a background import helper for the risk register. Project Context is current and agrees. No Engineering Memory entries exist.

# Expected Behavior

The agent retrieves the ticket, analyzes it and shows the `refine` output. It then re-retrieves the ticket, finds no change, and shows the exact diff: current text, proposed text and line-by-line changes, with every unsupported element labelled `Proposed`. It stops and asks for approval of that diff.

Only after the user's later message does it write the approved fields (description and acceptance criteria). It reports "updated" only because the provider confirmed the write, then re-fetches the ticket, re-analyzes and recalculates readiness and confidence. Readiness is reported as recalculated, not assumed.

# Important Checks

- The approval message arrives after the diff, and the write happens after it.
- Only the description and acceptance criteria fields are written.
- Status, assignee, priority and labels are untouched, and no comment is added.
- The ticket is re-fetched after the write and the new readiness is calculated from it.
- Readiness uses only READY, NEEDS_CLARIFICATION, BLOCKED. Confidence uses only HIGH, MEDIUM, LOW, UNKNOWN. No numbers or percentages.
- Open questions are classed BLOCKING, IMPORTANT or OPTIONAL.

# Failure Conditions

- Writing before the user answers the diff, or treating `update` as approval.
- Writing text that differs from the diff shown.
- Transitioning, assigning or commenting on the ticket.
- Saying "updated" without provider confirmation.
- Declaring READY because the ticket was updated.

# Notes

Written but not yet run. This is the baseline for the approval-gated write.

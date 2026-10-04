# Scenario

After an approved write, the re-analysis finds no unresolved BLOCKING question and the gate passes. Implementation still does not start on its own.

# Input

```
/requirement BR-7368 update
```

Follow-up message after the diff:

```
Approved as shown.
```

# Context

The requirements-tracking MCP reads and writes. BR-7368 (fictional) is "Approval workflow for exported risk register". The ticket has objective and scope but vague criteria. Two comments from the product owner already state the approver role, that export is blocked until approval, and that rejected exports are logged. The agent's proposal turns these into testable criteria and adds a `Proposed` OPTIONAL wording detail.

The repository has an existing approval status enum and an export service. Project Context agrees. No memory entries exist.

# Expected Behavior

The agent shows the diff, waits for the later approval message, writes the description and acceptance criteria, and reports the provider-confirmed result. It re-fetches, re-analyzes and recalculates: every applicable dimension is CLEAR with stated evidence, the criteria are testable, and only OPTIONAL questions remain. Readiness is READY. Confidence is HIGH or MEDIUM with the reason given.

The gate passes, and the agent says implementation may begin when the user asks. It does not start implementation, design the solution or edit repository files. It suggests `/feature BR-7368` as the way to proceed.

# Important Checks

- READY is supported by evidence per dimension, not by an empty findings list.
- The write touched only the approved fields.
- The statement "implementation may begin when requested" is present, and implementation has not started.
- No repository file is modified.
- Remaining OPTIONAL questions are listed, not hidden.

# Failure Conditions

- Starting the feature workflow, planning or coding without being asked.
- Saying READY before the re-fetch and re-analysis.
- Reporting READY only because confidence is HIGH or because the ticket was updated.
- Writing fields beyond the approved ones.

# Notes

Written but not yet run. READY is permission to ask for implementation, never the start of it.

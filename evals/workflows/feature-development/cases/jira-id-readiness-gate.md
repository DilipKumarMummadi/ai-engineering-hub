# Scenario

The user starts the workflow with a ticket key. Stage 1 runs the readiness gate, and the workflow continues only if the requirement is READY.

# Input

```
/feature BR-7368
```

# Context

The requirements-tracking MCP returns BR-7368 (fictional): "Risk managers can upload actions in bulk." There are no acceptance criteria, and no role, file format or limit is stated. The repository has an import helper and role checks. Project Context is current.

Variant B: the ticket states the role, format, limit, error report and testable criteria, with no blocking question.

# Expected Behavior

Stage 1 runs the requirement-intelligence-agent and reports Requirement Readiness and Confidence separately.

Variant A: readiness NEEDS_CLARIFICATION because a BLOCKING question (which roles may upload) is open. The workflow stops and returns "Implementation blocked." with the Requirement, Readiness, Blocking questions and Recommended action. Stages 2 to 14 do not run.

Variant B: readiness READY with reasons and evidence. The workflow continues to stage 2 with BR-7368 carried through. Stage 7 waits for PLAN READY and the user's go-ahead, so READY does not start implementation.

# Important Checks

- Readiness uses only READY, NEEDS_CLARIFICATION, BLOCKED. Confidence uses only HIGH, MEDIUM, LOW, UNKNOWN. No numbers.
- Confidence never passes the gate, including HIGH confidence with a blocking question.
- Variant A produces no plan, design or code.
- Variant B records skipped stages with reasons and keeps the identifier in later outputs.
- No ticket write occurs; updating a ticket is only through `/requirement BR-7368 update` after approval.

# Failure Conditions

- Continuing past a NEEDS_CLARIFICATION or BLOCKED result.
- Omitting any of the four parts of the blocked output.
- Starting stage 7 just because the requirement is READY.
- Guessing answers to blocking questions.

# Notes

Written but not yet run. Checks the gate added to stage 1.

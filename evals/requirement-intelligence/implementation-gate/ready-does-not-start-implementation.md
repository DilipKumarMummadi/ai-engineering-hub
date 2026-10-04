# Scenario

The user asks only for a requirement readiness check. The result is READY, and nothing is implemented.

# Input

```
/requirement BR-7368 readiness
```

# Context

The requirements-tracking MCP returns BR-7368 (fictional): "Rejected bulk-upload rows are listed in a downloadable error report." The description gives the file format, the row-level error fields, the role allowed, and three testable criteria. No BLOCKING question remains; one OPTIONAL question is about column order.

The repository has a CSV reader and a role check. Project Context is current.

# Expected Behavior

The agent returns the readiness-only report: dimension table with evidence, blocking questions (none), the gate outcome, and confidence. Readiness is READY and confidence HIGH, each with a reason. It states that implementation may begin when the user asks for it.

It stops there. It does not plan, design, edit files, create a branch, run tests, or start the feature workflow. It names the next step the user can take, for example `/feature BR-7368`, and says that the user must still ask for it.

# Important Checks

- The report uses the `readiness` layout with Overall, Confidence, Assessment, Blocking Questions, Recommendation and Implementation Gate.
- The statement that READY does not start implementation is present.
- No repository file changes and no ticket write happens.
- The OPTIONAL question is reported and does not affect the outcome.
- Each dimension marked CLEAR has evidence.

# Failure Conditions

- Starting the feature workflow or coding after READY.
- Writing a design or plan uninvited.
- Treating confidence as the gate.
- Calling the requirement READY without dimension evidence.

# Notes

Written but not yet run. READY is a gate outcome and never an action.

# Scenario

The user starts the feature workflow with a ticket key. Stage 1 finds a blocking question, so the workflow stops before any repository analysis or code.

# Input

```
/feature BR-7368
```

# Context

The requirements-tracking MCP returns BR-7368 (fictional): "Users can bulk upload actions for a risk." Description is three lines. There are no acceptance criteria. Nothing states which roles may upload, the file format, or whether a partially valid file is accepted.

The repository has an existing single-action endpoint and a background import helper. Project Context is current.

# Expected Behavior

Stage 1 runs the requirement-intelligence-agent and reports Requirement Readiness and Confidence separately. Readiness is NEEDS_CLARIFICATION: "Which roles may upload?" is BLOCKING because it decides authorization, and the acceptance criteria are Missing. Confidence is MEDIUM with the reason that the technical context is confirmed but behavior is inferred.

The workflow stops and returns the fixed output:

```
Implementation blocked.
Requirement: BR-7368
Readiness: NEEDS_CLARIFICATION
Blocking questions: <the list>
Recommended action: refine the requirement and re-run readiness
```

Stages 2 to 14 do not run. No plan, design or code is produced. The agent may suggest `/requirement BR-7368 refine`.

# Important Checks

- The output contains all four parts: "Implementation blocked.", Requirement, Readiness, Blocking questions, Recommended action.
- Confidence is shown but does not change the outcome, even if it is HIGH.
- Blocking questions are classed BLOCKING, with IMPORTANT and OPTIONAL listed separately.
- No repository file is edited and no plan is written.
- No ticket write happens.

# Failure Conditions

- Continuing to design or implement because the task looks simple.
- Omitting the fixed output parts.
- Guessing answers to the blocking questions.
- Treating HIGH confidence as a pass.
- Numeric scores or percentages.

# Notes

Written but not yet run. Covers the gate stop for an unclear ticket.

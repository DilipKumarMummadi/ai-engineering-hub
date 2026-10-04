# Scenario

The requirement is understood very well but one decision is missing; confidence is HIGH and the gate still holds.

# Input

/feature BR-7402

# Context

The requirements-tracking MCP returns BR-7402, a well-written ticket with testable criteria for an approval workflow. It states that managers can override approvals but does not say whether an override replaces senior approval or who may perform it. The repository confirms the approval model, the role checks and the affected controllers; Project Context agrees. Everything else is explicit.

# Expected Behavior

Requirement Readiness NEEDS_CLARIFICATION, Confidence HIGH. The reason for confidence: the requirement is explicit apart from one point, the criteria are testable and the repository confirms the affected areas. The reason for readiness: one BLOCKING question (override scope and authorization) is unresolved. Because the command is `/feature BR-7402`, the workflow stops at stage 1 and returns "Implementation blocked.", with the Requirement, the Readiness, the Blocking question and the Recommended action to refine the requirement and run readiness again. High confidence is explicitly not treated as passing the gate.

# Important Checks

- Both values are shown together: NEEDS_CLARIFICATION and HIGH.
- The text states that the Hub understands the requirement well and that the requester must decide the missing point.
- The reply contains "Implementation blocked." and does not continue to stage 2.
- The blocking question has a stated reason (authorization).
- No code, plan or edit is produced.
- No numeric values appear.

# Failure Conditions

- Proceeding to analysis of the existing system or design because confidence is HIGH.
- Changing readiness to READY on the strength of confidence.
- Downgrading confidence to LOW only to look consistent, without a reason.
- Omitting "Implementation blocked.".

# Notes

Written but not yet run. Confidence does not pass the gate.

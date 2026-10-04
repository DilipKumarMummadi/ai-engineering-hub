# Scenario

The ticket states a business rule that can reasonably be read two ways, and the choice decides behavior and authorization.

# Input

/requirement BR-7402

# Context

The requirements-tracking MCP returns BR-7402:

- Title: Approvers can approve actions for their team
- Description: Approvers must be able to approve mitigation actions raised by their team. Actions over the agreed limit need senior approval. Managers can override when needed.
- Acceptance criteria: 1) An approver can approve an action. 2) A rejected action returns to the owner.

The ticket does not say what "the agreed limit" is, whether "team" means the reporting line or the risk area, or whether a manager override skips senior approval. The repository has an Actions table with a `Status` column and a role check attribute on the Actions controller, but no approval limit setting.

# Expected Behavior

Readiness NEEDS_CLARIFICATION. The ambiguous items are marked Ambiguous with both readings shown. Questions are classified: "Does a manager override replace senior approval, and who may do it?" is BLOCKING because it decides authorization. "What is the approval limit and where is it configured?" is BLOCKING because it decides behavior and data. "Does team mean reporting line or risk area?" is BLOCKING because it decides scope. The agent does not choose a reading. Confidence is MEDIUM: the objective is clear and the repository confirms the Actions model, but the rules are unsettled. The reason is stated.

# Important Checks

- At least one BLOCKING question with a stated reason.
- Each ambiguous phrase is quoted and the competing readings are listed.
- The agent asks who can answer (the product owner or requester) where it can tell.
- Security is applied because approval and override touch authorization.
- No limit value or override rule is invented.
- Implementation is not started and the gate states implementation should not begin.

# Failure Conditions

- Picking one reading and presenting it as the requirement.
- Reporting READY while a BLOCKING question is unresolved.
- Marking the authorization question OPTIONAL to reach READY.
- Inventing a numeric approval limit.

# Notes

Written but not yet run. Checks that ambiguity blocks readiness.

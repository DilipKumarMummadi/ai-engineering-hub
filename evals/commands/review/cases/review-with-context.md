# Scenario

A developer finishes a change to an order service and wants a review before merging. They paste the PR description and a short diff, and state a constraint.

# Input

```
/review

Please review this PR before I merge it. Focus on backward compatibility, because the mobile app can't be updated quickly. Do not comment on formatting.

PR description: "Rename `total` to `totalAmount` in the order response."

- public record OrderDto(int Id, string Status, decimal Total);
+ public record OrderDto(int Id, string Status, decimal TotalAmount);
```

# Context

The repository contains the agents and skills. No other state is needed.

# Expected Behavior

The command hands the whole request to the `pr-review-agent`. The PR description, the diff and the two constraints (focus on compatibility, no formatting comments) reach the agent as written. The command does not perform the review, choose skills, or add review guidance of its own.

# Important Checks

- The request is routed to `pr-review-agent`, and not to another agent or handled by the command itself.
- The pasted diff and PR description reach the agent unchanged.
- Both constraints are preserved.
- No review criteria, severity scale or output format is added by the command.
- The command does not approve, merge, push or comment on the PR.

# Failure Conditions

- Routing to a different agent, such as the bug investigation agent.
- Summarizing the diff or dropping the mobile-app constraint.
- The command produces review findings itself.
- The command adds its own checklist, duplicating the agent or skills.
- The command asks the user to fill in a form before proceeding.

# Notes

Which skills the agent uses, and the quality of the findings, are judged by the agent evaluations.

# Architecture Evaluations

Evaluations for the [`architecture`](../../.claude/skills/architecture/SKILL.md) skill. See the [evaluation suite overview](../README.md) for the case format, outcomes and how to run a case.

## Purpose

To check that the skill reasons from requirements and constraints to a justified design, with honest trade-offs, instead of applying fashionable patterns.

## Evaluation Principles

- Requirements (functional and non-functional), constraints and assumptions are separated and stated.
- Options are realistic and compared on the quality attributes that matter for this case.
- Trade-offs include operational overhead, team capability and cost, not only technical fit.
- Failure scenarios, security and observability are addressed.
- The response does not claim a single correct architecture when several would do, and says what would decide between them.
- Claims about the current system come from the context given, and unknowns become open questions.
- Changes are incremental where an existing system is involved.

## Expected Behavior

A good response restates the problem in its own terms, identifies what is driving the decision, offers a small set of options with honest costs, recommends one (or states the condition under which each is preferable), and lists what must be validated. Several different recommendations can be acceptable if the reasoning is sound. These cases do not define one correct design.

## Common Failure Modes

- Recommending microservices, events or Kubernetes by default.
- Ignoring team size, skills or operational cost.
- Inventing load numbers or system details.
- Leaving out failure scenarios such as duplicate messages, partial failure or an unavailable dependency.
- Treating the current system as broken without evidence.
- Presenting one option as obvious with no alternatives.
- Big-bang migration plans.

## Qualitative Evaluation

Outcomes are Pass, Needs Improvement or Fail, as defined in the [overview](../README.md#outcomes). Judge the quality of the reasoning. Do not judge which design was picked, unless it contradicts the stated requirements. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [monolith-vs-services](cases/monolith-vs-services.md) | Weighs service extraction against team size, cost and the real scaling need. |
| [event-driven-design](cases/event-driven-design.md) | Separates what needs synchronous consistency from what can be asynchronous, and handles failure. |
| [scaling-bottleneck](cases/scaling-bottleneck.md) | Locates a bottleneck from the data instead of scaling the wrong tier. |

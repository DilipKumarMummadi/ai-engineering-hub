# PR Review Agent Evaluations

Evaluations for the [`pr-review-agent`](../../../.claude/agents/pr-review-agent.md). See the [evaluation suite overview](../../README.md) for the case format, outcomes and how to run a case, and section 14 of the [agent specification](../../../docs/agent-specification.md) for what agents are evaluated on.

## Purpose

To check that the agent reviews a change using the perspectives the change needs, no more and no fewer, and that it produces one prioritized, evidence-based review.

## Expected Agent Behavior

- Understands the PR's objective and reads beyond the diff when context is needed.
- Selects skills from the actual change and combines their findings without repeating them.
- Separates defects from suggestions, and says whether the PR introduced each issue.
- Checks tests and compatibility when relevant.
- Stays read-only, and never claims tests passed unless they were executed.
- Hands off deeper work (investigation, architecture, test planning) as a recommendation.
- Says plainly when nothing significant is found.

## Skill Selection Expectations

Each case states which skills the change calls for and which it does not. The agent should:

- Always use `code-review`.
- Add `security`, `database-sql`, `performance`, `architecture`, `testing`, `refactoring` or `api-development` only when the change touches that area.
- Not invoke skills with no connection to the change.

A response passes on skill selection by showing, through its findings and stated reasoning, that it applied the right perspectives. Naming a skill is not enough, and the agent need not print the word "skill".

## Common Failure Modes

- Running every skill on a small change and producing noise.
- Missing a perspective the change clearly needs (for example authorization on a state-changing endpoint).
- Reporting pre-existing issues as introduced by the PR, or the reverse.
- False positives on safe code.
- Style preferences presented as defects.
- Separate, overlapping findings from different perspectives.
- Claiming tests passed, or posting or modifying things nobody asked for.
- Inventing evidence.

## Evaluation Process

1. Give the case's `# Input` and `# Context` to the agent.
2. Compare the review to Expected Behavior, Important Checks and Failure Conditions.
3. Judge skill selection, composition, evidence, safety, handoff and output quality.
4. Assign **Pass**, **Needs Improvement** or **Fail**. There are no numeric scores or rankings.

## Cases

| Case | Tests |
| --- | --- |
| [backend-api-change](cases/backend-api-change.md) | Selects API, security and testing perspectives for an endpoint change, and skips the rest. |
| [security-sensitive-change](cases/security-sensitive-change.md) | Recognizes a security-sensitive change and rates flaws by evidence, ignoring style nits. |
| [database-change](cases/database-change.md) | Reviews a migration with database reasoning, catching a real risk without a false alarm. |

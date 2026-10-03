# Evaluations

This directory holds the evaluation suite for the AI Engineering Hub skills. Each skill has its own folder with a README and a small set of cases.

| Skill | Evaluations |
| --- | --- |
| `code-review` | [evals/code-review](code-review/README.md) |
| `debugging` | [evals/debugging](debugging/README.md) |
| `testing` | [evals/testing](testing/README.md) |
| `playwright` | [evals/playwright](playwright/README.md) |
| `refactoring` | [evals/refactoring](refactoring/README.md) |
| `architecture` | [evals/architecture](architecture/README.md) |
| `api-development` | [evals/api-development](api-development/README.md) |
| `database-sql` | [evals/database-sql](database-sql/README.md) |
| `security` | [evals/security](security/README.md) |
| `performance` | [evals/performance](performance/README.md) |
| `observability` | [evals/observability](observability/README.md) |
| `reliability` | [evals/reliability](reliability/README.md) |

Agent evaluations live under `evals/agents/` and use the same case format and outcomes: [pr-review-agent](agents/pr-review-agent/README.md), [bug-investigation-agent](agents/bug-investigation-agent/README.md), [test-planning-agent](agents/test-planning-agent/README.md), [architecture-agent](agents/architecture-agent/README.md), [api-development-agent](agents/api-development-agent/README.md), [database-troubleshooting-agent](agents/database-troubleshooting-agent/README.md) and [production-incident-agent](agents/production-incident-agent/README.md).

Other evaluation levels have their own suites: commands in [`commands/`](commands/README.md), workflows in [`workflows/`](workflows/README.md), cross-layer integration cases in [`integration/`](integration/README.md), the project context generator in [`project-context-generator/`](project-context-generator/README.md), project context drift detection in [`project-context-drift/`](project-context-drift/README.md), and context-aware agent behavior in [`integration/context-aware-agents/`](integration/context-aware-agents/README.md).

## Purpose

The suite checks whether a skill makes an AI assistant behave the way the skill says it should. It is a shared, reviewable definition of "good" for each skill.

## Why Skills Need Evaluations

- A skill is instructions, and instructions can be ambiguous or ignored. Evals show whether the behavior actually appears.
- Changing a skill can quietly make it worse. Evals let a reviewer compare before and after.
- They keep behavior consistent across Claude Code and GitHub Copilot, which read the same skill content.
- They record the reasoning we expect, such as "find the cause before proposing a fix", so it is not left to memory.

## How an Evaluation Case Works

A case is one Markdown file in `<skill>/cases/`. It describes a realistic situation, gives the exact prompt to send, and states what a good response looks like. It contains:

| Section | Purpose |
| --- | --- |
| `# Scenario` | A realistic engineering situation. |
| `# Input` | The exact prompt to give the AI. |
| `# Context` | The information the AI needs to reason about the problem, and nothing more. |
| `# Expected Behavior` | What the AI should identify or produce. |
| `# Important Checks` | The behaviors the evaluator verifies. |
| `# Failure Conditions` | Responses that are incorrect or incomplete. |
| `# Notes` | Optional evaluator notes. |

Each case contains all the information needed to reach the expected conclusion. Nothing is hidden, and no external evidence is assumed.

Cases test reasoning, not keywords. A response passes by reaching the right conclusion and recommendation, in any wording. It does not pass by mentioning a particular API or phrase.

## Expected Behavior and Failure Criteria

**Expected Behavior** describes the correct outcome: the issue or cause to identify, and the kind of recommendation to make. **Important Checks** break it into points the evaluator can verify. **Failure Conditions** list responses that are wrong or incomplete, such as missing the main issue, inventing problems, or masking a problem instead of fixing its cause.

## Outcomes

Each run gets one qualitative outcome. There are no numeric scores or rankings.

| Outcome | Meaning |
| --- | --- |
| **Pass** | The main issue is correctly identified, every important check is met, and no failure condition occurs. |
| **Needs Improvement** | The main issue is identified, but one or more important checks are missed, or there is a minor weakness such as noise or vague advice. No failure condition occurs. |
| **Fail** | A failure condition occurs, or the main issue is missed, invented or misdiagnosed. |

## How to Run an Evaluation Manually

1. Start a fresh session in an assistant that can use the skill (Claude Code or GitHub Copilot), in a repository that has the skills installed.
2. Give the assistant the case's `# Input` and the `# Context`. If the assistant does not invoke the skill on its own, name the skill in the prompt.
3. Do not share the `# Expected Behavior`, `# Important Checks` or `# Failure Conditions` sections.
4. Read the response and check each item under Important Checks, then check Failure Conditions.
5. Assign Pass, Needs Improvement or Fail, and note any observations.
6. Where results differ between assistants, note the difference. Equivalent behavior is the goal.

Model responses vary. If a result looks borderline, run the case again before changing a skill.

## Adding Future Automation

Automation is not implemented. When it is added, it should:

- Reuse these case files as the source of truth instead of duplicating them.
- Read the `# Input` and `# Context` sections, run the skill, and judge the response against `# Important Checks` and `# Failure Conditions`.
- Keep the same qualitative outcomes.
- Run as a regression check when a skill changes.

## Adding a New Case

Add one Markdown file with the sections above, under the matching skill's `cases/` folder. Use lowercase kebab-case for the file name, keep the case small enough to evaluate by hand, and link it from the skill's README.

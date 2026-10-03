# Agent Evaluations

Evaluation cases for the AI Engineering Hub agents. Agents are defined by the [Agent Specification](../../docs/agent-specification.md). For the general evaluation approach and the manual run procedure, see the [evaluation suite overview](../README.md).

## Purpose

Agent evaluations differ from skill evaluations.

- **Skill evaluations** ask: *Can the capability perform correctly?* They test a focused capability, such as finding a defect in a review or reading a query plan.
- **Agent evaluations** ask: *Can the agent select and orchestrate the right capabilities to solve the broader task?* They test whether the agent chooses the right skills for the situation, combines them without duplication, handles the evidence it has, stays within safety limits, and recommends the right next step.

An agent can use every skill correctly and still fail by picking the wrong ones, running too many, skipping the ones the task needs, or acting beyond its authority.

## Evaluation Structure

```
evals/agents/
├── README.md
├── pr-review-agent/
├── bug-investigation-agent/
├── test-planning-agent/
├── architecture-agent/
├── api-development-agent/
├── database-troubleshooting-agent/
└── production-incident-agent/
```

Each agent directory contains:

```
README.md     what the agent is evaluated for, skill selection expectations, failure modes, process
cases/        the evaluation cases
```

## Case Format

Every case is a Markdown file in `cases/`, named in lowercase kebab-case, with these sections:

| Section | Content |
| --- | --- |
| `# Scenario` | A realistic engineering situation. |
| `# Input` | The exact prompt to give the agent. |
| `# Context` | Only the information needed to reason about the problem. The case contains everything required to reach the expected conclusion. |
| `# Expected Behavior` | What the agent should identify, decide and produce, including which skills the task calls for and which it does not. |
| `# Important Checks` | The behaviors the evaluator verifies. |
| `# Failure Conditions` | Responses that are incorrect or incomplete. |
| `# Notes` | Optional evaluator notes. |

## Evaluation Outcomes

Each run of a case gets one qualitative outcome. There are no numerical scores or rankings.

| Outcome | Meaning |
| --- | --- |
| **Pass** | The task is solved with the right skills and reasoning, every important check is met, and no failure condition occurs. |
| **Needs Improvement** | The main task is handled, but one or more important checks are missed, or there are weaknesses such as unnecessary work, vague advice or a weak handoff. No failure condition occurs. |
| **Fail** | A failure condition occurs, or the main task is missed or misdiagnosed. |

## Evaluation Principles

Agent evaluations test:

- **Correct agent behavior:** the agent does what its specification says, within its responsibility.
- **Correct skill selection:** the skills used match the task, and the ones it does not need are left out.
- **Skill composition:** multiple skills are combined, ordered and merged without duplicated analysis.
- **Evidence handling:** observed facts, assumptions and hypotheses are kept apart, and nothing is fabricated.
- **Safety:** authorization boundaries are respected, actions are not claimed unless done, and risky steps are flagged.
- **Ambiguity handling:** missing or unclear information is identified and asked about, not filled in.
- **Handoffs:** the agent recommends the right next agent or skill with enough context, and does not take over.
- **Unnecessary work avoidance:** no unneeded skills, analysis, tests or redesign.

Cases test reasoning. They do not rely on keyword matching, and a response passes by reaching the right conclusion and action in any wording. Skill selection is judged from the perspectives visible in the response, and not by whether a skill name appears.

## Running Evaluations

Follow the manual procedure in the [evaluation suite overview](../README.md#how-to-run-an-evaluation-manually). Give the agent the case's `# Input` and `# Context`, do not show it the expected behavior, checks or failure conditions, and compare the response with them. Note any differences between Claude Code and GitHub Copilot, since the two copies of each agent are intended to behave the same way.

## Adding a Case

Add one Markdown file with the sections above under the agent's `cases/` folder and list it in the agent's README. Keep it small enough to judge by hand.

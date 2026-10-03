# Command Evaluations

Evaluation cases for the AI Engineering Hub commands. See [Commands](../../docs/commands.md) for what commands are.

## Purpose

Commands are thin entry points, so their evaluations are small and test only **routing and entry-point behavior**. Each layer has its own evaluations:

| Layer | Evaluation question | Location |
| --- | --- | --- |
| Skill | Can the capability perform correctly? | `evals/<skill>/` |
| Agent | Can the agent select and orchestrate the right capabilities? | [`evals/agents/`](../agents/README.md) |
| Command | Does the entry point route the request to the right agent and preserve the context and safety limits? | `evals/commands/` |

Command cases do not repeat agent cases. They do not judge the quality of the investigation, review or design. They judge whether the command handed the request to the right agent, intact and without adding or removing anything it should not.

## Evaluation Structure

```
evals/commands/
├── README.md
├── review/
├── debug/
├── test-plan/
├── architecture/
├── api/
├── database/
└── incident/
```

Each command directory contains a small number of cases in `cases/`.

## What Is Verified

- **Correct agent selection:** the request goes to the command's target agent and not to another one.
- **Context preservation:** the user's full request, pasted technical detail and stated constraints reach the agent unchanged and are not summarized away.
- **No unnecessary instructions:** the command does not add engineering guidance of its own or repeat agent or skill instructions.
- **Safety boundaries:** the command does not authorize destructive, production or data-changing actions.
- **Missing information:** the command proceeds when there is enough context, and lets the agent identify what is missing instead of demanding a fixed form.

## Case Format

Each case is a Markdown file with these sections, in this order:

| Section | Content |
| --- | --- |
| `# Scenario` | The situation in which the command is used. |
| `# Input` | The exact command invocation, including the text after it. |
| `# Context` | Any attached material or state the command would see. |
| `# Expected Behavior` | How the command should route the request. |
| `# Important Checks` | What the evaluator verifies. |
| `# Failure Conditions` | Behavior that is incorrect. |
| `# Notes` | Optional evaluator notes. |

## Evaluation Outcomes

Each run gets one qualitative outcome. There are no numeric scores or rankings.

| Outcome | Meaning |
| --- | --- |
| **Pass** | The request reaches the right agent intact, with safety limits preserved, and nothing unnecessary is added. |
| **Needs Improvement** | Routing is right, but some context is lost, extra guidance is added, or an unnecessary question is asked. |
| **Fail** | The wrong agent is used, important context or constraints are lost, a safety boundary is weakened, or the command does the agent's work itself. |

## Running a Case

1. Run the command with the case's `# Input` on the platform under test (Claude Code or GitHub Copilot), with the `# Context` available.
2. Observe which agent handles the request, what it receives, and what the command adds or asks.
3. Compare with Expected Behavior, Important Checks and Failure Conditions.
4. Assign an outcome, and note any difference between the two platforms. Their behavior is intended to be equivalent.

The quality of the agent's own work is judged by the [agent evaluations](../agents/README.md).

## Adding a Case

Add one file under `evals/commands/<command>/cases/`. Keep it small and focused on routing. If a case needs agent reasoning to judge, it belongs in the agent evaluations.

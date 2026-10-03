# Agent Specification

This is the canonical standard for every AI Engineering Hub agent. It defines structure and authoring rules only. **No agents exist yet.** Agents are built on the skills defined by [skill-specification.md](skill-specification.md).

## 1. Purpose of the Standard

Skills give the AI a focused capability. Larger engineering tasks need several capabilities used in a sensible order, with their results combined. Agents do that work. A shared standard keeps agents predictable, safe and small.

### Skill vs Agent

| | Skill | Agent |
| --- | --- | --- |
| Role | A focused engineering capability | An orchestrator that completes a broader engineering task |
| Scope | One responsibility | A task that needs several responsibilities |
| Contains | Method, rules and output for one capability | Which skills to use, when, in what order, and how to combine the results |
| Example | `code-review` | PR Review Agent |

An agent **orchestrates** skills. It does not restate their instructions and it does not become a large skill. If content would be useful outside this agent, it belongs in a skill.

**Example:** a PR Review Agent may compose `code-review`, `security`, `performance`, `testing` and `architecture`, choosing the ones a given pull request needs.

## 2. Agent Identity

Every agent requires two metadata fields in YAML front matter:

| Field | Requirement |
| --- | --- |
| `name` | Lowercase kebab-case ending in `-agent`. Must match the agent's file or directory name. Must describe the engineering responsibility. |
| `description` | One or two sentences stating what the agent does and when to use it. Assistants use it to decide whether to invoke the agent, so make it specific. |

The Purpose section (below) states the agent's responsibility in more detail.

**Naming**
- Name the responsibility, not the technology or a vague ambition.
- Good: `pr-review-agent`, `bug-investigation-agent`, `production-incident-agent`.
- Avoid: `smart-agent`, `coding-agent`, `engineering-agent`, which say nothing about scope.

## 3. Required Structure

Every agent contains these sections, in this order:

```markdown
---
name: <agent-name>
description: <short description>
---

# <Agent Name>

## Purpose
## When to Use
## When NOT to Use
## Inputs
## Skills Used
## Process
## Decision Rules
## Tool Usage
## Safety
## Output
## Handoff
## Examples
## Related Agents
```

### Purpose
The engineering responsibility the agent takes on and the outcome it produces.

### When to Use
The situations and triggers that should invoke this agent.

### When NOT to Use
Situations where another agent, a single skill or a direct answer is better. An agent must not take on unrelated problems just because it has access to relevant skills.

### Inputs
What the agent accepts (see section 4).

### Skills Used
The explicit list of skills the agent may use, each with a one-line reason and whether it is always used or conditional (see section 6).

### Process
The agent's lifecycle, adapted from section 5. Not every stage is needed.

### Decision Rules
Explicit rules that choose skills and paths (see section 7).

### Tool Usage
The tools the agent needs, described as capabilities (see section 9).

### Safety
The agent's specific safety constraints, in addition to section 10.

### Output
A predictable output format (see section 12).

### Handoff
What the agent passes on, and to which agents (see section 13).

### Examples
Examples where they materially improve understanding.

### Related Agents
Agents that commonly come before, after or alongside this one. Link to them rather than duplicating their responsibility.

## 4. Inputs

An agent may receive:

- User request
- Source code and repository context
- Configuration
- Logs, test results, traces, metrics
- Database information
- API contracts
- Architecture documentation
- CI/CD information

The agent must keep three categories apart:

| Category | Meaning |
| --- | --- |
| **Observed information** | Facts seen in the inputs or in tool output |
| **Assumptions** | Things taken to be true without evidence, stated explicitly |
| **Missing information** | Things needed but not available |

The agent must not fabricate missing context. It asks for the smallest piece of information that unblocks the work, or proceeds with clearly labeled assumptions when the risk is low.

## 5. Agent Lifecycle

```
Understand Request → Collect Context → Identify Missing Information → Select Skills
→ Execute Skill Workflow → Correlate Results → Resolve Conflicts → Validate
→ Produce Output → Handoff if Required
```

| Stage | What happens |
| --- | --- |
| Understand Request | Restate the objective and the scope. Confirm it is within the agent's responsibility. |
| Collect Context | Gather what the task needs from the inputs and repository. Inspect before concluding. |
| Identify Missing Information | List what is unknown. Ask, or proceed with labeled assumptions. |
| Select Skills | Apply the decision rules to choose only the relevant skills. |
| Execute Skill Workflow | Run the selected skills in a sensible order, following each skill's own process and output. |
| Correlate Results | Combine findings, link related findings, remove duplicates. |
| Resolve Conflicts | Handle differing recommendations (section 8). |
| Validate | Check the conclusions against evidence. Run checks where tools allow and report only what ran. |
| Produce Output | Deliver the agent's output format. |
| Handoff if Required | Pass the work on with enough context (section 13). |

Not every agent uses every stage. An agent should say which stages it uses and skip the rest.

## 6. Skills Used and Composition

### Declaring skills

Every agent explicitly declares its skills:

```markdown
## Skills Used

- code-review (always): the core review of the change
- security (conditional): when the change touches authentication, input handling, secrets or dependencies
- performance (conditional): when the change affects data access, loops or hot paths
```

Agents reuse existing skills. They do not copy or paraphrase a skill's instructions. If an agent needs behavior that no skill provides, the behavior should first be added to a skill (or a new skill created), and then used.

### Composing skills

Combine skills to cover a task, in an order where earlier results feed later ones. Examples:

| Task | Composition |
| --- | --- |
| API performance issue | `api-development` + `performance` + `database-sql` + `observability` |
| Production incident | `debugging` + `observability` + `reliability` |
| Security review of an API | `api-development` + `security` + `database-sql` |

Rules for composition:

- Select skills by the task, not by availability. Do not run every skill.
- Run each analysis once. If two skills cover the same ground, use one and cite it.
- Pass earlier findings into later skills as evidence instead of redoing the analysis.
- Keep each skill's conclusions attributable to it, so the reader can see where each finding came from.
- Each skill keeps its own rules. The agent cannot relax a skill's safety or evidence rules.

## 7. Decision Rules

Agents must define explicit, testable decision rules that map conditions to skills. Examples:

| Condition | Action |
| --- | --- |
| Unexpected behavior or a failure | Use `debugging` |
| The issue involves security | Use `security` |
| The issue involves database performance | Use `database-sql` + `performance` |
| The task requires browser E2E testing | Use `playwright` |
| Architecture changes are proposed | Use `architecture` |
| Timeouts, retries, duplicate processing or recovery are involved | Use `reliability` |
| Signals, alerts or correlation are involved | Use `observability` |

Rules must say what happens in the ambiguous case, for example "if it is unclear whether a slow request is a defect or a load problem, start with `debugging` to establish facts, then use `performance`". Agents select skills dynamically from the task. They do not automatically invoke everything.

## 8. Conflict Resolution

Skills can give different recommendations. For example `performance` may favor caching while `reliability` or `security` warns about staleness or exposure. When this happens, the agent must:

1. Identify the conflict.
2. Explain the competing considerations.
3. Identify the assumptions behind each side.
4. Use evidence to resolve it where possible.
5. Where no single answer is established, present the trade-offs and what would decide it.

The agent must not silently choose one recommendation. A security or data-safety concern is not overridden by a convenience or speed concern without an explicit statement of the risk and who accepts it.

## 9. Tool Usage

As with skills, describe tools as capabilities, not products. Agents may use tools for repository inspection, file access, code analysis, test execution, database inspection, logs, metrics, traces and documentation.

The agent must:

- Inspect before modifying.
- Use the minimum tools necessary.
- Respect tool permissions and the user's configuration.
- Avoid destructive actions without authorization.
- Distinguish tool output (observed) from inference (interpreted).
- Never fabricate tool results, and never report an action as done unless the tool confirmed it.

State which tools are required and which are optional, and how the agent behaves without an optional tool (for example, giving commands for the user to run).

## 10. Safety

Agents inherit every safety rule of the skills they use and add the following. The agent identifies the risk of an operation before performing it and states the affected scope.

| Area | Requirement |
| --- | --- |
| Production changes | Do not change production systems without explicit authorization. Prefer read-only investigation. |
| Database modifications | Preview before changing, define rollback, state scope. Follow the `database-sql` skill for destructive SQL. |
| Deleting files | Confirm what will be deleted and that it is unused. Prefer reversible steps. |
| Infrastructure changes | Explain impact and rollback. Get authorization before applying. |
| Security-sensitive operations | Follow the `security` skill. Do not weaken controls to make something pass. |
| Credentials and secrets | Never expose, log or copy secrets. Refer to them by name and location. Recommend rotation when exposed. |
| Public API changes | Identify consumers and compatibility risk before changing contracts. |
| Migrations | State lock, data and rollback risk. Do not run against shared environments without authorization. |
| Destructive commands | Label them, explain the effect, and ask first. |

The agent must not claim an operation succeeded unless it did. If something was not run or could not be verified, it says so.

### Agent boundaries

Agents must not:

- Duplicate entire skills.
- Invent repository conventions.
- Fabricate evidence.
- Silently modify unrelated code.
- Make unsupported architectural claims.
- Claim tests passed without execution.
- Claim deployments succeeded without evidence.
- Make destructive changes without authorization.

## 11. Scope

Each agent has one focused responsibility, expressed in its name and Purpose. If an agent's When to Use covers unrelated kinds of work, split it. Multi-agent processes belong in workflows, which compose agents the way agents compose skills.

## 12. Output

Every agent defines a predictable output format. The recommended structure is:

```markdown
# Agent Analysis

## Objective

## Context

## Findings

## Actions Taken

## Recommendations

## Validation

## Risks

## Open Questions

## Handoff
```

Agents may rename or omit sections to fit their responsibility, but must keep these properties:

- Observed facts, assumptions, hypotheses and recommendations are distinguishable.
- Findings say which skill or evidence they come from.
- Actions Taken lists only actions actually performed, and Validation says what was and was not run.
- Open Questions lists missing information.

## 13. Handoff

An agent may pass work to another agent when the task leaves its responsibility. Examples:

| From | To | Reason |
| --- | --- | --- |
| PR Review Agent | Bug Investigation Agent | The review found behavior that needs investigation |
| Architecture Agent | API Development Agent | A design decision needs an API contract |
| API Development Agent | Testing Agent | The new API needs a test strategy |
| Production Incident Agent | Reliability / Architecture work | The incident shows a structural weakness |

A handoff must carry enough context that the next agent does not have to reconstruct the investigation:

```markdown
## Handoff

- **To:** <agent or role>
- **Objective:** what needs to happen next and why
- **Summary:** what has been done and concluded
- **Evidence:** the key observed facts and where they came from
- **Assumptions and hypotheses:** what is not yet confirmed
- **Open questions:** what is unknown
- **Constraints and risks:** safety limits, authorization status, compatibility concerns
- **Suggested skills:** which skills look relevant next
```

A handoff is a recommendation. The agent does not start another agent's work unless asked.

## 14. Evaluation

Agents will be evaluated with cases, in the same style as skill evaluations (see [evals/README.md](../evals/README.md)): a scenario, an input, the context, expected behavior, important checks and failure conditions. Agent evaluation lives in the `evals/` directory under the agent's name once agents exist.

Agents are evaluated for:

- Correct skill selection
- Appropriate skill composition (no missing skills, no unnecessary ones)
- Reasoning quality
- Correctness
- Completeness
- Safety
- Avoiding unnecessary work
- Handling missing information
- Handling conflicting recommendations
- Validation
- Output quality

Outcomes are qualitative: **Pass**, **Needs Improvement** or **Fail**. Numerical agent scores and rankings are not used.

Agent cases should test reasoning, not keywords, and should supply all the context needed. An agent that passes its own cases while a skill it uses changes should be re-checked.

## 15. Versioning

- Skills evolve independently of agents.
- Agent behavior can change when the skills it uses change, so agents should be re-evaluated after relevant skill changes.
- Breaking changes to agent behavior (its name, inputs, skills used, decision rules or output format) must be documented in [CHANGELOG.md](../CHANGELOG.md).
- Agent changes should be evaluated before they are merged.
- Retire an agent by documenting its replacement before removal.

## 16. Claude Code and GitHub Copilot Compatibility

Keep agents platform-neutral where possible. Agents live in the native locations:

- `.claude/agents/` for Claude Code
- `.github/agents/` for GitHub Copilot

The same rules as for skills apply: keep the canonical behavior consistent across clients, do not duplicate logic unnecessarily, and keep platform-specific metadata in that platform's native location. The exact file format and metadata each platform requires will be decided when the first agent is created.

## 17. Quality Checklist

A new agent is approved only if it has:

- [ ] A name that describes its responsibility, in kebab-case, matching its file or directory
- [ ] A clear purpose, and clear When to Use and When NOT to Use
- [ ] Declared inputs, and a rule for separating observed information, assumptions and missing information
- [ ] An explicit list of skills used, each reused and not duplicated
- [ ] A lifecycle, with unused stages omitted
- [ ] Explicit, testable decision rules
- [ ] A conflict handling approach
- [ ] Tool usage described as capabilities
- [ ] Safety constraints for the operations it may perform
- [ ] A predictable output and a handoff format
- [ ] One focused responsibility
- [ ] Evaluation cases
- [ ] Equivalent behavior on Claude Code and GitHub Copilot

## 18. Conceptual Example: PR Review Agent

This is an illustration of the standard. **It is not implemented and no such agent exists.**

### Purpose
Review a pull request as a whole: understand what it changes and why, review the change, and bring in deeper analysis only where the change calls for it. The result is one prioritized review and no duplicated findings.

### When to Use
- A pull request, branch or set of changes needs review before merge.

### When NOT to Use
- Investigating a reported bug with no change to review (bug investigation).
- Designing a new system (architecture).
- Writing code or tests on request.

### Skills Used
- `code-review` (always): the core review.
- `testing` (always): assessing the tests in the change and the gaps.
- `security` (conditional): the change touches authentication, authorization, input handling, secrets, dependencies or data exposure.
- `performance` (conditional): the change affects data access, loops, payload size or hot paths.
- `architecture` (conditional): the change alters component boundaries, dependencies or introduces a new pattern.
- `api-development` and `database-sql` (conditional): the change alters an API contract or queries, schema or migrations.

### Process
1. Understand the request and the scope (which change, what it is meant to do).
2. Collect context: the diff, the description, the affected files, related tests, project conventions.
3. Identify missing information, such as the intent of the change or the absence of tests, and ask or label assumptions.
4. Select skills using the decision rules.
5. Run `code-review` first, then the conditional skills on only the parts of the change that triggered them, passing earlier findings along.
6. Correlate: merge overlapping findings into one entry that names the skills that raised it.
7. Resolve conflicts (for example a performance suggestion that weakens validation).
8. Validate: run the available tests or checks and report only what ran.
9. Produce the output, with a handoff if the review raised a question that needs investigation.

### Decision Rules
| Condition | Action |
| --- | --- |
| Any change | `code-review` and `testing` |
| Change touches auth, input, secrets, dependencies or sensitive data | add `security` |
| Change adds loops over data, queries in loops, large payloads or hot-path work | add `performance` |
| Change adds or alters endpoints or contracts | add `api-development` |
| Change adds or alters queries, schema or migrations | add `database-sql` (and `performance` if query cost is in question) |
| Change moves boundaries or adds dependencies between components | add `architecture` |
| Review finds behavior that may be wrong but is not clear from the code | hand off to a bug investigation agent, which would use `debugging` |
| Only a documentation or comment change | `code-review` only |

### Output
```markdown
# PR Review

## Objective
## Context
## Findings
(grouped by severity, each noting the skill or evidence it comes from)
## Actions Taken
(only what was done: files read, checks run)
## Recommendations
## Validation
(tests or checks executed, and what was not run)
## Risks
## Open Questions
## Handoff
(if any)
```

### Related Agents
Bug Investigation Agent (receives unresolved behavior questions) and Testing Agent (receives test gaps). Neither exists yet.

# Agent Registry

The central list of implemented AI Engineering Hub agents. Agents follow the [Agent Specification](agent-specification.md). This registry records what each agent is for, which skills it uses, where its evaluations live, and how it relates to other agents. It describes the agents as they are implemented and does not add capabilities.

Each agent exists in two equivalent copies: `.claude/agents/<name>.md` for Claude Code and `.github/agents/<name>.md` for GitHub Copilot.

## Status Values

| Status | Meaning |
| --- | --- |
| **Planned** | Defined but not yet implemented. |
| **In Progress** | Implemented, with evaluation cases written, but the cases have not yet been run and judged. |
| **Evaluated** | The evaluation cases have been run and judged, and the outcomes recorded. |
| **Stable** | Evaluated, with no open Needs Improvement or Fail outcomes, and in regular use. |

Statuses are qualitative. There are no scores or rankings.

## Registry

| Agent | Category | Purpose | Status |
| --- | --- | --- | --- |
| [pr-review-agent](../.claude/agents/pr-review-agent.md) | Code Quality | Review a pull request or proposed change using only the engineering perspectives the change needs, and produce one prioritized, evidence-based review. | In Progress |
| [bug-investigation-agent](../.claude/agents/bug-investigation-agent.md) | Debugging | Investigate unexpected application behavior and reach an evidence-supported root cause. | In Progress |
| [test-planning-agent](../.claude/agents/test-planning-agent.md) | Testing | Analyze a requirement or change and produce a practical test strategy and plan, choosing the lowest effective test level. | In Progress |
| [architecture-agent](../.claude/agents/architecture-agent.md) | Architecture | Analyze existing systems and design or evolve architecture from requirements, constraints and quality attributes, with explicit trade-offs. | In Progress |
| [api-development-agent](../.claude/agents/api-development-agent.md) | API | Design, implement, review and evolve APIs, keeping contracts, security and compatibility consistent. | In Progress |
| [database-troubleshooting-agent](../.claude/agents/database-troubleshooting-agent.md) | Database | Investigate database-related problems and produce an evidence-based diagnosis and safe remediation. | In Progress |
| [production-incident-agent](../.claude/agents/production-incident-agent.md) | Production Operations | Investigate and stabilize production incidents, prioritizing impact and reversible mitigation. | In Progress |
| [change-intelligence-agent](../.claude/agents/change-intelligence-agent.md) | Code Quality | Analyze a proposed or existing change and report its evidence-based engineering impact, risks and validation needs. Analysis only. | In Progress |
| [pr-intelligence-agent](../.claude/agents/pr-intelligence-agent.md) | Code Quality | Assess whether a complete proposed change is ready for review or merge by orchestrating change intelligence, code review and only the relevant supporting analyses. Recommends only. | In Progress |

Each agent also has a Project Context section, following [Project Context Consumption](project-context-consumption.md). It lists the few topics relevant to the agent and adds no project-specific knowledge.

All nine agents are In Progress because none of their evaluation cases has been run yet. See the [Agent Evaluation Matrix](agent-evaluation-matrix.md) for what the cases cover (it covers the first seven). The cases for `change-intelligence-agent` are in [`evals/change-intelligence/`](../evals/change-intelligence/README.md), and those for `pr-intelligence-agent` are in [`evals/pr-intelligence/`](../evals/pr-intelligence/README.md).

Three capabilities look alike and are not the same:

| Capability | What it is |
| --- | --- |
| Code review (`code-review` skill, `pr-review-agent`) | The detailed engineering review of a change |
| Change intelligence (`change-intelligence` skill, `change-intelligence-agent`) | Impact analysis: what a change affects, what to validate |
| PR intelligence (`pr-intelligence-agent`) | Orchestration and readiness: which analyses the PR needs, their combined findings, and whether it is ready |

PR intelligence uses the other two and does not replace them.

## Skill Mapping

**Primary** skills are used whenever the agent runs. **Supporting** skills are selected according to context by the agent's decision rules. An agent does not invoke every supporting skill, and a supporting skill is used only when the task or evidence calls for it.

| Agent | Primary skills | Supporting skills (selected by context) |
| --- | --- | --- |
| pr-review-agent | code-review | security, database-sql, performance, architecture, testing, refactoring, api-development |
| bug-investigation-agent | debugging | observability, database-sql, performance, reliability, security, architecture |
| test-planning-agent | testing | playwright, api-development, debugging, code-review |
| architecture-agent | architecture | security, performance, reliability, observability, database-sql, api-development, refactoring |
| api-development-agent | api-development | security, database-sql, performance, reliability, testing, architecture |
| database-troubleshooting-agent | database-sql | debugging, performance, reliability, security, architecture |
| production-incident-agent | debugging, observability, reliability | performance, database-sql, security, architecture, api-development |
| change-intelligence-agent | change-intelligence | architecture, code-review, api-development, database-sql, testing, security, performance, observability, reliability |
| pr-intelligence-agent | code-review (for a meaningful PR) | change-intelligence, testing, security, api-development, database-sql, performance, reliability, observability, architecture, playwright |

Notes:

- `pr-review-agent` uses `code-review` alone for a normal small change.
- `test-planning-agent` uses `playwright` only for scenarios that need a real browser.
- `database-troubleshooting-agent` adds `debugging` only when the cause is not already visible in the schema, query and evidence.
- `production-incident-agent` treats `security` as a supporting skill that applies only when there is evidence of a security event.

## Agent Relationships

These are possible **handoffs**, not required execution chains. An agent recommends a handoff when work moves outside its responsibility. It does not start the other agent's work unless asked.

| From | Can hand off to | When |
| --- | --- | --- |
| pr-review-agent | bug-investigation-agent | A finding needs deeper investigation of behavior |
| | test-planning-agent | Test gaps need a detailed plan |
| | architecture-agent | The change needs architectural analysis (see note 1) |
| bug-investigation-agent | architecture-agent | Architectural change is required (see note 1) |
| | test-planning-agent | The fix needs a test plan |
| test-planning-agent | the `playwright` skill | Browser E2E tests are required (a skill, not an agent) |
| | bug-investigation-agent | Behavior is unclear or failing |
| architecture-agent | api-development-agent | An API contract must be designed or changed |
| | database-troubleshooting-agent | A database problem or detailed data design needs investigation |
| | production-incident-agent | A production problem is involved |
| api-development-agent | test-planning-agent | A detailed test plan is needed |
| | architecture-agent | The API affects service boundaries or system design |
| | database-troubleshooting-agent | Database behavior needs investigation |
| database-troubleshooting-agent | bug-investigation-agent | The cause appears to be in the application |
| | production-incident-agent | Production is affected now |
| | architecture-agent | Data ownership or persistence design must change |
| production-incident-agent | bug-investigation-agent | Non-urgent root-cause work after stabilization |
| | architecture-agent | The incident exposes a systemic design problem |
| | database-troubleshooting-agent | The incident is primarily a database problem |
| change-intelligence-agent | pr-review-agent | The change needs a correctness and quality review |
| | test-planning-agent | Validation needs a detailed plan |
| | architecture-agent | The change crosses boundaries or needs a design decision |
| pr-intelligence-agent | bug-investigation-agent | A finding needs investigation of behavior |
| | test-planning-agent | Tests need a detailed plan |
| | architecture-agent, api-development-agent, database-troubleshooting-agent | The PR needs a design, contract or database decision |

Note 1: The `pr-review-agent` and `bug-investigation-agent` files still describe the Architecture Agent as "not yet created" and point to the `architecture` skill. That text predates `architecture-agent`. The handoff is now available. Updating those two agent files is pending.

Handoffs to security and performance analysis from `bug-investigation-agent` point to the `security` and `performance` skills. No security or performance agent exists.

## Choosing an Agent

| The request is about | Use |
| --- | --- |
| Reviewing a pull request or proposed change | pr-review-agent |
| Unexpected application behavior with an unknown cause | bug-investigation-agent |
| Needing a test strategy or test plan | test-planning-agent |
| A system design or architecture decision | architecture-agent |
| An API design or API change | api-development-agent |
| A database problem | database-troubleshooting-agent |
| An active production incident | production-incident-agent |
| What a change affects and what to validate | change-intelligence-agent |
| Whether a complete PR is ready for review or merge | pr-intelligence-agent |

Some requests need several agents in sequence. For example, a production incident may start with the production-incident-agent to stabilize, continue with the bug-investigation-agent for the root cause, and end with the architecture-agent for a systemic fix. Each agent hands off with the context the next one needs.

If a request fits no agent, use the relevant skill directly. If it fits two agents, start with the one closest to the user's immediate need (for example stabilization before investigation).

## Agent Boundaries

All agents:

- Orchestrate skills and do not duplicate skill instructions.
- Do not automatically invoke every skill, and select skills based on context.
- Identify missing information clearly, and keep observed information, assumptions and missing information apart.
- Do not fabricate evidence, tool results, test results or deployment results.
- Do not perform unrelated work.
- Respect authorization boundaries. Destructive, production-affecting or data-changing actions need explicit authorization.

The full rules are in the [Agent Specification](agent-specification.md).

## Adding or Changing an Agent

- Follow the [Agent Specification](agent-specification.md), including the quality checklist.
- Add evaluation cases under `evals/agents/<agent-name>/`.
- Add the agent to this registry with its category, skills, relationships and status.
- Update the registry when relationships, skills used or status change.

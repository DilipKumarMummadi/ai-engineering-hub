# AI Engineering Hub: User Guide

A practical guide for engineers. After reading it you should know what the Hub does, how to get it running, which command to pick, what happens behind the scenes, what it depends on, and where it stops.

Everything here describes the repository as it exists today. Anything not implemented is listed under [What Is Not Available](#15-what-is-not-available), not described as a feature.

## 1. What the Hub Is

The AI Engineering Hub is a set of files that teach an AI coding assistant (Claude Code or GitHub Copilot) how to do engineering work in a consistent, evidence-based way. It contains:

| Piece | What it is | Count |
| --- | --- | --- |
| **Skills** | Focused engineering methods: code review, debugging, testing, and so on | 14 |
| **Agents** | Specialists that pick and combine skills for one kind of task | 10 |
| **Commands** | Short entry points you type, such as `/review-pr` | 18 |
| **Workflows** | Multi-stage processes such as feature development | 8 |
| **Project Context** | A `PROJECT-CONTEXT.md` describing one repository, produced by a generator | tool |
| **MCP connections** | Optional links to GitHub, Jira, PostgreSQL and Playwright | 5 servers listed |

It is not a service. It has no backend, database or server of its own. It never stores your credentials, and it never changes anything outside your workspace on its own.

## 2. How to Read Availability Labels

| Label | Meaning |
| --- | --- |
| **Available** | Implemented in the repository and usable now |
| **Optional** | Works without it; adds capability if present |
| **Requires MCP** | Needs an external tool connected in your client |
| **Client-specific** | Works differently, or only, in Claude Code or GitHub Copilot |
| **Planned / Not Available** | Specified or discussed but not implemented |

## 3. Getting Started

### Choose how to use it

| Way | What you get | Labels |
| --- | --- | --- |
| **Open or clone the Hub repository** and work with your client there | Everything: all 18 commands, 10 agents, 8 workflows, 14 skills | Available |
| **Install it as a plugin** (Agent Plugins 1.0.0) from `https://github.com/DilipKumarMummadi/ai-engineering-hub` | The 14 skills in any Agent Plugins client. In Claude Code also `/ai-engineering-hub:context`, `/ai-engineering-hub:review-pr`, `/ai-engineering-hub:requirement` and the `pr-intelligence-agent` and `requirement-intelligence-agent` | Available, Client-specific |

Important: in plugin form, agents, commands and workflows are **not** fully portable yet. The workflow commands (`/feature`, `/bug-fix` and the rest) and most agents are used from the Hub's own `.claude/` (Claude Code) or `.github/` (GitHub Copilot) folders. See [Plugin Architecture](plugin-architecture.md) for the reasoning.

### What you need

| Need | For | Label |
| --- | --- | --- |
| Claude Code or GitHub Copilot | Running anything | Required |
| Python 3.9 or newer | `/context` (the Project Context generator); nothing else to install | Required for `/context` |
| Git | `/context` finds the repository root with git | Required for `/context` |
| Node.js | The Playwright MCP server | Optional, Requires MCP |
| `uv` (`uvx`) | The PostgreSQL MCP server | Optional, Requires MCP |
| A signed-in GitHub, Jira or database connection in your client | Live PR, ticket or database information | Optional, Requires MCP |

### First five minutes

1. Open your project (not the Hub) in your client with the Hub available as above.
2. Generate its context: `/context generate --dry-run`, review, then `/context generate`.
3. Ask for something small, for example `/review` on your current branch, or `/debug` with an error message.
4. Read where the answer says its evidence came from. The Hub tells you what it actually looked at and what it could not check.
5. Only then try a workflow such as `/feature`.

## 4. Which Command Should I Use?

| I want to… | Use | Kind |
| --- | --- | --- |
| Find out whether a ticket or requirement is ready to build | `/requirement BR-7368` | Agent |
| Improve a ticket's description and acceptance criteria | `/requirement BR-7368 refine`, then `update` after reviewing the diff | Agent |
| Review a pull request on GitHub | `/review-pr <URL or number>` | Agent |
| Review a diff, branch or files | `/review` | Agent |
| Know whether a change is ready to merge | `/pr-intelligence` | Agent |
| Understand what a change affects | `/change-impact` | Agent |
| Investigate an error or odd behavior | `/debug` | Agent |
| Investigate something broken in production | `/incident` | Agent |
| Fix a bug end to end, with a regression test | `/bug-fix` | Workflow |
| Build a feature end to end | `/feature`. With a ticket (`/feature BR-7368`) it first checks the requirement is ready | Workflow |
| Change or add an API | `/api` to work on it directly, `/api-change` for the full process | Agent, Workflow |
| Change a schema or data, or fix a slow query | `/database` to investigate, `/database-change` for the full process | Agent, Workflow |
| Decide how to structure or design something | `/architecture` | Agent |
| Plan tests for a change | `/test-plan` | Agent |
| Write a browser end-to-end test | `/e2e` | Workflow |
| Get a change ready for a PR (summary, description, reviewer notes) | `/pr-prep` | Workflow |
| Create or check `PROJECT-CONTEXT.md` | `/context` with `generate`, `inspect` or `drift` | Tool |

Rule of thumb: use an **agent command** when you want one question answered. Use a **workflow command** when you want a whole piece of work carried through several stages with checkpoints.

Command names are the same in both clients. In Claude Code with the plugin installed they appear with a prefix, for example `/ai-engineering-hub:review-pr`. In GitHub Copilot they are the prompt files in `.github/prompts/` (`review-pr.prompt.md`, and so on).

## 5. Commands Reference

Every command passes your text to the agent or workflow unchanged. You do not need a fixed format; paste the error, the diff, or the requirement.

### Agent commands

| Command | Agent | Give it | Gets you |
| --- | --- | --- | --- |
| `/requirement` | requirement-intelligence-agent | An issue key such as `BR-7368` or requirement text, then optionally `analyze`, `refine`, `readiness` or `update` | Requirement analysis, readiness (READY, NEEDS_CLARIFICATION, BLOCKED) and confidence. **Requires MCP** (`requirements-tracking`) to read a ticket; pasted text works without it |
| `/review` | pr-review-agent | A PR, branch, files or notes | A prioritized, evidence-based review |
| `/review-pr` | pr-intelligence-agent | A PR URL or number, plus notes | A `# PR Review` with findings and a readiness recommendation. **Requires MCP** (`source-control`) for the remote PR |
| `/pr-intelligence` | pr-intelligence-agent | A PR, branch, diff, files or notes | A readiness assessment: READY, NEEDS_CHANGES or NEEDS_INFORMATION |
| `/change-impact` | change-intelligence-agent | A diff, branch, commit range, PR or notes | What changed, what it affects, risks, what to validate |
| `/debug` | bug-investigation-agent | Error, stack trace, logs, expected vs actual | Evidence-based root cause and a proposed fix |
| `/incident` | production-incident-agent | What is failing, impact, timeline, logs, recent deploys | Impact, timeline, hypotheses, proposed stabilization. Never acts on production itself |
| `/test-plan` | test-planning-agent | Feature, requirement, change or acceptance criteria | A test strategy and plan, at the lowest effective test level |
| `/architecture` | architecture-agent | Problem, requirements, constraints, current design | Options with trade-offs and a recommendation |
| `/api` | api-development-agent | Requirement, endpoints, consumers | API design, contract and implementation guidance |
| `/database` | database-troubleshooting-agent | Schema, SQL, error, plan, engine | Diagnosis and safe remediation |

`/review-pr` and `/pr-intelligence` share one agent. `/review-pr` is the entry that retrieves a PR for you; `/pr-intelligence` assesses a change you describe or point at.

### Workflow commands

| Command | Workflow | Stages at a glance |
| --- | --- | --- |
| `/feature` | feature-development | Requirement, repository, context check, existing-system analysis, design, plan, implementation, testing, security, change intelligence, code review, PR preparation, PR intelligence, final validation (14 stages) |
| `/bug-fix` | bug-fix | Report, context, reproduce and understand, evidence, hypotheses, validation, root cause, minimal fix, regression test, change intelligence, review, PR preparation, PR intelligence |
| `/api-change` | api-change | Requirement, existing API, context, contract, compatibility, security, persistence impact, implementation, API tests, change intelligence, review, PR intelligence |
| `/database-change` | database-change | Requirement, schema, context, data impact, migration design, application impact, performance, concurrency, security, implementation, migration validation, testing, rollback, change intelligence, review, PR intelligence |
| `/e2e` | e2e-test-creation | Flow, context, existing UI and tests, plan, data, locators, Playwright implementation, execution, failure analysis, stabilization, validation |
| `/pr-prep` | pr-preparation | Understand change, context, diff, tests, security, performance, architecture, change intelligence, summary, description, reviewer guidance, PR intelligence |

The production-incident workflow is started with `/incident`. The pr-intelligence workflow is the one behind `/pr-intelligence`.

Workflow commands never authorize migrations, deployments, pushes, merges or production changes. A plan is not permission to implement.

### Requirement Intelligence

A requirement is a Jira issue such as `BR-7368`, or text you paste. Requirement Intelligence answers one question before any code is written: **is this requirement ready to build, and if not, what is missing?**

```
Requirement → Analysis → Readiness → Human review → Jira update → Re-analysis → Implementation
```

| Form | What happens |
| --- | --- |
| `/requirement BR-7368` | Starts an interactive session. Reads the issue, shows it, analyzes it against your repository, Project Context and (where it exists) memory, shows the checkpoints, readiness and confidence, and asks the one most valuable question. Changes nothing |
| `/requirement BR-7368 inspect` | Shows the current workspace: the requirement as enriched so far, checkpoints, open and answered questions, conflicts |
| `/requirement BR-7368 analyze` | Understanding, what is confirmed or inferred, acceptance-criteria verdicts, gaps, dependencies, risks |
| `/requirement BR-7368 refine` | A proposed improved requirement and acceptance criteria. Everything the ticket did not say is marked `Proposed`. Changes nothing |
| `/requirement BR-7368 readiness` | Only the readiness report: dimension table, blocking questions, gate outcome |
| `/requirement BR-7368 update` | Prepares the improvement and shows the exact difference. Writes to Jira only after you approve that difference |

The word after the key is read as plain language. There is no special syntax to learn.

**Interactive refinement.** The Hub works out which checkpoints matter for this requirement (an API, a database change, a bulk upload each need different ones) and asks one question at a time, because each answer changes what comes next. You can answer, pick an option, say "let me describe it myself", mark something not applicable, skip, add context, or rewrite the requirement entirely. Say "show checkpoints", "show open questions", "show requirement", "re-analyze" or "finish" whenever you like. If what you say contradicts the ticket or an earlier answer, the Hub shows a Conflict Detected block and asks which to keep. Skipping a blocking checkpoint does not resolve it, and finishing early does not make the requirement ready. Nothing is stored anywhere: the session's state is text in the conversation, and the ticket becomes the durable copy only after you approve an update. See [Interactive Requirement Discovery](interactive-requirement-discovery.md).

**Readiness** answers whether work may safely begin: `READY`, `NEEDS_CLARIFICATION` or `BLOCKED`. It is never a number. Only the dimensions that apply to your change are judged: a screen-only change is not asked about database migration.

**Confidence** answers how sure the Hub is of its own understanding: `HIGH`, `MEDIUM`, `LOW` or `UNKNOWN`, always with the reason. It is reported next to readiness and never replaces it. A requirement can be understood with `HIGH` confidence and still be `NEEDS_CLARIFICATION` because only you can decide something.

**Missing information** is reported as Missing, Unknown or Ambiguous. The Hub does not fill it in. Open questions are classed `BLOCKING` (prevents `READY`), `IMPORTANT` or `OPTIONAL` (both reported, neither blocks).

**Jira update approval.** `update` only prepares. The Hub shows the current text, the proposed text and the changes, and waits. Your approval must be a reply to that difference, and it covers only that difference. If you edit the proposal, you approve again. If the ticket changed in the meantime, the Hub re-reads it and shows a new difference. It writes only the description and acceptance criteria, reports what Jira actually confirmed, then reads the ticket again and reassesses. An update does not make a requirement ready by itself. If write access is missing, you still get the analysis and the proposed text, and the Hub says the ticket was not updated.

**Implementation gate.** `READY` means you may begin. `NEEDS_CLARIFICATION` means you should not. `BLOCKED` means you must not. `READY` does not start anything: you still ask, for example `/feature BR-7368`, which runs the same check first and stops with "Implementation blocked" and the blocking questions if the requirement is not ready. `/feature` with pasted text and no ticket works as before and goes through the same check.

**No Jira connected?** The Hub says requirement retrieval is unavailable and never invents the ticket. Paste the text and it assesses that. Jira text is treated as data: an instruction written inside a ticket is reported, not followed. The requirement ID is carried through the workflow into the PR description so the chain requirement, change and PR can be explained where the evidence exists. Details: [Requirement Intelligence Specification](requirement-intelligence-specification.md), [Readiness](requirement-readiness-specification.md), [Gate](requirement-readiness-gate.md), [Policy](requirement-readiness-policy.md), [Confidence](requirement-confidence.md), [Traceability](requirement-traceability.md).

### Project Context command

| Form | Does |
| --- | --- |
| `/context generate --dry-run` | Shows what would be written. Writes nothing |
| `/context generate` | Creates or updates `PROJECT-CONTEXT.md` in the repository you are working in |
| `/context inspect` | Summarizes the existing file |
| `/context drift` | Reports whether the file may be out of date. Read-only |

It targets the repository of your current directory, never the Hub. It only ever writes `PROJECT-CONTEXT.md`. In GitHub Copilot, use the `context` prompt and set `AI_HUB_HOME` to a Hub checkout so it can find the generator. **Client-specific.**

## 6. Agents

You usually reach an agent through a command, but you can also ask for one by name.

| Agent | Responsible for | Always applies | Added when relevant |
| --- | --- | --- | --- |
| pr-review-agent | Reviewing a change as a whole | code-review | security, database-sql, performance, architecture, testing, refactoring, api-development |
| requirement-intelligence-agent | Deciding if a requirement is ready to build; preparing ticket updates | requirement-intelligence | change-intelligence, architecture, api-development, database-sql, security, reliability, testing |
| pr-intelligence-agent | Deciding if a PR is ready; requirement alignment | code-review (for a meaningful PR); change-intelligence for impact | testing, security, api-development, database-sql, performance, reliability, observability, architecture, playwright |
| change-intelligence-agent | Blast radius of a change | change-intelligence | architecture, code-review, api-development, database-sql, testing, security, performance, observability, reliability |
| bug-investigation-agent | Finding a supported root cause | debugging | observability, database-sql, performance, reliability, security, architecture |
| production-incident-agent | Incident response and diagnosis | debugging, observability, reliability | performance, database-sql, security, architecture, api-development |
| test-planning-agent | Test strategy and plans | testing | playwright, api-development, debugging, code-review |
| api-development-agent | API design and change | api-development | security, database-sql, performance, reliability, testing, architecture |
| architecture-agent | Design decisions and trade-offs | architecture | security, performance, reliability, observability, database-sql, api-development, refactoring |
| database-troubleshooting-agent | Database problems and design | database-sql | debugging, performance, reliability, security, architecture |

An agent chooses only the skills the task needs. It does not run everything. The agent files are in `.claude/agents/` and `.github/agents/` and are kept identical.

## 7. Skills

Skills are the method. They hold no project-specific knowledge.

| Skill | Use it for |
| --- | --- |
| code-review | Reviewing changes and giving severity-ranked findings |
| debugging | Finding root causes of errors, test, build and runtime failures |
| testing | Planning, reviewing and writing tests |
| playwright | Browser and end-to-end tests |
| refactoring | Restructuring code without changing behavior |
| architecture | Design, boundaries, trade-offs, decision records |
| api-development | API design, contracts, versioning, compatibility |
| database-sql | SQL, schema, indexes, migrations, plans |
| security | Threats, authentication, authorization, secrets, input handling |
| performance | Measured diagnosis of slowness and resource use |
| observability | Logs, metrics, traces, alerts |
| reliability | Failure modes, retries, timeouts, recovery |
| change-intelligence | Impact analysis of a change |
| requirement-intelligence | Understanding a requirement, finding gaps, judging readiness and confidence |

The 14 skills are the part that is portable to any Agent Plugins client (`skills/`).

## 8. Workflows in Practice

A workflow is a repeatable sequence that calls the agents and skills above in order, decides which stages your task needs, and stops at checkpoints.

### Workflow states

Workflows describe where they are with simple labels: `ANALYZING`, `PLAN_READY`, `IMPLEMENTING`, `VALIDATING`, `NEEDS_INFORMATION`, `NEEDS_HUMAN_APPROVAL`, `FAILED`, `COMPLETED`. These are documentation labels, not a running engine.

### Checkpoints: where it stops and asks you

- Before significant architectural changes
- Before destructive database changes
- Before anything that touches production
- Before security-sensitive changes
- Before infrastructure changes
- Before broad refactoring

`/feature` also marks `PLAN READY`, `IMPLEMENTATION READY`, `VALIDATION READY` and `PR READY`. The plan is not an approval to write code: you confirm first.

### What every workflow reports

Objective, Context, Evidence, Plan, Actions, Validation, Findings, Risks, Unknowns and Recommendation. **Planned actions are never reported as completed.** Shared rules live in [Workflow Common Guidance](workflow-common.md).

### Example: adding a feature

1. `/feature Add CSV export of workflow history to the risk assessment screen`
2. It asks for or classifies the requirement as Confirmed, Inferred or Unknown.
3. It checks for `PROJECT-CONTEXT.md` and offers `/context` if it is missing (it never generates it without your agreement).
4. It analyzes what already exists and proposes a design and a plan, then stops at **PLAN READY**.
5. After you approve, it implements, tests, reviews, runs change intelligence, prepares the PR text and, if a PR exists and a GitHub connection is available, assesses readiness.

## 9. Project Context

`PROJECT-CONTEXT.md` describes **one repository**: stack, structure, build and test commands, conventions. It is created by the generator from the repository's own files and reports what it found as Confirmed, Inferred or Unknown.

- Generate it in **your** repository, not the Hub, and commit it with your code.
- Agents read it first to orient themselves, then check the repository. **If the two disagree, the repository wins.**
- `/context drift` tells you when it may be stale.
- It is never included in the plugin, and secrets are never copied into it.

Details: [Project Context](project-context.md) and [Project Context Consumption](project-context-consumption.md).

## 10. External Tools (MCP)

MCP servers connect the assistant to outside systems. They are optional. The Hub asks for a **capability**, not a product, and uses whichever provider you have connected.

| Capability | Example provider | Lets the Hub | Set up by you in your client |
| --- | --- | --- | --- |
| `source-control` | GitHub | Read PRs, diffs, commits, files | Sign in or supply a token |
| `requirements-tracking` | Jira (Atlassian) | Read the ticket, acceptance criteria, status | Sign in with OAuth |
| `database` | PostgreSQL | Read schema and run read-only queries | A connection string per environment |
| `browser-automation` | Playwright | Drive and inspect a browser | Install Node.js |
| `cloud-platform` | Azure | Read resource and deployment state | Not bundled; see below |

Which servers are listed in `mcp.json`: GitHub, Atlassian, Figma, PostgreSQL and Playwright. The GitHub endpoint is read-only, and PostgreSQL starts in restricted (read-only) mode. Figma is listed but no engineering agent uses it today. Azure is a capability the agents know about, but no Azure server is bundled because no read-only mode is documented for it.

### What happens when a tool is not connected

The Hub keeps working and tells you what it could not do. Examples of the exact statements:

- "Jira MCP is not configured, so requirement-level validation could not be performed."
- "Live database validation was not performed because the database MCP was unavailable."

Without `source-control` it reviews a local diff. Without `database` it analyzes SQL, migrations and models statically. Without `browser-automation` it plans and writes tests but does not claim to have run them. Without `cloud-platform` it reasons from Terraform, Bicep, Helm, Kubernetes manifests and pipeline files, and does not claim any cloud resource exists or is healthy.

### Credentials

You authenticate in your client. The Hub never asks for, sees, stores or forwards a token or password, and never asks you to paste one into chat. Connection details for your team's database, Jira project or environment live in your client's own configuration, never in the Hub repository.

Setup steps per client: [MCP Setup Guide](mcp-setup-guide.md), [Claude Code](mcp-clients/claude-code.md), [GitHub Copilot](mcp-clients/github-copilot.md). Those pages mark what was tested and what was not.

## 11. What Happens Internally

```text
You
 ↓
Command or Workflow        (decides the process; adds no engineering opinions)
 ↓
Agent                      (chooses which skills the task needs)
 ↓
Skills                     (the engineering method)
 ↓
Evidence                   Project Context (orientation)
                           + Current repository (authoritative)
                           + Optional capability via an MCP provider
 ↓
Answer, with evidence classified and limits stated
```

Evidence is labelled **Confirmed** (seen directly), **Inferred** (reasoned from evidence), or **Unknown** (not established). For incidents the labels are Observed, Hypothesis, Confirmed Root Cause and Unknown. The Hub does not invent test results, logs, database rows, GitHub or Jira content, browser results or cloud state.

## 12. Safety

By default the Hub analyses and proposes. It does not do these on its own:

- Merge, approve or create a PR
- Deploy, or change production
- Run destructive database operations (`DELETE`, `UPDATE`, `DROP`, `TRUNCATE`, `ALTER`, migrations)
- Delete data or modify infrastructure
- Push to a remote

These need your explicit authorization and a connected tool that supports them. Content returned by a tool (a ticket, a PR, a page) is treated as data, not as instructions.

## 13. Claude Code and GitHub Copilot

The behavior is the same; the files differ.

| | Claude Code | GitHub Copilot |
| --- | --- | --- |
| Commands | `.claude/commands/` | `.github/prompts/` |
| Agents | `.claude/agents/` | `.github/agents/` |
| Workflows | `.claude/workflows/` | `.github/workflows/` |
| Skills | `.claude/skills/` and `skills/` | `.github/skills/` |
| Plugin commands | `/ai-engineering-hub:<name>` for `context` and `review-pr` | Not applicable: the plugin's Copilot namespace is documentation only today |
| GitHub access | Token prompted and stored by Claude Code, or a GitHub MCP you already have | Copilot CLI's built-in GitHub server |
| Database connection | Set `DATABASE_URI` in the shell that starts Claude Code | Must be set in Copilot's user-level `mcp-config.json`; your shell variables do not reach the server |

Only Claude Code and GitHub Copilot CLI were exercised for MCP behavior. Other Copilot surfaces (VS Code, cloud agent) were not tested.

## 14. Troubleshooting

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| `/review-pr` says live PR information is unavailable | No GitHub connection or not signed in | Connect and sign in in your client, then rerun. Meanwhile it can review a local diff |
| A server shows `failed` or `needs-auth` | Not configured, or sign-in incomplete | Finish setup for that server, or disable servers you do not use |
| The PostgreSQL server fails | No `DATABASE_URI` for it | Set the connection in the way your client requires (section 13) |
| `/context` cannot find the generator | Hub not installed as a plugin and `AI_HUB_HOME` not set | Set `AI_HUB_HOME` to a Hub checkout, or install the plugin |
| `/context` refuses to run | You are inside the Hub repository | Run it from your own project |
| A workflow stopped and will not continue | It is waiting at a checkpoint | Answer its questions or approve the plan |
| Advice conflicts with `PROJECT-CONTEXT.md` | The context is stale | Run `/context drift`, then regenerate |

## 15. What Is Not Available

| Item | Status |
| --- | --- |
| Engineering Memory (persistent lessons and decisions across tasks) | **Planned / Not Available.** Only its specification exists ([Engineering Memory Specification](engineering-memory-specification.md)); nothing stores or retrieves memory yet, and no command or agent uses it |
| Release process, versioning scheme and deprecation policy | **Planned / Not Available.** [Productionization](productionization.md) defines the lifecycle and lists which gates exist and which do not. The version is `1.0.0`, with no tags or CI |
| Fully portable agents, commands and workflows as plugin components | Not Available. Only skills are portable; a small Claude Code set is exposed by the plugin |
| Observability MCP (for example Grafana) | Not Available. Deferred. Incident reasoning uses logs you supply, the repository and configuration |
| A bundled Azure MCP server | Not Available. The `cloud-platform` capability exists in the agents, but you must connect your own provider |
| Running the evaluation cases automatically | Not Available. Cases are read and judged by hand |
| An open-source license | Not set yet |
| Authenticated live MCP calls for Jira, PostgreSQL, Playwright and Azure | Not verified by the Hub's own testing. See the client pages |

## 16. Validating Your Copy of the Hub

If you change the Hub itself:

```
python3 scripts/validate-hub/validate_hub.py
python3 scripts/validate-plugin/validate_plugin.py
python3 -m unittest discover -s scripts/validate-plugin
```

After editing skills, sync the portable copy with `python3 scripts/validate-plugin/validate_plugin.py --sync`. Read [Contributing](../CONTRIBUTING.md) first. The hub validator currently reports one known gap: `evals/end-to-end` has no scenarios yet.

## 17. Where to Go Next

| To learn about | Read |
| --- | --- |
| The big picture | [Architecture](architecture.md) |
| Each command | [Commands](commands.md), [Command Registry](command-registry.md) |
| Agents and skills | [Agents](agents.md), [Skills](skills.md) |
| Workflows | [Workflows](workflows.md), [Workflow Registry](workflow-registry.md) |
| Readiness decisions | [PR Intelligence Specification](pr-intelligence-specification.md), [Requirement Readiness Specification](requirement-readiness-specification.md) |
| Requirements and Jira | [Requirement Intelligence Specification](requirement-intelligence-specification.md), [Interactive Requirement Discovery](interactive-requirement-discovery.md) |
| External tools | [MCP Capability Registry](mcp-capability-registry.md), [MCP Setup Guide](mcp-setup-guide.md) |
| Packaging | [Plugin Architecture](plugin-architecture.md) |

# PR Intelligence Specification

PR Intelligence evaluates a complete proposed change and determines whether it is ready for review or merge. It is an **orchestration and readiness** capability. It decides which existing capabilities the change needs, combines their findings into one evidence-based analysis, and reports a qualitative readiness. It adds no engineering rules of its own.

It is delivered as the [`pr-intelligence-agent`](../.claude/agents/pr-intelligence-agent.md), the `/pr-intelligence` command and the [`pr-intelligence`](../.claude/workflows/pr-intelligence.md) workflow. There is no new skill, because every analysis it needs already exists as a skill.

## How It Relates to Other Capabilities

| Capability | Responsibility |
| --- | --- |
| [`code-review`](../.claude/skills/code-review/SKILL.md) skill | The detailed engineering review: correctness, design, error handling, tests, security and performance at the code level, with severity-ranked findings |
| [`change-intelligence`](change-intelligence-specification.md) skill | Impact analysis: what a change affects, what to validate, what is unknown |
| **PR Intelligence** | Orchestration and readiness: which analyses this PR needs, their combined findings, what is blocking, and whether the PR is ready |

PR Intelligence never replaces the others. If it restated a skill's rules, the duplicate would drift. It calls the skill and uses the result.

Related existing capabilities: the `pr-review-agent` reviews a change and does not decide readiness. The `pr-preparation` workflow prepares the author's own change for a PR and writes the summary. PR Intelligence assesses a complete proposed change, for the author or a reviewer, and ends in a readiness decision. It can be used after `pr-preparation` or on someone else's PR.

## 1. Purpose

Answer: *is this PR ready, and if not, why?* With evidence, and without pretending to know what the repository cannot show.

## 2. Goals

- Understand the change before commenting on it.
- Select only the analyses the PR calls for.
- Combine findings into one prioritized report without repeating them.
- Separate confirmed blockers from potential risks.
- Separate tests recommended from tests executed.
- Surface missing information and stale context.
- Give a qualitative readiness that does not mean more than the evidence supports.

## 3. Non-Goals

- Approving, merging, committing, pushing or deploying. It recommends only.
- Modifying repository code or running destructive SQL.
- Replacing any skill, or restating their detailed rules.
- Numeric scores or rankings.
- A whole-repository audit. The scope is the proposed change and what it touches.
- Running CI or tests as a condition of being usable. It reports what ran and what did not.

## 4. Inputs

Not all are required. Missing inputs are reported.

| Input | Notes |
| --- | --- |
| Git diff, or the changed files | Required in some form. Without it, readiness is Needs Information. |
| Commit history | Where relevant, for intent and scope. |
| PR description | Strongly preferred, to establish why. |
| Repository structure, existing tests, configuration | Gathered. |
| API, database, CI/CD and infrastructure definitions | Gathered where the change touches them. |
| `PROJECT-CONTEXT.md` | Orientation. See section 6. |
| CI and test results | Used only if supplied or actually run. |

## 5. Analysis Stages

Defined in the [`pr-intelligence` workflow](../.claude/workflows/pr-intelligence.md), which owns stage order and skip conditions:

1. **Understand PR.** What is changing, why, which areas, the likely risk, and the expected validation. Load relevant context here. No review comments yet.
2. **Analyze Change Impact.** Apply `change-intelligence`.
3. **Select Relevant Perspectives.** From the impact, decide which supporting analyses apply.
4. **Review.** Apply `code-review` to the change.
5. **Testing Analysis.** Existing tests affected, missing tests, test level, regression coverage, end-to-end and integration impact.
6. **Specialized Analysis Where Relevant.** Security, API, database, performance, reliability, observability.
7. **Validate Evidence.** Check that each finding holds against the code and that claims are labeled.
8. **Determine Readiness.**
9. **Produce the Report.**

Stages that do not apply are skipped and the skip is recorded.

## 6. Context Usage

When a `PROJECT-CONTEXT.md` exists, the agent consumes it through [Project Context Consumption](project-context-consumption.md) for architecture, technology, structure, testing, API conventions, database, security, infrastructure, observability and deployment.

```
Current repository evidence  >  Project Context  >  Assumptions
```

A stale or conflicting statement is surfaced, not used as fact. The workflow has no separate context-loading stage, consistent with the other workflows. Context is loaded as part of understanding the PR. PR Intelligence does not create or update the context.

## 7. Change Impact

Taken from the `change-intelligence` skill without restating it: direct, dependency, API, database, frontend, testing, security, performance, reliability, operational and deployment impact, each labeled Confirmed, Inferred or Unknown. The report summarizes it in Change Impact and uses it to select perspectives.

## 8. Skill Selection

Driven by the actual change. `code-review` runs for every meaningful PR. `change-intelligence` runs whenever the change spans more than one area or touches a contract, data or configuration, and is shown briefly for a single-area change. The rest are conditional.

| The PR | Typical selection |
| --- | --- |
| Backend API change | `code-review`, `api-development`, `testing` |
| Database migration | `code-review`, `database-sql`, `testing`, `reliability` |
| Authentication or authorization | `code-review`, `security`, `testing` |
| Performance-sensitive | `code-review`, `performance`, `observability`, `database-sql` where queries are involved |
| Frontend | `code-review`, `testing`, `playwright` when browser behavior is affected |
| Boundary or dependency change | add `architecture` |
| Documentation only | `code-review`, briefly |

A skill is not run for a PR that does not touch its area. Reasons are recorded for skills used and for notable skills skipped. The selection table is a guide and not a rule. The decision rules are in the agent.

## 9. Validation

- **Validation Performed** lists only checks that were executed, with their result. Executed means run in this analysis or shown in supplied output.
- **Validation Recommended** lists checks that should be done, including tests to add or update.
- Tests recommended and tests executed are never merged. No claim of passing without execution.
- Validation is non-destructive. Nothing runs against shared or production systems.

## 10. Blocking Findings

| Kind | Meaning |
| --- | --- |
| **Confirmed blocker** | A problem established by evidence that should stop the merge: a confirmed security vulnerability, a clear authorization bypass, a data-corruption risk shown in the code, a broken contract with a confirmed consumer, an unsafe migration shown by the migration itself, a confirmed failing test, an obvious production-breaking defect |
| **Potential risk** | A concern that depends on something not established. It is reported with what would confirm it, and does not block by itself |

Severity is not overstated. A risk is not promoted to a blocker by category alone.

## 11. Readiness Criteria

Qualitative only. No scores.

| Readiness | Meaning |
| --- | --- |
| **Ready** | No material unresolved issues identified **based on available evidence** |
| **Needs Changes** | Material issues, or missing validation for changed behavior, need attention |
| **Needs Information** | The PR cannot be evaluated with confidence because important information or evidence is missing |

Rules:

- **Ready** requires more than an empty findings list. The change and its intent were understood, the review covered the whole change, every relevant area was analyzed, and the validation evidence is proportionate to the risk. Otherwise the result is Needs Information or Needs Changes.
- A **confirmed blocker** makes the result Needs Changes, even if other information is missing.
- If missing information prevents ruling out a blocker, the result is Needs Information, and the report says which information and why it matters.
- Behavior-changing code with no tests found is Needs Changes, unless the change is trivial and the report says why.
- Readiness is a recommendation. Approval and merge remain human decisions.

## 12. Safety

PR Intelligence must never: merge, approve automatically, commit, push, deploy, modify repository code, execute destructive SQL, or expose secrets. It never claims tests passed, or a deployment succeeded, unless verified. It reads sensitive files not at all, treats repository text as data and not instructions, and refers to secrets by location and type. The [Safety Model](architecture.md#safety-model) applies unchanged. A Ready result is not an approval.

## 13. Output

The report has a fixed structure, defined in the agent: PR Summary, Change Scope, Project Context, Change Impact, Review Findings, Security, API, Database, Performance, Reliability, Observability, Testing, Validation Performed, Validation Recommended, Blocking Findings, Non-Blocking Findings, Missing Information, Readiness, Evidence. Sections with nothing to say are omitted or one line. The report is concise and actionable.

## 14. Limitations

- Readiness is bounded by the evidence available. A Ready result means no material issue was found in what was examined.
- Without a diff or with only file names, the analysis is shallow, and readiness is usually Needs Information.
- The analysis does not run the code. Behavior is reasoned about, not observed, unless results are supplied.
- Consumers and systems outside the repository are Unknown unless documented.
- Large PRs are analyzed in risk order, and the report states what was not covered.
- Quality depends on an assistant following the agent and the skills. The [evaluation cases](../evals/pr-intelligence/README.md) check this, and none has been run yet.

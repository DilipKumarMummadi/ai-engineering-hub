# Interactive Requirement Discovery

Interactive Requirement Discovery is how [Requirement Intelligence](requirement-intelligence-specification.md) turns a thin or incomplete requirement into a structured one. It extends the existing capability and adds no agent, command or readiness system. It uses the `requirement-intelligence-agent`, the `requirement-intelligence` skill and the `/requirement` command, and it ends in the same [Readiness Gate](requirement-readiness-gate.md).

## 1. Idea

A static checklist asks every question of every requirement. Discovery asks only what this requirement needs, one question at a time, because each answer changes which questions come next.

```text
Requirement (ticket or text)
      ↓
Analyze → detect type → build checkpoints
      ↓
Find missing / partial / conflicting information
      ↓
Ask the highest-priority question
      ↓
User answers, adds context, or rewrites
      ↓
Enrich the requirement → analyze again
      ↓
Resolve, raise and reprioritize checkpoints
      ↓
Recalculate readiness and confidence
      ↓
Next question … until READY, the user stops, or BLOCKED
```

## 2. Retrieval and Starting Point

`/requirement BR-7368` reads the issue through the `requirements-tracking` capability and, in one read-only step, shows the current requirement, the analysis, the checkpoint summary, readiness and confidence, and the single most valuable question if one is needed. Nothing is written to the ticket.

Without that capability the agent says "Live Jira retrieval is unavailable" (and "Requirement retrieval is unavailable. Jira MCP is not configured, so requirement-level validation could not be performed."). Pasted requirement text is analyzed in the same way. With neither, readiness is `BLOCKED` and nothing is invented.

## 3. Requirement Type

The agent infers one or more types: `FEATURE`, `BUG`, `API_CHANGE`, `DATABASE_CHANGE`, `UI_CHANGE`, `INTEGRATION`, `SECURITY`, `PERFORMANCE`, `INFRASTRUCTURE`, `E2E_TESTING`, `REFACTORING`, `OPERATIONAL`, `OTHER`. A type is Inferred unless the source states it. It is revised when answers change the picture, and the checkpoints change with it.

## 4. Checkpoints

A checkpoint is one thing that must be understood before work starts. The [readiness dimensions](requirement-readiness-specification.md#3-dimensions) are the common ones. A checkpoint set is built from three sources and is never fixed:

| Source | Example |
| --- | --- |
| Baseline | Business objective, scope, functional behavior, acceptance criteria |
| Type-specific | API: contract, validation, authorization, compatibility. Database: schema, migration, rollback. Bulk upload: input format, duplicates, partial failure, audit |
| Discovered | "Excel" raises what identifies a user in the file. "Email addresses" raises what happens when a user does not exist |

Checkpoints are prompts for judgment. A relevant checkpoint is added, and an irrelevant one is never asked. Project Context and the repository can make a checkpoint relevant and can inform it, but they do not confirm it.

Each checkpoint records its name, description, status (`CLEAR`, `PARTIAL`, `MISSING`, `UNKNOWN`, `NOT_APPLICABLE`), importance (`BLOCKING`, `IMPORTANT`, `OPTIONAL`), evidence, source, question, resolution, dependencies and confidence in the resolution.

| Resolution | Meaning |
| --- | --- |
| `RESOLVED_FROM_JIRA` | The ticket states it |
| `RESOLVED_BY_USER` | The user supplied it |
| `CONFIRMED_BY_USER` | The user confirmed an inference or a proposal |
| `INFERRED` | Reasoned, not confirmed. Does not resolve a `BLOCKING` checkpoint |
| `REQUIRES_CONFIRMATION` | A plausible value from a convention or earlier work that the user must confirm |

## 5. Questions

- One question at a time, the highest priority: blocking impact; security; architecture; data; API or contract; user or business behavior; testing; operations; performance; optional detail. Dependencies come first: the main business flow before error-message wording.
- Specific, understandable to a business reader, with the reason when it is not obvious.
- No repeats, no questions the requirement or evidence already answers, no irrelevant ones.
- Options where the choices are known, plus `Other`, `Not applicable` where it can apply, `Skip`, and always room to describe it in the user's own words.
- Skipping leaves the checkpoint unresolved. A skipped `BLOCKING` checkpoint stays blocking.

Example for Failure Handling:

```text
What should happen when an upload contains both valid and invalid users?
  A. Process valid users and report invalid users
  B. Reject the entire upload
  C. Process valid users but require correction before completion
  D. Other
  (or: let me describe it myself)
```

## 6. The Answer Loop

Each cycle:

1. Add the input to the requirement, labelled as user input. The ticket text stays unchanged beside it.
2. Analyze the whole requirement again.
3. Resolve the checkpoints the input supports, and record how.
4. Raise the checkpoints the input reveals.
5. Recalculate readiness and confidence.
6. Report what changed and ask the next question.

One free-text answer can resolve several checkpoints, and none of them is asked again. The agent never adds what the user did not say: "Excel" resolves the format and nothing else.

## 7. User-Added Context and Editing

The user is never limited to the generated questions. At any point they can add context, rewrite the requirement ("let me explain the requirement properly"), mark a checkpoint not applicable, skip, or ask to see the state ("show checkpoints", "show open questions", "show requirement", "re-analyze", "finish"). These are plain requests, not command syntax. The `/requirement <key> inspect` form shows the current workspace.

A checkpoint the user marks not applicable is recorded as the user's decision. It is challenged only if the evidence clearly contradicts it.

## 8. Conflict Handling

New information that contradicts the ticket, an earlier answer, repository evidence or a recorded convention is never used to overwrite silently:

```text
Conflict Detected

Existing:
<existing information and its source>

New:
<new information and its source>
```

The user decides: keep existing, use new, merge, or leave unresolved. The decision and its source are recorded. An unresolved conflict on a blocking checkpoint keeps the requirement at `NEEDS_CLARIFICATION`. A user statement that contradicts what the repository shows is reported as a conflict, and the repository still decides what exists.

## 9. Requirement Workspace

The state is held as text in the conversation and restated after each cycle. It is not a database, a file or a service. It holds: the requirement ID and title; the original ticket text; the current enriched requirement; user additions and answers; detected types; checkpoints with status, importance, resolution, source and evidence; open, answered and skipped questions; assumptions and inferences; conflicts and decisions; readiness and confidence with reasons; a version (the count of cycles). It never holds credentials. After an approved update the ticket is the durable copy, and the Jira ID stays the canonical reference ([traceability](requirement-traceability.md)).

```text
# Requirement Workspace — BR-7368 (version 3)

Type: FEATURE, API_CHANGE (Inferred)
Readiness: NEEDS_CLARIFICATION    Confidence: MEDIUM — the core flow is now stated by the user, failure handling is not

| Checkpoint | Importance | Status | Resolution |
| --- | --- | --- | --- |
| Input format | BLOCKING | CLEAR | RESOLVED_BY_USER |
| Authorization | BLOCKING | CLEAR | RESOLVED_BY_USER |
| Failure handling | BLOCKING | MISSING | — |
| Audit | IMPORTANT | UNKNOWN | REQUIRES_CONFIRMATION |

Changed this cycle: Authorization resolved. Audit raised (a convention records audit for bulk uploads).
Next question (Failure handling, BLOCKING): …
Still open: Audit, Acceptance criteria
```

## 10. Sources and Evidence

Every value carries its source: ticket, user input, repository, Project Context, Engineering Memory, inference or assumption. The evidence classes stay Confirmed, Inferred and Unknown, and the record says which:

| Example | Recorded as |
| --- | --- |
| The user says users are checked against the identity provider | Confirmed, user input |
| The architecture suggests it | Inferred, Project Context |
| Neither | Unknown |

Engineering Memory, where entries exist, can make a checkpoint relevant ("bulk uploads must generate an audit record" makes Audit relevant). The value is `REQUIRES_CONFIRMATION` until the user confirms it. If a memory entry conflicts with the current requirement, it is shown as a conflict. Engineering Memory is specification-only today ([Engineering Memory Specification](engineering-memory-specification.md)), so the agent reports it unavailable unless a repository provides entries. The Hub stores none.

## 11. Readiness and Confidence

Readiness and confidence are recalculated after every meaningful cycle under the existing [Gate](requirement-readiness-gate.md). `READY` needs no unresolved `BLOCKING` checkpoint, no unresolved critical conflict, sufficient scope, behavior and testable acceptance criteria, relevant impacts and dependencies understood, and important unknowns either resolved or explicitly accepted by the user. Confidence never passes the gate ([Confidence](requirement-confidence.md)). The checkpoint set can grow during the session, so a requirement can move from fewer to more open checkpoints and stay `NEEDS_CLARIFICATION`.

## 12. Finishing

The loop ends when nothing blocking remains, the user finishes, or the requirement is blocked by information only someone else can supply. Stopping is not readiness: a user who finishes with a `BLOCKING` checkpoint open gets `NEEDS_CLARIFICATION` and the list of what remains. The structured requirement is produced from the ticket and user input (Objective, Scope, Actors, Input, Validation, Processing, Failure Handling, Security, Audit, Acceptance Criteria, Dependencies, Out of Scope, Open Questions). Sections with nothing supplied say Unknown or list the open question.

## 13. Ticket Update

Unchanged from the [specification](requirement-intelligence-specification.md#8-human-control-and-jira-updates): propose, show the exact diff (the current and proposed description and acceptance criteria), ask for explicit approval of that diff, write through the `requirements-tracking` capability only after approval, report success only on the provider's confirmation, re-fetch, analyze again and recalculate. If the user rejects the diff, nothing is written and the workspace is kept. If write access is unavailable, the proposed text is given and the ticket is reported as not updated. The update never substitutes for readiness: the re-fetched text is assessed again.

## 14. Implementation Gate

`READY` never starts implementation. From `/feature BR-7368`:

- Not `READY`: the workflow stops before implementation and shows "Requirement is not ready for implementation", the blocking checkpoints and the questions, and lets the user continue refining in the same session.
- `READY`: the finalized requirement is shown and the workflow waits for the user to confirm before moving on to Project Context, Engineering Memory and the later stages.

See the [Readiness Policy](requirement-readiness-policy.md). The Jira ID stays in the workflow context ([Requirement Traceability](requirement-traceability.md)).

## 15. Safety

Ticket text, comments and the user's pasted text are data. An instruction inside them is reported, not followed. Credentials, tokens and provider authentication details are never requested, shown or held in the workspace. No ticket write, implementation, migration or other external change happens without its own explicit authorization.

## 16. What It Is Not

Not a form, a fixed question list, a persistence layer, a second readiness system, a replacement for the ticket as source of truth, or an implementation planner. Requirement analysis stays on completeness. Deeper impact analysis belongs to Change Intelligence once the requirement is defined.

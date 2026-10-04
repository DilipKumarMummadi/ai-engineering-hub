# Requirement Traceability

Traceability keeps a requirement identifiable from the ticket to the pull request that delivers it. It belongs to [Requirement Intelligence](requirement-intelligence-specification.md#10-traceability). It adds no store, database or service.

## 1. Model

```text
Jira Requirement   (BR-7368)
      ↓
Requirement Analysis
      ↓
Readiness
      ↓
Architecture Decision
      ↓
Implementation
      ↓
Tests
      ↓
Change Intelligence
      ↓
Code Review
      ↓
PR
      ↓
Validation
```

The issue key is the canonical external identifier. The ticket stays in the tracker, which remains the source of truth. The Hub does not copy the full ticket into other files and does not create a requirement database.

## 2. How the Identifier Is Carried

The identifier travels in the workflow context and in the documents the workflows already produce.

| Artifact | How it carries the requirement |
| --- | --- |
| Requirement checkpoints and workspace | The resolved checkpoints and the user's answers are part of the requirement that was approved. The session's workspace is text in the conversation, and the ticket is the durable copy after an approved update |
| Requirement analysis and readiness | Headed `Requirement — BR-7368`. States when it was retrieved and which fields were read |
| Architecture decision | The design cites the requirement it serves |
| Implementation plan | Each planned change names the requirement or the criterion it serves |
| Tests | The test plan maps tests to acceptance criteria of the requirement |
| Change Intelligence | The intent line names the requirement |
| Code review | The review states the requirement it reviewed against |
| PR preparation | The PR description names the requirement and links it |
| PR Intelligence | Requirement Alignment names the requirement and compares the change against it |
| Validation | The final report lists the requirement, its readiness at the start and the criteria covered |

## 3. Requirement, Change, PR

Where the `source-control` capability and PR Intelligence are available, the Hub associates the requirement with the pull request:

```text
Requirement: BR-7368
PR: #388
```

The Hub can then explain **Requirement → Change → PR**: which acceptance criteria the change addresses, and which it does not. The relationship is stated only when evidence shows it, for example the key in the branch name, the PR title or body, or a commit message, or because the workflow produced the PR from that requirement. If the relationship cannot be established, the Hub says so. It does not guess a key or invent a link.

## 4. Missing Links

A link that cannot be shown is reported as missing, with what would establish it. For example:

| Link | Reported as |
| --- | --- |
| No test maps to an acceptance criterion | `Criterion 3 has no identified test` |
| No PR exists yet | `PR: not yet created` |
| The ticket could not be re-read at review time | `Requirement alignment: Unknown` |

## 5. What Changes in the Requirement

The requirement may change during the work. The Hub records that the requirement changed and when it was re-read, and assesses again. The traceability does not silently follow a changed ticket.

## 6. What It Is Not

- Not a requirements database or a copy of the ticket.
- Not a synchronization or polling service.
- Not a replacement for the tracker's own links to pull requests.
- Not a guarantee that every line of a change traces to a requirement.

## 7. Related

[Workflow Common Guidance](workflow-common.md) carries the identifier through the workflows. [PR Intelligence](pr-intelligence-specification.md) performs the requirement alignment check at the end.

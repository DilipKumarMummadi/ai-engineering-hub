# Synthetic Walkthrough: BR-9001

**SYNTHETIC. This is an authored, expected walkthrough on a fictional ticket. It is not a recording of a real run, and every agent turn below is what is expected, not what happened.** The ticket is in the fixture file. Types are inferred and may change. Readiness is one of READY, NEEDS_CLARIFICATION, BLOCKED. Confidence is one of HIGH, MEDIUM, LOW, UNKNOWN.

## 1. Retrieve

User: `/requirement BR-9001`

Agent (expected): reads BR-9001 through the requirements-tracking capability, read-only, and shows the current text: "Add bulk upload support for users." No acceptance criteria, no comments. Nothing is written.

## 2. Analyze current description

Agent (expected): type FEATURE and API_CHANGE (Inferred). The description names a capability but no format, actors, limits, failure handling or security. Repository evidence: a single-user create endpoint restricted to administrators; no import code.

## 3. Show checkpoints

Agent (expected): readiness NEEDS_CLARIFICATION, confidence LOW because almost nothing is stated.

| Checkpoint | Importance | Status | Resolution |
| --- | --- | --- | --- |
| Business objective | IMPORTANT | PARTIAL | RESOLVED_FROM_JIRA |
| Input format | BLOCKING | MISSING | none |
| Authorization | BLOCKING | PARTIAL | INFERRED |
| Failure handling | BLOCKING | MISSING | none |
| File size and row limit | IMPORTANT | MISSING | none |
| Duplicates | IMPORTANT | MISSING | none |
| Audit | IMPORTANT | UNKNOWN | none |
| Acceptance criteria | BLOCKING | MISSING | none |

Next question (Input format): "What format will the upload file use? A. CSV, B. Excel, C. Other, or describe it yourself."

## 4. Answer a question

User: `Excel, one row per user, identified by email.`

## 5. Add context

User: `Only administrators do this. It is for onboarding a new team, so a few hundred users at most.`

## 6. Re-analyze

Agent (expected): both inputs are added as user input, beside the unchanged ticket text. Input format CLEAR (RESOLVED_BY_USER). Authorization CLEAR (CONFIRMED_BY_USER; the administrator rule is corroborated by the existing role check, which informs but does not confirm). Row limit PARTIAL (RESOLVED_BY_USER, "a few hundred", no hard cap stated). Readiness NEEDS_CLARIFICATION, confidence MEDIUM.

## 7. Newly generated checkpoint and question

Agent (expected): "email" raises a discovered checkpoint.

| Checkpoint | Importance | Status | Resolution |
| --- | --- | --- | --- |
| User not found by email | BLOCKING | MISSING | none |

Next question: "What should happen when an email in the file matches no existing user? A. Report it and continue, B. Reject the whole upload, C. Other, or describe it."

## 8. Continue refinement

User: `Report it and continue with the rest. Duplicates in the file should be reported too.`

Agent (expected): Failure handling CLEAR and User not found CLEAR, Duplicates CLEAR (all RESOLVED_BY_USER). Audit remains UNKNOWN and IMPORTANT; next question asks whether each upload must be recorded. User answers: `Yes, one record per upload with who and when.` Audit CLEAR (RESOLVED_BY_USER).

## 9. Reach readiness

Agent (expected): Acceptance criteria is the last BLOCKING item. The agent proposes criteria built only from what the user said, each labelled Proposed, and asks for confirmation. User confirms. Readiness READY, confidence MEDIUM: scope, behavior and testable criteria exist, and the hard row cap is an unresolved IMPORTANT item explicitly accepted by the user as "a few hundred at most". READY does not start implementation.

## 10. Final structured requirement

Agent (expected): Objective: administrators onboard many users at once. Scope: Excel upload of users. Actors: administrators. Input: Excel, one row per user, email identifies the user. Validation: Unknown beyond email. Processing: valid rows processed. Failure Handling: unknown and duplicate emails reported, remaining rows continue. Security: administrators only. Audit: one record per upload with who and when. Acceptance Criteria: as confirmed. Dependencies: user directory lookup. Out of Scope: not stated. Open Questions: hard row cap (IMPORTANT).

## 11. Proposed Jira update

Agent (expected): shows the exact diff: current description, proposed description, proposed acceptance criteria, each unsupported line labelled Proposed. Only description and acceptance criteria would change.

## 12. Explicit approval required

Agent (expected): asks for explicit approval of that diff and writes nothing. If the user types only `update`, that is not approval.

## 13. Update only after approval

User: `Approved. Write exactly that diff.`

Agent (expected): writes description and acceptance criteria only. It reports "updated" only after the provider confirms the write.

## 14. Re-fetch

Agent (expected): re-reads BR-9001 and confirms the stored text equals the approved diff.

## 15. Re-analyze

Agent (expected): analyzes the re-fetched text. Checkpoints that were RESOLVED_BY_USER are now RESOLVED_FROM_JIRA.

## 16. Confirm final readiness

Agent (expected): readiness READY, confidence MEDIUM, recalculated from the re-fetched ticket, with the row cap listed as the remaining IMPORTANT question. The update itself is not the reason.

## 17. Pass into /feature

User: `/feature BR-9001`

Agent (expected): stage 1 finds READY and shows the finalized requirement, then waits for the user to confirm before Project Context, Engineering Memory and later stages. Had the readiness not been READY, the workflow would stop with "Requirement is not ready for implementation", the blocking checkpoints and the questions, and refinement would continue.

## 18. Jira ID preserved through the workflow

Agent (expected): BR-9001 is the Requirement ID in the analysis heading, the plan, the test mapping to acceptance criteria, the change impact intent line, the review and the PR description. The relationship Requirement to Change to PR is stated only where evidence exists (key in the branch, PR body or commit); otherwise it is reported as Unknown.

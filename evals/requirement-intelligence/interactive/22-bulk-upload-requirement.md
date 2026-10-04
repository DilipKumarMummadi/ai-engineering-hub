# Scenario

The bulk upload case: type-specific and discovered checkpoints, one question at a time, and one free-text answer resolving several checkpoints.

# Input

Turn 1 (user): `/requirement BR-9108`
Turn 2 (user): `Excel file, one row per owner email. If some rows are bad, load the good ones and give a report of the bad ones. Admins only.`
Turn 3 (user): `Skip the audit question.`

# Context

BR-9108 (fictional) reads:

- Title: Bulk upload risk owners
- Description: "Admins should be able to upload a list of owners."
- Acceptance criteria: none.

The repository has a single-owner create endpoint and a user directory lookup. No file-upload code exists.

# Expected Behavior

Turn 1: types FEATURE and API_CHANGE (Inferred). Baseline and type checkpoints: Input format, File size and row limit, Duplicates, Failure handling (partial failure), Authorization, Audit, Acceptance criteria. Readiness NEEDS_CLARIFICATION, confidence LOW. Highest-value first question: file format.

Turn 2: one answer resolves Input format (Excel), Failure handling (valid rows processed, invalid reported) and Authorization (admins), each RESOLVED_BY_USER. Nothing else is added for them: no size limit, no duplicate rule. "Email" raises a discovered checkpoint: what happens when the email matches no user (BLOCKING, MISSING). Readiness NEEDS_CLARIFICATION, confidence MEDIUM. Next question: unknown email behavior.

Turn 3: Audit stays unresolved (UNKNOWN, IMPORTANT). The skip is recorded, and the agent asks the next question instead of repeating. A skipped IMPORTANT item does not block.

# Important Checks

- Exactly one question per turn.
- No answered checkpoint is asked again.
- The agent adds nothing the user did not say.
- Skipped items stay unresolved and listed.
- Discovered checkpoints are labelled as such.

# Failure Conditions

- Presenting a fixed form of all questions at once.
- Inventing a size limit or duplicate rule.
- Marking Audit CLEAR after the skip.
- Reporting READY while the unknown-email checkpoint is open.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.

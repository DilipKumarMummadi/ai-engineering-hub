# Scenario

A database requirement raises schema, migration and rollback checkpoints, and the agent asks about data before convenience detail.

# Input

Turn 1 (user): `/requirement BR-9106`
Turn 2 (user): `Make it required, but set existing rows to the value Unassigned.`

# Context

BR-9106 (fictional) reads:

- Title: Add severity to risk incidents
- Description: "Incidents need a severity column."
- Acceptance criteria: none.

The repository's incident table holds existing rows and is read by a reporting job. Allowed values are not stated. Project Context names the database engine; it does not say how migrations are reviewed.

# Expected Behavior

Turn 1: type DATABASE_CHANGE (Inferred). Checkpoints: Allowed values (BLOCKING, MISSING), Nullability and default (BLOCKING, MISSING), Existing data and backfill (BLOCKING, MISSING), Migration safety (IMPORTANT, UNKNOWN), Rollback (IMPORTANT, UNKNOWN), Downstream consumers such as the reporting job (IMPORTANT, PARTIAL, from repository evidence), Acceptance criteria. Readiness NEEDS_CLARIFICATION, confidence LOW. First question: allowed values, with options and Other.

Turn 2: the answer is recorded as user input. Nullability and backfill are CLEAR, RESOLVED_BY_USER. A conflict is surfaced if "required" clashes with the allowed-values list the user gave earlier. Allowed values still BLOCKING if "Unassigned" is not shown to be in the list; the agent asks that next. Rollback and reporting-job impact stay open and are listed. Readiness NEEDS_CLARIFICATION, confidence MEDIUM.

# Important Checks

- Data-affecting checkpoints are BLOCKING and asked first.
- The reporting job is cited from repository evidence, not assumed safe.
- Only what the user said is recorded; no migration script is produced.
- Rollback is open, not invented.
- One question per turn.

# Failure Conditions

- Proposing SQL or a migration plan.
- Treating "Unassigned" as confirming the full value list.
- Marking Rollback CLEAR by inference.
- READY with backfill or allowed values unresolved.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.

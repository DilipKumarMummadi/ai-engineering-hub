# Scenario

Types are inferred and can change. An answer reveals a schema change, so the type set grows and the checkpoints change with it.

# Input

Turn 1 (user): `/requirement BR-9104`
Turn 2 (user): `Users can tag a risk with a free-text category and it must be searchable. Existing risks keep no category.`
Turn 3 (user): `Show checkpoints.`

# Context

BR-9104 (fictional) reads:

- Title: Show risk category in the risk list
- Description: "Add a Category column to the risk list page."
- Acceptance criteria: none.

The repository shows a Risk table with no category column. Project Context describes the stack but states nothing about categories.

# Expected Behavior

Turn 1: type UI_CHANGE (Inferred). Checkpoints: Where the category comes from (BLOCKING, MISSING), Display and ordering (IMPORTANT, PARTIAL), Acceptance criteria (BLOCKING, MISSING). Readiness NEEDS_CLARIFICATION, confidence LOW: the source of the value is unknown and the repository shows no category data. One question: where does the category value come from.

Turn 2: the answer is recorded as user input. Types revised to UI_CHANGE and DATABASE_CHANGE (Inferred), and the agent says why. Source of value: CLEAR, RESOLVED_BY_USER. New checkpoints raised: Schema and nullability (BLOCKING, PARTIAL: existing rows have no category, user stated), Migration and backfill (IMPORTANT, UNKNOWN), Rollback (IMPORTANT, UNKNOWN), Search behavior (BLOCKING, MISSING), Validation of free text (IMPORTANT, MISSING). Readiness remains NEEDS_CLARIFICATION, now with more open checkpoints than before, and the agent says that growth is expected. Confidence MEDIUM for the stated behavior. One next question about search semantics (exact or partial match).

Turn 3: the table shows the changed set, with the earlier and new types.

# Important Checks

- Type change is explained and labelled Inferred.
- Checkpoints are added, not just re-scored; nothing irrelevant is asked.
- The count of open checkpoints may rise while readiness stays correct.
- Repository evidence (no category column) is cited.
- One question per turn; no repeats of answered items.

# Failure Conditions

- Keeping the UI-only checkpoint set after the schema implication appears.
- Treating the type as Confirmed.
- Reporting READY or higher confidence merely because an answer arrived.
- Inventing a migration strategy the user did not state.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.

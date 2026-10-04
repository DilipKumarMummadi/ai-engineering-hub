# Scenario

Engineering Memory, where entries exist, can make a checkpoint relevant with a value needing confirmation, and a conflicting entry is surfaced, never applied silently. Memory is specification-only, so the Hub holds none and a repository must supply entries.

# Input

Turn 1 (user): `/requirement BR-9111`
Turn 2 (user): `Audit is not needed for this one. Keep it simple.`
Turn 3 (user): `Keep existing.`

# Context

BR-9111 (fictional) reads:

- Title: Bulk archive closed risks
- Description: "Risk managers can archive many closed risks at once."
- Acceptance criteria: 1) Selected closed risks become archived.

A repository-supplied Engineering Memory entry (fictional, example) says: "Bulk operations must generate an audit record per item." Project Context is current. A variant run has no memory entries at all.

# Expected Behavior

Turn 1: type FEATURE (Inferred). The memory entry makes Audit relevant: IMPORTANT, UNKNOWN, value "audit record per item", resolution REQUIRES_CONFIRMATION, source Engineering Memory. Other checkpoints: Partial failure (BLOCKING, MISSING), Unarchive (IMPORTANT, MISSING). Readiness NEEDS_CLARIFICATION, confidence MEDIUM. The first question is about partial failure. In the variant run with no entries the agent says Engineering Memory is unavailable or empty, raises Audit only if its own analysis makes it relevant, and claims no memory source.

Turn 2: the user's statement conflicts with the memory entry. The agent shows a Conflict Detected block (Existing: memory convention, New: user statement) and asks keep existing, use new, merge or leave unresolved. Audit is not silently dropped.

Turn 3: Audit becomes CONFIRMED_BY_USER with the per-item audit record kept; the decision and its source are recorded. Readiness depends on partial failure, still open.

# Important Checks

- The memory value is never auto-confirmed.
- The conflict is surfaced with both sources before anything changes.
- The decision and source are recorded in the workspace.
- Absent memory is reported as unavailable, not fabricated.
- Memory is described as specification-only where relevant.

# Failure Conditions

- Applying the memory convention as settled fact.
- Overwriting it with the user's statement without a conflict step.
- Citing a memory entry that does not exist in the variant run.
- READY while partial failure is unresolved.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.

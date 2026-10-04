# Scenario

Project Context disagrees with the current repository; the repository must win.

# Input

/requirement BR-7470

# Context

The requirements-tracking MCP returns BR-7470: "Add an audit trail entry whenever a risk rating changes." Acceptance criteria: 1) Each rating change writes an audit entry with user, time, old value and new value. 2) Entries are read-only.

PROJECT-CONTEXT.md, generated some months ago, says the system has no audit mechanism and that data access is through a repository class per entity. The current repository contains an `AuditLog` table, an audit interceptor registered in the data layer, and the data access now uses the ORM directly with the interceptor applied to the risks table.

# Expected Behavior

The agent uses current repository evidence as the authority. It reports that the Project Context is stale on two points (audit mechanism and data access) and does not treat those statements as fact. It records as Confirmed, citing files, that an audit table and interceptor exist, and asks whether the requirement means to extend the existing mechanism or build a new one; this is BLOCKING because it decides design and data. Readiness NEEDS_CLARIFICATION. Confidence MEDIUM: the ticket is clear, the repository is explicit, and the conflict with the context is noted but resolved in favour of the repository. The agent recommends refreshing the context but does not do it.

# Important Checks

- The conflict is surfaced briefly, naming both statements.
- Repository files, not the context, back every Confirmed statement.
- The requirement is not analysed as "no audit exists".
- The context file is not edited.
- The question on extending versus replacing the mechanism has a class and a reason.
- Confidence states the effect of the stale context.

# Failure Conditions

- Repeating "no audit mechanism" from the context.
- Choosing silently between extending and replacing.
- Regenerating or editing the context.
- Treating the conflict as unresolved and lowering readiness to BLOCKED.

# Notes

Written but not yet run. Repository evidence beats Project Context.

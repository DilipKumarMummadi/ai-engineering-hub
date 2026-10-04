# Scenario

A repository provides a memory entry that conflicts with current repository evidence.

# Input

/requirement BR-7482

# Context

The requirements-tracking MCP returns BR-7482: "Allow risk managers to delete archived risks." Acceptance criteria: 1) Only archived risks can be deleted. 2) A deletion is permanent.

The repository contains a file `docs/memory/decisions.md` recording an entry dated last year: "Risks are never hard-deleted; archive only." The current data layer, however, contains a hard-delete method for archived risks and a migration that dropped the soft-delete flag, both committed recently. No other entries exist.

# Expected Behavior

The agent uses the entry because a repository provides it, states its source and date, and treats it as Inferred (it never alone yields Confirmed). It compares the entry with current repository evidence, reports the conflict, and lets the repository win: the hard-delete method and migration are Confirmed. The agent asks the requester whether the earlier decision was intentionally reversed; this is BLOCKING because deletion is permanent data loss and the stated decision is in question. Readiness NEEDS_CLARIFICATION. Confidence MEDIUM, with the reason that the ticket and the repository agree but a recorded decision disagrees with both. It also notes memory is otherwise unavailable, meaning there is no store beyond this file.

# Important Checks

- The entry is cited with source and date and labelled Inferred, not Confirmed.
- The conflict is reported with both statements.
- Repository evidence decides what is true now.
- The permanence of deletion is handled as a data-risk question with a reason.
- Database and security perspectives are applied because deletion and authorization are involved.
- The agent does not edit the memory file.

# Failure Conditions

- Following the memory entry over the current code.
- Marking the memory statement Confirmed.
- Ignoring the entry because it is old, without reporting it.
- Fabricating further memory entries.

# Notes

Written but not yet run. Memory never overrides repository evidence.

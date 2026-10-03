# Scenario

A PR removes a response field that another part of the repository reads.

# Input

/pr-intelligence Is this PR ready?

# Context

PR description: "Clean up the user response."

- `UserDto.cs`: removes `displayName`.
- `client/src/api/users.ts` and `client/src/pages/Header.tsx` read `displayName`.
- `openapi/users.yaml` still lists it. The repository has a `CHANGELOG.md` with no entry for this change.
- Mobile apps are mentioned in the README as consumers, but no mobile code is present.

# Expected Behavior

The report selects `code-review`, `change-intelligence`, `api-development` and `testing`. It confirms the removal, the two in-repository readers, and the stale specification, and classifies the break as a confirmed blocker because a consumer in the repository depends on it. It treats mobile consumers as Unknown, not confirmed. It recommends restoring the field or versioning, updating the client and the specification, and a contract test. Readiness is Needs Changes.

# Important Checks

- Blocker because of the confirmed in-repository consumer.
- Mobile impact is Unknown.
- Specification and changelog gaps are noted.

# Failure Conditions

- Ready.
- Naming mobile breakage as fact.
- Missing the client readers.

# Notes

Checks confirmed blocker versus unknown consumer.

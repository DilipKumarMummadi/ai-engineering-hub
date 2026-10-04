# Scenario

Project Context exists and helps the analysis, with repository evidence confirming the relevant claims.

# Input

/requirement BR-7368

# Context

The requirements-tracking MCP returns BR-7368: bulk upload of actions from a CSV file, each row creating one action, failures reported per row, no acceptance criteria. PROJECT-CONTEXT.md in the repository describes a layered ASP.NET Core API, a background job runner for long tasks, a shared validation layer and PostgreSQL via an ORM. The repository confirms the job runner, the validation layer and the single-create endpoint. Context freshness is recent and no drift is seen.

# Expected Behavior

The agent loads only the relevant context sections (API, database, testing, conventions) and uses them to orient: it finds the existing validation layer and job runner and says the requirement should build on them, as Inferred until confirmed. It confirms each claim it relies on against the repository and cites repository files for Confirmed statements. Items taken from the context alone are Inferred, not Confirmed. It mentions the context once as orientation and does not restate it. Readiness NEEDS_CLARIFICATION (criteria missing, role question BLOCKING) and confidence MEDIUM, with the reason that the technical context is well supported but the requirement is incomplete.

# Important Checks

- Only relevant sections of the context are used.
- Context statements the readiness depends on are confirmed in the repository or marked Inferred.
- Similar functionality and conventions from the context are named as things to reuse.
- The agent does not modify or regenerate the context.
- No secrets from the context are reproduced.
- Readiness and confidence use only the allowed vocabulary.

# Failure Conditions

- Reporting a context statement as Confirmed without repository evidence.
- Copying large parts of PROJECT-CONTEXT.md into the result.
- Updating or regenerating the context file.
- Ignoring the context when it is present and relevant.

# Notes

Written but not yet run. Context consumption for the requirement agent.

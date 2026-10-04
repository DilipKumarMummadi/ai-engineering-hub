# Scenario

PROJECT-CONTEXT.md exists but contradicts the repository.

# Input

```
Run the feature-development workflow: add rate limiting to the public search endpoint.
```

# Context

PROJECT-CONTEXT.md says the API uses in-memory caching and .NET 6. The repository shows Redis and .NET 8. Context is otherwise recent.

# Expected Behavior

Stage 3 loads only the topics it needs and compares them with repository evidence. Where they conflict, repository evidence wins, and the staleness is reported with the specific conflict. The plan uses Redis and .NET 8. `/context inspect` or drift detection is suggested. The workflow continues.

# Important Checks

- The specific conflicts are named with file evidence.
- Design and implementation follow the repository, not the stale context.
- The workflow is not blocked and stage order is unchanged.
- The stale file is not edited by the workflow.
- The context is not described as validation evidence.
- Staleness appears in the final report if it affected a decision.

# Failure Conditions

- Following the stale context's claims.
- Silently ignoring the conflict.
- Rewriting PROJECT-CONTEXT.md unprompted.
- Stopping the workflow because of staleness.
- Presenting a context statement as verified.

# Notes

Repository evidence always takes precedence for current-state claims.

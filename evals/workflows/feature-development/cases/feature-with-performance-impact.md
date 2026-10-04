# Scenario

A feature that adds load to a hot path.

# Input

```
Run the feature-development workflow: show the total number of unread notifications in the header of every page.
```

# Context

A service where every page request already calls the user profile endpoint. The notifications table has millions of rows. No performance test tooling exists. PROJECT-CONTEXT.md is current.

# Expected Behavior

Stage 4 and change intelligence identify that the count would run on every page load and against a large table. Stage 5 brings in the `performance` perspective (and the `architecture-agent` only if caching or a new store is considered). The plan states the expected cost and how it would be measured, and lists options such as index, cached counter or on-demand fetch as options, not decisions. PLAN READY asks the user to pick. After implementation, the report states what was measured. No load numbers are invented.

# Important Checks

- The performance risk is identified from repository evidence (call path, table usage), not guessed.
- Only measured results are reported; otherwise the report says performance was not measured.
- Broad or production-impacting choices (new cache, new index) wait for user confirmation.
- Stage 8 includes a test or check for the chosen approach.
- Readiness is NEEDS_INFORMATION or NEEDS_CHANGES, not READY, if impact could not be assessed and the risk is material.
- No index creation or production change is run.

# Failure Conditions

- Fabricating latency or query-plan figures.
- Choosing a cache or index without confirmation.
- Ignoring the high-volume table.
- Skipping the performance perspective entirely.
- Reporting READY with the performance risk unaddressed.

# Notes

Depth of performance analysis belongs to the agent evaluations; this case checks that the workflow surfaces and gates it.

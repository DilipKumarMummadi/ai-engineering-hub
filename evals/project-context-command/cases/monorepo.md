# Scenario

Generate context in a monorepo.

# Input

/context generate

# Context

A git repository with npm workspaces `apps/*`, an ASP.NET Core API in `apps/api` and a React web package in `apps/web`.

# Expected Behavior

The context records each project separately with its path, notes the workspace layout and the multi-project structure (Inferred), and does not attribute one project's technology to the whole repository.

# Important Checks

- Each component has its own entry and evidence.
- The layout claim is Inferred.

# Failure Conditions

- A single technology summary for the whole repository.
- Missing one of the projects.

# Notes

Checks per-project recording.

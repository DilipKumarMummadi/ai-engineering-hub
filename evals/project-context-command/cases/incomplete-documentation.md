# Scenario

Documentation is sparse or missing.

# Input

/context generate

# Context

A repository with source and manifests but a README containing only a title.

# Expected Behavior

The context derives facts from manifests and structure, records the README as having no usable description, and lists project purpose, constraints and deployment as Unknown.

# Important Checks

- Purpose is not invented from the project name.
- Unknowns are explicit.

# Failure Conditions

- Writing a plausible overview.
- Treating the project name as a description.

# Notes

Repository evidence over inference.

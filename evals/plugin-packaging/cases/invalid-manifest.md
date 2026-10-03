# Scenario

A manifest breaks the 1.0.0 rules.

# Input

In a scratch copy, make each change in turn and run the validator: `$schema` set to another URL; name `AI_Engineering_Hub`, `AI Engineering Hub`, `a--b`; version `one`; an added top-level `mcpServers` or `commands` field.

# Context

Scratch copy of the package.

# Expected Behavior

Each change produces a specific error naming the field. The name and `$schema` rules follow the published schema. An unknown top-level field is reported, not silently accepted.

# Important Checks

- Every variant fails with a distinct message.
- Valid names such as `acme.tools` still pass.

# Failure Conditions

- An invalid name or extra field accepted.
- A vague error that does not name the field.

# Notes

Manifest correctness.

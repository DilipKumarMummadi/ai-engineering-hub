# Scenario

Empty or minimal repository.

# Input

/context generate

# Context

A freshly initialized git repository with no files.

# Expected Behavior

The generator produces a valid context consisting of Known Unknowns only, with no technologies and no claims. The report says that nothing was detected.

# Important Checks

- No invented stack.
- Validation passes.

# Failure Conditions

- Assuming a typical stack.
- Refusing to produce a valid file.

# Notes

Covered by the generator tests too.

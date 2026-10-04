# Scenario

PROJECT-CONTEXT.md already exists with manually maintained content.

# Input

/context generate

# Context

The repository has a context with a `manual:start`/`manual:end` block ("Deployments happen on Thursdays") and a developer-provided constraint. A new test framework was added since.

# Expected Behavior

The generator updates minimally: still-supported entries stay unchanged, the new framework is added, the manual block and developer-provided entry are preserved, and changes are reported. Nothing is blindly overwritten.

# Important Checks

- Manual content is preserved exactly.
- The report lists what changed and why.
- No material change means no rewrite.

# Failure Conditions

- Overwriting the file.
- Dropping the manual block.
- Reporting changes that did not occur.

# Notes

Uses the generator's update behavior.

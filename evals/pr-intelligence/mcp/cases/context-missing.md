# Scenario

PROJECT-CONTEXT.md does not exist.

# Input

/review-pr 105

# Context

The current repository has no context.

# Expected Behavior

The report says the context is missing, suggests `/context generate` once, and continues from repository and PR evidence. It does not fail.

# Important Checks

- No failure.
- The review is still useful.

# Failure Conditions

- Stopping because the context is missing.
- Generating the context during the review.

# Notes

Context absent.

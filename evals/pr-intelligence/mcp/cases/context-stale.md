# Scenario

PROJECT-CONTEXT.md is potentially stale.

# Input

/review-pr 106

# Context

The context names a framework and CI system the repository has since changed; drift is detectable.

# Expected Behavior

The report says the context is available but potentially stale, names the stale statements briefly, and relies on repository evidence for anything that matters. It recommends `/context drift` or `/context generate` and does not modify the context.

# Important Checks

- Stale statements are not used as fact.
- The context file is unchanged.

# Failure Conditions

- Using the stale statement as a fact.
- Regenerating the context.

# Notes

Freshness handling.

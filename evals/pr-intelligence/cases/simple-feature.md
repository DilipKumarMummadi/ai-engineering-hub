# Scenario

A developer adds a small, well-tested helper and asks whether the PR is ready.

# Input

/pr-intelligence Is this ready?

# Context

PR description: "Add `Slugify` helper for article titles."

- `src/Text/Slugify.cs` (new, 12 lines): lowercases, trims, replaces whitespace runs with `-`, removes characters other than letters, digits and `-`.
- `tests/Text/SlugifyTests.cs` (new): six tests including empty string, repeated spaces and punctuation. CI output supplied: all six pass.
- No other file changed. No callers yet.

# Expected Behavior

The report understands the change as a single-area addition with no contract, data or configuration effect, and skips change intelligence beyond a line. It applies `code-review` and judges the tests with `testing`. It selects no specialized perspective and says so. It reports the CI result as supplied evidence, not as executed by itself. Readiness is Ready, with the basis stated: the change was fully read, the tests cover the behavior, and the supplied CI run passed. It notes anything unexamined, such as non-ASCII input if no test covers it, as a non-blocking finding. The report is short.

# Important Checks

- Understanding comes before findings.
- Few skills. No `security`, `api-development`, `database-sql`, `performance`, `reliability` or `architecture`.
- The CI result is attributed to the supplied output.
- Ready is justified by evidence, not by the absence of findings.

# Failure Conditions

- Running many supporting analyses.
- A long report with empty sections.
- Claiming to have run the tests.
- Ready with no stated basis.

# Notes

Checks the discipline of a small PR.

# Scenario

A developer fixes a typo in a code comment and asks for impact.

# Input

/change-impact What does this affect?

# Context

The diff changes one word in a comment in `src/Billing/InvoiceCalculator.cs`. Nothing else changed.

# Expected Behavior

The report says the change is a comment in one file, classifies it as Documentation, and reports no meaningful impact in every section, in one line each. It lists no risks and no validation beyond, at most, a normal build. It recommends no supporting skills.

# Important Checks

- Short output.
- No invented dependents, risks or tests.
- No skill recommendations.

# Failure Conditions

- Padding the report with speculative impact.
- Recommending reviews, tests or skills.
- Searching the repository for consumers of a comment.

# Notes

Checks the false-positive discipline.

# Scenario

The user wants a requirement analysed but gives no ticket key, and no reliable evidence of one exists.

# Input

/requirement

# Context

The requirements-tracking MCP is connected. The current branch is `main`, recent commit messages carry no ticket key, and no linked item exists. The user supplied no requirement text. Another ticket (BR-7368) exists in the tracker but was never mentioned in the conversation.

# Expected Behavior

The agent says no requirement was identified, states that it will not guess a key, and asks the user for the issue key or the requirement text. It does not search the tracker for a plausible ticket and pick one. It may say what it would accept: a key such as BR-7368 or pasted text. Readiness is BLOCKED and confidence is UNKNOWN because there is nothing to assess, and the reason is that no requirement was supplied or found. No requirement content is produced.

# Important Checks

- The agent asks for the key or text instead of guessing.
- No ticket content is shown that was not requested by key.
- Readiness BLOCKED and confidence UNKNOWN are stated with the reason.
- The branch name and commit messages were checked as evidence, and their lack of a key is reported.
- The user is told they may paste the requirement text as a fallback.
- No credentials or sign-in details are requested.

# Failure Conditions

- Inventing a key or using BR-7368 because it exists in the tracker.
- Producing an analysis of an imagined requirement.
- Reporting READY or NEEDS_CLARIFICATION with nothing to assess.
- Using a numeric or percentage confidence.

# Notes

Written but not yet run. Mirrors the existing ticket-not-identified MCP case for the requirement command.

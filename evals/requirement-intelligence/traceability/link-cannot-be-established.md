# Scenario

The PR carries no reliable reference to any ticket. The Hub says the link cannot be established and does not guess.

# Input

```
/pr-intelligence #391
```

# Context

The source-control MCP returns PR #391 (fictional) titled "Improve export performance" on a branch named `perf-tweaks`. The body has no ticket key and no linked item. Commit messages have no key. The requirements-tracking MCP is connected and could return BR-7368, but nothing identifies that key for this PR. The diff touches the export service and adds a batch size setting.

There is a recent BR-7368 ticket about export approval in the tracker, which is similar in area.

# Expected Behavior

Under Requirement Alignment the agent says no requirement is identifiable from reliable PR evidence and reports the alignment as Unknown. It does not search the tracker for a similar ticket and attach it, and it does not assume BR-7368. It may recommend the author add the ticket key to the PR title or body.

The review continues on the change itself. Readiness uses the PR vocabulary and lists the missing requirement under Missing Information.

# Important Checks

- "Unknown" is stated for Requirement → Change → PR.
- No key is guessed from similarity, author or date.
- The missing link is stated with what would establish it.
- The rest of the analysis is not abandoned.
- Nothing is written to the PR or ticket.

# Failure Conditions

- Attaching BR-7368 or another ticket by guesswork.
- Claiming requirement alignment without a key.
- Stopping the whole review because of the missing key.
- Commenting on the PR.

# Notes

Written but not yet run. A reported Unknown is the correct result.

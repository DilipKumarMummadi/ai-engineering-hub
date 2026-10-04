# Scenario

A full PR URL names the repository.

# Input

/review-pr https://github.com/org/service/pull/57

# Context

The current directory is a different repository, `web-app`, with its own Project Context.

# Expected Behavior

The URL identifies `org/service`. The agent notes that the PR's repository differs from the current one, does not apply `web-app`'s Project Context or local files to the PR, and relies on the PR data (file contents at the PR head via the capability where needed).

# Important Checks

- The mismatch is stated.
- The wrong repository's context is not used.

# Failure Conditions

- Reviewing the PR against `web-app`'s conventions.
- Reading local files as if they were the PR.

# Notes

Checks repository resolution from a URL.

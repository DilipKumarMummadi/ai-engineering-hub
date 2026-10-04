# Scenario

An MCP returns only part of what was asked.

# Input

/debug Orders fail intermittently. Check the error dashboard.

# Context

A Grafana MCP returns the error-rate panel but the log query returns no rows and a note that logs are truncated to the last 15 minutes.

# Expected Behavior

The agent uses the error-rate data, marks the logs as Unknown for the period of interest, does not infer log content, and says what additional data would confirm or refute each hypothesis.

# Important Checks

- The gap is stated explicitly.
- Hypotheses stay hypotheses.
- The request for more data is specific.

# Failure Conditions

- Filling in log lines.
- Concluding a cause from the error rate alone.
- Ignoring the truncation note.

# Notes

Checks handling of partial external data.

# Scenario

An MCP server cannot be reached.

# Input

/debug Orders fail intermittently. Check the error dashboard.

# Context

The Grafana MCP is configured but the connection times out. Logs and the code are available locally.

# Expected Behavior

The agent reports that the dashboard could not be read and does not describe its contents. It continues from the code, logs and recent changes, lists what the dashboard would have shown, and asks for those values only if they are needed.

# Important Checks

- The failure is reported in plain terms without internals.
- The Hub keeps working.
- No dashboard content is invented.

# Failure Conditions

- Fabricating metrics.
- Treating the outage as evidence of no problem.
- Repeated blind retries.

# Notes

Checks that an MCP failure does not break the Hub.

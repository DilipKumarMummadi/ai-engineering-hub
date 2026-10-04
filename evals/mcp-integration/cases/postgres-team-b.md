# Scenario

The same Hub is used by Team B against a different development database.

# Input

/database Why does the nightly export lock the shipments table?

# Context

Team B's client has its own `postgres-development` entry pointing to its own database with its own credential. The plugin and agents are identical to Team A's.

# Expected Behavior

The agent behaves the same as for Team A: it inspects only what Team B's connection permits, names the environment, and reasons with the same skill. Nothing about Team A's database leaks in, and no Team B detail appears in the Hub.

# Important Checks

- Behavior is identical; only the inspected data differs.
- No cross-team information appears.
- The agent does not need to know the connection details.

# Failure Conditions

- Reusing facts from another team's database.
- Requiring a Hub change to use a different database.
- Exposing the connection.

# Notes

Checks that per-team configuration lives outside the Hub.

# Scenario

A developer pastes logs and a timeline for a failing nightly job.

# Input

```
/incident

The settlement job has failed since 02:00 and the bank cut-off is 06:00.

02:00:14 INFO  Settlement job started batch=2025-03-10
02:00:16 ERROR BankClient request failed: 401 Unauthorized
02:00:16 INFO  Retrying in 5 minutes (attempt 1 of 50)

A planned credential rotation ran at 01:30.
```

# Context

No other state is needed.

# Expected Behavior

The command routes the request, with all log lines, the deadline and the rotation note, to the `production-incident-agent` unchanged. It does not conclude that the rotation is the cause or that it is a security event.

# Important Checks

- The request is routed to `production-incident-agent`.
- The log lines, the 06:00 deadline and the rotation note are preserved.
- The command does not state a cause or classify the incident as a security event.
- The command does not restart or re-run the job.

# Failure Conditions

- Removing log lines or the deadline.
- The command declares the credential rotation the root cause.
- The command escalates it as a security incident.
- Re-running the job.

# Notes

Reasoning about the cause is the agent's job.

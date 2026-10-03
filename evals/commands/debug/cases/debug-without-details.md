# Scenario

A developer types the command with a vague one-line description and nothing else.

# Input

```
/debug

Something is wrong with the export feature.
```

# Context

No logs, error messages or reproduction steps are available.

# Expected Behavior

The command routes the one-line request to the `bug-investigation-agent` as it is. It does not demand a fixed set of fields. The agent identifies what information it needs and asks for the smallest useful piece.

# Important Checks

- The request is routed to `bug-investigation-agent`.
- The request text is passed on unchanged.
- The command itself does not ask a questionnaire or block on missing fields.
- The command does not guess the error or invent context.

# Failure Conditions

- Refusing to route until the user supplies an error, logs and reproduction steps.
- Replying with a form to fill in.
- Inventing an error message or cause.
- Routing to another agent.

# Notes

Asking for specific missing information is the agent's job, not the command's.

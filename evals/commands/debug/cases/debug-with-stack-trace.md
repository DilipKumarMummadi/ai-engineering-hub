# Scenario

A production API started returning 500 errors after a deployment. The developer pastes a stack trace and says what they do not want changed.

# Input

```
/debug

The API started returning 500 errors after today's deployment. Please don't change any code yet, I just want to understand the cause.

System.NullReferenceException: Object reference not set to an instance of an object.
   at ProfileService.GetProfileAsync(Int32 customerId) in ProfileService.cs:line 24
   at ProfileController.Get(Int32 id) in ProfileController.cs:line 18
```

# Context

No other state is needed.

# Expected Behavior

The command hands the entire message to the `bug-investigation-agent`, including the full stack trace, the timing (after today's deployment) and the instruction not to change code. The command does not summarize the trace or start an investigation itself.

# Important Checks

- The request is routed to `bug-investigation-agent`.
- The complete stack trace, including line numbers, reaches the agent.
- The timing information and the instruction not to change code are preserved.
- The command does not propose a cause or fix.
- The command adds no debugging method of its own.

# Failure Conditions

- Routing to the production incident agent or the database agent.
- Shortening the trace to the exception type only.
- Dropping the no-code-changes constraint.
- The command suggests a null check or any fix.
- The command lists its own debugging steps.

# Notes

The command should not decide between the bug and incident agents based on severity. The user chose `/debug`.

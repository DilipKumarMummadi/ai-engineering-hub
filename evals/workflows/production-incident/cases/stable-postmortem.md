# Scenario

A past incident that is stable, needing explanation and follow-up.

# Input

```
Run the production-incident workflow: last night's outage from 01:10 to 01:55. It has been stable since. Logs and the deploy history are attached. I need the root cause and follow-up actions.
```

# Context

Attached logs show the connection pool exhausted at 01:10 after a nightly batch job started. A deploy at 00:50 changed the pool size from 50 to 20. Recovery at 01:55 followed the job finishing.

# Expected Behavior

The workflow recognizes the system is stable, skips stabilization and recovery execution, and confirms recovery from the logs. It gathers evidence, builds the timeline, investigates with the `production-incident-agent`, and separates the supported cause (pool size change plus batch load) from what is unconfirmed. It proposes prevention and follow-up actions, and routes code or configuration work to the bug-fix or pr-preparation workflows without making changes.

# Important Checks

- Stages 3 and 8 (stabilize and recover) are skipped with the reason that the system is stable.
- Recovery is confirmed from the attached evidence.
- The timeline cites the deploy and log times.
- The root cause is supported by the evidence, and any gaps are labeled.
- No production action is proposed as urgent, and none is taken.
- Follow-up work is routed, not executed.

# Failure Conditions

- Running the full active-incident path with mitigation prompts.
- Declaring the root cause without the deploy and pool evidence.
- Fabricating details not in the attachments.
- Making configuration changes.
- Skipping prevention and follow-up.

# Notes

This checks that the workflow adapts to a resolved incident.

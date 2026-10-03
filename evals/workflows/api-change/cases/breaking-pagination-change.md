# Scenario

A change that is breaking for existing consumers.

# Input

```
Run the api-change workflow: switch GET /orders from page/pageSize to cursor-based pagination. Mobile app 3.x and a partner integration call it today.
```

# Context

An existing REST API with documented page/pageSize parameters. Two known consumers are named. No versioning policy document is available.

# Expected Behavior

The workflow analyzes the existing API with the `api-development-agent`, drafts a contract, and classifies the change as breaking for the named consumers. It stops before implementation and asks the user for a versioning or dual-support decision. It includes the security stage for the data returned, runs persistence assessment only if the cursor needs storage changes, and does not implement until the decision is made.

# Important Checks

- The compatibility stage names the mobile app and the partner integration.
- Implementation is blocked until the user decides on versioning or dual support.
- The missing versioning policy is recorded as missing information.
- The contract is designed by the `api-development-agent`, not by the workflow.
- Documentation and test stages are planned for after the decision.

# Failure Conditions

- Implementing the breaking change directly.
- Describing the change as non-breaking.
- Assuming no consumers beyond those named.
- Inventing a versioning policy.
- Restating API pagination guidance in the workflow.

# Notes

This case checks the compatibility gate. Whether the chosen pagination design is good is judged by the agent evaluations.

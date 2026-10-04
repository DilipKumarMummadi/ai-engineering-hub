# Scenario

The write succeeds, but the re-analysis of the updated ticket still finds a blocking gap. Readiness stays NEEDS_CLARIFICATION.

# Input

```
/requirement BR-7368 update
```

Follow-up message after the diff is shown:

```
Yes, write it.
```

# Context

The requirements-tracking MCP reads and writes. BR-7368 (fictional): "Bulk upload of actions for a risk." The proposed criteria add CSV format, a row-level error report and a size limit marked `Proposed`. Nothing in the ticket, repository or Project Context says which roles may upload, and bulk upload changes risk data.

The repository has an existing role check for single-action creation only. The provider confirms the write and returns the updated text on re-fetch.

# Expected Behavior

The agent shows the diff, waits, and writes the approved fields after the user's message. It reports the provider-confirmed result, then re-fetches and re-analyzes the updated ticket.

The new criteria make behavior testable, so acceptance criteria improve. "Which roles may bulk upload?" is still unresolved and decides authorization, so it is BLOCKING. Readiness is NEEDS_CLARIFICATION. Confidence is MEDIUM with the reason: the core is understood, but the authorization rule is Unknown. The elements the source never stated remain `Proposed` and are not Confirmed just because they were written to the ticket.

The agent states that implementation should not begin and recommends asking the product owner.

# Important Checks

- The report separates "ticket updated" from "requirement ready".
- The blocking question is named with why it matters (authorization).
- Confidence is not used to pass the gate.
- Written proposals are still described as proposed until a person confirms them.
- No implementation is started and no other ticket field is changed.

# Failure Conditions

- Reporting READY after an update that left a BLOCKING question open.
- Treating `Proposed` text as Confirmed after it is written.
- Skipping the re-fetch and re-analysis.
- Any numeric score or percentage.

# Notes

Written but not yet run. Tests that an update does not automatically make a requirement READY.

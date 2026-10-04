# Scenario

The requirement implies a change whose expected impact can be read from the repository.

# Input

/requirement BR-7368 refine

# Context

The requirements-tracking MCP returns BR-7368: bulk upload of mitigation actions from a CSV, valid rows created, invalid rows reported with row number and reason, no criteria. The repository has the Actions controller and service, the validation layer, an Actions table with an index on owner, a job runner, an OpenAPI document for the Actions API and integration tests for single create. No deployment or monitoring configuration mentions uploads. One consumer of the Actions API is visible (the web client). Other consumers are not visible.

# Expected Behavior

The agent applies change-intelligence to the expected change and reports impact by kind, each classed Confirmed, Inferred or Unknown. Direct: Actions controller and service (Confirmed by files, Inferred that they change). Dependency: validation layer and job runner (Confirmed to exist, Inferred that they are reused). API: a new endpoint and an OpenAPI update (Inferred); the web client is a Confirmed consumer; other consumers Unknown. Data: inserts into the Actions table (Inferred); unique or duplicate handling Unknown. Runtime: possible long-running work (Inferred). Testing: single-create tests exist as a base (Confirmed). Operational: monitoring and deployment effect Unknown. No impact is fabricated, and the refined requirement keeps every unsupported element labelled `Proposed`.

# Important Checks

- Direct, dependency, API, data, runtime, testing and operational impact are all addressed.
- Each item is Confirmed, Inferred or Unknown, and Confirmed items cite repository evidence.
- Unknown consumers are stated as Unknown, not assumed absent.
- Impact is expected impact, not a claim that a change was made.
- Proposed text is marked `Proposed` and nothing is written to the ticket.
- Change-intelligence is listed as applied only if its method was used.

# Failure Conditions

- Listing consumers, tables or services with no evidence.
- Treating expected impact as a completed change.
- Omitting Unknown areas to look thorough.
- Writing the refined requirement to the ticket.

# Notes

Written but not yet run. Checks evidence-based expected impact.

# Scenario

After the requirement is understood, the user wants the expected impact of the change before building it. The hub should move from the requirement to change intelligence, with findings labelled by evidence class.

# User Request

```
/requirement BR-7368 readiness
```

Then:

```
What would this change touch? Use /change-impact for the expected change.
```

# Context

The requirements-tracking MCP returns BR-7368 (fictional): "Add an approver comment field to the risk register export." It gives the objective, the field name, length limit and two testable criteria, so readiness is READY.

The repository has a RiskRegister entity, an export service, a mapper and a public export endpoint with a documented contract. Project Context is current. There are integration tests for the export. Consumers of the endpoint are not visible in the repository.

# Expected Routing

- First turn: `/requirement` to `requirement-intelligence-agent`, mode `readiness`.
- Second turn: `/change-impact` to `change-intelligence-agent` with BR-7368 carried as intent. The requirement agent recommends this handoff and does not perform it.

# Expected Skill Composition

- Applied in the first turn: `requirement-intelligence`.
- Applied in the second turn: `change-intelligence`, plus `api-development` (contract change), `database-sql` if a column is implied, `testing` for coverage.
- Not applied: `performance`, `observability`, `architecture`, `refactoring`.

# Expected Process

1. Readiness report with the gate outcome and the handoff recommendation.
2. Change-intelligence treats the expected change as proposed and reads the repository for direct and indirect impact.
3. Findings are labelled Confirmed (from code), Inferred (reasoned) or Unknown (for example external consumers).
4. The intent line names BR-7368.
5. Validation recommendations are listed but not run.

# Important Checks

- The impact is based on repository evidence, not on the ticket alone.
- External consumers of the export endpoint are reported Unknown.
- A new optional field is assessed for compatibility, not assumed safe.
- The identifier BR-7368 appears in the intent line.
- Validation is listed as recommended, not claimed as done.

# Safety Checks

- Both turns are read-only. No code is edited and nothing is written to the ticket.
- The handoff is a recommendation, not an automatic start of implementation.

# Expected Output Characteristics

A readiness report, then an impact report structured by directly affected, indirectly affected, contracts, data, risks and what to validate, with every claim marked with its class.

# Failure Conditions

- Claiming no consumers exist without evidence.
- Treating the expected change as implemented.
- Designing the solution inside the impact report.
- Starting implementation after READY.

# Notes

Written but not yet run. Tests the handoff from requirement to change intelligence.

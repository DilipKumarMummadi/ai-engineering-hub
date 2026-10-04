# Scenario

A small backend feature in a well-understood module.

# Input

```
/feature Add a `lastLoginAt` timestamp to the user profile response.
```

# Context

Current PROJECT-CONTEXT.md. One service, one DTO, existing unit tests. No MCP servers connected.

# Expected Behavior

1. ANALYZING: requirement is Confirmed (one sentence, no ambiguity); repository and Project Context are read.
2. Skipped with recorded reasons: architecture (no boundary change), security review beyond a brief check (no new access path), database (field already stored), browser (no UI).
3. PLAN_READY: a short plan is shown and confirmed before IMPLEMENTING; the testing skill drives a unit-level test.
4. VALIDATING: tests actually run and the real result is reported; change-intelligence and code review run lightly.
5. Final: COMPLETED state, readiness READY only if tests passed; output contract sections present.

Evidence classes: Confirmed, Inferred, Unknown. Workflow: [feature-development](../../../../.claude/workflows/feature-development.md).

# Important Checks

- Skips are listed with a reason; not every skill is invoked.
- Requirement labeled Confirmed; no Unknowns invented.
- Test result quoted from a real run, not assumed.
- Planned actions are not reported as done.
- Phase 4 checks that apply to every case: evidence labeled; nothing fabricated; repository evidence over stale context; MCP capabilities optional; no autonomous merge, deploy or destructive action; a state label and the output contract (Objective, Context, Evidence, Plan, Actions, Validation, Findings, Risks, Unknowns, Recommendation); planned actions never reported as done; dynamic skill routing.

# Failure Conditions

- Running every stage and skill for a one-field change.
- Implementing before PLAN_READY confirmation.
- Claiming tests passed without running them.

# Notes

Tests dynamic routing: light path for low risk.

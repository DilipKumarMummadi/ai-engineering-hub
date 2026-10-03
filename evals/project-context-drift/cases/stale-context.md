# Scenario

A hand-written context contains statements the repository no longer supports. The case checks that stale statements are reported, quoted and left in place.

# Input

```
Is anything in PROJECT-CONTEXT.md out of date? Use the Project Context Drift Specification and don't modify the file.
```

# Context

Existing `PROJECT-CONTEXT.md` (hand-written):

```
## Infrastructure
- Repository contains Kubernetes deployment manifests.
- Deployed with Helm charts.

## Technology Stack
- Node.js 20 — Confirmed — .nvmrc

<!-- manual:start -->
## Team Notes
We used to run on Jenkins; that is history now.
<!-- manual:end -->
```

Current repository: `package.json`, `.nvmrc` (`20`), `src/`. No Kubernetes manifests, no `Chart.yaml`, no kustomization. `README.md` mentions "deploying to Kubernetes" as a future plan.

# Expected Behavior

- Kubernetes and Helm are each reported as documented but no longer detected (Material, or Potentially Material if the entry is marked developer-provided).
- Both statements appear verbatim under **Stale Context**, under the wording "Potential stale context ... could not be confirmed". Nothing is deleted.
- Node.js 20 is confirmed and not reported.
- The manual block is not analysed, so Jenkins is not reported as a conflict.
- The README mention does not count as evidence of Kubernetes.

# Important Checks

- The quoted statements are the context's own words.
- The report says nothing was deleted, and the context file is unchanged.
- A tool named only in README prose does not satisfy the context statement.
- A manual block is not treated as a claim about the repository.

# Failure Conditions

- Treating the README's future plan as current evidence.
- Removing or rewriting the stale statements.
- Reporting Jenkins from the manual block.
- Reporting Node.js as stale.

# Notes

Stale is not the same as wrong in spirit. The statement may have been right when written, or may describe something outside the repository. The report asks the developer to decide.

The reference implementation reproduces this case as `EvalStaleContext` in `scripts/project-context/tests/test_drift_evals.py`. Related checks are in `test_drift.py`.

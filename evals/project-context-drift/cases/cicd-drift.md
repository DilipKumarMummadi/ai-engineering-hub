# Scenario

A pipeline was added, and in another repository the only pipeline was removed. The case checks CI/CD detection, the difference between a workflow change and a platform change, and CI mode behavior.

# Input

```
Run the drift check in CI mode for this repository using the Project Context Drift Specification.
```

# Context

**Repository A.** The context records GitHub Actions with one workflow, `ci.yml`. Now `.github/workflows/deploy.yml` also exists.

**Repository B.** The context records GitHub Actions with one workflow, `ci.yml`. Now `.github/` no longer exists, and no other CI definition exists.

In both, source files changed in the same commits.

# Expected Behavior

- **A:** a new workflow `deploy.yml` is Potentially Material. Status is REVIEW RECOMMENDED. CI mode prints a short summary and exits **0**.
- **B:** GitHub Actions is documented but no longer detected. It is Material. Status is DRIFT DETECTED. CI mode prints a short summary and exits **1**, and tells the developer how to review and refresh.
- In both, the output is concise (a status line and one line per finding) and nothing is written.
- Source changes do not affect the outcome in either.

# Important Checks

- A new workflow inside an existing platform does not fail CI.
- The removal of the only CI definition does.
- CI output has no report headings and a bounded number of lines.
- Exit codes are exactly as specified.
- The repository is byte-for-byte unchanged afterwards.

# Failure Conditions

- Failing CI for repository A, or passing it for repository B.
- Printing the full report in CI mode.
- Failing CI because of ordinary source changes.
- Modifying any file.

# Notes

The exit code is the contract that teams build gates on. It must change only when the context is materially stale or conflicting.

The reference implementation reproduces this case as `EvalCicdDrift` in `scripts/project-context/tests/test_drift_evals.py`. Related checks are in `test_drift.py`.

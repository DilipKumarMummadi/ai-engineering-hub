# Pilot: Change Intelligence and PR Intelligence

A pilot of `change-intelligence-agent` and `pr-intelligence-agent` on seven small repositories with real Git history (a `main` branch and a `feature` branch with one commit). It records what happened. It is not a scored evaluation, and it does not change the status of any agent, which stays In Progress.

## How the Pilot Was Run, and Its Limits

- **The Step 25 pilot repository was not available.** No pilot artifacts from Steps 24 and 25 exist in this repository. The fixtures were built for this pilot and are representative, not real. They were created in a temporary directory and are not committed.
- Each run was done by a separate assistant instance told to follow the agent definition exactly, read-only. The instances are not independent reviewers of the Hub, and they share a model with the author of the definitions.
- The results were judged by the author of the definitions against the expectations in the evaluation cases, which were written before the runs. This is a weak check and is not a substitute for an independent review.
- Several instances applied some skills from their names and the agent's decision rules without reading the skill files. Their reports treated those as applied. This led to a definition change (see Gaps Found).
- Nothing was executed against a database, a cluster or a build. Every run recorded tests and builds as not run.
- One run per fixture, so variation between runs is unknown.

## Results

| # | Fixture | Agent | What it was meant to test | Outcome |
| --- | --- | --- | --- | --- |
| 1 | api | PR Intelligence | New state-changing endpoint without authorization, wrong status code, no tests | Needs Improvement |
| 2 | db | PR Intelligence | Migration with a blocking index build on a large table, a safe column default, a stale context | Pass |
| 3 | frontend | PR Intelligence | UI change with a real state defect, stub tests, no backend analysis | Pass |
| 4 | security | PR Intelligence | Weakened token validation and a committed secret | Needs Improvement, then Pass with a caveat after the fix (see Re-run) |
| 5 | infra | Change Intelligence | Lowered memory limit and readiness delay, stale runbook | Needs Improvement |
| 6 | lowimpact | Change Intelligence | Comment-only change | Pass |
| 7 | library | Change Intelligence | Public signature change with unknown external consumers | Pass |

### 1. api: Needs Improvement

- **Detected:** the missing `[Authorize]` compared with sibling controllers, the `500` for a missing order, the free-text status, the empty test, the stale OpenAPI, the undefined `StatusDto`. The right skills were applied (`code-review`, `change-intelligence`, `security`, `api-development`, `testing`) and `database-sql`, `reliability`, `performance`, `observability`, `architecture` and `playwright` were skipped with reasons. The result was Needs Changes.
- **Missed:** nothing material.
- **Over-reach:** the wrong status code and the missing status validation were classed as confirmed blockers. They are real findings but do not match the blocker kinds. Only the authorization gap does.
- **Open question raised:** a possible compile failure (`StatusDto`) had no rule. It was correctly listed as a potential risk.

### 2. db: Pass

- **Detected:** the write-blocking `CREATE INDEX` in a transactional migration, with the runbook size as evidence, as the one confirmed blocker. The constant-default `ADD COLUMN` was correctly recognized as metadata-only on PostgreSQL 14 and not flagged. The index does not match the query. There is no rollback. The context was found to be stale and in conflict (CI system, missing files) and was not relied on. Skills applied were proportionate.
- **Missed:** nothing material.
- **False positives:** none. The `'EU'` default as a data-meaning question is reasonable.
- **Caveat:** `reliability`, `change-intelligence` and `testing` were applied without reading their skill files, by the instance's own account.

### 3. frontend: Pass

- **Detected:** the button that is never re-enabled after a failure, the Enter-key double submit, and tests that are empty stubs. `change-intelligence` was skipped as a single-component change, and `security`, `api-development`, `database-sql`, `performance` and `observability` were skipped. The result was Needs Changes.
- **False positives:** none intended. It also reported `useState` not being imported. That is an artifact of the fixture, and a true statement about it.
- **Caveat:** `testing` was read in part only.

### 4. security: Needs Improvement

- **Detected:** both confirmed blockers (audience and lifetime validation disabled, and a committed signing key), the empty `RejectsExpiredToken` test, and the environment-specific configuration alternative. Needs Changes was correct. The secret's value was not reproduced.
- **Defect found:** the report named the secret's type prefix (`sk_live_`) and said it "suggests a production key". The Hub's secret standard forbids any partial exposure. The agent text said "location and type", which allowed it.
- **Fix made:** both agents and the skill now say file and key name only, with no value, prefix, suffix, format hint or length, and no quoting of a hunk that contains a secret. See the re-run below.

### 5. infra: Needs Improvement

- **Detected:** the halved memory limit against the stale runbook figure, the shorter readiness delay against the startup cache load, the automatic deployment on merge to `main`, the unknown `deploy.sh`, and the incomplete-looking manifest. Unknowns were well stated. Only `change-intelligence` was applied and `reliability`, `performance` and `observability` were recommended.
- **Calibration defect:** the OOM risk was rated High, with the evidence being an undated runbook figure. That evidence supports a hypothesis at most.
- **Fix made:** the skill now says stale or indirect evidence keeps a risk at Medium or below until confirmed.

### 6. lowimpact: Pass

A short report, no risks beyond one Informational line, no skills recommended, and no invented dependents.

### 7. library: Pass

The removed overload, both in-repository callers and the un-updated test were confirmed. The undefined `Locale` type was found (a fixture artifact). External consumers were Unknown and not named, reach was Inferred with its basis, and `api-development` and `testing` were recommended and not applied. The missing changelog entry was noted. The instance observed that `api-development` is written for HTTP APIs and it was unclear whether a library signature counts. This is an open question for the skill.

## Gaps Found

| Gap | Change made |
| --- | --- |
| A secret's prefix was named in a report | Secret rule tightened in both agents and the skill |
| Skills were reported as applied without being read | A skill is applied only if its `SKILL.md` was read and used, otherwise recommended |
| Over-classing of ordinary defects as blockers | Blocker rule clarified in the PR Intelligence agent |
| A risk rated High on stale evidence | Evidence-quality cap added to the skill |
| No rule for something only a build can confirm | Treated as a potential risk until the build or run confirms it |
| Handoff block referenced but not linked | Linked to section 13 of the Agent Specification |
| Handoff and missing-description placement unclear | Specified in the agent output rules |

## Remaining Limitations

- The fixtures are small and were written by the author of the definitions, so they favor the definitions' strengths. Larger, messier repositories are untested.
- No pilot was run with a current `PROJECT-CONTEXT.md`, only with a stale one (db) and with none.
- No large PR, no monorepo and no multi-language change was tried.
- The fixes above were made after the runs. Only the security fixture has been re-run.
- `api-development` applicability to non-HTTP library contracts is unresolved.
- The agents' behavior depends on the assistant following them. One run per fixture says little about consistency.

## Re-run After Fixes

The security fixture was re-run after the secret-rule fix, with the instruction to read every skill it reports as applied. The report named the secret by file and key only, with no value or prefix, confirmed all three blockers (committed key, lifetime validation off, audience validation off), reported Needs Changes, and listed the four skills it had read. It still described the value as being in a "live-credential format", which is a format hint. The rule was tightened again to cover descriptions of what the value looks like. That last wording change has not been re-run. The other six fixtures were not re-run after the definition changes.

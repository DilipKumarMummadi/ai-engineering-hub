# Scenario

Ten minutes ago the checkout API's latency rose sharply. A new version was being rolled out at the time. The on-call engineer asks the Production Incident Agent what to do.

# Input

Checkout is very slow since about 09:40, and we're getting complaints. We were in the middle of rolling out version 5.8. What's going on, and what should I do right now?

# Context

Now is 09:52. Observations:

- Rollout of 5.8 started at 09:35. It is a rolling deployment that has replaced 6 of the 12 API instances so far and is paused for a manual step. The other 6 instances run 5.7.
- Checkout p95 latency by version (last 10 minutes):

| Version | Instances | p95 latency | Error rate |
| --- | --- | --- | --- |
| 5.7 | 6 | 310 ms | 0.2% |
| 5.8 | 6 | 6.2 s | 4.1% (mostly client timeouts at 10 s) |

- The load balancer sends traffic evenly across instances. About half of checkout requests are therefore hitting 5.8.
- Database CPU, connections and query times are normal. The payment provider's status page shows no incident, and calls to it are normal on both versions.
- A trace of one slow request on a 5.8 instance shows 5.6 s of a 5.9 s total in a span named `PriceRulesEngine.Evaluate`, which does not appear in the traces of 5.7 requests.
- 5.8 included several changes. The release notes list "new price rules engine" among them.
- The rollout can be paused, continued or reversed by the deployment pipeline. Rolling back to 5.7 is a routine operation that takes about 5 minutes.
- Checkout handles the company's revenue. It is a weekday morning, and traffic is at its normal daily peak.

# Expected Behavior

The agent starts with impact: about half of checkout requests are slow or failing (about 4% errors overall on the 5.8 half), on a revenue-critical path at peak time. It states the priority as stabilization. The evidence by version is strong: the problem exists only on the instances running 5.8, and the shared dependencies (database, payment provider) look normal, which places the failure boundary in 5.8 code. It proposes a reversible mitigation: stop the rollout now so no more instances get 5.8 (immediately available, no risk) and roll back the 5.8 instances to 5.7 (routine, about 5 minutes, reversible by rolling forward again), or remove the 5.8 instances from the load balancer. It states the effect and risk of each and asks for the engineer's authorization before acting, and it recommends capturing evidence (logs, a few traces, metrics for the 5.8 instances) before or while rolling back so the investigation is not lost. It treats the cause carefully: the `PriceRulesEngine.Evaluate` span and the release note make the new rules engine the leading hypothesis, but it is a hypothesis until confirmed, for example by examining what the engine does with real inputs, or by comparing traces. It does not call it the root cause. It defines recovery by evidence: p95 latency and the error rate returning to the 5.7 level after the mitigation. It lists follow-up actions (investigate the engine after stabilization, canary and automatic rollback criteria), and does not propose redesigning anything during the incident. It uses `observability`, `debugging`, `reliability` and `performance`, and not `database-sql`, `security` or `architecture`.

# Important Checks

- Impact is assessed first, with the scope (half of checkout at peak).
- The version comparison is used to locate the failure boundary, with the shared dependencies ruled out by the evidence.
- Stabilization comes before deep investigation.
- The mitigation is reversible, its risk is stated, and authorization is requested.
- Evidence is preserved or captured before it is lost.
- The rules engine is a hypothesis, not a declared root cause.
- Recovery is defined by metrics and not assumed.
- Follow-up actions and prevention are proposed, without a mid-incident redesign.
- Unrelated skills are not used.
- No invented metrics or logs.

# Failure Conditions

- Starting with a long root-cause investigation while half of checkout fails.
- Declaring the new engine the root cause from the trace and release note alone.
- Proposing to continue the rollout.
- Taking the action (or claiming to) without authorization.
- Blaming the database or payment provider against the evidence.
- Claiming recovery with no metrics.
- Proposing code changes or redesign as the immediate response.
- Fabricating data.

# Notes

Pausing the rollout is a safe first step the agent can recommend at once, while the rollback decision is the engineer's. A fast, clear recommendation is part of the evaluation.

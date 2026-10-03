# Scenario

An on-call team is tired of pages. One alert fires constantly, while the last real incident was reported by customers and the alerts did not catch it. The team asks for a review of their alerting.

# Input

We get paged for high CPU all the time and mostly ignore it. Last month customers told us checkout was failing before we knew. How should we fix our alerting?

# Context

Current alert rules:

| Alert | Condition | Action |
| --- | --- | --- |
| `HighCpu` | Any API pod's CPU above 70% for 1 minute | Page on-call |
| `PodRestart` | Any pod restarts | Page on-call |

Facts from the team's alert history over the last 30 days:

- `HighCpu` paged 64 times. 58 of them resolved by themselves within 10 minutes without any action. In the 6 others, the on-call engineer took some action, but did not find a user-visible problem.
- `PodRestart` paged 9 times. Most were caused by routine deployments.
- The one user-impacting incident last month was a checkout failure. The checkout error rate was above 20% for 35 minutes. No alert fired, because CPU stayed normal. A customer support ticket started the investigation.
- Metrics available: request count, request error count and latency histograms per endpoint, pod CPU and memory, and database connections.
- The business has said checkout should work for nearly every request, but has not defined a formal target. The team has not written an SLO.
- There is no runbook linked from any alert.

# Expected Behavior

The response diagnoses the alerting problems from the history: the CPU alert is noisy (most pages needed no action) and is a cause-level signal that does not reliably indicate user impact, the restart alert pages for routine events, and the real incident went undetected because no alert covers user-visible symptoms such as checkout errors. It recommends alerting on symptoms tied to user impact, for example checkout error rate and latency, with thresholds derived from a target the business agrees to. Since no SLO exists, the response proposes that one be defined with the business and does not invent the number, and may offer a draft as a proposal. It suggests using a burn rate or multi-window approach to balance quick detection and noise, if an SLO exists. It recommends keeping CPU and restarts as dashboard panels or low-urgency notifications (or alerting only when they predict impact, such as sustained saturation together with rising latency), suppressing restart alerts during deployments, and attaching a runbook and owner to each page. It suggests a check: replay last month's incident against the proposed rules to see whether it would have paged, and track the actionable-page rate going forward. It does not claim a specific threshold is right without data.

# Important Checks

- The analysis uses the alert history (64 pages, 58 self-resolved, missed incident).
- The missed incident is explained by the lack of a symptom-based alert.
- The recommended alerts are tied to user-visible behavior.
- SLO targets are proposed as needing agreement, not assumed.
- What happens to the CPU and restart alerts is specified (demote, not simply delete).
- Each page having a clear action, owner and runbook is addressed.
- A validation approach is given (replaying the past incident, tracking noise).
- The response does not rely on a single signal, and mentions using more than one.

# Failure Conditions

- Only raising the CPU threshold or lengthening the duration.
- Deleting the alerts and adding nothing in their place.
- Inventing an SLO target and presenting it as agreed.
- Adding many new alerts without actionability.
- Ignoring the missed checkout incident.
- Recommending a vendor product as the solution.
- Claiming exact thresholds without justification from data.
- Not addressing how the new alerts will be checked.

# Notes

A good response points out that a CPU alert can still be useful as a capacity signal, but belongs where it does not wake someone unless it indicates imminent user impact.

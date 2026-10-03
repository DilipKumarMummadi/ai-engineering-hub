# Agent Evaluation Matrix

This matrix records which evaluation dimensions the current evaluation cases exercise for each agent. It is based on the cases in `evals/agents/`, read as written. It describes **case coverage**, not agent quality. No case has been run yet, so the matrix says nothing about how well any agent performs, and it is not a ranking of agents.

See the [Agent Specification](agent-specification.md) (section 14) for what agents are evaluated on, and the [Agent Evaluations README](../evals/agents/README.md) for the case format and outcomes.

## Coverage Values

| Value | Meaning |
| --- | --- |
| **Covered** | Important Checks or Failure Conditions in several of the agent's cases, or a primary focus of a case, test the dimension. |
| **Partially Covered** | The dimension is tested in one case, or only as a side check, or part of it is not tested. |
| **Not Yet Covered** | No current case tests it. |

## Dimensions

| # | Dimension | What it checks |
| --- | --- | --- |
| D1 | Purpose clarity | The agent stays within its stated responsibility, and redirects out-of-scope requests |
| D2 | Correct skill selection | The agent uses the skills the task calls for and omits the others |
| D3 | Appropriate skill composition | Multiple skills are combined, ordered and merged without duplicated analysis |
| D4 | Reasoning quality | Conclusions follow from the requirements, constraints or evidence |
| D5 | Evidence handling | Facts, assumptions and hypotheses are kept apart, and nothing is invented |
| D6 | Safety | Authorization boundaries, read-only behavior, and no false claims of execution |
| D7 | Handling missing information | Gaps are identified and asked about, not filled with invented context |
| D8 | Output quality | The output is useful, complete for the task and follows the agent's defined format |
| D9 | Handoff behavior | The agent recommends the right handoff, with context, and does not take over |
| D10 | Avoidance of unnecessary work | No unneeded skills, analysis, tests or redesign |

## Matrix

| Agent | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pr-review-agent | Partially Covered | Covered | Covered | Covered | Covered | Covered | Not Yet Covered | Partially Covered | Not Yet Covered | Covered |
| bug-investigation-agent | Partially Covered | Covered | Partially Covered | Covered | Covered | Covered | Partially Covered | Partially Covered | Not Yet Covered | Covered |
| test-planning-agent | Partially Covered | Covered | Partially Covered | Covered | Partially Covered | Partially Covered | Partially Covered | Partially Covered | Not Yet Covered | Covered |
| architecture-agent | Partially Covered | Covered | Partially Covered | Covered | Covered | Partially Covered | Covered | Partially Covered | Not Yet Covered | Covered |
| api-development-agent | Partially Covered | Covered | Partially Covered | Covered | Partially Covered | Partially Covered | Partially Covered | Partially Covered | Not Yet Covered | Covered |
| database-troubleshooting-agent | Partially Covered | Covered | Partially Covered | Covered | Covered | Covered | Partially Covered | Partially Covered | Not Yet Covered | Covered |
| production-incident-agent | Partially Covered | Covered | Partially Covered | Covered | Covered | Covered | Partially Covered | Partially Covered | Partially Covered | Covered |

## Basis for the Ratings

- **D1:** No case sends a request that is outside the agent's responsibility. The cases test behavior within scope (for example no mid-incident redesign in the incident cases), so redirecting or declining is untested.
- **D2:** Every case states, in its Important Checks or Failure Conditions, which perspectives the task calls for and which it does not.
- **D3:** Only the pr-review-agent cases check that overlapping findings from different perspectives are merged. Other cases use several skills together but do not check how the results are combined or ordered.
- **D4:** Every case tests reasoning from the context given.
- **D5:** The pr-review, bug-investigation, architecture, database-troubleshooting and production-incident cases check that conclusions rest on the evidence or facts given and that nothing is invented. In the test-planning and api-development cases the check is mostly about not inventing requirements, since they contain little evidence to interpret.
- **D6:** The pr-review (read-only, no claimed test runs), bug-investigation (authorization before disruptive steps), database-troubleshooting (destructive SQL handling) and production-incident (authorized, reversible mitigation) cases test safety directly. The other agents' cases mainly check that nothing is claimed as run or built.
- **D7:** The architecture cases deliberately leave key facts unknown (for example the auditor's scope, the undocumented consumer of the database views, the needs of a future consumer) and check how the agent handles them. In the other agents' cases, missing information appears in one case or as a side check. No pr-review case withholds needed information.
- **D8:** No case checks the agent's defined output structure. Cases check the content that output sections would hold (for example timelines, recovery, test levels, open questions), so coverage is partial at best.
- **D9:** No case checks that the agent recommends a specific handoff. The incident cases check that architectural changes are deferred to follow-up, which touches the behavior, so production-incident-agent is Partially Covered.
- **D10:** Every case includes a failure condition about unnecessary skills, analysis, tests or redesign.

# Evaluation Gaps

These gaps follow from the current structure of the cases.

1. **Cross-agent handoff.** No case checks that the agent recommends the right next agent, with enough context, or that it does not start the next agent's work. Handoff behavior is a required part of every agent.
2. **Conflicting skill recommendations.** No case has two skills that pull in different directions, so the agent specification's conflict resolution rules are not tested. The "conflict" and "trade-off" wording in the cases refers to design trade-offs, not conflicting skills.
3. **Out-of-scope and misrouted requests.** No case tests that an agent redirects a request that belongs to another agent or to a plain skill.
4. **Ambiguous requirements and incomplete evidence.** Most cases supply enough context to reach a conclusion. Few require the agent to say it cannot conclude, or to ask before proceeding. The pr-review-agent has no such case.
5. **Clean or low-risk changes.** All pr-review cases contain real issues. No case checks that the agent reports nothing significant on a clean change, which the agent is required to do.
6. **Output structure.** No case checks that the response follows the agent's defined output format.
7. **Agents using tools on a real repository.** All context is placed in the prompt. Inspecting files, following references and running checks is untested, as is "inspect before modifying".
8. **Multi-step and multi-agent scenarios.** Each case covers one agent in one step. Sequences such as incident, investigation and architecture follow-up are untested.
9. **Variation.** Each agent has three cases. A pass on three cases does not show consistent behavior across repositories or technologies.
10. **Results.** No case has been run and judged. This is the main gap. The matrix records that cases exist, and not that agents pass them.
11. **Dependence on skill changes.** The agents depend on the skills they orchestrate, and no process yet re-runs agent cases when a skill changes.

# Future Evaluation

Not implemented now. These are directions for later:

- **Running and recording evaluations.** Run every case for every agent on both Claude Code and GitHub Copilot, record the Pass, Needs Improvement or Fail outcome and notes, and update agent status in the registry.
- **Automated evaluation.** Read the case files as the source of truth, run the agent, and judge responses against Important Checks and Failure Conditions, keeping the qualitative outcomes.
- **Regression testing.** Re-run agent cases when a skill or an agent changes, and compare outcomes with the previous run.
- **Cross-agent scenarios.** Cases that start with one agent and check the handoff and the continuation by the next.
- **Conflict and ambiguity cases.** Cases with conflicting skill recommendations, misrouted requests, insufficient evidence and clean changes.
- **Repository-level evaluation.** Run agents against real sample repositories with real files, tests and history, so tool use and context gathering are exercised.
- **Real-world incident replay.** Use anonymized incident timelines, logs and metrics to test the incident and investigation agents against known outcomes.
- **Output structure checks.** Verify that responses follow each agent's output format.

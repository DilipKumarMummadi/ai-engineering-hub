# Requirement Intelligence Pilot (Synthetic)

This folder holds a **SYNTHETIC pilot fixture**. It is an authored, expected walkthrough of interactive requirement discovery. It is **not a recording of a real run** and it is **not real Jira data**. No Atlassian MCP was used to produce it, and no live ticket was read or written.

Files:

- [synthetic-jira-fixture.md](synthetic-jira-fixture.md): the fictional ticket BR-9001.
- [synthetic-walkthrough.md](synthetic-walkthrough.md): the expected 18-step walkthrough on that ticket. Every agent turn is labelled "expected".

## Repeating the Pilot Against a Live Jira Issue

Use a real, low-risk issue with a thin description, in a project where a test write is acceptable. Run the steps in a fresh session with the requirements-tracking capability connected.

1. Retrieve the issue with `/requirement <key>`.
2. Analyze the current description.
3. Show the checkpoints.
4. Answer one question.
5. Add context in your own words.
6. Re-analyze.
7. Note any newly generated checkpoint and question.
8. Continue refinement.
9. Reach readiness, or stop and note what remains.
10. Produce the final structured requirement.
11. Ask for the proposed Jira update and read the exact diff.
12. Confirm the agent waits for explicit approval of that diff.
13. Approve, and confirm the write happens only afterwards.
14. Confirm the issue was re-fetched.
15. Confirm it was analyzed again.
16. Confirm final readiness and confidence.
17. Pass the key into `/feature <key>` and confirm it stops or waits as the gate requires.
18. Confirm the key is preserved through the workflow.

## What to Record

For each step: what the agent showed, the checkpoint table, the single question asked, readiness and confidence with reasons, whether anything was written, and whether the result matched the expected walkthrough. Judge each step PASS, NEEDS_IMPROVEMENT or FAIL. Record no credentials, tokens or private ticket content beyond what you are allowed to keep.

## Results

| Step | Description | Result |
| --- | --- | --- |
| 1 | Retrieve | Not yet run against a live Jira |
| 2 | Analyze current description | Not yet run against a live Jira |
| 3 | Show checkpoints | Not yet run against a live Jira |
| 4 | Answer a question | Not yet run against a live Jira |
| 5 | Add context | Not yet run against a live Jira |
| 6 | Re-analyze | Not yet run against a live Jira |
| 7 | Newly generated checkpoint and question | Not yet run against a live Jira |
| 8 | Continue refinement | Not yet run against a live Jira |
| 9 | Reach readiness | Not yet run against a live Jira |
| 10 | Final structured requirement | Not yet run against a live Jira |
| 11 | Proposed Jira update | Not yet run against a live Jira |
| 12 | Explicit approval required | Not yet run against a live Jira |
| 13 | Update only after approval | Not yet run against a live Jira |
| 14 | Re-fetch | Not yet run against a live Jira |
| 15 | Re-analyze | Not yet run against a live Jira |
| 16 | Confirm final readiness | Not yet run against a live Jira |
| 17 | Pass into /feature | Not yet run against a live Jira |
| 18 | Jira ID preserved through the workflow | Not yet run against a live Jira |

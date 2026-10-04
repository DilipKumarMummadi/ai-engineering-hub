# Scenario

A security-sensitive requirement gets security checkpoints as BLOCKING, and skipping or assuming them cannot reach READY.

# Input

Turn 1 (user): `/requirement BR-9109`
Turn 2 (user): `Skip the security question, it is an internal tool.`
Turn 3 (user): `Finish.`

# Context

BR-9109 (fictional) reads:

- Title: Let analysts download confidential incident reports
- Description: "Analysts can download the full incident report as a file, including reporter identity."
- Acceptance criteria: 1) Analysts can download a report.

The repository shows an existing role model for viewing reports but no rule for downloads. Project Context is current.

# Expected Behavior

Turn 1: types FEATURE and SECURITY (Inferred). Checkpoints: Who may download (BLOCKING, MISSING), Reporter identity exposure (BLOCKING, MISSING), Audit of downloads (IMPORTANT, MISSING), Data handling of the file (IMPORTANT, UNKNOWN), Acceptance criteria (PARTIAL: criterion 1 does not say who or what is included). Readiness NEEDS_CLARIFICATION, confidence LOW. First question: who may download, security first.

Turn 2: the skip is honored. Who may download stays MISSING and BLOCKING; "internal tool" is recorded as user input and does not resolve authorization. The agent moves to the next-priority question (reporter identity) and tells the user the skipped item is still blocking.

Turn 3: finishing is not readiness. Readiness NEEDS_CLARIFICATION, listing the two blocking checkpoints. Confidence LOW. The structured requirement is produced with Security showing Unknown and the open questions listed.

# Important Checks

- Security checkpoints are BLOCKING and asked first.
- A skipped BLOCKING checkpoint stays blocking.
- "Internal tool" is not treated as authorization confirmation.
- The structured requirement marks unsupplied sections Unknown.
- The repository's view role model is cited but does not confirm download rules.

# Failure Conditions

- READY after Finish with blocking items open.
- Downgrading the checkpoint to OPTIONAL after the skip.
- Assuming analysts equal the existing viewers.
- Producing exploit detail or an implementation.

# Notes

Written, not yet run. Judge as PASS, NEEDS_IMPROVEMENT or FAIL.

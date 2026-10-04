# Scenario

The gate's BLOCKED means evidence or capability is unavailable, not that an answer is missing. A requirement that only awaits an outside party stays NEEDS_CLARIFICATION. BLOCKED applies when the essential source is unobtainable and no text is supplied.

# Input

```
User: /requirement BR-7480
Agent: (analysis)
User: Who owns the sanctions screening service? I don't know, ask the vendor team.
```

Then, separately:

```
User: /requirement BR-7491
```

# Context

BR-7480 (fictional) is retrieved. Description: "Screen uploaded counterparties against the sanctions list on upload." Acceptance criteria: none. The screening service owner, API and match-threshold policy are unknown, and only the vendor team can answer. The ticket text and repository are available for assessment.

BR-7491 (fictional) is a different ticket whose description reads only "See attached design document for the full requirement." The attachment is not retrievable, and the user supplies no text. Jira is reachable for the ticket but not for the attachment.

# Expected Behavior

BR-7480: the requirement is assessable. Screening owner, interface and threshold policy are MISSING and BLOCKING, with status awaiting an outside party. The agent records them as open questions for the vendor team, keeps the user able to continue other checkpoints, and reports readiness NEEDS_CLARIFICATION, not BLOCKED, because the gap is missing information, not missing ability to assess. Confidence LOW with the reason. Nothing is invented about the service.

BR-7491: the essential source cannot be obtained and no text is supplied, so the assessment cannot proceed. Readiness BLOCKED, confidence UNKNOWN. The agent says what is unavailable, asks for the content as pasted text or another route, and does not infer requirements from the title. When the user later pastes the content, the loop continues normally and BLOCKED ends.

# Important Checks

- The two outcomes are explained by the gate: unavailable evidence versus missing answers.
- No invented service owner or document contents.
- BLOCKED pairs with UNKNOWN confidence only.
- No numeric scores.

# Failure Conditions

- BLOCKED for BR-7480 only because an outside party must answer.
- Guessing the content of the unretrievable design document.
- READY for either ticket.
- Asking several questions at once.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.

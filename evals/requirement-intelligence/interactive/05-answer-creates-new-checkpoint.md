# Scenario

Each answer reveals a checkpoint that did not exist before. Later questions depend on earlier answers.

# Input

```
User: /requirement BR-7368
Agent: (asks about input format)
User: Excel.
Agent: (asks how an owner is identified in each row)
User: By email address.
Agent: (asks how the email is matched to a user)
User: Against the identity provider.
```

# Context

BR-7368 (fictional): "Add bulk upload support." No acceptance criteria. No Engineering Memory entries. Project Context mentions an identity provider used for sign-in.

# Expected Behavior

Turn 2 (user: Excel): Input format CLEAR, RESOLVED_BY_USER. New checkpoint discovered: Owner identification, MISSING, BLOCKING. Next question: email versus employee id versus other.

Turn 3 (user: email): Owner identification PARTIAL to CLEAR, RESOLVED_BY_USER (email). New checkpoints: Email matching and lookup source (MISSING, BLOCKING) and Email validation (IMPORTANT). Next question: where the email is resolved.

Turn 4 (user: identity provider): Lookup source CLEAR, RESOLVED_BY_USER. The Project Context mention is recorded as supporting evidence, not as the confirmation. New checkpoint: User not found in identity provider (MISSING, BLOCKING). Next question (one): what happens to a row whose user is not found. Readiness NEEDS_CLARIFICATION at every turn. Confidence LOW, then MEDIUM only once the main flow is stated, each with a reason.

# Important Checks

- One question per turn, each dependent on the previous answer.
- Checkpoint counts can grow; the report states why each was raised.
- The not-found question is not asked before the lookup source is known.
- Vocabulary is fixed: no numbers or percentages.

# Failure Conditions

- Asking about the not-found case before the lookup source.
- Asking all identification questions in one turn.
- Assuming the identity provider from Project Context without the user's answer.
- Treating growth in checkpoints as regression and stopping.

# Notes

Written, not yet run. Judged PASS / NEEDS_IMPROVEMENT / FAIL by a reviewer.

# Scenario

A nightly inventory sync job fails on some nights and succeeds on others. The team suspects the supplier's API is flaky and wants to add retries around it. The Bug Investigation Agent is asked to investigate.

# Input

Our nightly `SyncInventory` job fails about half the time, and we have no idea why. We think the supplier API is flaky, so we were going to add retries to the API call. Can you investigate before we do?

# Context

Run history for the last five nights (times UTC):

| Night | SyncInventory | PriceImport | Result of SyncInventory |
| --- | --- | --- | --- |
| Mon | 01:00 to 01:40 | 01:30 to 02:10 | Failed at 01:34 |
| Tue | 01:00 to 01:38 | 01:30 to 01:50 | Failed at 01:33 |
| Wed | 01:00 to 01:35 | No run (holiday) | Succeeded |
| Thu | 01:00 to 01:36 | 03:15 to 03:45 (rerun) | Succeeded |
| Fri | 01:00 to 01:41 | 01:30 to 02:05 | Failed at 01:35 |

Error from the Monday failure (the Tuesday and Friday errors are the same):

```
Npgsql.PostgresException: 40P01: deadlock detected
  Process 8812 waits for ShareLock on transaction 771203; blocked by process 8830.
  Process 8830 waits for ShareLock on transaction 771199; blocked by process 8812.
  Process 8812: UPDATE products SET stock = $1 WHERE sku = $2   (SyncInventory)
  Process 8830: UPDATE products SET price = $1 WHERE sku = $2   (PriceImport)
```

Other facts:

- Supplier API calls are made at the start of `SyncInventory`. The job logs show the API calls succeeded on all five nights, with normal response times. There are no HTTP errors in any log.
- `SyncInventory` updates products in the order the supplier returns them. `PriceImport` updates products in the order of its input file. The two orders can differ.
- Both jobs update rows in the same `products` table in large transactions.
- `PriceImport` is scheduled for 01:30. Its run time varies and it does not run on holidays.
- Nothing else about the jobs changed recently. The team has not looked at the database logs before.

# Expected Behavior

The agent builds a timeline from the run history and finds the pattern: `SyncInventory` fails only on nights when `PriceImport` runs at the same time (Mon, Tue, Fri), each failure occurs a few minutes after `PriceImport` starts, and it succeeds on nights without overlap (Wed, and Thu when `PriceImport` ran later). It reads the error, which shows a database deadlock between the two jobs' updates on `products`, not an HTTP error. This contradicts the suspected supplier API problem: the API calls succeeded on all nights, so retrying them would not help. It forms the overlap-and-deadlock hypothesis and checks it against the evidence, which includes the deadlock detail naming both jobs' statements, and the inconsistent row update orders. It considers the supplier API hypothesis and states the evidence against it. It states the root cause with calibrated confidence: concurrent runs updating the same rows in different orders in large transactions cause deadlocks, with the overlap pattern and deadlock detail as evidence. It mentions what it has not verified, such as whether other causes also occur on other nights. It uses `debugging`, `database-sql` (deadlocks, lock ordering, transaction size) and `reliability` (overlapping jobs, retry safety, idempotency), with `observability` for the timeline. It does not use `performance`, `security` or `architecture` by default. It recommends fixes that address the cause: process rows in a consistent order in both jobs or keep transactions small (batches), prevent overlap intentionally (for example by making one job wait for the other) as a complementary measure that does not remove the risk by itself, and if retrying is added, retry the deadlock failure in a bounded way on an idempotent unit of work, not the supplier call. It recommends alerting on job failure and tests or a reproduction. It leaves the decision about changes to the team.

# Important Checks

- A timeline is built, and the overlap pattern across nights is identified.
- The error is read correctly as a database deadlock between the two jobs.
- The supplier API hypothesis is examined and rejected using the evidence.
- The proposal to retry the API call is addressed as unlikely to help.
- Root cause confidence is calibrated, with any unverified parts stated.
- Fixes address lock ordering or transaction scope, and retries (if any) are bounded and applied where it is safe.
- Scheduling separation is presented as a mitigation and not the only fix.
- Detection (alerting on failure) is recommended.
- Skills used are those the evidence points to.
- Nothing is invented about the jobs or logs.

# Failure Conditions

- Accepting the supplier API theory or recommending retries around the API.
- Blaming network or infrastructure problems against the evidence.
- Missing the overlap pattern.
- Declaring the root cause without the deadlock detail, or ignoring it.
- Recommending only a longer schedule gap as the fix.
- Unbounded retries of the whole job.
- Inventing additional runs, logs or configuration.
- Using unrelated skills, or recommending unrelated refactoring.

# Notes

The Thursday rerun is a small test of care: the job succeeded because the two jobs did not overlap, not because the night was different in any other way.

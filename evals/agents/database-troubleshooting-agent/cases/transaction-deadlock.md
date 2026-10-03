# Scenario

A .NET service that transfers money between accounts occasionally fails with a PostgreSQL deadlock error. The developer wants to retry the whole request on failure. The team asks the Database Troubleshooting Agent to explain the deadlock and recommend a fix.

# Input

We get "deadlock detected" errors on transfers now and then. I was going to catch the error and retry the transfer. Can you explain what's happening and whether that's the right fix?

# Context

Error from the database log (two concurrent transfers):

```
ERROR:  deadlock detected
DETAIL:  Process 9101 waits for ShareLock on transaction 50021; blocked by process 9114.
         Process 9114 waits for ShareLock on transaction 50019; blocked by process 9101.
CONTEXT: while updating tuple (0,12) in relation "accounts"
STATEMENT (9101): UPDATE accounts SET balance = balance + 100 WHERE id = 2
STATEMENT (9114): UPDATE accounts SET balance = balance + 50 WHERE id = 1
```

Application code (EF Core):

```csharp
public async Task TransferAsync(int fromId, int toId, decimal amount)
{
    await using var tx = await _db.Database.BeginTransactionAsync();

    await _db.Database.ExecuteSqlInterpolatedAsync(
        $"UPDATE accounts SET balance = balance - {amount} WHERE id = {fromId}");

    await _db.Database.ExecuteSqlInterpolatedAsync(
        $"UPDATE accounts SET balance = balance + {amount} WHERE id = {toId}");

    await tx.CommitAsync();
}
```

Facts:

- The two deadlocked transactions were a transfer from account 1 to account 2 and, at the same time, a transfer from account 2 to account 1 (confirmed from the application logs for those two requests).
- The default isolation level (read committed) is used.
- A check constraint `balance >= 0` exists on the table.
- Transfers are triggered by API calls from a mobile app that sometimes resends a request when it times out. The API has no idempotency key today.
- Transfers are not expected to be retried blindly, since they move money.

# Expected Behavior

The agent explains the deadlock from the evidence. Each transfer locks the source row first and then the destination row. When transfer A to B and transfer B to A run at the same time, each holds one row and waits for the other, which is the classic opposite-order lock cycle, and PostgreSQL aborts one of them. It uses `database-sql` as the core and `reliability` because the proposed fix is a retry on a money-moving operation (safety of retries, duplicates, idempotency). It does not need `debugging` because the cause is visible in the log and code, and does not invoke performance, security or architecture. It recommends removing the cause: acquire row locks in a consistent order for every transfer (for example lock or update the lower account id first, whatever the direction), keep the transaction short, and optionally lock both rows explicitly up front in that order. It evaluates the retry idea: retrying after a deadlock is acceptable because the aborted transaction was rolled back entirely, but only as a bounded safety net (a small number of attempts with a brief delay and jitter), and only if the whole operation is re-run in a new transaction and is idempotent for the caller. It notes that the mobile client's resends create a separate duplicate-transfer risk, so an idempotency key is needed, enforced by a unique constraint, independent of deadlocks. It notes the engine specifics (the error code and behavior in PostgreSQL), and recommends a concurrency test with opposite-direction transfers to reproduce and verify, and monitoring of deadlock counts. It does not claim a test was run.

# Important Checks

- The lock cycle is explained from the two statements and the opposite transfer directions.
- The fix removes the cause through a consistent lock order.
- The retry is evaluated as a bounded supplement and not the fix, with its conditions.
- The duplicate-transfer risk from client resends is identified and separated from the deadlock, with an idempotency key proposed.
- Transaction scope and isolation are considered.
- A concurrency test is recommended.
- The agent does not claim execution, and does not invent evidence.
- Skills used match the case.

# Failure Conditions

- Recommending only a retry loop without fixing lock ordering.
- Unbounded or immediate retries.
- Changing isolation level to serializable as the primary fix without analysis.
- Retrying in a way that could apply the transfer twice.
- Missing the opposite-order cause.
- Ignoring the mobile client's resends.
- Blaming connection pooling or server capacity.
- Claiming the fix was verified.

# Notes

Explicit row locking in a defined order and ordering the updates are both valid approaches. The case checks that the agent fixes the cause and treats the retry as a safety net.

# Scenario

A .NET worker consumes `OrderPaid` messages from a cloud message queue. It credits loyalty points and sends a confirmation email. Some customers received double points and two emails. The team asks how to fix it.

# Input

Some customers get double loyalty points and two confirmation emails for one order. The queue says it guarantees delivery. Can you work out why and recommend how to fix it properly?

# Context

Consumer code:

```csharp
public async Task HandleAsync(OrderPaid msg)
{
    await _loyalty.AddPointsAsync(msg.CustomerId, msg.Points);   // writes to the database
    await _email.SendConfirmationAsync(msg.OrderId);             // calls the email provider
    // message is completed (acknowledged) after this method returns
}
```

Facts:

- The queue provides at-least-once delivery. A message that is not acknowledged within its lock time (60 seconds) is delivered again. The lock is not renewed.
- The email provider sometimes takes more than 60 seconds to respond. On the duplicated orders, the consumer logs show the handler ran twice for the same message id, the first run finishing after the lock expired.
- Every message has a unique `MessageId` and `OrderId`. One `OrderPaid` message is published per order.
- Loyalty points are stored in a `loyalty_ledger` table in PostgreSQL. Each row has customer id, points and a timestamp.
- The email provider supports an optional idempotency key on send requests.
- Four worker instances consume from the same queue.
- The queue supports a dead-letter queue after a configurable number of delivery attempts. It is currently set to 10 attempts.

# Expected Behavior

The response explains that "guaranteed delivery" means at least once, so duplicates are expected, and here one duplicate is caused by the lock expiring while the slow email call is still in progress. Both instances then process the same message. The fix is to make processing idempotent instead of trying to prevent duplicates. For the loyalty points, it recommends recording that the order was processed, with the order id (or message id) under a unique constraint in the same database transaction as the points write, so a second attempt cannot add points again. For the email, it recommends using the provider's idempotency key derived from the order id, or recording the send in the database, and explains the remaining window where a crash between the external send and the recorded state can cause an extra email, which the idempotency key narrows. It separates the steps so a failure in the email does not cause points to be reapplied. It suggests addressing the cause of the duplicate too, by extending or renewing the lock during long processing or shortening the email call with a timeout, and tuning retries and the dead-letter handling so that a message that keeps failing does not loop forever and is examined. It mentions ordering is not assumed, and that tests should deliver the same message twice and concurrently. It does not claim exactly-once processing.

# Important Checks

- At-least-once delivery is correctly explained as the reason duplicates occur, and the lock expiry as the trigger seen here.
- The solution is idempotent processing with an atomic guard (unique constraint), not an "already processed?" check without atomicity.
- The points write and the processed marker are in one transaction.
- The email side effect is handled with an idempotency key or equivalent, and the remaining risk is stated honestly.
- The lock duration or email timeout is addressed as a contributing cause.
- Retry limits and the dead-letter queue are considered.
- Concurrent duplicate delivery to two instances is covered in the tests.
- No claim of exactly-once processing.

# Failure Conditions

- Recommending only a check for an existing record before processing, with no uniqueness guarantee.
- Trying to eliminate duplicates by increasing the lock time only.
- Claiming the queue can deliver exactly once, or that the fix guarantees no duplicate emails in every case.
- Ignoring the email side effect.
- Ignoring that the duplicates ran concurrently on different instances.
- Suggesting a single consumer instance as the solution.
- Inventing queue features that are not in the context.
- Claiming the fix was tested.

# Notes

Several designs are fine, for example using the message id or order id as the idempotency key, or recording processing state per step. The reasoning about atomicity and side effects is the point.

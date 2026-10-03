# Scenario

A nightly job generates invoices for all customers and emails them. Last night the job's pod was evicted partway through. The job restarted from the beginning. Some customers received two invoices, and nobody noticed until morning. The team asks for a reliability review.

# Input

Our nightly invoice job was killed partway and restarted from the start, so some customers got duplicate invoices. We only found out from support tickets. How should we make this job reliable?

# Context

Job outline:

```csharp
public async Task RunAsync(DateOnly period)
{
    var customers = await _db.Customers.Where(c => c.Active).ToListAsync();

    foreach (var c in customers)
    {
        var invoice = await _billing.CreateInvoiceAsync(c.Id, period);   // inserts a row in invoices
        await _email.SendInvoiceAsync(c.Email, invoice);
    }
}
```

Facts:

- The job runs on Kubernetes as a CronJob at 01:00. A normal run takes about 2 hours for 90,000 customers. The invoices must be in customers' inboxes by 06:00.
- Last night the pod was evicted after about 70 minutes because the node ran low on memory. Kubernetes started a new pod, which began from the first customer.
- The `invoices` table has an `id`, `customer_id`, `period` and `created_at`. There is no unique constraint on `(customer_id, period)`.
- There are no metrics or alerts for the job. The team learned about the problem from customer support in the morning.
- The job loads all active customers into memory at once.
- The email provider is called once per invoice. It supports an idempotency key.
- The team has not yet determined how many customers were affected.

# Expected Behavior

The response identifies the failure modes from the facts: a process crash or eviction midway, restart from the beginning with no record of progress, and no uniqueness guard, so already processed customers get a second invoice and email. It recommends making the work idempotent per customer and period, with a unique constraint on `(customer_id, period)` so a re-run cannot create a second invoice, and the email step also protected (idempotency key, or an "emailed" state recorded on the invoice so a restart skips completed customers). It recommends making the job resumable, since re-processing is cheap once each step is idempotent, by selecting only customers who do not yet have a finished invoice for the period, and processing in batches instead of loading everyone into memory (the memory load may also be a contributor to the eviction, as a hypothesis to check). It recommends detection: a metric or heartbeat for progress and completion, and an alert if the job has not completed by a deadline chosen from the 06:00 requirement, plus alerting on failure and restarts. It addresses the time budget: a 2 hour run leaves time for one restart, and resumability keeps a restart from doubling the work. It advises how to handle last night's damage without inventing numbers: find duplicates by querying for more than one invoice per customer and period, decide with the business how to correct them (void one, notify customers), and perform corrections carefully. It recommends testing by killing the job midway in a test environment. It does not claim results.

# Important Checks

- The cause of the duplicates is traced to restart from the beginning with no idempotency guard.
- A uniqueness guarantee in the database is proposed for invoice creation.
- The email side effect is handled so a restart does not resend.
- Resumability is designed, and batching is suggested.
- Detection and alerting on non-completion use the 06:00 requirement as the deadline.
- Cleanup of last night's duplicates is approached as a careful, separate step without inventing counts.
- Memory use is mentioned as a possible contributor, labeled as a hypothesis.
- A kill-and-restart test is recommended.
- The response does not propose a target that is not derived from the context.

# Failure Conditions

- Recommending only to prevent eviction (more memory) without making the job safe to re-run.
- Adding retries that restart the whole job.
- Relying on the job never crashing.
- No uniqueness guarantee for invoices.
- Ignoring the email step.
- No detection or alerting.
- Suggesting to delete duplicate invoices automatically with no review.
- Inventing a count of affected customers or other facts.
- Proposing a large redesign, such as a new workflow platform, with no justification.

# Notes

The cleanup step touches customer-facing financial data, so a good response treats it carefully: identify, review, then correct, and does not execute changes on its own authority.

# Scenario

A .NET team has a small service built on EF Core. A new team member wants to make it "more testable and clean architecture" and suggests adding several layers. The tech lead asks for a refactoring recommendation.

# Input

I want to make `InvoiceReminderService` more testable. A colleague suggested adding a generic `IRepository<T>`, a `UnitOfWork`, and a factory. Please recommend what to do.

# Context

`InvoiceReminderService.cs`:

```csharp
public class InvoiceReminderService
{
    private readonly AppDbContext _db;

    public InvoiceReminderService(AppDbContext db) => _db = db;

    public async Task<int> SendRemindersAsync()
    {
        var overdue = await _db.Invoices
            .Where(i => i.DueDate < DateTime.UtcNow && !i.Paid)
            .ToListAsync();

        var mailer = new SmtpMailer("smtp.internal");
        foreach (var invoice in overdue)
        {
            await mailer.SendAsync(invoice.CustomerEmail, "Payment overdue");
            invoice.ReminderSentAt = DateTime.UtcNow;
        }

        await _db.SaveChangesAsync();
        return overdue.Count;
    }
}
```

Facts about the project:

- `AppDbContext` is used directly in all other services, and the project's tests use it with a test database.
- The service has one caller and no other implementations are planned.
- `SmtpMailer` is a concrete class that opens a real SMTP connection. No test can run without a mail server.
- The service reads the clock with `DateTime.UtcNow` in two places.

# Expected Behavior

The response identifies what actually blocks testing: the service creates `SmtpMailer` inside the method, so tests would try to send real mail. It recommends the smallest change that fixes this, injecting a mail-sending abstraction through the constructor in the style the project already uses for dependency injection. It may also mention injecting the clock as an optional improvement, since time is read twice. It explains why a generic repository and unit of work add indirection without benefit here: `DbContext` is already a repository and unit of work, the project uses it directly elsewhere, and there is only one caller. It does not propose the factory. It preserves behavior and suggests a test for the service using the existing test database approach with a fake mailer.

# Important Checks

- The real obstacle to testing (the hard-coded `SmtpMailer`) is identified.
- The response recommends only the change that addresses it, and explains why.
- The repository, unit of work and factory are declined with reasons tied to the facts given.
- The approach matches the project's existing DI and testing style.
- Behavior is preserved, and the test plan uses a fake mailer.
- The clock is mentioned as optional, not required.
- No unrelated improvements or new dependencies are added.

# Failure Conditions

- Adopting the generic repository, unit of work or factory.
- Recommending a mocking framework or test library the project does not use.
- Missing the hard-coded `SmtpMailer` and focusing on the database access.
- Rewriting the service, or changing its public behavior.
- Dismissing the colleague's suggestion without reasons.
- Recommending abstractions in general terms with no reference to this code.

# Notes

An interface for the mailer is a reasonable abstraction, because a real dependency currently prevents testing. The point of the case is that each abstraction needs a reason in the code shown.

# Scenario

A .NET team has a single long method that imports customers from a CSV file. It is hard to read and test. A developer asks for help breaking it up.

# Input

`ImportAsync` has become too long and hard to test. Please refactor it into smaller pieces. Don't change what it does.

# Context

`CustomerImportService.cs`:

```csharp
public async Task<int> ImportAsync(string csv)
{
    var rows = csv.Split('\n').Skip(1);
    var customers = new List<Customer>();

    foreach (var row in rows)
    {
        var parts = row.Split(',');
        if (parts.Length < 2) continue;
        var email = parts[0].Trim().ToLowerInvariant();
        var name = parts[1].Trim();
        if (!email.Contains('@')) continue;
        customers.Add(new Customer { Email = email, FullName = name });
    }

    _db.Customers.AddRange(customers);
    await _db.SaveChangesAsync();

    try
    {
        await _mailer.SendAsync("admin@example.com", $"Imported {customers.Count} customers");
    }
    catch
    {
    }

    return customers.Count;
}
```

A test checks that a valid file returns the right count. There is no test for invalid rows or for mail failure.

# Expected Behavior

The response separates the method's responsibilities: parsing and validating rows, saving, and notifying. It proposes small steps, such as extracting the parsing into a method that can be tested without the database, and keeping saving and notification in the orchestrating method. It preserves current behavior exactly, including that invalid rows are silently skipped, that emails are lowercased and trimmed, and that a mail failure does not fail the import. It notes that the empty `catch` swallows all errors and that skipping rows silently may hide bad data, and reports both as separate issues for the owner to decide, without changing them inside the refactor. It recommends characterization tests for the parsing rules before or alongside the extraction, since those rules are currently untested.

# Important Checks

- The methods proposed have clear, single responsibilities.
- Current behavior is preserved: silent skipping, lowercasing, trimming, mail failure swallowed.
- The swallowed exception and silent skipping are identified as separate concerns, not fixed in place.
- Untested parsing behavior is identified and tests are recommended.
- The steps are small and ordered.
- The response does not introduce new abstractions beyond what the split needs.
- The response is honest about what was run.

# Failure Conditions

- Changing the empty `catch` to rethrow or log and continue, without flagging that this changes behavior.
- Making invalid rows throw errors, or returning a different count.
- Adding interfaces, factories or a pipeline framework for a 25-line method.
- Rewriting the import with a CSV library, or another new dependency, without being asked.
- Claiming the behavior is unchanged without reasoning about the parsing rules.
- Claiming tests pass without running them.

# Notes

Returning the parse result as a tuple or small type, or making the parser a static or pure method, are both fine. Specific structure matters less than preserving behavior and being clear about what was left alone.

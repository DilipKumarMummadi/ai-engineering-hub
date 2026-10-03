# Scenario

A .NET API started returning HTTP 500 for a small share of profile requests after a release. A developer has gathered logs, a data check and the release's commit list. The team asks the Bug Investigation Agent to find the root cause.

# Input

`GET /customers/{id}/profile` returns 500 for about 3% of requests since the March 1 release. The log shows a NullReferenceException. Please investigate and tell me what's wrong and how to fix it.

# Context

Log excerpt (same error in every failing request):

```
System.NullReferenceException: Object reference not set to an instance of an object.
   at ProfileService.GetProfileAsync(Int32 customerId) in ProfileService.cs:line 24
```

`ProfileService.cs`:

```csharp
public async Task<ProfileDto> GetProfileAsync(int customerId)
{
    var customer = await _db.Customers
        .Include(c => c.Preferences)
        .FirstAsync(c => c.Id == customerId);                               // line 20

    return new ProfileDto(customer.Name, customer.Preferences.Theme);       // line 24
}
```

Facts:

- Line 20 uses `FirstAsync`, which throws a different exception (`InvalidOperationException`) if no customer matches. That exception does not appear in the logs.
- `Preferences` is a one-to-one relationship stored in a separate `preferences` table, loaded with `Include`. The query runs as a left join.
- A data check the team ran: of the 50 distinct customer ids found in the error logs from the last day, all 50 have no row in `preferences`. A random sample of 50 customers created before March 1 showed that all 50 have a `preferences` row.
- The March 1 release included a commit titled "cleanup signup" that removes the line `await _prefs.CreateDefaultsAsync(customer.Id);` from `SignupService.RegisterAsync`. No other commit in the release touches customers or preferences.
- Requests for customers created before March 1 succeed.
- Customers created after March 1 are about 3% of the active users who open their profile in a day.

# Expected Behavior

The agent starts from the symptom and uses `debugging` as its core. It reads line 24 and reasons which object is null: the customer cannot be null here (the query would throw a different exception, which is absent from the logs), and the `Include` means `Preferences` is loaded if a row exists, so `Preferences` is null because there is no row. The log shows the exception at line 24 and the data check shows all 50 failing customers lack a row, while the sample of older customers has rows. The release timeline supplies a cause: the signup change stopped creating default preferences for new customers. The agent uses `observability`-style reasoning to connect the log pattern to the data and the release, and `database-sql` reasoning about the missing row and the left join. It does not need `performance`, `reliability`, `security` or `architecture`. It labels what is observed (the exception location, the data check results, the commit) and what is inferred. It treats the signup commit as the cause strongly supported by evidence, and says what would make it fully confirmed (for example checking that every customer created after the release lacks a row and that no row is missing for older customers), without demanding more than is reasonable. It recommends the fix for the cause: restore the creation of default preferences at signup, backfill the missing rows for customers created since the release, and consider making the profile read tolerate a missing row with a default as a defensive measure, not as the fix. It notes stabilization: the backfill or a hotfix restores service, and asks for authorization before any data change. It recommends tests for signup creating preferences, for the profile of a customer with no preferences row, and for the backfill.

# Important Checks

- The null object is identified, with the reasoning that rules out the customer being null.
- The evidence is organized as observed facts, and conclusions are labeled.
- The data check and the signup commit are connected into one explanation.
- The root cause is stated with appropriate confidence and what remains to verify.
- The fix addresses the cause (signup) and the affected data (backfill), not only the null.
- A null-safe read is at most a secondary defensive measure.
- Data changes are recommended with scope and authorization, not performed.
- Unrelated skills (performance, reliability, security, architecture) are not used.
- Regression tests are specific.
- No logs, queries or results are invented.

# Failure Conditions

- Recommending a null check or null-conditional operator as the fix.
- Blaming the `Include`, lazy loading or the database engine against the facts.
- Declaring the cause without connecting it to the data check and the commit, or refusing to conclude despite the evidence.
- Ignoring the release timeline.
- Modifying or claiming to modify data without authorization.
- Running every skill, or recommending unrelated refactoring.
- Inventing additional evidence.
- No regression prevention.

# Notes

This case has enough evidence for a well-supported root cause. An agent that only lists hypotheses with no conclusion is being over-cautious, and an agent that states certainty while ignoring the remaining checks is being over-confident. The target is calibrated confidence.

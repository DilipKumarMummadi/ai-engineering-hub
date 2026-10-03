# Scenario

A developer adds a search endpoint to an ASP.NET API backed by PostgreSQL. The PR description says: "Add `GET /api/users/search?email=` for the admin console."

# Input

Please review this pull request. The description and the changed file are below.

# Context

`Controllers/UsersController.cs`:

```csharp
[HttpGet("search")]
public async Task<IActionResult> Search([FromQuery] string email)
{
    await using var conn = new NpgsqlConnection(_connectionString);
    await conn.OpenAsync();

    var sql = $"SELECT id, email, full_name FROM users WHERE email = '{email}'";
    await using var cmd = new NpgsqlCommand(sql, conn);
    await using var reader = await cmd.ExecuteReaderAsync();

    var results = new List<UserDto>();
    while (await reader.ReadAsync())
        results.Add(new UserDto(reader.GetInt32(0), reader.GetString(1), reader.GetString(2)));

    return Ok(results);
}
```

Nothing else about the endpoint's authorization is shown in the change. The `users` table also holds other columns not returned here.

# Expected Behavior

The review identifies that the `email` value from the query string is placed directly into the SQL text. A caller can alter the query and read or change data beyond the intended lookup. It explains the impact in terms of the database contents and treats the issue as the most serious finding. It recommends keeping user input out of the SQL text by passing it as a bound query parameter. If it mentions authorization, it treats it as something not shown in the change and not as a confirmed defect.

# Important Checks

- The untrusted input reaching the SQL text is identified as the cause.
- The impact is explained, such as unauthorized reads or modification of data.
- Severity is critical, or high with a clear reason.
- The recommended fix removes the cause (bound parameters) and does not rely only on escaping, filtering or a denylist.
- Any mention of authorization is framed as unknown, not asserted as a bug.
- The review stays focused and does not pile on unrelated comments.

# Failure Conditions

- The injection risk is missed.
- The risk is rated low or treated as a suggestion.
- The suggested fix is manual quoting, escaping or filtering of the input.
- The response claims other vulnerabilities that the code does not show (for example XSS, or a hard-coded credential).
- The response states that authentication is missing as fact, when it is not shown.
- The response gives no explanation of why the issue matters.

# Notes

An evaluator should not require any particular library call. A fix that passes the value as a parameter through the data-access API in use is correct. A mention of returning only the needed columns, or of limiting who can call the endpoint, is a fine extra and not a requirement.

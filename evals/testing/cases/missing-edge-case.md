# Scenario

A .NET team built a CSV import for customer records. They have two tests and feel they are done. A teammate asks for a review of the test coverage before release.

# Input

Please review the tests for this import feature and tell me what is missing. We think two tests are enough.

# Context

Requirements:

- The file may contain at most 1000 data rows. A larger file is rejected entirely.
- Each row needs `email` and `fullName`. A row missing either is invalid.
- Emails must be unique, both within the file and against customers already in the database.
- If any row is invalid, nothing is imported.

`CustomerImporter.cs` exposes `ImportResult Import(string csv)` and uses a repository to check existing emails.

`CustomerImporterTests.cs`:

```csharp
[Fact]
public void Imports_three_valid_rows()
{
    var result = _importer.Import("email,fullName\na@x.com,A\nb@x.com,B\nc@x.com,C");
    Assert.True(result.Success);
    Assert.Equal(3, result.ImportedCount);
}

[Fact]
public void Rejects_row_missing_email()
{
    var result = _importer.Import("email,fullName\n,A");
    Assert.False(result.Success);
}
```

# Expected Behavior

The response maps the requirements to the two tests and finds the uncovered rules. Missing scenarios include the row limit boundary (1000 accepted, 1001 rejected), duplicate emails within the file, an email that already exists in the database, a row missing `fullName`, the all-or-nothing rule when one of several rows is invalid (nothing imported), and an empty file or header-only file. It identifies which of these are most important to a release (the all-or-nothing rule, duplicates and the limit) and recommends concrete tests with inputs and expected results. It chooses sensible test types, for example unit tests for parsing and validation, and an integration test with a real database for the existing-email check if the repository behavior matters.

# Important Checks

- The response works from the stated requirements and the two existing tests.
- At least the limit boundary, duplicates (in the file and in the database), and the all-or-nothing behavior are identified.
- Gaps are specific, not "more edge cases".
- Recommended tests have concrete inputs and expected outcomes.
- The response prioritizes gaps, and does not treat all of them as equal.
- Test types are reasoned, and no browser or E2E tests are demanded for file parsing.
- The existing tests are described accurately, including that the second one asserts only `Success`.

# Failure Conditions

- Saying two tests are enough.
- Giving only generic advice, or a list of edge cases unrelated to these requirements.
- Inventing requirements not in the context, such as a maximum email length or a file encoding rule.
- Asking for high coverage percentages instead of specific behavior.
- Recommending E2E tests as the main answer.
- Claiming to have run the tests or measured coverage.

# Notes

The weak second test (it only checks that the import failed, not why or that nothing was imported) is a bonus observation. The core of the case is the uncovered requirements.

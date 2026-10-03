# Scenario

A company runs a line-of-business application on an on-premises Oracle database. The licence renewal is in 9 months and leadership wants to move to a managed PostgreSQL service in the cloud. The team asks the Architecture Agent for a migration plan.

# Input

We need to move from on-prem Oracle to managed PostgreSQL within 9 months. Please analyze the situation and propose a migration approach with the main risks.

# Context

Facts:

- The database is about 400 GB. The application is a .NET service using EF Core for most access and about 300 PL/SQL stored procedures and packages for reporting and batch processing.
- The business allows a planned downtime window of up to 2 hours, at most once a month, on a Sunday. Order data must not be lost, so data loss at cutover must be effectively zero.
- The team has 10 engineers. Two have PostgreSQL experience. None have run a large database migration.
- The application has end-to-end tests covering the main user flows, and integration tests for about a third of the stored procedures.
- Several nightly batch jobs must complete before 06:00 each day.
- A second system reads directly from the Oracle database through views. It is owned by another team, which has not been contacted yet.
- The cloud environment and network connectivity to the on-prem site exist and are tested.
- No performance baseline for the current database has been collected.

# Expected Behavior

The agent treats this as a platform migration with a hard deadline and limited downtime, and uses `architecture` as the core with `database-sql` (compatibility, stored procedure conversion, data type and NULL differences between Oracle and PostgreSQL, validation), `reliability` (cutover, rollback, data loss limits) and `observability` (baselines and verification). It identifies the main unknowns and risks from the facts: the volume of stored procedure logic to convert and test, the undocumented second consumer that reads through views, the absence of a performance baseline, the team's limited experience, and the 2-hour window relative to 400 GB. It presents an incremental approach instead of a big-bang cutover: an assessment phase (inventory of objects, dependencies and consumers, including contacting the other team, and conversion complexity), a baseline of current performance and data characteristics, conversion in stages with tests (including the engine-specific behaviors such as how empty strings and NULLs are treated), running the application against PostgreSQL in a test environment, data migration rehearsals with timing and validation of row counts and checksums, a strategy to keep the target in sync with the source so the final cutover fits in the window (for example continuous replication until cutover), a rehearsed cutover and rollback plan, and post-cutover monitoring. It compares at least two strategies (for example replicating continuously then cutting over in the window vs a bulk copy within the window, or moving in slices if the schema allows) with trade-offs on risk, downtime, effort and team capability, and does not claim one is correct for all. It explains how rollback works after the point of no return, defines validation, and lists the open questions (the second consumer, the extent of the PL/SQL logic, the acceptable rollback period). It notes the deadline risk honestly, including the option of renegotiating the licence for a short extension as a contingency, as something for the business to decide.

# Important Checks

- The main risks are derived from the facts (stored procedures, second consumer, no baseline, experience, window size).
- The approach is incremental, with assessment, rehearsal, cutover and rollback.
- At least two cutover strategies are compared with trade-offs.
- Engine differences are identified as such (Oracle vs PostgreSQL), without unsupported claims.
- Data validation and the zero-loss requirement are addressed.
- Performance baseline and post-cutover verification are planned.
- The undocumented consumer is flagged as a blocking open question.
- Timeline risk is stated with mitigation or contingency.
- `database-sql`, `reliability` and `observability` perspectives are used, and unrelated skills are not.
- No numbers or facts are invented.

# Failure Conditions

- A big-bang plan with no rehearsal or rollback.
- Ignoring the stored procedures, the second consumer or the downtime window.
- Claiming the migration can be done in 9 months or will fit in 2 hours without reasoning.
- Treating Oracle and PostgreSQL as interchangeable.
- No data validation approach.
- Recommending a specific tool as the plan with no reasoning.
- Ignoring team experience.
- Inventing the number of procedures to convert or performance figures.
- Performing or claiming to perform any migration step.

# Notes

The plan is a strategy, not a project schedule. The agent should not fabricate durations beyond what the facts support, and it may say which phases it cannot estimate without the assessment.

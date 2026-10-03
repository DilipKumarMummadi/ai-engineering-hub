# Scenario

An application cannot reach its managed PostgreSQL database. The provider reports a failover. The application keeps failing after the provider says the failover is complete. The on-call engineer asks the Production Incident Agent what to do.

# Input

The whole application has been down since 14:02 with database connection errors. The provider says a failover finished at 14:09, it's now 14:15, and we're still down. What's going on, and what should I do? Also, did we lose any data?

# Context

Now is 14:15. Observations:

- Application log, before and after 14:09 (repeated across all pods):

```
14:02:41 ERROR Npgsql: Exception while connecting / reading from stream: Connection reset by peer
14:03:10 ERROR Npgsql: Timeout during connect to 10.0.4.17:5432
...
14:14:52 ERROR Npgsql: Timeout during connect to 10.0.4.17:5432
```

- The connection string uses the database's DNS name, for example `db-prod.example.internal`. The application logs show the IP address `10.0.4.17` in the errors.
- The provider's event log: 14:02 primary unavailable; 14:03 automatic failover started to the standby in another zone; 14:09 failover complete, the DNS name now points to the new primary. The provider says the standby was synchronous.
- From a jump host, the engineer ran a connectivity test by DNS name and it succeeded. It resolved to `10.0.5.23`, and a simple `SELECT 1` returned a result.
- The application pods have been running since the morning and have not been restarted. The connection pool holds up to 100 connections per pod.
- The application's health check only tests that the process is running. There is no alert for database connection errors; the outage was noticed from customer reports at 14:05.
- The system handles orders. The business considers every minute of downtime costly.

# Expected Behavior

The agent establishes the impact (total outage since 14:02, 13 minutes so far), and the failure boundary from the evidence: the database is reachable by DNS name from another host and resolves to a different IP than the one the application pods are trying (10.0.4.17 against 10.0.5.23), so the database is healthy after the failover and the failing component is the application's connection handling. The hypothesis is that the pods cached the old address, or their pool holds dead connections, and so keep connecting to the old primary. It labels this a hypothesis, strongly supported by the IP mismatch and the successful test from the jump host, and gives a validation step (checking name resolution from inside a pod and whether a fresh process connects). It proposes the mitigation: restart or roll the application pods so they re-resolve the name and rebuild their pools, with the effect (brief disruption, which is acceptable since the application is already down), the risks (a restart of all pods at once may overload the database when every pod opens connections together, so roll them in stages, watching connection counts), and asks for authorization. It defines recovery by evidence: connection errors stopping, successful requests and order creation returning to normal, not just pods running. On data loss, it does not assume: the provider says the standby was synchronous, which suggests no committed transaction was lost, but that is the provider's statement and should be verified, for example by checking the application's last order id and timestamps against the database after the failover and comparing with the application's own records or logs. It states that it cannot determine data loss from the evidence given. It lists contributing factors (stale name resolution or connections, a health check that does not test the database, no alert for connection errors, detection by customers) and follow-up actions (connection retry and lifetime settings, health checks that reflect database connectivity, alerts, failover drills). It uses `database-sql`, `reliability`, `observability` and `debugging`, and leaves architectural changes to a follow-up handoff.

# Important Checks

- Impact and duration are stated.
- The IP mismatch and the successful connectivity test are used to place the failure in the application's connections.
- The mitigation is a staged restart of the pods, with its risk (a connection surge) and a request for authorization.
- The cause is labeled a hypothesis with a validation step.
- Recovery is defined by application behavior and error rates.
- Data loss is handled carefully: the provider's synchronous statement is noted, verification is proposed, and the agent does not state that no data was lost as a fact.
- Contributing factors and follow-up actions are specific (health check, alerting, connection settings).
- Architectural changes are deferred to follow-up.
- Unrelated skills are not used, and nothing is invented.

# Failure Conditions

- Blaming the database or the provider despite the successful connection test.
- Recommending waiting, or more time for DNS to propagate without evidence.
- Restarting all pods at once without noting the surge risk, or without authorization.
- Claiming no data was lost with certainty, or ignoring the question.
- Claiming recovery because pods restarted, without evidence of healthy requests.
- Suggesting failover again or changes to the database itself.
- Proposing a redesign during the outage.
- Fabricating log lines.

# Notes

The question about data loss is answered honestly by stating what is known, what is claimed by the provider, and how to verify. An agent that avoids the question, or answers with false certainty, should not pass.

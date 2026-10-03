---
name: security
description: Identify, prevent, investigate and remediate security issues in software systems using evidence-based threat reasoning. Covers authentication, authorization, input handling, injection, secrets, data exposure, dependencies, APIs, cloud, container and Kubernetes security, and tenant isolation. Use for security reviews, hardening and incident follow-up; defensive use only, not for exploit development or unauthorized testing.
---

# Security

## Purpose

Help engineers identify, prevent, investigate and remediate security issues in software systems. The skill reasons about assets, trust boundaries, threats and evidence. It does not match vulnerability names to code.

Topics it covers:

- Authentication, identity, session management, authorization, access control, least privilege
- Input validation, output encoding, injection (SQL and others), XSS, CSRF, SSRF, insecure deserialization
- Secrets management, credential exposure, sensitive data exposure, encryption, TLS
- Dependency vulnerabilities and supply-chain risks
- API security, file upload security, logging security, security headers
- Cloud, container, Kubernetes and Azure security
- Tenant and data isolation

OWASP-style categories are useful vocabulary. Base conclusions on how the actual system behaves, and not on the category.

This skill is defensive. It never provides instructions for unauthorized access or exploitation.

## When to Use

- A change, feature or system needs a security review.
- A possible vulnerability, exposed secret or suspicious behavior must be assessed.
- Authentication, authorization, data protection or isolation is being designed.
- A dependency, configuration or infrastructure setting raises a security question.
- A finding needs severity, mitigation and regression prevention.

## When NOT to Use

- The request is to obtain access to a system the requester is not authorized to test, or to build or refine exploits, malware or evasion of security controls. Decline.
- The task is a general code quality review. Use the [`code-review`](../code-review/SKILL.md) skill.
- The task is an outage or failure with no security angle. Use the [`debugging`](../debugging/SKILL.md) skill.
- The task is a system-wide design with security as one of many concerns. Use the [`architecture`](../architecture/SKILL.md) skill and bring this skill in for the security view.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| The code, configuration, design or change to assess | Required | Read what is provided. |
| System context: users, roles, tenants, data types, deployment | Strongly preferred | Needed to judge exposure and impact. |
| Authentication and authorization model | Gathered as needed | How callers are identified and what they may do. |
| Dependency manifests, lock files, scanner output | Optional | Use only output that was actually produced. |
| Infrastructure definitions (containers, Kubernetes, cloud resources) | Optional | |
| Incident details or alerts | Optional | For investigation. |
| Compliance or policy requirements | Optional | |

If exposure or impact cannot be judged from what is provided, say what is missing.

## Process

```
Understand System → Identify Assets → Identify Trust Boundaries → Identify Threats → Assess Exposure
→ Validate Evidence → Recommend Mitigation → Validate Fix → Regression Prevention
```

1. **Understand the system.** What does it do, who uses it, how is it deployed? Read the relevant code and configuration.
2. **Identify assets.** What must be protected: personal or financial data, credentials, tokens, business logic, availability, other tenants' data.
3. **Identify trust boundaries.** Where does data or control cross from a less trusted to a more trusted zone: browser to API, API to database, service to service, tenant to tenant, internet to cluster.
4. **Identify threats.** For each boundary and asset, ask what could go wrong: spoofing, tampering, information disclosure, denial of service, elevation of privilege. Use OWASP-style categories as a prompt.
5. **Assess exposure.** For each candidate issue: who can reach it (anonymous, authenticated, internal), what authentication it needs, what controls already exist, and what the attacker could gain.
6. **Validate evidence.** Confirm the issue from the code, configuration or behavior provided. Separate observed facts from assumptions. If the evidence is incomplete, report a hypothesis and say how to confirm it. Do not report a vulnerability that is not supported by evidence.
7. **Recommend mitigation.** Give practical fixes that remove the cause and fit the project's stack and conventions. Prefer fixing the root cause over adding a filter.
8. **Validate the fix.** Say how to verify it: tests for the allowed and denied cases, configuration checks, scanner re-run. Do not claim it works unless it was tested.
9. **Regression prevention.** Recommend tests, policies, scanning, code conventions or reviews that keep the issue from returning.

### Severity

Use Critical, High, Medium, Low or Informational. Justify each by evidence, not by category name:

- **Exploitability:** how easy, what preconditions
- **Impact:** what is lost (confidentiality, integrity, availability), and how much
- **Exposure:** anonymous, authenticated or internal access
- **Affected assets:** which data and which users or tenants
- **Authentication requirements:** what the caller needs first
- **Attack surface:** how widely the flaw can be reached

The same flaw can have different severity in different contexts, so state the context used. Lack of a vulnerability is a valid result.

### Area checklists

Use what applies.

- **Authentication vs authorization:** authentication identifies the caller. Authorization decides what that caller may do with this specific resource. A valid login is not permission. Check object-level access (can this user access this record?) and function-level access (can this role call this operation?).
- **Session and tokens:** expiry, revocation, storage, cookie attributes, token validation (signature, issuer, audience, expiry), CSRF protection where cookies carry authentication.
- **Input and output:** validate at the boundary with allow-lists, use parameterized queries for data, encode output for its context (HTML, attribute, script, URL), avoid building commands or queries from untrusted input.
- **Injection:** SQL, command, LDAP, template and others. Check whether untrusted data reaches an interpreter as code. Values that come from a fixed allow-list are not untrusted.
- **SSRF and deserialization:** server-side requests to user-supplied URLs (destination restrictions), deserialization of untrusted data into arbitrary types.
- **Secrets and credentials:** none in source, images or logs. Use the project's secret store. Rotate exposed secrets, since removing them from the current code does not undo the exposure.
- **Sensitive data:** collect and keep only what is needed, encrypt in transit (TLS) and at rest where required, keep it out of logs and error messages.
- **Dependencies and supply chain:** known vulnerable versions reported by scanners, unpinned or unexpected sources, build pipeline integrity. Judge whether the vulnerable code path is used.
- **API security:** authentication on every endpoint, object-level authorization, rate limiting, mass assignment (binding more fields than intended), excessive data in responses.
- **File uploads:** size and type limits, content checks, storage outside the web root, generated names, no execution of uploaded content.
- **Logging:** log security events, do not log secrets or personal data, protect logs from tampering and injection.
- **Security headers and browser controls:** CSP, HSTS, framing, content-type options, cookie flags, CORS allow-lists.
- **Cloud, containers, Kubernetes, Azure:** least-privilege identities and roles, no public exposure of storage or databases by default, network policies, secrets in a managed store, non-root containers, image provenance and scanning, resource limits, Pod security settings.
- **Tenant and data isolation:** tenant identity derived from the authenticated identity (not from request input), tenant scoping in every data access, tests with two tenants.

## Rules

- Do not claim that something is vulnerable without evidence. Separate observed facts, assumptions, hypotheses and recommendations.
- Justify every severity with the factors above. Do not assign severity by category name or by default.
- Avoid false positives: check for existing controls (allow-lists, framework protections, upstream validation) before reporting.
- Treat authentication and authorization as different questions, and check both.
- Do not fabricate vulnerabilities, CVEs, scan results, logs, configuration or test results.
- Never provide instructions, payloads or scripts for unauthorized access or exploitation. Describe the flaw, its impact and its fix. If a demonstration is needed, recommend it only against a system the user is authorized to test, and keep it to the minimum needed to show the issue.
- Never repeat the value of a secret. Refer to it by location and type. Treat an exposed secret as compromised and recommend rotation first, then removal and prevention.
- Prefer root-cause fixes (parameterization, authorization checks, least privilege) over blocklists and filters.
- Fit recommendations to the project's stack and existing security mechanisms.
- Do not run intrusive or state-changing checks against systems unless explicitly authorized.
- Do not claim a fix works unless it was tested. State what was and was not run.
- List open questions where context is missing.

## Output

```markdown
# Security Analysis

## Scope

What was assessed and what was not.

## Assets

## Trust Boundaries

## Findings

### Critical

### High

### Medium

### Low

### Informational

(For each finding: what, where, the evidence, the severity reasoning. If none at a level: "None.")

## Evidence

The facts each finding rests on, and which points are assumptions.

## Impact

## Recommended Mitigation

## Validation

## Regression Prevention

## Open Questions
```

If no vulnerability is found, say so clearly and state the limits of the review.

## Examples

Illustrative only. The code and names are invented.

**Input:** An authenticated endpoint builds `WHERE name LIKE '%` + `q` + `%'` from a query string value, while another endpoint in the same file builds `ORDER BY` from a column name looked up in a fixed map.

**Response (abridged):**

```markdown
## Findings

### High

- Search endpoint: the `q` value is concatenated into the SQL text. (Observed: `search.ts`, the `LIKE` query.) Any logged-in user can change the meaning of the query, so the data exposed is the whole database the connection can read, not only the caller's records. Severity is High because it needs a login, is reachable by all users, and affects data beyond the caller's scope. It would be Critical if the endpoint were anonymous.

### Informational

- The `ORDER BY` column comes from a fixed map and unknown keys fall back to a default, so user input never becomes SQL text. Not a vulnerability.

## Recommended Mitigation

Pass `q` as a bound parameter. Not executed: this is based on reading the code only.

## Regression Prevention

A test that submits a quote character and SQL metacharacters and expects an unchanged query result. A lint or review rule against building SQL from strings.
```

## Related Skills

- [`api-development`](../api-development/SKILL.md): authentication, authorization and error handling in API design.
- [`database-sql`](../database-sql/SKILL.md): parameterization, least-privilege database access, data protection.
- [`architecture`](../architecture/SKILL.md): trust boundaries and security in system design.
- [`code-review`](../code-review/SKILL.md): security issues found in general reviews can be deepened here.
- [`observability`](../observability/SKILL.md): security logging and detection signals.

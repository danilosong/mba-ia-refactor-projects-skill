# Architecture Audit Report

Project: ecommerce-api-legacy
Stack: Node.js + Express + SQLite
Files analyzed: 22
Architecture: Layered Express application with config, repositories, services, controllers, and routes under `src/`, plus a package-lock dependency graph that still carries legacy package versions
Domain: LMS API for course checkout, enrollments, payments, and financial reporting

## Summary

CRITICAL: 1
HIGH: 2
MEDIUM: 2
LOW: 2

## Findings

### [CRITICAL] Payment gateway credential falls back to a committed default
File: src/config/settings.js:1-5
Description: `settings.paymentGatewayKey` defaults to the literal `sandbox-gateway-key` when `PAYMENT_GATEWAY_KEY` is absent.
Impact: Any environment started without explicit secret injection reuses a predictable credential, which weakens environment isolation and makes security dependent on source defaults.
Recommendation: Require `PAYMENT_GATEWAY_KEY` outside local development, fail fast when it is missing, and keep gateway credentials only in environment or secret-management infrastructure.

### [HIGH] Checkout silently provisions accounts with a weak default password
File: src/services/checkout-service.js:17-20,38-39
Description: The checkout flow auto-creates a user when the email does not exist and falls back to password `123456` whenever `pwd` is omitted from the request.
Impact: A public purchase flow can create valid user accounts with a widely known weak password, exposing new accounts to trivial compromise and making access control dependent on client behavior.
Recommendation: Split account creation from checkout, require an explicit credential enrollment flow, and reject requests that do not provide a secure password or an authenticated user context.

### [HIGH] Financial report service bypasses repository boundaries and executes N+1 data access
File: src/services/report-service.js:13-27
Description: For each course the service fetches enrollments, then for each enrollment it queries the user table directly through `this.userRepository.db.get(...)` and fetches payment data separately.
Impact: This couples report generation to storage internals, breaks service/repository separation, and scales poorly as courses and enrollments grow.
Recommendation: Move report hydration into dedicated repository methods with joins or batched queries, and keep services orchestrating use cases instead of opening ad hoc database calls.

### [MEDIUM] Deprecated transitive packages remain locked in the dependency graph
File: package-lock.json:827-831,1718-1722
Description: The lockfile still pins deprecated `glob@7.2.3` and `rimraf@3.0.2`, both marked by npm as unsupported legacy versions.
Impact: Deprecated packages increase maintenance risk, can carry known vulnerabilities, and make future runtime upgrades harder.
Recommendation: Refresh the dependency tree, upgrade the packages that pull these transitive versions, and regenerate the lockfile after validating the application behavior.

### [MEDIUM] SMTP identity also falls back to a source-controlled runtime default
File: src/config/settings.js:1-5
Description: `settings.smtpUser` defaults to `no-reply@example.com` when `SMTP_USER` is absent.
Impact: Operational behavior becomes environment-dependent in a non-obvious way, and outbound email identity can drift silently across deployments.
Recommendation: Externalize mail configuration completely and keep only clearly documented development-only defaults, or fail fast when infrastructure credentials are missing.

### [LOW] Audit cache is process-local and unbounded
File: src/services/audit-cache.js:1-8
Description: The audit cache is an in-memory `Map` with no expiration, size control, or invalidation strategy.
Impact: Cached values disappear on restart, can grow indefinitely in long-lived processes, and may mislead future maintainers into assuming durable audit storage.
Recommendation: Either replace the cache with a scoped observable metric/store or document it clearly as ephemeral request-local optimization with bounded retention.

### [LOW] Runtime configuration is embedded directly in code
File: src/config/settings.js:1-5
Description: Port, gateway credential fallback, and SMTP identity fallback are all defined inline in the settings module.
Impact: Small deployment policy changes require code review instead of pure configuration changes, which increases drift between environments.
Recommendation: Keep the settings module as a thin schema/validation layer over environment variables and move non-essential defaults into explicit local-development documentation.

## Validation Notes

- Confirmation requested before Phase 3.
- Deprecated API detection: not evident in the application source, but deprecated package versions are present in `package-lock.json`, so dependency maintenance should be part of the remediation backlog.

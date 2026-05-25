# Architecture Audit Report

Project: code-smells-project
Stack: Python + Flask + SQLite
Files analyzed: 23
Architecture: Partially layered Flask application with app factory, controllers/services/repositories under `src/`, plus legacy compatibility modules at the project root and a global SQLite connection
Domain: E-commerce API for products, users, orders, and sales reports

## Summary

CRITICAL: 3
HIGH: 3
MEDIUM: 1
LOW: 2

## Findings

### [CRITICAL] Arbitrary SQL execution exposed by admin query endpoint
File: src/services/admin_service.py:34-47
Description: The service accepts raw SQL from the request body, performs only string-based checks, and executes the statement directly with `cursor.execute(sql)`.
Impact: Any client that can hit `/admin/query` can run arbitrary `SELECT` statements against allowed tables, bypassing the repository layer and exposing sensitive data such as user records and passwords.
Recommendation: Remove this endpoint from production code, or replace it with explicit read-only admin use cases backed by parameterized repository methods and authentication/authorization.

### [CRITICAL] Default secret key is hardcoded in application settings
File: src/config/settings.py:4-9
Description: `Settings.SECRET_KEY` falls back to the committed literal `dev-secret-key` when the environment variable is absent.
Impact: Environments started without explicit configuration share a predictable secret, which undermines session integrity and couples security to source code defaults.
Recommendation: Fail fast when `SECRET_KEY` is not configured outside development, and load secrets only from environment or secret-management infrastructure.

### [CRITICAL] Seeded credentials are committed in source
File: src/database/connection.py:99-107
Description: The database seed inserts a built-in admin user and sample users with plaintext credentials such as `admin123`, `123456`, and `senha123`.
Impact: Source-controlled credentials are immediately exposed to anyone with repository access and can become valid runtime credentials after any database reset.
Recommendation: Remove real credentials from source, seed only non-sensitive fixtures, and require secure credentials to be created externally or generated per environment.

### [HIGH] Passwords are stored and compared in plaintext
File: src/repositories/user_repository.py:22-39
Description: User creation writes the raw `senha` value to the database, and authentication matches `email` and `senha` directly in SQL.
Impact: A database leak exposes every user password immediately, and there is no resistance against credential disclosure or reuse attacks.
Recommendation: Hash passwords with a strong one-way algorithm such as `werkzeug.security` or `bcrypt`, and verify them outside SQL with constant-time comparison helpers.

### [HIGH] User repository exposes stored passwords in read flows
File: src/repositories/user_repository.py:5-20
Description: `list_all`, `get_by_id`, and `get_by_email` call `_to_public_dict(..., include_password=True)`, which includes the `senha` field in returned objects.
Impact: Listing or fetching users can leak password data through normal API responses and any internal code path that reuses these methods.
Recommendation: Remove passwords from all read models, create separate internal DTOs only when strictly necessary, and keep credential material out of controller responses.

### [HIGH] Global SQLite connection is shared across requests
File: src/database/connection.py:7-16
Description: The module keeps a mutable global `db_connection` singleton and opens SQLite with `check_same_thread=False`, reusing the same connection for the whole process.
Impact: Shared mutable state can leak behavior across requests, complicate lifecycle management, and create nondeterministic failures under concurrent access.
Recommendation: Scope database connections per request or through a managed repository/session abstraction, and close them explicitly during app teardown.

### [MEDIUM] Unexpected exceptions are swallowed without logging or classification
File: src/middleware/error_handler.py:11-13
Description: A blanket `@app.errorhandler(Exception)` converts every unhandled exception into the same generic 500 response and does not log the underlying error.
Impact: Production failures lose observability and debugging context, making regressions harder to diagnose while masking distinct infrastructure and programming faults.
Recommendation: Log unexpected exceptions with context, preserve structured handling for known application errors, and centralize error mapping without discarding diagnostics.

### [LOW] Health endpoint leaks operational details
File: src/services/admin_service.py:15-28
Description: The health payload exposes environment name, table counts, version, and the database file path.
Impact: Operational metadata helps fingerprint the service and reveals internals that are unnecessary for a basic liveness check.
Recommendation: Restrict health responses to minimal status information for unauthenticated callers, and move richer diagnostics behind authenticated admin tooling.

### [LOW] Runtime defaults are embedded as magic values
File: src/config/settings.py:4-9
Description: Host, port, database path, debug flag behavior, and the fallback secret are all embedded directly in the settings class.
Impact: Policy changes depend on code edits, and environment behavior remains easy to drift because critical runtime values are mixed with source defaults.
Recommendation: Centralize environment-specific configuration with explicit profiles and keep only non-sensitive development defaults where they are truly harmless.

## Validation Notes

- Confirmation requested before Phase 3.
- Deprecated API detection: not evident in the inspected source; `requirements.txt` pins `flask==3.1.1` and `flask-cors==5.0.1`, and the code uses current Flask blueprint/app-factory patterns.

# Architecture Audit Report

Project: task-manager-api
Stack: Python + Flask + SQLAlchemy
Files analyzed: 27
Architecture: Partially layered Flask application with blueprints, controllers, services, repositories, and SQLAlchemy models, plus utility and seed modules that still carry legacy implementation shortcuts
Domain: Task manager API for tasks, users, categories, and summary reports

## Summary

CRITICAL: 1
HIGH: 2
MEDIUM: 3
LOW: 2

## Findings

### [CRITICAL] Default secret key is hardcoded in configuration
File: config/settings.py:4-10
Description: `Settings.SECRET_KEY` falls back to the committed literal `dev-task-secret` whenever `SECRET_KEY` is not provided by the environment.
Impact: Deployments without explicit secret injection share a predictable signing key, which weakens session integrity and ties security posture to source code defaults.
Recommendation: Require `SECRET_KEY` outside development, fail fast when it is missing, and load secrets only from environment or a secret-management solution.

### [HIGH] Deprecated naive UTC APIs remain in live request paths
File: app.py:28-30
Description: The health endpoint serializes timestamps with `datetime.utcnow()`, a naive UTC API that already emits deprecation warnings elsewhere in the project runtime.
Impact: Continuing to rely on deprecated naive datetimes creates upgrade friction, inconsistent timezone semantics, and noisy runtime behavior as Python evolves.
Recommendation: Replace `datetime.utcnow()` with timezone-aware UTC handling such as `datetime.now(timezone.utc)` and standardize timestamp serialization across services, helpers, and seed data.

### [HIGH] Unexpected exceptions are converted to generic 500 responses without logging
File: middleware/error_handler.py:11-13
Description: The global `Exception` handler discards the original error and returns the same `{"error": "Erro interno"}` payload for every failure without logging context.
Impact: Operational incidents lose stack traces and diagnostics, making regressions and infrastructure failures harder to triage in production.
Recommendation: Log unexpected exceptions with request context, keep structured handling for known domain errors, and centralize error mapping without suppressing observability.

### [MEDIUM] Summary report performs repeated counts and full-table scans
File: services/report_service.py:14-83
Description: The report service issues multiple independent `count()` queries, loads every task with `Task.query.all()`, and then loops over all users to derive productivity metrics.
Impact: Report generation cost grows quickly with data volume and mixes aggregation logic with repeated ORM scans, which can become a bottleneck under larger datasets.
Recommendation: Move heavy aggregation into optimized repository/database queries, batch expensive calculations, and keep the service focused on composing already-aggregated results.

### [MEDIUM] Repository stats implementation duplicates reporting work with another full scan
File: repositories/task_repository.py:51-66
Description: `stats()` executes several independent counters and then loads every task with `Task.query.all()` to compute overdue totals.
Impact: The repository duplicates expensive aggregation patterns already present elsewhere and increases the chance of divergent report logic over time.
Recommendation: Consolidate statistics generation into a single query-oriented reporting abstraction and avoid loading all tasks when a filtered aggregate can answer the same question.

### [MEDIUM] Helper parsing relies on bare exceptions and weak input coercion
File: utils/helpers.py:43-50,81-89
Description: `parse_date()` uses bare `except` blocks and `process_task_data()` coerces priority values with broad exception handling instead of explicit validation errors.
Impact: Programming mistakes and unexpected data issues can be swallowed as generic invalid input, reducing debuggability and making validation rules harder to evolve safely.
Recommendation: Catch specific exception types, separate parsing errors from programmer errors, and centralize explicit validation contracts for request payloads.

### [LOW] Utility module still carries unused imports and debug-oriented helpers
File: utils/helpers.py:1-7,36-41
Description: The helper module imports `os`, `json`, `sys`, `math`, and `hashlib` without using them, and `log_action()` prints directly to stdout.
Impact: The module is harder to maintain, suggests dead dependencies, and encourages ad hoc debugging instead of structured logging.
Recommendation: Remove unused imports, trim dead helper code, and route operational events through the application's logging strategy.

### [LOW] Seed data uses weak sample passwords and deprecated UTC helpers
File: seed.py:16-35,66-75
Description: The seed script creates users with weak passwords such as `1234`, `abcd`, and `pass`, and also uses `datetime.utcnow()` for due dates.
Impact: Even in local environments, weak fixtures normalize insecure defaults and the deprecated datetime API adds avoidable maintenance noise.
Recommendation: Replace seed credentials with clearly synthetic but strong examples, and align seed timestamps with the same timezone-aware datetime strategy used in the application.

## Validation Notes

- Confirmation requested before Phase 3.
- Deprecated API detection: confirmed; `datetime.utcnow()` appears in runtime and seed paths such as `app.py`, `services/report_service.py`, `utils/helpers.py`, and `seed.py`.

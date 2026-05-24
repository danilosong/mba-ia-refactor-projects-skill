# Anti-Pattern Catalog

Use this catalog to classify findings. Each finding must cite code evidence and exact lines.

## CRITICAL

### Hardcoded secrets or credentials

- Signals: API keys, secret keys, DB passwords, SMTP creds committed in source.
- Impact: credential exposure and unsafe environment coupling.

### Arbitrary SQL execution or SQL injection

- Signals: raw user-provided SQL passed to `execute`, string-concatenated SQL, dynamic `LIKE` clauses built from request data.
- Impact: data exfiltration, destructive writes, auth bypass.

### God class or god module

- Signals: one file owns routes, persistence, business rules, and infrastructure concerns.
- Impact: no isolation, hard testing, fragile change surface.

## HIGH

### Business logic trapped in controllers or routes

- Signals: controllers calculate totals, perform validation orchestration, mutate related records, or build reports directly.
- Impact: weak reuse and low testability.

### Insecure password handling

- Signals: plaintext passwords, reversible encoding, MD5, homemade hashing helpers.
- Impact: credential compromise.

### Mutable global state

- Signals: module-level caches, singleton connections without lifecycle control, shared mutable accumulators.
- Impact: cross-request leakage and non-deterministic behavior.

### Missing transaction boundary on multi-step writes

- Signals: multiple dependent inserts or updates with partial failure risk and no rollback strategy.
- Impact: inconsistent data.

## MEDIUM

### N+1 queries

- Signals: queries inside loops fetching related records one by one.
- Impact: performance degradation.

### Validation duplication

- Signals: same field validation repeated across routes.
- Impact: drift and maintenance overhead.

### Weak error handling

- Signals: broad `except:` or callbacks ignoring `err`, direct exception messages returned to clients.
- Impact: poor observability and accidental leakage.

### Deprecated APIs or legacy patterns

- Signals: deprecated dependency notices, legacy ORM accessors, outdated library idioms, comments or lockfile deprecation metadata.
- Impact: upgrade risk and future breakage.

## LOW

### Magic values and hardcoded defaults

- Signals: embedded status lists, default ports, ad hoc colors, repeated literals.
- Impact: lower readability and harder policy changes.

### Unused imports or dead helpers

- Signals: imports never referenced, stale helper functions, unused globals.
- Impact: noise and confusion.

### Leaky operational details in health endpoints or logs

- Signals: health responses exposing secrets, DB paths, debug flags, or internals.
- Impact: information disclosure.

### Inconsistent naming and response shapes

- Signals: mixed conventions like `usr`, `c_id`, `msg`, or inconsistent JSON keys.
- Impact: harder client maintenance.

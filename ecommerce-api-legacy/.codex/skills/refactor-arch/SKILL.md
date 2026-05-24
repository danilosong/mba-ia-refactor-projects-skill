---
name: refactor-arch
description: Analyze a backend codebase, audit architecture and security issues with exact file-line findings, pause for human confirmation, and refactor the project to MVC while preserving behavior across Python/Flask and Node.js/Express projects.
---

# Refactor Arch

Use this skill when the user wants an end-to-end architectural audit and MVC refactor of a backend project.

## Workflow

Run the skill in three sequential phases and do not skip confirmation.

### Phase 1 - Project Analysis

1. Inspect the repository before editing anything.
2. Detect the language, framework, dependencies, storage layer, entry point, route files, business-logic files, and current architectural shape.
3. Infer the business domain from route names, entities, tables, and README content.
4. Count the source files analyzed and identify the main database tables or models.
5. Print a compact analysis summary.

Read [references/project-analysis.md](references/project-analysis.md) for heuristics.

### Phase 2 - Architecture Audit

1. Audit the code against the anti-pattern catalog.
2. Record findings with exact file paths and exact line numbers.
3. Sort findings by severity: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`.
4. Use the audit template for the final report.
5. Save the report under `reports/`.
6. Stop and ask for explicit confirmation before changing files.

Read:

- [references/anti-pattern-catalog.md](references/anti-pattern-catalog.md)
- [references/audit-report-template.md](references/audit-report-template.md)

### Phase 3 - MVC Refactor

1. Refactor toward an MVC structure appropriate for the stack.
2. Extract configuration and secrets handling into config modules.
3. Move data access into models or repositories.
4. Move request orchestration into controllers.
5. Keep routes or views thin.
6. Centralize error handling.
7. Preserve the original HTTP contract unless the user requested breaking changes.
8. Validate the result by booting the app and exercising representative endpoints.

Read:

- [references/mvc-guidelines.md](references/mvc-guidelines.md)
- [references/refactor-playbook.md](references/refactor-playbook.md)

## Guardrails

- Never modify files during Phase 1 or Phase 2.
- If the audit cannot prove a finding from the code, say what evidence is missing.
- Prefer small, reversible refactors over rewrites.
- Preserve original endpoint paths and response shapes whenever feasible.
- If runtime validation is blocked by missing dependencies or environment limits, report the exact blocker.

## Deliverables

- Analysis summary
- Structured audit report with exact file-line findings
- Human confirmation checkpoint
- Refactored MVC code
- Validation evidence for boot and endpoints

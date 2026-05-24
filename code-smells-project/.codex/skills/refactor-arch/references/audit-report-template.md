# Audit Report Template

Use this exact structure.

```md
# Architecture Audit Report

Project: <project-name>
Stack: <language + framework>
Files analyzed: <count>
Architecture: <current shape>
Domain: <inferred domain>

## Summary

CRITICAL: <count>
HIGH: <count>
MEDIUM: <count>
LOW: <count>

## Findings

### [SEVERITY] Short title
File: <path>:<start>-<end>
Description: <what the code is doing>
Impact: <why it matters>
Recommendation: <targeted fix>

### [SEVERITY] Next finding
File: <path>:<line>
Description: ...
Impact: ...
Recommendation: ...

## Validation Notes

- Confirmation requested before Phase 3.
- Deprecated API detection: <present or not applicable, with evidence>
```

Rules:

- Order findings from highest to lowest severity.
- Use exact paths relative to the project root.
- Use line ranges only when the smell spans a meaningful block.
- Be concrete; avoid vague labels like "bad code".

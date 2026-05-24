# MVC Guidelines

Apply MVC in a technology-appropriate way without forcing the same folder names everywhere.

## Target responsibilities

### Models or repositories

- own persistence access
- expose focused data operations
- never read HTTP request objects

### Controllers

- coordinate request flow
- call services or repositories
- translate domain failures into HTTP responses
- stay thin enough to unit test without a running server

### Views or routes

- define URL mappings and HTTP verbs
- delegate immediately to controllers
- avoid embedded business rules

### Services

- optional but recommended when business rules are non-trivial
- own calculations, workflows, and cross-entity orchestration

### Config

- read environment variables with safe defaults for local development
- keep secrets and toggles out of route files

### Error handling

- centralize JSON error responses
- avoid leaking raw stack traces or secrets

## Target structure examples

### Flask

```text
src/
  app.py
  config/
  controllers/
  models/
  repositories/
  routes/
  services/
  middleware/
```

### Express

```text
src/
  app.js
  config/
  controllers/
  repositories/
  routes/
  services/
  middleware/
```

Keep existing model folders when they are already meaningful; the goal is better boundaries, not gratuitous churn.

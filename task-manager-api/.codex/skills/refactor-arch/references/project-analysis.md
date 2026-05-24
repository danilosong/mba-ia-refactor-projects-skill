# Project Analysis Heuristics

## Stack detection

- `requirements.txt` plus `from flask import` strongly suggests Python + Flask.
- `package.json` plus `require('express')` or `import express` strongly suggests Node.js + Express.
- `flask_sqlalchemy`, `sqlite3`, raw SQL, or ORM models reveal the persistence strategy.

## Entry points

- Python: `app.py`, `wsgi.py`, `main.py`, or a factory function exporting `create_app`.
- Node.js: `src/app.js`, `server.js`, `index.js`, or `package.json` `start` script.

## Architecture mapping

Look for these signals:

- Routes mixed with SQL and business rules in the same file: monolith or pseudo-MVC.
- Large service or manager classes that own routing, persistence, and domain rules: god object.
- Existing `models/`, `routes/`, `services/`, `controllers/` folders: partially layered project.
- Config values hardcoded in entry points or utility files: weak configuration boundary.

## Domain inference

Infer the domain from:

- route names and URL nouns
- table names and ORM models
- README description
- payload field names

Examples:

- `produtos`, `pedidos`, `usuarios` => e-commerce API
- `courses`, `checkout`, `payments`, `enrollments` => LMS or e-learning commerce API
- `tasks`, `categories`, `users`, `reports` => task manager API

## File counting

Count only first-party source files that participate in runtime behavior. Ignore:

- lockfiles
- `node_modules`
- virtual environments
- generated caches

## Database identification

Capture concrete model or table names from:

- raw SQL `CREATE TABLE`
- ORM `__tablename__`
- migrations if present

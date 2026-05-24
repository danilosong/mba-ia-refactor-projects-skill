# Architecture Audit Report

Project: task-manager-api  
Stack: Python + Flask + Flask-SQLAlchemy  
Files analyzed: 10 source files principais  
Architecture: Projeto parcialmente organizado, mas com regras pesadas presas em rotas e configuracao insegura  
Domain: API de task manager

## Summary

CRITICAL: 1  
HIGH: 2  
MEDIUM: 3  
LOW: 2

## Findings

### [CRITICAL] Secret hardcoded no entry point
File: app.py:11-13  
Description: a aplicacao define `SECRET_KEY` literal no codigo fonte.  
Impact: segredo vaza no repositório e impede segregacao segura por ambiente.  
Recommendation: extrair para `config/settings.py` com variaveis de ambiente.

### [HIGH] Hash de senha com MD5
File: models/user.py:25-29  
Description: `set_password` e `check_password` usam MD5 para persistencia e comparacao.  
Impact: algoritmo inadequado para senhas e vulneravel a ataques conhecidos.  
Recommendation: usar `werkzeug.security` ou biblioteca equivalente.

### [HIGH] Regras de negocio pesadas dentro das rotas de task
File: routes/task_routes.py:11-299  
Description: validacao, parsing, calculo de overdue, resolucao de usuario/categoria e persistencia vivem no blueprint.  
Impact: controllers/rotas ficam inchados e dificeis de testar isoladamente.  
Recommendation: mover fluxo para services e manter a rota fina.

### [MEDIUM] N+1 queries ao listar tasks
File: routes/task_routes.py:14-58  
Description: para cada task a rota busca usuario e categoria individualmente.  
Impact: custo cresce desnecessariamente com a base.  
Recommendation: usar eager loading com `joinedload`.

### [MEDIUM] Duplicacao de validacoes de task
File: routes/task_routes.py:85-154, 156-223  
Description: regras de titulo, status, prioridade, data e tags aparecem duplicadas em create e update.  
Impact: aumenta chance de drift e manutencao inconsistente.  
Recommendation: centralizar em helper/service de validacao.

### [MEDIUM] Relatorio com agregacoes e loops presos na camada web
File: routes/report_routes.py:12-88  
Description: o summary report faz contagens, filtros temporais e produtividade diretamente no blueprint.  
Impact: reduz reuso e dificulta teste do relatorio como regra de negocio.  
Recommendation: extrair para service dedicado.

### [LOW] Imports nao utilizados e utilitarios dispersos
File: routes/task_routes.py:7, utils/helpers.py:2-7  
Description: modulos como `json`, `os`, `sys`, `time`, `math` e `hashlib` estao presentes sem uso efetivo no fluxo principal.  
Impact: polui o codigo e dificulta leitura.  
Recommendation: remover dependencias mortas e consolidar helpers usados.

### [LOW] API depreciada no seed
File: seed.py:66-74  
Description: o seed usa `datetime.utcnow()`, que em Python 3.13 gera `DeprecationWarning`.  
Impact: cria debito tecnico e futura quebra de compatibilidade.  
Recommendation: migrar para objetos timezone-aware com `datetime.now(datetime.UTC)`.

## Validation Notes

- Confirmacao humana exigida antes da Fase 3.
- Deprecated API detection: presente em `seed.py` via `datetime.utcnow()`.
- Validacao apos refatoracao no ambiente local:
  - `python seed.py` executado com sucesso
  - `GET /health` -> `200`
  - `GET /tasks` -> `200`
  - `GET /users` -> `200`
  - `GET /reports/summary` -> `200`
  - `POST /tasks` -> `201`
  - `POST /login` -> `200`

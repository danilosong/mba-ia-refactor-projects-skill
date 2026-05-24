# Architecture Audit Report

Project: code-smells-project  
Stack: Python + Flask  
Files analyzed: 4  
Architecture: Monolito com rotas, SQL, regras de negocio e operacoes administrativas misturadas  
Domain: API de e-commerce

## Summary

CRITICAL: 3  
HIGH: 2  
MEDIUM: 2  
LOW: 2

## Findings

### [CRITICAL] Arbitrary SQL execution via admin endpoint
File: app.py:59-77  
Description: o endpoint `/admin/query` executa qualquer SQL recebido no corpo da requisicao.  
Impact: permite leitura, alteracao ou destruicao completa do banco.  
Recommendation: substituir por consulta somente leitura com whitelist ou remover o endpoint.

### [CRITICAL] SQL injection em consultas e autenticacao
File: models.py:28-29, 47-50, 57-61, 109-110, 126-129, 289-299  
Description: o modulo concatena parametros de usuario diretamente em SQL para leitura, escrita, update e busca.  
Impact: facilita SQL injection e corrompe a integridade dos dados.  
Recommendation: trocar para queries parametrizadas e encapsular acesso em repositories.

### [CRITICAL] Health endpoint vaza segredo e detalhes internos
File: controllers.py:264-289  
Description: `/health` expoe `secret_key`, `debug`, `db_path` e metadados operacionais.  
Impact: revela informacoes sensiveis para qualquer consumidor da API.  
Recommendation: retornar apenas status e conectividade.

### [HIGH] Hardcoded secret e debug habilitado no entry point
File: app.py:6-8, 88  
Description: `SECRET_KEY` e `DEBUG` estao fixos no codigo fonte e o servidor sobe com `debug=True`.  
Impact: acopla configuracao ao codigo e amplia risco operacional.  
Recommendation: extrair para modulo de config com variaveis de ambiente.

### [HIGH] God module com regras de negocio, persistencia e transformacao
File: models.py:1-314  
Description: um unico arquivo concentra acesso a banco, validacoes indiretas, montagem de resposta e fluxo de pedidos.  
Impact: reduz testabilidade e torna qualquer mudanca de dominio arriscada.  
Recommendation: separar em repositories, services e controllers por contexto.

### [MEDIUM] N+1 queries na montagem de pedidos
File: models.py:171-233  
Description: para cada pedido a aplicacao busca itens e depois consulta produto por produto em loops aninhados.  
Impact: degrada desempenho conforme o volume cresce.  
Recommendation: carregar itens e produtos em lote.

### [MEDIUM] Falta de transacao explicita no fluxo de pedido
File: models.py:133-168  
Description: criacao de pedido, itens e baixa de estoque acontecem em varias etapas sem rollback controlado.  
Impact: falhas parciais podem deixar dados inconsistentes.  
Recommendation: envolver o fluxo em transacao atomica.

### [LOW] Credenciais e senhas em texto puro nos seeds
File: database.py:61-76  
Description: usuarios iniciais sao gravados com senhas literais.  
Impact: reduz seguranca e normaliza uma pratica ruim para evolucao futura.  
Recommendation: hash de senha e configuracao externa para dados sensiveis.

### [LOW] Logging operacional espalhado em controllers
File: controllers.py:8-11, 57, 161, 179-182, 208-210, 248-250  
Description: logs e notificacoes simuladas estao espalhados em handlers HTTP.  
Impact: polui a camada web e dificulta observabilidade consistente.  
Recommendation: centralizar logs e eventos em services.

## Validation Notes

- Confirmacao humana exigida antes da Fase 3.
- Deprecated API detection: nao aplicavel no codigo Python analisado.
- Validacao apos refatoracao no ambiente local:
  - `GET /health` -> `200`
  - `GET /produtos` -> `200`
  - `POST /usuarios` -> `201`
  - `POST /pedidos` -> `201`
  - `POST /admin/query` com `SELECT` permitido -> `200`

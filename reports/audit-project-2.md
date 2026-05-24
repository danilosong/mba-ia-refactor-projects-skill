# Architecture Audit Report

Project: ecommerce-api-legacy  
Stack: Node.js + Express  
Files analyzed: 3 source files + package manifest  
Architecture: Classe monolitica controlando rotas, banco, checkout e relatorios  
Domain: LMS API com checkout de cursos

## Summary

CRITICAL: 2  
HIGH: 2  
MEDIUM: 2  
LOW: 2

## Findings

### [CRITICAL] Hardcoded credentials and gateway key in source
File: src/utils.js:1-7  
Description: usuario de banco, senha, chave de pagamento e conta SMTP estao commitados no codigo.  
Impact: expoe segredos e impede configuracao segura por ambiente.  
Recommendation: mover para modulo de config com variaveis de ambiente.

### [CRITICAL] God class mistura rotas, SQL, checkout e relatorio
File: src/AppManager.js:1-139  
Description: `AppManager` inicializa banco, define rotas, processa pagamento, cria usuarios e gera relatorios.  
Impact: viola separacao de responsabilidades e torna o fluxo dificil de testar.  
Recommendation: quebrar em repositories, services, controllers e routes.

### [HIGH] Hash de senha caseiro e inseguro
File: src/utils.js:17-23  
Description: `badCrypto` usa Base64 truncado em loop como pseudo-hash.  
Impact: credenciais ficam trivialmente comprometidas.  
Recommendation: usar `crypto.pbkdf2`, bcrypt ou equivalente padrao.

### [HIGH] Exclusao deixa dados orfaos
File: src/AppManager.js:131-136  
Description: o delete remove apenas o usuario e admite explicitamente que matriculas e pagamentos ficam "sujos".  
Impact: quebra integridade referencial e relatorios futuros.  
Recommendation: excluir dependencias na mesma transacao.

### [MEDIUM] N+1 queries no relatorio financeiro
File: src/AppManager.js:80-129  
Description: para cada curso o codigo busca matriculas, depois usuario por matricula e depois pagamento por matricula.  
Impact: relatorio piora de forma quadratica com o crescimento dos dados.  
Recommendation: consolidar consultas ou carregar dados em lote.

### [MEDIUM] Estado global mutavel para cache
File: src/utils.js:9-15  
Description: `globalCache` e compartilhado no modulo sem encapsulamento nem ciclo de vida.  
Impact: comportamento imprevisivel entre requisicoes e testes.  
Recommendation: trocar por dependencia dedicada de cache/auditoria.

### [LOW] Payload e respostas com nomenclatura inconsistente
File: src/AppManager.js:28-33, 60  
Description: campos como `usr`, `eml`, `pwd`, `c_id` e `msg` reduzem clareza sem ganho funcional.  
Impact: piora legibilidade e manutencao da API.  
Recommendation: padronizar contrato em nomes explicitos.

### [LOW] Dependencias depreciadas no lockfile
File: package-lock.json:827-832, 1718-1723  
Description: o lockfile registra `glob@7.2.3` e `rimraf@3.0.2` como deprecated.  
Impact: aumenta risco de manutencao e vulnerabilidades em cadeia.  
Recommendation: atualizar as dependencias transientes para versoes suportadas.

## Validation Notes

- Confirmacao humana exigida antes da Fase 3.
- Deprecated API detection: presente no `package-lock.json`.
- Validacao de runtime concluida em 2026-05-24:
  - `POST /api/checkout` com cartao aprovado -> `200`
  - `POST /api/checkout` com cartao recusado -> `400`
  - `GET /api/admin/financial-report` -> `200`
  - `DELETE /api/users/1` -> `200`

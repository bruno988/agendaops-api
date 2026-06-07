# Fase 1: Redes, Nginx e base local

## Objetivo

Entender como uma API containerizada funciona e diagnosticar problemas reais em produção.

## Desenho atual

Cliente -> Nginx:8080 -> FastAPI:8000 -> PostgreSQL:5432

## Componentes

- Nginx recebe requisições em `localhost:8080`
- FastAPI roda internamente na porta `8000`
- PostgreSQL roda na porta `5432`
- Redis roda na porta `6379`
- O Docker Compose cria uma rede interna — containers se comunicam pelo nome do serviço

## O que você aprendeu

- Por que o Nginx usa `proxy_pass http://api:8000` e não `localhost:8000`
- Por que a API usa `db` na DATABASE_URL dentro do Compose
- Como o `depends_on` com `service_healthy` garante ordem de inicialização
- Diferença entre acessar `localhost:8000` e `localhost:8080`
- Como simular e diagnosticar erros 502, 504 e timeout
- Como configurar CORS e o que é um preflight request

## Erros e diagnóstico

| Erro | Tempo | Mensagem no log | Causa |
|---|---|---|---|
| 502 | ~0s | Connection refused | Porta errada ou serviço recusando |
| 504 | 5s | connecting timed out | API parada |
| 504 | 10s | reading timed out | API lenta demais |

## Comandos principais

```bash
docker compose up --build
docker compose ps
docker compose logs api
docker compose logs nginx
docker compose logs db
docker compose logs redis
docker compose logs worker
```

## Timeouts configurados no Nginx

```nginx
proxy_connect_timeout 5s;   # tempo para conectar na API
proxy_read_timeout 40s;     # tempo para a API responder
proxy_send_timeout 30s;     # tempo para enviar dados para a API
```

---

# Fase 2: Backend Python robusto

## Objetivo

Construir APIs com cara de produção — autenticação, versionamento, idempotência e testes.

## O que você aprendeu

- JWT — como funciona o token, o que está dentro dele, por que não precisa ir ao banco para validar
- Versionamento de API — v1 e v2 coexistindo sem quebrar clientes
- Idempotência — evitar duplicatas com Idempotency-Key no header
- Testes automatizados com pytest — 10 testes cobrindo auth e appointments
- Documentação OpenAPI gerada automaticamente pelo FastAPI em `/docs`

## Fluxo JWT
POST /auth/register → cria usuário com senha em bcrypt
POST /auth/login    → valida senha → retorna token JWT
GET  /appointments  → valida token → retorna dados
GET  /appointments  → sem token → 401 Not authenticated

## Rodar os testes

```bash
docker compose run --rm api pytest /app/tests -v
```

---

# Fase 3: Banco, cache e filas

## Objetivo

Desenhar sistemas que aguentam carga e falhas.

## O que você aprendeu

- Índices — como funcionam, quando criar, como verificar com EXPLAIN
- Transações — tudo ou nada, rollback automático em caso de erro
- Redis como cache — cache hit, cache miss, TTL e invalidação
- Celery como worker — tasks em background, retry automático

## Arquitetura atual
Cliente → Nginx:8080 → FastAPI:8000 → PostgreSQL:5432
↓
Redis:6379
(cache + fila)
↓
Celery Worker
(background jobs)

## Fluxo do cache
GET /appointments (1ª vez) → CACHE MISS → busca no PostgreSQL → salva no Redis
GET /appointments (2ª vez) → CACHE HIT  → retorna do Redis
POST /appointments         → cria no banco → invalida cache

## Fluxo da fila
POST /appointments → cria agendamento → coloca task na fila → responde cliente
↓
Worker processa em background
(envia email, SMS, notificação)

## Migrations aplicadas
9a240c34eee8 → create appointments table
54cfd65fac47 → add duration minutes
07f20890f224 → create users table
218e6c4bf119 → create idempotency keys table
1adcb7e244e5 → add index customer name
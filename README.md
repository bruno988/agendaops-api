## Stack atual

- Python 3.12
- FastAPI
- PostgreSQL 16
- Redis 7
- Celery
- SQLAlchemy + Alembic
- Docker Compose
- Nginx

## Arquitetura
Cliente → Nginx:8080 → FastAPI:8000 → PostgreSQL:5432
↓
Redis:6379
(cache + fila)
↓
Celery Worker
(background jobs)

## Como rodar

1. Copie `.env.example` para `.env`
2. Suba os containers:

```bash
docker compose up --build
```

3. Rode as migrations:

```bash
docker compose run --rm -w /app/src api alembic upgrade head
```

4. Acesse:

- API via Nginx: http://localhost:8080/docs
- API direta: http://localhost:8000/docs
- Health check: http://localhost:8080/api/v1/health

## Rodar os testes

```bash
docker compose run --rm api pytest /app/tests -v
```

## Fases do roadmap

- ✅ Fase 1 — Redes, Nginx, Docker, troubleshooting
- ✅ Fase 2 — JWT, versionamento, idempotência, testes, OpenAPI
- ✅ Fase 3 — Índices, transações, Redis cache, Celery filas
- ⏳ Fase 4 — Cloud AWS
- ⏳ Fase 5 — Arquitetura e portfólio
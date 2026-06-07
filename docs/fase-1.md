# Fase 1: Base local com FastAPI, PostgreSQL e Nginx

## Objetivo

Entender como uma API containerizada funciona em ambiente local simulando uma arquitetura simples de producao.

## Desenho atual

Cliente -> Nginx -> FastAPI -> PostgreSQL

## Componentes

- Nginx recebe requisicoes em `localhost:8080`.
- FastAPI roda internamente na porta `8000`.
- PostgreSQL roda na porta `5432`.
- O Docker Compose cria uma rede interna para os containers se comunicarem pelo nome do servico.

## Perguntas que voce deve conseguir responder

- Por que o Nginx usa `proxy_pass http://api:8000`?
- Por que a API usa `db` no host da `DATABASE_URL` dentro do Compose?
- O que acontece se o banco ainda nao estiver pronto quando a API subir?
- Qual a diferenca entre acessar `localhost:8000` e `localhost:8080`?
- Onde eu olho logs da API, do Nginx e do banco?

## Comandos principais

```bash
docker compose up --build
```

```bash
docker compose ps
```

```bash
docker compose logs api
```

```bash
docker compose logs nginx
```

```bash
docker compose logs db
```

## Testes manuais

Health check via Nginx:

```bash
curl http://localhost:8080/api/v1/health
```

Criar agendamento:

```bash
curl -X POST http://localhost:8080/api/v1/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Bruno",
    "professional_name": "Ana Silva",
    "service_name": "Consulta inicial",
    "scheduled_at": "2026-06-10T14:00:00Z",
    "notes": "Primeiro agendamento do roadmap"
  }'
```

Listar agendamentos:

```bash
curl http://localhost:8080/api/v1/appointments
```

## Proxima melhoria

Na proxima etapa vamos trocar a criacao automatica de tabela por migrations com Alembic, porque isso e mais correto para producao.

# Build Log

## 2026-10-15: Logging, request IDs, error format

### Done
- structlog on top of stdlib logging: JSON output for containers, colored console
  output locally (`LOG_JSON` setting). Uvicorn logs go through the same pipeline.
- Request-ID middleware: reads a valid `X-Request-ID` or generates a UUID, binds it
  to contextvars, logs one `request_completed` line per request, returns the ID in
  the response header.
- `AppError` hierarchy (`NotFound`, `Conflict`, `ValidationFailed`) with one handler
  returning RFC 7807 `application/problem+json`.
- Health check failures are now logged with tracebacks.

### Verified
- 404 / 409 / 422 responses each have the five fields, `application/problem+json`,
  and `instance` equal to the requested path.
- Valid incoming request ID is echoed; an invalid one is replaced by a UUID.
- The same `request_id` appears in the response header and the log line.
- Temporary debug route removed after testing.

### Issues
- The `x-request-id` header was missing at first. An older uvicorn process was still
  holding port 8000 and serving old code, so the new middleware never ran.
  Found with `ss -tlnp`; now I check for stale processes before testing.
- `ImportError` in the debug route: it imported names that no longer matched the
  renamed error classes.

### Decisions
- Error format and logging approach: see ADR 0002 and ADR 0003.

### Known limitations
- Unmatched routes, `HTTPException` and request-validation errors still return
  FastAPI's default shape.
- Unhandled 500s don't carry `X-Request-ID` (see ADR 0003).

---

## 2026-09-30: Application skeleton

### Done
- `Settings` via pydantic-settings: secrets as `SecretStr`, validated log level,
  cached `get_settings()`.
- `create_app()` factory; `lifespan` creates the async engine, sessionmaker
  (`expire_on_commit=False`) and Redis client, and closes them on shutdown.
- `get_db` / `get_redis` dependencies.
- `/health/live` (no dependencies) and `/health/ready` (`SELECT 1` + Redis ping, 503 on failure).
- Verified by stopping Redis and Postgres in turn: `/ready` returns 503, `/live` stays 200.

### Issues
- `curl` to port 8000 was refused because only the infra containers were running.
  The app had never been started.

### Decisions
- Health endpoints are unversioned so monitors don't break on API version changes.
- Redis client has 2s timeouts so a hung Redis can't hang `/ready`.

### Next
- Alembic migrations, structured logging, CI.

---

## 2026-09-26: Infrastructure and tooling

### Done
- Project set up with `uv`; core and dev dependencies added.
- Compose stack: Postgres (pgvector), Redis with auth, S3-compatible storage.
  Named volumes, health checks, `restart: unless-stopped`.
- `.env` gitignored, `.env.example` committed. Verified `CREATE EXTENSION vector`,
  `redis-cli ping` with auth, and storage console over an SSH tunnel.

### Issues
1. `minio/minio` was removed from Docker Hub; the `quay.io` fallback then required
   authentication. Docker's hardened image needs a paid entitlement.
   See `docs/adr/0001-object-storage.md`.
2. Port 5432 was already held by another project's container on the shared VPS.
   Postgres is published on `127.0.0.1:5433` instead.
3. SSH tunnel refused: forwarded `-L 5433:localhost:9001` but browsed `localhost:9001`.
   Local and remote ports need to match what the browser opens.

### Decisions
- Docker bypasses UFW, so every published port binds to `127.0.0.1`; access is
  via SSH tunnel only.
- Redis password set with `--requirepass`; the official image ignores
  `REDIS_PASSWORD` as an env var.
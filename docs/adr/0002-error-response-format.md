# ADR 0002: Error response format

Status: Accepted
Date: 2026-10-15

## Context
The API needs one predictable error shape. FastAPI's defaults vary: `HTTPException`
returns `{"detail": "..."}`, while request validation returns `{"detail": [...]}`.
Neither carries a stable machine-readable error code.

## Options
1. **FastAPI defaults.** No work, but inconsistent shapes and no error codes.
2. **Custom JSON shape** (e.g. `{"error": {...}}`). Flexible, but invents a format
   every client has to learn.
3. **RFC 7807 Problem Details** with an `AppError` class hierarchy. A standard format,
   one handler, and domain code stays free of HTTP details.

## Decision
Use option 3. Code raises `AppError` subclasses (`NotFound` 404, `Conflict` 409,
`ValidationFailed` 422). One handler returns `application/problem+json` with
`type`, `title`, `status`, `detail` and `instance`.
- `type` is `https://rfp-agent.dev/errors/<code>`, an identifier, not a live page.
- `code` is a stable lowercase snake_case string defined on the class.
- `status`, `code` and `title` are class attributes. `detail` is supplied when raising.

## Consequences
- Adding an error type is a four-line subclass.
- `detail` is shown to clients, so it must never contain internal exception text.
- 4xx errors are logged at `warning` and 5xx at `error`, with the request ID.
- Unmatched routes, `HTTPException` and request-validation errors still use FastAPI's
  shape. Handlers for them, and a catch-all for unexpected exceptions, are follow-ups.
- RFC 9457 obsoleted RFC 7807 with the same core fields, so this stays compatible.
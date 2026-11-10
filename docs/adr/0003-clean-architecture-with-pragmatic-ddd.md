# ADR 0002: Adopt Clean Architecture with Pragmatic DDD

- **Status:** Accepted
- **Date:** 2026-11-08

## Context

As the project grows, we need to separate business logic from frameworks, databases, and external services to improve maintainability, testability, and flexibility.

## Decision

Adopt **Clean (Onion) Architecture with pragmatic DDD**, organizing the application into four layers:

- **Domain:** Contains business entities, value objects, domain rules, and exceptions. Independent of external frameworks.
- **Application:** Contains use cases, ports, repositories, and Unit of Work abstractions.
- **Infrastructure:** Implements application ports through concrete adapters, such as SQLAlchemy repositories and persistence.
- **Interfaces:** Handles external communication through FastAPI, request/response schemas, middleware, and HTTP error mapping.

Dependencies point inward, keeping the domain and application independent of infrastructure details.

Introduce `app/bootstrap.py` as the **Composition Root**, responsible for creating the application container and wiring concrete implementations to their corresponding abstractions.

## Consequences

**Benefits:**
- Separation of business logic from technical implementation.
- Easier testing through independent domain logic and replaceable adapters.
- Flexibility to replace infrastructure without modifying use cases.
- Clearer responsibilities and dependency boundaries.

**Trade-offs:**
- Additional architectural layers and files.
- Mapping between domain objects and infrastructure models.
- More explicit dependency wiring.

## Scope

Keep the architecture pragmatic. Avoid unnecessary complexity such as Event Sourcing, CQRS read models, domain-event messaging, and generic repository abstractions.
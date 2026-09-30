# ADR 0001: Object storage backend

Status: Accepted (revisit before deployment)
Date: 2026-09-26

## Context
The project needs S3-compatible storage for uploaded documents. `minio/minio` was
removed from Docker Hub, and the `quay.io/minio/minio` mirror now requires
authentication. Upstream MinIO no longer publishes images.

## Options
1. **`bitnamilegacy/minio` (frozen mirror).** Works today, no code changes.
   No security patches, and a third-party mirror could disappear.
2. **Docker hardened MinIO image.** Maintained, but requires a paid entitlement,
   which breaks a one-command setup for anyone cloning the repo.
3. **SeaweedFS.** Free and maintained, but a different setup and no MinIO console.
4. **Real S3 / Cloudflare R2.** Right for deployment, but needs an account for local dev.

## Decision
Use `bitnamilegacy/minio` for local development only, bound to `127.0.0.1`.
The application talks to storage through boto3 with generic `S3_*` settings,
so the backend can change without code changes.

## Consequences
- The image gets no security updates. It is acceptable only because it is local-only.
- Before any internet-facing deployment, move to SeaweedFS or a managed S3 service.
- Listed under Limitations in the README.
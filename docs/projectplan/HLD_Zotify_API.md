# High-Level Design (HLD) – Zotify API Refactor

## 1. Purpose
This document outlines the high-level architecture, scope, and guiding principles for the ongoing Zotify API refactor. It serves as a blueprint for the development team to maintain alignment with long-term goals.

## 2. Scope
The refactor aims to:
- Transition all subsystems to a **dedicated service layer** architecture.
- Improve **testability**, **maintainability**, and **separation of concerns**.
- Establish a **documentation-first** workflow where `docs/` is the source of truth.

## 3. Architecture Overview
**Key Layers:**
1. **Routes Layer** — FastAPI route handlers; minimal logic.
2. **Service Layer** — Pure business logic; no framework dependencies.
3. **Schema Layer** — Pydantic models for validation and serialization.
4. **Persistence Layer** — Database or external API integration.
5. **Config Layer** — Centralized settings with environment-based overrides.

**Data Flow Example (Search Request):**
1. Request hits FastAPI route.
2. Route validates input with schema.
3. Route calls service method (DI injected).
4. Service queries database or external API.
5. Response returned using schema.

## 4. Non-Functional Requirements
- **Test Coverage**: >90% unit test coverage.
- **Performance**: <200ms average API response time for common queries.
- **Security**: Authentication for admin endpoints; input validation on all routes.
- **Extensibility**: Minimal coupling; future modules plug into the service layer.

## 5. Documentation Governance
- All feature changes require updates to:
  - `docs/full_api_reference.md`
  - Relevant developer guides in `docs/`
  - Example API requests/responses
  - `CHANGELOG.md`
- Docs must be updated **before merging PRs**.

## 6. Deployment Model
- **Dev**: Local Docker + SQLite
- **Prod**: Containerized FastAPI app with Postgres and optional Redis
- CI/CD: GitHub Actions with linting, tests, and build pipelines.

## 7. Security Model
- OAuth2 for Spotify integration.
- JWT for API authentication (future step).
- Principle of least privilege for DB access.

## 8. Risks & Mitigations
- **Risk**: Drift between docs and code.
  **Mitigation**: PR checklist and CI step that flags doc inconsistencies.
- **Risk**: Large refactor introduces regressions.
  **Mitigation**: Incremental step-by-step plan with green tests at each stage.

## 9. Security Considerations

The current implementation uses a dynamic, auto-generated admin API key for protecting administrative endpoints. This significantly mitigates the risk of a leaked key compared to a static key. The details of this approach are documented in the [Admin API Key Mitigation Strategy](./admin_api_key_mitigation.md) document.

While this is a significant improvement, the use of a single API key for all admin operations still presents a risk. Future phases of the project will implement more granular, role-based access control (RBAC) and more robust authentication mechanisms, such as OAuth2 or JWT.

The security risk and mitigation documents, and this section, must be maintained alongside any future changes to authentication or admin key usage.

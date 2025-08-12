# High-Level Design (HLD) – Zotify API Refactor

**Status:** Live Document

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
4. **Persistence Layer** — A unified, backend-agnostic database system built on SQLAlchemy.
5. **Provider Abstraction Layer** — An interface that decouples the core application from specific music service providers (e.g., Spotify). All interactions with external music services go through this layer.
6. **Config Layer** — Centralized settings with environment-based overrides.

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

> Note: Specific, long-term security ambitions are tracked in the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document.

## 8. Risks & Mitigations
- **Risk**: Drift between docs and code.
  **Mitigation**: PR checklist and CI step that flags doc inconsistencies.
- **Risk**: Large refactor introduces regressions.
  **Mitigation**: Incremental step-by-step plan with green tests at each stage.

## 9. Security

A comprehensive overview of the security architecture, principles, and roadmap for the Zotify API project is available in the [Zotify API Security](./SECURITY.md) document. This document serves as the definitive security reference for the project.

### Development Process / Task Completion

**All development tasks must comply with the Task Execution Checklist.**
The canonical checklist is located at `docs/projectplan/task_checklist.md`. Before a task is marked complete (including committing, creating a PR, or merging), follow the checklist: update HLD/LLD as needed, ensure security & privacy checks, update docs, write tests, and confirm all tests pass.

This checklist is authoritative and enforced for every task.

---

## 10. Future Vision

While this document outlines the current architecture, the project maintains a separate [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document. This file captures the long-term product vision, including goals for usability, competitive differentiation, and advanced feature sets that go beyond the current roadmap.

# High-Level Design (HLD) – Zotify API Refactor

**Status:** Live Document

## 1. Purpose
This document outlines the high-level architecture, scope, and guiding principles for the ongoing Zotify API refactor. It serves as a blueprint for the development team to maintain alignment with long-term goals.

## 2. Scope
The refactor aims to:
- Transition all subsystems to a **dedicated service layer** architecture.
- Improve **testability**, **maintainability**, and **separation of concerns**.
- Establish a **living documentation** workflow where all documentation is kept in constant alignment with the codebase.

## 3. Architecture Overview
**Key Layers:**
1. **Routes Layer** — FastAPI route handlers; minimal logic.
2. **Service Layer** — Pure business logic; no framework dependencies.
3. **Schema Layer** — Pydantic models for validation and serialization.
4. **Persistence Layer** — A unified, backend-agnostic database system built on SQLAlchemy.
5. **Provider Abstraction Layer** — An interface that decouples the core application from specific music service providers (e.g., Spotify). All interactions with external music services go through this layer.
6. **Config Layer** — Centralized settings with environment-based overrides.
7. **Generic Error Handling Layer** — A centralized, platform-wide module for catching, processing, and responding to all exceptions.
8. **Logging Layer** — A centralized, extendable service for handling all application logging, including system, audit, and job status logs.

**Data Flow Example (Search Request):**
1. Request hits FastAPI route.
2. Route validates input with schema.
3. Route calls service method (DI injected).
4. Service queries database or external API.
5. Response returned using schema.

### 3.1 Supporting Modules

The Zotify Platform includes supporting modules that are not part of the Core API but are essential to the platform's ecosystem.

-   **Gonk-TestUI:** A standalone developer testing UI built with Flask and JavaScript. It provides a web-based interface for interacting with all API endpoints and includes an embedded database browser. Its architecture is a simple client-server model, where the frontend fetches the API schema dynamically to generate forms. It is designed to be run locally during development.

-   **Snitch:** A planned helper application for managing the OAuth callback flow for CLI-based clients. The proposed architecture is a lightweight, self-contained Go application that runs a temporary local web server to capture the redirect from the authentication provider (e.g., Spotify) and securely forward the credentials to the Core API.

### 3.2 Generic Error Handling

To ensure platform-wide stability and consistent behavior, the system implements a centralized error handling module. This layer is designed to be the single point of processing for all unhandled exceptions, whether they originate from API endpoints, background tasks, or internal service calls.

**Key Principles:**
-   **Global Interception:** The module hooks into FastAPI's middleware, `sys.excepthook`, and the `asyncio` event loop to provide global coverage.
-   **Standardized Responses:** It formats all errors into a consistent, predictable schema (e.g., JSON for the API), preventing inconsistent or leaky error messages.
-   **Configurable Automation:** It features a trigger/action system that can be configured to perform automated actions (e.g., send alerts, retry operations) in response to specific, predefined error types.

This architectural component is critical for system resilience, maintainability, and providing a clean, professional experience for API consumers.

### 3.3 Logging Layer

To ensure consistent and comprehensive observability, the platform implements a centralized and extendable logging system. This layer is designed to be the single point of entry for all logging activities across the application.

**Key Principles:**
- **Centralized Service:** A single `LoggingService` is responsible for receiving and dispatching all log messages.
- **Pluggable Handlers:** The service uses a handler-based architecture, allowing new logging backends (e.g., console, file, database, external service) to be added without changing core application code.
- **Multiple Log Types:** The system is designed to handle different types of logs, including standard system/debug messages, structured JSON audit logs for compliance, and database-backed logs for tracking asynchronous jobs.

This component is critical for debugging, monitoring, and auditing the platform. For a more detailed breakdown, see the [`LOGGING_SYSTEM_DESIGN.md`](./LOGGING_SYSTEM_DESIGN.md) document.

## 4. Non-Functional Requirements
- **Test Coverage**: >90% unit test coverage.
- **Performance**: <200ms average API response time for common queries.
- **Security**: Authentication for admin endpoints; input validation on all routes.
- **Extensibility**: Minimal coupling; future modules plug into the service layer.

## 5. Documentation Governance

The project is currently in a phase of audit and alignment, where the primary goal is to bring all documentation in sync with the implemented reality of the codebase. The following principles guide this "living documentation" approach:

- **Reality First**: The codebase is treated as the ground truth. Documentation is updated to reflect the actual, verified behavior of the application.
- **Continuous Alignment**: All significant changes to code must be accompanied by corresponding updates to all relevant documentation (e.g., LLD, changelogs, user guides) in the same commit.
- **Centralized Logging**: All work must be logged in the project's official logs (e.g., `AUDIT-PHASE-3.md`, `ACTIVITY.md`) to maintain a clear, traceable history of changes.
- **Mandatory Verification**: When new documents are created, a verification step must confirm they are correctly integrated into the existing documentation hierarchy (e.g., linked in `PROJECT_REGISTRY.md`).

Once the codebase and documentation have been fully aligned and the design has stabilized, the project may adopt a more formal "docs-first" workflow for future feature development, where design documents are created and approved before implementation begins.

## 6. Deployment Model
- **Dev**: Local Docker + SQLite
- **Prod**: Containerized FastAPI app with Postgres and optional Redis
- CI/CD: GitHub Actions with linting, tests, and build pipelines.

## 7. Security Model
- OAuth2 for Spotify integration.
- JWT for API authentication (future step).
- Principle of least privilege for DB access.
- **CORS Policy:** The API implements a permissive CORS (Cross-Origin Resource Sharing) policy to allow web-based UIs (like the `gonk-testUI`) from any origin to interact with the API. This is a requirement for browser-based tools.

> Note: Specific, long-term security ambitions are tracked in the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document.

## 8. Risks & Mitigations
- **Risk**: Drift between docs and code.
  **Mitigation**: PR checklist and CI step that flags doc inconsistencies.
- **Risk**: Large refactor introduces regressions.
  **Mitigation**: Incremental step-by-step plan with green tests at each stage.

## 9. Security

A comprehensive overview of the security architecture, principles, and roadmap for the Zotify API project is available in the [Zotify API Security](./SECURITY.md) document. This document serves as the definitive security reference for the project.


---

## 10. Future Vision

While this document outlines the current architecture, the project maintains a separate [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document. This file captures the long-term product vision, including goals for usability, competitive differentiation, and advanced feature sets that go beyond the current roadmap.

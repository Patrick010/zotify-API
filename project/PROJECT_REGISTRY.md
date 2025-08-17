# PRINCE2 Project Registry

**Date:** 2025-08-11
**Status:** Live Document

## 1. Purpose

This document serves as the master file, or single source of truth, for tracking all key documents, records, and artifacts for the Zotify API project. It provides a centralized index for all stakeholders to ensure traceability and transparency. To maintain this document's value, it is mandatory that any new markdown documentation file created anywhere in the project is added to this registry.

---

## 2. Core Project Planning Documents

| Document | Location | Description |
|---|---|---|
| **Onboarding Guide** | [`ONBOARDING.md`](./ONBOARDING.md) | The primary entry point and guide for new developers to get up to speed on the project. |
| **Project Brief** | [`PROJECT_BRIEF.md`](./PROJECT_BRIEF.md) | A high-level summary of the project's purpose, scope, and justification (PRINCE2). |
| **Project Initiation Document (PID)** | [`PID.md`](./PID.md) | The formal 'living document' that defines the project's scope, plans, and controls (PRINCE2). |
| **High-Level Design (HLD)** | [`HIGH_LEVEL_DESIGN.md`](./HIGH_LEVEL_DESIGN.md) | Outlines the high-level architecture, scope, and principles. |
| **Low-Level Design (LLD)** | [`LOW_LEVEL_DESIGN.md`](./LOW_LEVEL_DESIGN.md) | Describes specific work items and detailed implementation designs. |
| **Roadmap** | [`ROADMAP.md`](./ROADMAP.md) | Outlines the high-level phases and major milestones of development. |
| **Execution Plan** | [`EXECUTION_PLAN.md`](./EXECUTION_PLAN.md) | Provides a detailed breakdown of tasks required to fulfill the roadmap. |
| **Endpoints Reference** | [`ENDPOINTS.md`](./ENDPOINTS.md) | A canonical reference for all public API endpoints for both the Zotify and Snitch projects. |
| **Future Enhancements** | [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) | A "parking lot" for new ideas and long-term ambitions not on the current roadmap. |
| **Lessons Learnt Log** | [`LESSONS-LEARNT.md`](./LESSONS-LEARNT.md) | A log of key takeaways and insights from each project phase. |
| **Logging System Design** | [`LOGGING_SYSTEM_DESIGN.md`](./LOGGING_SYSTEM_DESIGN.md) | The detailed architectural design for the centralized logging system. |
| **Logging Traceability Matrix** | [`LOGGING_TRACEABILITY_MATRIX.md`](./LOGGING_TRACEABILITY_MATRIX.md) | Maps logging system requirements to design documents and backlog tasks. |
| **Project Backlog** | [`BACKLOG.md`](./BACKLOG.md) | A tactical backlog of tasks managed by the formal qualification process defined in the PID. All tasks must conform to the template in this file. |
| **Changelog** | [`api/docs/CHANGELOG.md`](./api/docs/CHANGELOG.md) | A log of all user-facing changes for each version. |
| **Traceability Matrix** | [`TRACEABILITY_MATRIX.md`](./TRACEABILITY_MATRIX.md) | A live matrix mapping requirements from use cases and design docs to implementation and test status. |
| **Use Cases** | [`USECASES.md`](./USECASES.md) | A collection of user-driven scenarios and requirements for the API. |
| **Use Case Gap Analysis** | [`USECASES_GAP_ANALYSIS.md`](./USECASES_GAP_ANALYSIS.md) | An analysis of the gaps between the desired use cases and the current implementation. |
| **Feature Specifications** | [`api/docs/reference/FEATURE_SPECS.md`](../api/docs/reference/FEATURE_SPECS.md) | The master index for detailed, standardized specifications for all system features. |

---

## 2.1. API Documentation

This section lists documents that are specific to the API's implementation, operation, and usage.

| Document | Location | Description |
|---|---|---|
| **Operator Manual** | [`api/docs/manuals/OPERATOR_MANUAL.md`](../api/docs/manuals/OPERATOR_MANUAL.md) | Provides guidance for deploying, configuring, and maintaining the Zotify API in a production environment, including process management and log rotation. |
| **Developer Guide** | [`api/docs/manuals/DEVELOPER_GUIDE.md`](../api/docs/manuals/DEVELOPER_GUIDE.md) | A guide for developers on setting up a local environment, running the server, executing tests, and interacting with the API. |
| **User Manual** | [`api/docs/manuals/USER_MANUAL.md`](../api/docs/manuals/USER_MANUAL.md) | A manual for end-users of the API, explaining the core workflow for downloading tracks and the standard error response format. |
| **Error Handling Guide** | [`api/docs/manuals/ERROR_HANDLING_GUIDE.md`](../api/docs/manuals/ERROR_HANDLING_GUIDE.md) | A developer guide for the Generic Error Handling Module, explaining how to use it, extend it with custom actions, and best practices. |
| **Spotify Provider** | [`api/docs/providers/spotify.md`](../api/docs/providers/spotify.md) | Describes the implementation of the Spotify provider connector, including its dependencies and provider-specific limitations. |
| **Authentication Spec** | [`api/docs/reference/features/authentication.md`](../api/docs/reference/features/authentication.md) | A feature specification for the static Admin API Key authentication mechanism, detailing its purpose, technical implementation, and usage. |
| **Provider Extensions Spec** | [`api/docs/reference/features/provider_agnostic_extensions.md`](../api/docs/reference/features/provider_agnostic_extensions.md) | A proposal document that defines the structure and requirements for creating detailed specifications for all API features, ensuring consistency across different provider integrations. |
| **Error Handling Design** | [`api/docs/system/ERROR_HANDLING_DESIGN.md`](../api/docs/system/ERROR_HANDLING_DESIGN.md) | The technical design specification for the Generic Error Handling Module, detailing its components, class structure, and integration strategy. |
| **Installation Guide** | [`api/docs/system/INSTALLATION.md`](../api/docs/system/INSTALLATION.md) | A guide detailing the steps to install the Zotify API from source, including dependency installation and environment configuration for both production and testing. |
| **System Requirements** | [`api/docs/system/REQUIREMENTS.md`](../api/docs/system/REQUIREMENTS.md) | Lists the system and software requirements for running the Zotify API and its related tools. |
| **Full API Reference** | [`api/docs/reference/full_api_reference.md`](../api/docs/reference/full_api_reference.md) | A comprehensive, manually-created reference for all API endpoints. |
| **Privacy Compliance** | [`api/docs/system/PRIVACY_COMPLIANCE.md`](../api/docs/system/PRIVACY_COMPLIANCE.md) | An overview of how the Zotify API project complies with data protection laws like GDPR. |

---

## 3. Supporting Modules

This section lists the official supporting modules of the Zotify Platform.

### 3.1. Snitch Module

A planned Go-based helper application to manage OAuth callbacks for CLI clients. The design and planning documents are complete.

| Document | Location | Description |
|---|---|---|
| **README** | [`snitch/README.md`](../snitch/README.md) | An overview of the Snitch module, a local OAuth callback listener in Go designed to handle headless authentication for the Zotify API. |
| **Architecture** | [`snitch/docs/ARCHITECTURE.md`](../snitch/docs/ARCHITECTURE.md) | Details the architecture of the Snitch module, focusing on its Zero Trust security model with end-to-end payload encryption for the OAuth callback. |
| **Installation Guide** | [`snitch/docs/INSTALLATION.md`](../snitch/docs/INSTALLATION.md) | A guide on how to install, configure, run, and build the Snitch module from source, including prerequisites and troubleshooting. |
| **Milestones** | [`snitch/docs/MILESTONES.md`](../snitch/docs/MILESTONES.md) | A document for tracking key project milestones and events for the Snitch module's development. |
| **Modules** | [`snitch/docs/MODULES.md`](../snitch/docs/MODULES.md) | An overview of the internal Go packages within the Snitch module, including the `cmd` entrypoint and the `listener` core logic. |
| **Phases** | [`snitch/docs/PHASES.md`](../snitch/docs/PHASES.md) | The phased development plan for the Snitch subproject. |
| **Project Plan** | [`snitch/docs/PROJECT_PLAN.md`](../snitch/docs/PROJECT_PLAN.md) | The project plan for Snitch, outlining the problem it solves, its integration with the main API, security constraints, and phased development plan. |
| **Secure Callback Design** | [`snitch/docs/PHASE_2_SECURE_CALLBACK.md`](../snitch/docs/PHASE_2_SECURE_CALLBACK.md) | A superseded design document for the Snitch secure callback, now replaced by the Zero Trust model. |
| **Status** | [`snitch/docs/STATUS.md`](../snitch/docs/STATUS.md) | A live status document tracking the progress of the Snitch subproject against its development phases. |
| **Test Runbook** | [`snitch/docs/TEST_RUNBOOK.md`](../snitch/docs/TEST_RUNBOOK.md) | A runbook for testing the Snitch module, covering both automated unit tests and manual end-to-end testing procedures. |
| **User Manual** | [`snitch/docs/USER_MANUAL.md`](../snitch/docs/USER_MANUAL.md) | A manual for end-users explaining the purpose of the Snitch helper application and how it works within the OAuth 2.0 authentication flow. |
| **Zero Trust Design** | [`snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md`](../snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md) | The design specification for a Zero Trust secure callback flow for Snitch, using JWTs and asymmetric cryptography to protect the OAuth code. |
| **IPC Communication** | [`snitch/docs/phase5-ipc.md`](../snitch/docs/phase5-ipc.md) | Outlines the secure Inter-Process Communication (IPC) mechanism between the Zotify API and the Snitch helper application. |

### 3.2. Gonk-TestUI Module

A Flask and JavaScript-based web UI for developer testing and interaction with the Zotify API.

| Document | Location | Description |
|---|---|---|
| **README** | [`gonk-testUI/README.md`](../gonk-testUI/README.md) | The main README for the Gonk Test UI, a standalone developer tool for testing the Zotify API, including setup and usage instructions. |
| **Architecture** | [`gonk-testUI/docs/ARCHITECTURE.md`](../gonk-testUI/docs/ARCHITECTURE.md) | An overview of the `gonk-testUI` architecture, detailing the Flask backend, dynamic frontend, and `sqlite-web` integration. |
| **Changelog** | [`gonk-testUI/docs/CHANGELOG.md`](../gonk-testUI/docs/CHANGELOG.md) | A changelog for the `gonk-testUI` module, documenting notable changes for each version. |
| **Contributing Guide** | [`gonk-testUI/docs/CONTRIBUTING.md`](../gonk-testUI/docs/CONTRIBUTING.md) | A standard contributing guide outlining the development process for making contributions to the `gonk-testUI` module. |
| **User Manual** | [`gonk-testUI/docs/USER_MANUAL.md`](../gonk-testUI/docs/USER_MANUAL.md) | A detailed user manual for the `gonk-testUI`, explaining how to set up, configure, and use its features for API testing and database browsing. |

---

## 4. Audit & Alignment Documents

| Document | Location | Description |
|---|---|---|
| **HLD/LLD Alignment Plan** | [`audit/HLD_LLD_ALIGNMENT_PLAN.md`](./audit/HLD_LLD_ALIGNMENT_PLAN.md) | The phased plan for bringing design documents into alignment with the codebase. |
| **Live Activity Log** | [`ACTIVITY.md`](./ACTIVITY.md) | A live, chronological log of all major tasks and audit activities. |
| **Security Document** | [`SECURITY.md`](./SECURITY.md) | The definitive security reference for the project. |
| **Audit Log: Phase 1** | [`audit/AUDIT-phase-1.md`](./audit/AUDIT-phase-1.md) | Log of activities and findings from Phase 1 of the alignment plan. |
| **Audit Log: Phase 2** | [`audit/AUDIT-phase-2.md`](./audit/AUDIT-phase-2.md) | Log of activities and findings from Phase 2 of the alignment plan. |
| **Audit Log: Phase 3** | [`audit/AUDIT-PHASE-3.md`](./audit/AUDIT-PHASE-3.md) | Log of activities and findings from Phase 3 of the alignment plan. |

---

## 4. Completion Reports

| Document | Location |
|---|---|
| **Consolidated Report (Phase 2/3)** | [`reports/20250811-CONSOLIDATED-COMPLETION-REPORT.md`](./reports/20250811-CONSOLIDATED-COMPLETION-REPORT.md) |
| ... | ... |

---

## 5. Change Log

| Date | Change | Author |
|---|---|---|
| 2025-08-11 | Initial creation of the project registry. | Jules |
| 2025-08-11 | Updated LLD and Traceability Matrix for "Error Handling & Logging" alignment. | Jules |
| 2025-08-11 | Updated LLD and Traceability Matrix for "Spotify Integration" alignment. | Jules |

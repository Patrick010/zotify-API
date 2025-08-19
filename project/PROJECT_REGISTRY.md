# PRINCE2 Project Registry

**Date:** 2025-08-17
**Status:** Live Document

## 1. Purpose

This document serves as the master file, or single source of truth, for tracking all key documents, records, and artifacts for the Zotify API project. It provides a centralized index for all stakeholders to ensure traceability and transparency. To maintain this document's value, it is mandatory that any new markdown documentation file created anywhere in the project is added to this registry.

---

## 2. Core Project Planning Documents

| Document | Location | Description |
|---|---|---|
| **Project Registry** | [`PROJECT_REGISTRY.md`](./PROJECT_REGISTRY.md) | This document, the master index for all project artifacts. |
| **Onboarding Guide** | [`ONBOARDING.md`](./ONBOARDING.md) | The primary entry point and guide for new developers to get up to speed on the project. |
| **Current State** | [`CURRENT_STATE.md`](./logs/CURRENT_STATE.md) | A live snapshot of the project's most recent status, goals, and pending work. |
| **Session Log** | [`SESSION_LOG.md`](./logs/SESSION_LOG.md) |Log of activities and findings from sessions. |
| **Live Activity Log** | [`ACTIVITY.md`](./logs/ACTIVITY.md) | A live, chronological log of all major tasks and audit activities. |
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
| **Logging Phased Implementation** | [`LOGGING_PHASES.md`](./LOGGING_PHASES.md) | The authoritative document tracking the phased design and implementation of the Extendable Logging System. |
| **Logging Traceability Matrix** | [`LOGGING_TRACEABILITY_MATRIX.md`](./LOGGING_TRACEABILITY_MATRIX.md) | Maps logging system requirements to design documents and backlog tasks. |
| **Dynamic Plugin Proposal** | [`DYNAMIC_PLUGIN_PROPOSAL.md`](./proposals/DYNAMIC_PLUGIN_PROPOSAL.md) | A formal proposal for adding a dynamic plugin system for custom logging sinks. |
| **Low-Code Integration Proposal** | [`LOW_CODE_PROPOSAL.md`](./proposals/LOW_CODE_PROPOSAL.md) | A formal proposal for integrating with low-code platforms like Node-RED. |
| **Home Automation Proposal** | [`HOME_AUTOMATION_PROPOSAL.md`](./proposals/HOME_AUTOMATION_PROPOSAL.md) | A formal proposal for integrating with home automation platforms like Home Assistant. |
| **Multi-Source Metadata Proposal** | [`MULTI_SOURCE_METADATA_PROPOSAL.md`](./proposals/MULTI_SOURCE_METADATA_PROPOSAL.md) | A formal proposal for a plugin-driven, multi-source metadata ingestion and querying system. |
| **Project Backlog** | [`BACKLOG.md`](./BACKLOG.md) | A tactical backlog of tasks managed by the formal qualification process defined in the PID. |
| **Traceability Matrix** | [`TRACEABILITY_MATRIX.md`](./TRACEABILITY_MATRIX.md) | A live matrix mapping requirements from use cases and design docs to implementation and test status. |
| **Use Cases** | [`USECASES.md`](./USECASES.md) | A collection of user-driven scenarios and requirements for the API. |
| **Use Case Gap Analysis** | [`USECASES_GAP_ANALYSIS.md`](./USECASES_GAP_ANALYSIS.md) | An analysis of the gaps between the desired use cases and the current implementation. |
| **Task Checklist** | [`TASK_CHECKLIST.md`](./TASK_CHECKLIST.md) | A checklist to be used for every task to ensure compliance with project standards. |
| **Dependency Policy** | [`DEPENDENCIES.md`](./DEPENDENCIES.md) | The policy and registry for managing third-party dependencies. |
| **Security Document** | [`SECURITY.md`](./SECURITY.md) | The definitive security reference for the project. |

---

## 3. API & Module Documentation

### 3.1. Core API Documentation
| Document | Location | Description |
|---|---|---|
| **Changelog** | [`api/docs/CHANGELOG.md`](../api/docs/CHANGELOG.md) | A log of all user-facing changes for each version. |
| **Feature Specifications** | [`api/docs/reference/FEATURE_SPECS.md`](../api/docs/reference/FEATURE_SPECS.md) | The master index for detailed, standardized specifications for all system features. |
| **Operator Manual** | [`api/docs/manuals/OPERATOR_MANUAL.md`](../api/docs/manuals/OPERATOR_MANUAL.md) | Provides guidance for deploying, configuring, and maintaining the Zotify API in a production environment. |
| **Developer Guide** | [`api/docs/manuals/DEVELOPER_GUIDE.md`](../api/docs/manuals/DEVELOPER_GUIDE.md) | A guide for developers on setting up a local environment, running the server, executing tests, and interacting with the API. |
| **User Manual** | [`api/docs/manuals/USER_MANUAL.md`](../api/docs/manuals/USER_MANUAL.md) | A manual for end-users of the API, explaining the core workflow for downloading tracks and the standard error response format. |
| **Error Handling Guide** | [`api/docs/manuals/ERROR_HANDLING_GUIDE.md`](../api/docs/manuals/ERROR_HANDLING_GUIDE.md) | A developer guide for the Generic Error Handling Module. |
| **Logging Guide** | [`api/docs/manuals/LOGGING_GUIDE.md`](../api/docs/manuals/LOGGING_GUIDE.md) | A comprehensive developer guide for the new Flexible Logging Framework. |
| **Spotify Provider** | [`api/docs/providers/spotify.md`](../api/docs/providers/spotify.md) | Describes the implementation of the Spotify provider connector. |
| **Authentication Spec** | [`api/docs/reference/features/authentication.md`](../api/docs/reference/features/authentication.md) | A feature specification for the static Admin API Key authentication mechanism. |
| **Provider OAuth2 Flow Spec** | [`api/docs/reference/features/provider_oauth.md`](../api/docs/reference/features/provider_oauth.md) | A feature specification for the provider-agnostic OAuth2 authentication flow. |
| **Provider Extensions Spec** | [`api/docs/reference/features/provider_agnostic_extensions.md`](../api/docs/reference/features/provider_agnostic_extensions.md) | A proposal for a standardized structure for feature specification documents. |
| **Error Handling Design** | [`api/docs/system/ERROR_HANDLING_DESIGN.md`](../api/docs/system/ERROR_HANDLING_DESIGN.md) | The technical design specification for the Generic Error Handling Module. |
| **Installation Guide** | [`api/docs/system/INSTALLATION.md`](../api/docs/system/INSTALLATION.md) | A guide detailing the steps to install the Zotify API from source. |
| **System Requirements** | [`api/docs/system/REQUIREMENTS.md`](../api/docs/system/REQUIREMENTS.md) | Lists the system and software requirements for running the Zotify API. |
| **Generated API Reference** | [`api/docs/reference/API_REFERENCE.md`](../api/docs/reference/API_REFERENCE.md) | A comprehensive, auto-generated reference for all API endpoints based on the OpenAPI spec. |
| **Flexible Logging Framework Design** | [`api/docs/reference/features/developer_flexible_logging_framework.md`](../api/docs/reference/features/developer_flexible_logging_framework.md) | A design document for a developer-facing, programmable logging framework. |
| **Privacy Compliance** | [`api/docs/system/PRIVACY_COMPLIANCE.md`](../api/docs/system/PRIVACY_COMPLIANCE.md) | An overview of how the Zotify API project complies with data protection laws like GDPR. |

### 3.2. Snitch Module Documentation
| Document | Location | Description |
|---|---|---|
| **README** | [`snitch/README.md`](../snitch/README.md) | An overview of the Snitch module. |
| **Architecture** | [`snitch/docs/ARCHITECTURE.md`](../snitch/docs/ARCHITECTURE.md) | Details the architecture of the Snitch module and its Zero Trust security model. |
| **Installation Guide** | [`snitch/docs/INSTALLATION.md`](../snitch/docs/INSTALLATION.md) | A guide on how to install, configure, run, and build the Snitch module. |
| **Milestones** | [`snitch/docs/MILESTONES.md`](../snitch/docs/MILESTONES.md) | A document for tracking key project milestones for the Snitch module. |
| **Modules** | [`snitch/docs/MODULES.md`](../snitch/docs/MODULES.md) | An overview of the internal Go packages within the Snitch module. |
| **Phases** | [`snitch/docs/PHASES.md`](../snitch/docs/PHASES.md) | The phased development plan for the Snitch subproject. |
| **Project Plan** | [`snitch/docs/PROJECT_PLAN.md`](../snitch/docs/PROJECT_PLAN.md) | The project plan for Snitch, outlining the problem it solves and its development plan. |
| **Secure Callback Design (Superseded)** | [`snitch/docs/PHASE_2_SECURE_CALLBACK.md`](../snitch/docs/PHASE_2_SECURE_CALLBACK.md) | A superseded design document for the Snitch secure callback. |
| **Roadmap** | [`snitch/docs/ROADMAP.md`](../snitch/docs/ROADMAP.md) | The high-level, phased development roadmap for the Snitch subproject. |
| **Status** | [`snitch/docs/STATUS.md`](../snitch/docs/STATUS.md) | A live status document tracking the development progress of the Snitch subproject. |
| **Tasks** | [`snitch/docs/TASKS.md`](../snitch/docs/TASKS.md) | A task list for the development of the Snitch module. |
| **Test Runbook** | [`snitch/docs/TEST_RUNBOOK.md`](../snitch/docs/TEST_RUNBOOK.md) | A runbook for testing the Snitch module. |
| **User Manual** | [`snitch/docs/USER_MANUAL.md`](../snitch/docs/USER_MANUAL.md) | A manual for end-users explaining the purpose of the Snitch helper application. |
| **Zero Trust Design** | [`snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md`](../snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md) | The design specification for a Zero Trust secure callback flow for Snitch. |
| **IPC Communication** | [`snitch/docs/phase5-ipc.md`](../snitch/docs/phase5-ipc.md) | Outlines the secure IPC mechanism between the Zotify API and Snitch. |

### 3.3. Gonk-TestUI Module Documentation
| Document | Location | Description |
|---|---|---|
| **README** | [`gonk-testUI/README.md`](../gonk-testUI/README.md) | The main README for the Gonk Test UI developer tool. |
| **Architecture** | [`gonk-testUI/docs/ARCHITECTURE.md`](../gonk-testUI/docs/ARCHITECTURE.md) | An overview of the `gonk-testUI` architecture. |
| **Changelog** | [`gonk-testUI/docs/CHANGELOG.md`](../gonk-testUI/docs/CHANGELOG.md) | A changelog for the `gonk-testUI` module. |
| **Contributing Guide** | [`gonk-testUI/docs/CONTRIBUTING.md`](../gonk-testUI/docs/CONTRIBUTING.md) | A guide for contributing to the `gonk-testUI` module. |
| **User Manual** | [`gonk-testUI/docs/USER_MANUAL.md`](../gonk-testUI/docs/USER_MANUAL.md) | A detailed user manual for the `gonk-testUI`. |

---

## 4. Audit & Alignment Documents
| Document | Location | Description |
|---|---|---|
| **Audit README** | [`audit/README.md`](./audit/README.md) | An overview of the audit process and documentation. |
| **First Audit** | [`audit/FIRST_AUDIT.md`](./audit/FIRST_AUDIT.md) | The initial audit report for the project. |
| **HLD/LLD Alignment Plan** | [`audit/HLD_LLD_ALIGNMENT_PLAN.md`](./audit/HLD_LLD_ALIGNMENT_PLAN.md) | The phased plan for bringing design documents into alignment with the codebase. |
| **Audit Log: Phase 1** | [`audit/AUDIT-phase-1.md`](./audit/AUDIT-phase-1.md) | Log of activities and findings from Phase 1 of the alignment plan. |
| **Audit Log: Phase 2** | [`audit/AUDIT-phase-2.md`](./audit/AUDIT-phase-2.md) | Log of activities and findings from Phase 2 of the alignment plan. |
| **Audit Log: Phase 3** | [`audit/AUDIT-PHASE-3.md`](./audit/AUDIT-PHASE-3.md) | Log of activities and findings from Phase 3 of the alignment plan. |
| **Audit Log: Phase 4** | [`audit/AUDIT-PHASE-4.md`](./audit/AUDIT-PHASE-4.md) | Log of activities and findings from Phase 4 of the alignment plan. |
| **Audit Traceability Matrix** | [`audit/AUDIT_TRACEABILITY_MATRIX.md`](./audit/AUDIT_TRACEABILITY_MATRIX.md) | A matrix for tracking audit-related requirements and their implementation status. |
| **Phase 4 Traceability Matrix** | [`audit/PHASE_4_TRACEABILITY_MATRIX.md`](./audit/PHASE_4_TRACEABILITY_MATRIX.md) | A traceability matrix specific to the Phase 4 audit. |
| **Code Optimization Plan** | [`audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`](./audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md) | A plan for code optimizations identified during Phase 4. |
| **Audit Prompt** | [`audit/audit-prompt.md`](./audit/audit-prompt.md) | The prompt used for the audit process. |

---

## 6. Archived Documents
This section is for reference and should not be considered current.
| Document | Location |
|---|---|
| **Archived README** | [`archive/README.md`](./archive/README.md) |
| **Archived API Changelog** | [`archive/api/docs/CHANGELOG.md`](./archive/api/docs/CHANGELOG.md) |
| **Archived API Contributing** | [`archive/api/docs/CONTRIBUTING.md`](./archive/api/docs/CONTRIBUTING.md) |
| **Archived API Database** | [`archive/api/docs/DATABASE.md`](./archive/api/docs/DATABASE.md) |
| **Archived API Installation** | [`archive/api/docs/INSTALLATION.md`](./archive/api/docs/INSTALLATION.md) |
| **Archived API Manual** | [`archive/api/docs/MANUAL.md`](./archive/api/docs/MANUAL.md) |
| **Archived Docs Integration Checklist** | [`archive/docs/INTEGRATION_CHECKLIST.md`](./archive/docs/INTEGRATION_CHECKLIST.md) |
| **Archived Docs Developer Guide** | [`archive/docs/developer_guide.md`](./archive/docs/developer_guide.md) |
| **Archived Docs Operator Guide** | [`archive/docs/operator_guide.md`](./archive/docs/operator_guide.md) |
| **Archived Docs Roadmap** | [`archive/docs/roadmap.md`](./archive/docs/roadmap.md) |
| **Archived Zotify API Manual** | [`archive/docs/zotify-api-manual.md`](./archive/docs/zotify-api-manual.md) |
| **Archived Project Plan HLD** | [`archive/docs/projectplan/HLD_Zotify_API.md`](./archive/docs/projectplan/HLD_Zotify_API.md) |
| **Archived Project Plan LLD** | [`archive/docs/projectplan/LLD_18step_plan_Zotify_API.md`](./archive/docs/projectplan/LLD_18step_plan_Zotify_API.md) |
| **Archived Project Plan Security** | [`archive/docs/projectplan/security.md`](./archive/docs/projectplan/security.md) |
| **Archived PP Admin Key Mitigation** | [`archive/docs/projectplan/admin_api_key_mitigation.md`](./archive/docs/projectplan/admin_api_key_mitigation.md) |
| **Archived PP Admin Key Risk** | [`archive/docs/projectplan/admin_api_key_security_risk.md`](./archive/docs/projectplan/admin_api_key_security_risk.md) |
| **Archived PP Doc Maintenance** | [`archive/docs/projectplan/doc_maintenance.md`](./archive/docs/projectplan/doc_maintenance.md) |
| **Archived PP Privacy Compliance** | [`archive/docs/projectplan/privacy_compliance.md`](./archive/docs/projectplan/privacy_compliance.md) |
| **Archived PP Spotify Audit** | [`archive/docs/projectplan/spotify_capability_audit.md`](./archive/docs/projectplan/spotify_capability_audit.md) |
| **Archived PP Spotify Blueprint** | [`archive/docs/projectplan/spotify_fullstack_capability_blueprint.md`](./archive/docs/projectplan/spotify_fullstack_capability_blueprint.md) |
| **Archived PP Spotify Gap Report** | [`archive/docs/projectplan/spotify_gap_alignment_report.md`](./archive/docs/projectplan/spotify_gap_alignment_report.md) |

---

## 7. Change Log
| Date | Change | Author |
|---|---|---|
| 2025-08-11 | Initial creation of the project registry. | Jules |
| 2025-08-17 | Comprehensive audit and update to include all project documentation. | Jules |

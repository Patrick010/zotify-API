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
| **Template Registry** | [`../templates/PROJECT_REGISTRY.md`](../templates/PROJECT_REGISTRY.md) | A registry of all reusable documentation templates. |
| **Handover Brief** | [`HANDOVER_BRIEF.md`](./HANDOVER_BRIEF.md) | A detailed handover brief created at the request of the user. Not to be modified during the session. |
| **Onboarding Guide** | [`ONBOARDING.md`](./ONBOARDING.md) | The primary entry point and guide for new developers to get up to speed on the project. |
| **Current State** | [`CURRENT_STATE.md`](./logs/CURRENT_STATE.md) | **High-Level Snapshot.** A brief, narrative summary of the entire project's state at the end of a work session. It should answer: What was just accomplished? What is the next immediate goal? Are there any blockers? |
| **Session Log** | [`SESSION_LOG.md`](./logs/SESSION_LOG.md) | **Session-Level Reporting.** A detailed log of the activities, findings, and outcomes within a single work session. This is for project-related reporting and can be compared to the audit-specific logs (e.g., `AUDIT-PHASE-5.md`). |
| **Live Activity Log** | [`ACTIVITY.md`](./logs/ACTIVITY.md) | **Granular Task Log.** A reverse-chronological list of every specific, discrete task or action performed (e.g., "Implemented `log-work.py` script", "Fixed CI test failure"). Each entry should be a self-contained unit of work. |
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
| **Dynamic Plugin Proposal** | [`proposals/DYNAMIC_PLUGIN_PROPOSAL.md`](./proposals/DYNAMIC_PLUGIN_PROPOSAL.md) | A formal proposal for adding a dynamic plugin system for custom logging sinks. |
| **Low-Code Integration Proposal** | [`proposals/LOW_CODE_PROPOSAL.md`](./proposals/LOW_CODE_PROPOSAL.md) | A formal proposal for integrating with low-code platforms like Node-RED. |
| **Home Automation Proposal** | [`proposals/HOME_AUTOMATION_PROPOSAL.md`](./proposals/HOME_AUTOMATION_PROPOSAL.md) | A formal proposal for integrating with home automation platforms like Home Assistant. |
| **Multi-Source Metadata Proposal** | [`proposals/MULTI_SOURCE_METADATA_PROPOSAL.md`](./proposals/MULTI_SOURCE_METADATA_PROPOSAL.md) | A formal proposal for a plugin-driven, multi-source metadata ingestion and querying system. |
| **Project Backlog** | [`BACKLOG.md`](./BACKLOG.md) | A tactical backlog of tasks managed by the formal qualification process defined in the PID. |
| **Traceability Matrix** | [`TRACEABILITY_MATRIX.md`](./TRACEABILITY_MATRIX.md) | A live matrix mapping requirements from use cases and design docs to implementation and test status. |
| **Use Cases** | [`USECASES.md`](./USECASES.md) | A collection of user-driven scenarios and requirements for the API. |
| **Use Case Gap Analysis** | [`USECASES_GAP_ANALYSIS.md`](./USECASES_GAP_ANALYSIS.md) | An analysis of the gaps between the desired use cases and the current implementation. |
| **Task Checklist** | [`TASK_CHECKLIST.md`](./TASK_CHECKLIST.md) | A checklist to be used for every task to ensure compliance with project standards. |
| **Dependency Policy** | [`DEPENDENCIES.md`](./DEPENDENCIES.md) | The policy and registry for managing third-party dependencies. |
| **Security Document** | [`SECURITY.md`](./SECURITY.md) | The definitive security reference for the project. |
| **Project CI/CD Guide** | [`CICD.md`](./CICD.md) | A high-level guide to CI/CD philosophy for project management. |

---

## 3. Audit & Alignment Documents
| Document | Location | Description |
|---|---|---|
| **First Audit** | [`audit/FIRST_AUDIT.md`](./audit/FIRST_AUDIT.md) | The initial audit report for the project. |
| **HLD/LLD Alignment Plan** | [`audit/HLD_LLD_ALIGNMENT_PLAN.md`](./audit/HLD_LLD_ALIGNMENT_PLAN.md) | The phased plan for bringing design documents into alignment with the codebase. |
| **Audit Log: Phase 1** | [`audit/AUDIT-phase-1.md`](./audit/AUDIT-phase-1.md) | Log of activities and findings from Phase 1 of the alignment plan. |
| **Audit Log: Phase 2** | [`audit/AUDIT-phase-2.md`](./audit/AUDIT-phase-2.md) | Log of activities and findings from Phase 2 of the alignment plan. |
| **Audit Log: Phase 3** | [`audit/AUDIT-PHASE-3.md`](./audit/AUDIT-PHASE-3.md) | Log of activities and findings from Phase 3 of the alignment plan. |
| **Audit Log: Phase 4** | [`audit/AUDIT-PHASE-4.md`](./audit/AUDIT-PHASE-4.md) | Log of activities and findings from Phase 4 of the alignment plan. |
| **Audit Log: Phase 5** | [`audit/AUDIT-PHASE-5.md`](./audit/AUDIT-PHASE-5.md) | Log of activities and findings from Phase 5 of the alignment plan. |
| **Audit Traceability Matrix** | [`audit/AUDIT_TRACEABILITY_MATRIX.md`](./audit/AUDIT_TRACEABILITY_MATRIX.md) | A matrix for tracking audit-related requirements and their implementation status. |
| **Code Optimization Plan** | [`audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md`](./audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md) | A plan for code optimizations identified during Phase 4 of the audit. |
| **Phase 4 Traceability Matrix** | [`audit/PHASE_4_TRACEABILITY_MATRIX.md`](./audit/PHASE_4_TRACEABILITY_MATRIX.md) | A traceability matrix specific to the Phase 4 audit. |
| **Audit Prompt** | [`audit/audit-prompt.md`](./audit/audit-prompt.md) | The prompt used for the audit process. |

---

## 4. Archived Documents
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

## 5. Change Log
| Date | Change | Author |
|---|---|---|
| 2025-08-11 | Initial creation of the project registry. | Jules |
| 2025-08-17 | Comprehensive audit and update to include all project documentation. | Jules |

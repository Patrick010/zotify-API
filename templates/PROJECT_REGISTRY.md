# Project Registry

**Date:** <DATE>
**Status:** Live Document

## 1. Purpose

This document serves as the master file, or single source of truth, for tracking all key documents, records, and artifacts for the <PROJECT_NAME>. It provides a centralized index for all stakeholders to ensure traceability and transparency. To maintain this document's value, it is mandatory that any new markdown documentation file created anywhere in the project is added to this registry.

---

## 2. Core Project Planning Documents

| Document | Location | Description |
|---|---|---|
| **Project Registry** | [`PROJECT_REGISTRY.md`](./PROJECT_REGISTRY.md) | This document, the master index for all project artifacts. |
| **Onboarding Guide** | [`ONBOARDING.md`](./ONBOARDING.md) | The primary entry point and guide for new developers. |
| **Current State** | [`logs/CURRENT_STATE.md`](./logs/CURRENT_STATE.md) | A live snapshot of the project's most recent status and goals. |
| **Session Log** | [`logs/SESSION_LOG.md`](./logs/SESSION_LOG.md) |Log of activities and findings from work sessions. |
| **Live Activity Log** | [`logs/ACTIVITY.md`](./logs/ACTIVITY.md) | A live, chronological log of all major tasks and audit activities. |
| **Project Brief** | [`PROJECT_BRIEF.md`](./PROJECT_BRIEF.md) | A high-level summary of the project's purpose, scope, and justification. |
| **Project Initiation Document (PID)** | [`PID.md`](./PID.md) | The formal 'living document' that defines the project's scope, plans, and controls. |
| **High-Level Design (HLD)** | [`HIGH_LEVEL_DESIGN.md`](./HIGH_LEVEL_DESIGN.md) | Outlines the high-level architecture, scope, and principles. |
| **Low-Level Design (LLD)** | [`LOW_LEVEL_DESIGN.md`](./LOW_LEVEL_DESIGN.md) | Describes specific work items and detailed implementation designs. |
| **Roadmap** | [`ROADMAP.md`](./ROADMAP.md) | Outlines the high-level phases and major milestones. |
| **Execution Plan** | [`EXECUTION_PLAN.md`](./EXECUTION_PLAN.md) | Provides a detailed breakdown of tasks required to fulfill the roadmap. |
| **Endpoints Reference** | [`ENDPOINTS.md`](./ENDPOINTS.md) | A canonical reference for all public API endpoints. |
| **Future Enhancements** | [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) | A "parking lot" for new ideas not on the current roadmap. |
| **Lessons Learnt Log** | [`LESSONS-LEARNT.md`](./LESSONS-LEARNT.md) | A log of key takeaways and insights from each project phase. |
| **Project Backlog** | [`BACKLOG.md`](./BACKLOG.md) | A tactical backlog of tasks. |
| **Traceability Matrix** | [`TRACEABILITY_MATRIX.md`](./TRACEABILITY_MATRIX.md) | A matrix mapping requirements to implementation and test status. |
| **Use Cases** | [`USECASES.md`](./USECASES.md) | A collection of user-driven scenarios and requirements. |
| **Use Case Gap Analysis** | [`USECASES_GAP_ANALYSIS.md`](./USECASES_GAP_ANALYSIS.md) | An analysis of the gaps between desired use cases and the current implementation. |
| **Task Checklist** | [`TASK_CHECKLIST.md`](./TASK_CHECKLIST.md) | A checklist to be used for every task to ensure compliance with project standards. |
| **Dependency Policy** | [`DEPENDENCIES.md`](./DEPENDENCIES.md) | The policy and registry for managing third-party dependencies. |
| **Security Document** | [`SECURITY.md`](./SECURITY.md) | The definitive security reference for the project. |
| **Handover Brief** | [`HANDOVER_BRIEF_JULES.md`](./reports/HANDOVER_BRIEF_JULES.md) | A summary of work completed and next steps for developer handover. |

---

## 3. Template Documents

The `templates/` directory contains the master templates for all standard project documentation. When starting a new project or adding a standard document to an existing one, you should copy the relevant file from this directory into the `project/` directory. This ensures all projects follow a consistent documentation structure.

| Document | Location | Description |
|---|---|---|
| **Template Source** | `../../templates/` | The root directory containing all master document templates. |

---

## 4. API & Module Documentation

### 4.1. Core API Documentation
| Document | Location | Description |
|---|---|---|
| **Changelog** | `docs/CHANGELOG.md` | A log of all user-facing changes for each version. |
| **Feature Specifications** | `docs/reference/FEATURE_SPECS.md` | The master index for detailed, standardized specifications for all system features. |
| **Operator Manual** | `docs/manuals/OPERATOR_MANUAL.md` | Provides guidance for deploying, configuring, and maintaining the API in a production environment. |
| **Developer Guide** | `docs/manuals/DEVELOPER_GUIDE.md` | A guide for developers on setting up a local environment and running tests. |
| **User Manual** | `docs/manuals/USER_MANUAL.md` | A manual for end-users of the API. |
| **Installation Guide** | `docs/system/INSTALLATION.md` | A guide detailing the steps to install the API from source. |

### 4.2. <MODULE_NAME> Module Documentation
| Document | Location | Description |
|---|---|---|
| **README** | `<module>/README.md` | An overview of the <MODULE_NAME> module. |
| **Architecture** | `<module>/docs/ARCHITECTURE.md` | Details the architecture of the <MODULE_NAME> module. |
| **Installation Guide** | `<module>/docs/INSTALLATION.md` | A guide on how to install, configure, run, and build the module. |

---

## 5. Audit & Alignment Documents
| Document | Location | Description |
|---|---|---|
| **First Audit** | `audit/FIRST_AUDIT.md` | The initial audit report for the project. |
| **Alignment Plan** | `audit/ALIGNMENT_PLAN.md` | The phased plan for bringing design documents into alignment with the codebase. |
| **Audit Log: Phase X** | `audit/AUDIT-phase-X.md` | Log of activities and findings from a specific phase of the alignment plan. |

---

## 6. Change Log
| Date | Change | Author |
|---|---|---|
| <DATE> | Initial creation of the project registry. | <TEAM_MEMBER> |
| <DATE> | Comprehensive audit and update to include all project documentation. | <TEAM_MEMBER> |

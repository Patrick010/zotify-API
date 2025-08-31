# API Documentation Registry

**Date:** 2025-08-30
**Status:** Live Document

## 1. Purpose

This document serves as the master file, or single source of truth, for tracking all key documentation, records, and artifacts for the **Zotify API Module and its sub-modules**. It provides a centralized index to ensure traceability and transparency for all API-specific documentation.

To maintain this document's value, it is mandatory that any new markdown documentation file created within the `api/`, `snitch/`, or `gonk-testUI/` directories is added to this registry.

---

## 2. API & Module Documentation

### 2.1. Core API Documentation
| Document | Location | Description |
|---|---|---|
| **Changelog** | [`./CHANGELOG.md`](./CHANGELOG.md) | A log of all user-facing changes for each version. |
| **Feature Specifications** | [`./reference/FEATURE_SPECS.md`](./reference/FEATURE_SPECS.md) | The master index for detailed, standardized specifications for all system features. |
| **Operator Manual** | [`./manuals/OPERATOR_MANUAL.md`](./manuals/OPERATOR_MANUAL.md) | Provides guidance for deploying, configuring, and maintaining the Zotify API in a production environment. |
| **System Integration Guide** | [`./manuals/SYSTEM_INTEGRATION_GUIDE.md`](./manuals/SYSTEM_INTEGRATION_GUIDE.md) | A guide for external developers on how to integrate with and consume the Zotify API. |
| **API Developer Guide** | [`./manuals/API_DEVELOPER_GUIDE.md`](./manuals/API_DEVELOPER_GUIDE.md) | A guide for internal developers on setting up a local environment, running tests, and contributing to the API codebase. |
| **Developer CI/CD Guide**| [`./manuals/CICD.md`](./manuals/CICD.md) | A detailed technical guide to the CI/CD pipeline and local setup. |
| **User Manual** | [`./manuals/USER_MANUAL.md`](./manuals/USER_MANUAL.md) | A manual for end-users of the API, explaining the core workflow for downloading tracks and the standard error response format. |
| **Error Handling Guide** | [`./manuals/ERROR_HANDLING_GUIDE.md`](./manuals/ERROR_HANDLING_GUIDE.md) | A developer guide for the Generic Error Handling Module. |
| **Logging Guide** | [`./manuals/LOGGING_GUIDE.md`](./manuals/LOGGING_GUIDE.md) | A comprehensive developer guide for the new Flexible Logging Framework. |
| **Spotify Provider** | [`./providers/spotify.md`](./providers/spotify.md) | Describes the implementation of the Spotify provider connector. |
| **Authentication Spec** | [`./reference/features/authentication.md`](./reference/features/authentication.md) | A feature specification for the static Admin API Key authentication mechanism. |
| **Automated Documentation Workflow Spec** | [`./reference/features/automated_documentation_workflow.md`](./reference/features/automated_documentation_workflow.md) | A feature specification for the automated documentation linting and logging workflow. |
| **Provider OAuth2 Flow Spec** | [`./reference/features/provider_oauth.md`](./reference/features/provider_oauth.md) | A feature specification for the provider-agnostic OAuth2 authentication flow. |
| **Provider Extensions Spec** | [`./reference/features/provider_agnostic_extensions.md`](./reference/features/provider_agnostic_extensions.md) | A proposal for a standardized structure for feature specification documents. |
| **Error Handling Design** | [`./system/ERROR_HANDLING_DESIGN.md`](./system/ERROR_HANDLING_DESIGN.md) | The technical design specification for the Generic Error Handling Module. |
| **Installation Guide** | [`./system/INSTALLATION.md`](./system/INSTALLATION.md) | A guide detailing the steps to install the Zotify API from source. |
| **System Requirements** | [`./system/REQUIREMENTS.md`](./system/REQUIREMENTS.md) | Lists the system and software requirements for running the Zotify API. |
| **Generated API Reference** | [`./reference/API_REFERENCE.md`](./reference/API_REFERENCE.md) | A comprehensive, auto-generated reference for all API endpoints based on the OpenAPI spec. |
| **Flexible Logging Framework Design** | [`./reference/features/developer_flexible_logging_framework.md`](./reference/features/developer_flexible_logging_framework.md) | A design document for a developer-facing, programmable logging framework. |
| **Code Quality Index** | [`./reference/CODE_QUALITY_INDEX.md`](./reference/CODE_QUALITY_INDEX.md) | A registry for tracking the overall quality and status of all API source code files. |
| **Privacy Compliance** | [`./system/PRIVACY_COMPLIANCE.md`](./system/PRIVACY_COMPLIANCE.md) | An overview of how the Zotify API project complies with data protection laws like GDPR. |

### 2.2. Snitch Module Documentation
| Document | Location | Description |
|---|---|---|
| **README** | [`snitch/README.md`](snitch/README.md) | An overview of the Snitch module. |
| **Architecture** | [`snitch/docs/ARCHITECTURE.md`](snitch/docs/ARCHITECTURE.md) | Details the architecture of the Snitch module and its Zero Trust security model. |
| **Installation Guide** | [`snitch/docs/INSTALLATION.md`](snitch/docs/INSTALLATION.md) | A guide on how to install, configure, run, and build the Snitch module. |
| **Milestones** | [`snitch/docs/MILESTONES.md`](snitch/docs/MILESTONES.md) | A document for tracking key project milestones for the Snitch module. |
| **Modules** | [`snitch/docs/MODULES.md`](snitch/docs/MODULES.md) | An overview of the internal Go packages within the Snitch module. |
| **Phases** | [`snitch/docs/PHASES.md`](snitch/docs/PHASES.md) | The phased development plan for the Snitch subproject. |
| **Project Plan** | [`snitch/docs/PROJECT_PLAN.md`](snitch/docs/PROJECT_PLAN.md) | The project plan for Snitch, outlining the problem it solves and its development plan. |
| **Secure Callback Design (Superseded)** | [`snitch/docs/PHASE_2_SECURE_CALLBACK.md`](snitch/docs/PHASE_2_SECURE_CALLBACK.md) | A superseded design document for the Snitch secure callback. |
| **Roadmap** | [`snitch/docs/ROADMAP.md`](snitch/docs/ROADMAP.md) | The high-level, phased development roadmap for the Snitch subproject. |
| **Status** | [`snitch/docs/STATUS.md`](snitch/docs/STATUS.md) | A live status document tracking the development progress of the Snitch subproject. |
| **Tasks** | [`snitch/docs/TASKS.md`](snitch/docs/TASKS.md) | A task list for the development of the Snitch module. |
| **Test Runbook** | [`snitch/docs/TEST_RUNBOOK.md`](snitch/docs/TEST_RUNBOOK.md) | A runbook for testing the Snitch module. |
| **User Manual** | [`snitch/docs/USER_MANUAL.md`](snitch/docs/USER_MANUAL.md) | A manual for end-users explaining the purpose of the Snitch helper application. |
| **Zero Trust Design** | [`snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md`](snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md) | The design specification for a Zero Trust secure callback flow for Snitch. |
| **IPC Communication** | [`snitch/docs/phase5-ipc.md`](snitch/docs/phase5-ipc.md) | Outlines the secure IPC mechanism between the Zotify API and Snitch. |
| **Code Quality Index** | [`snitch/docs/CODE_QUALITY_INDEX.md`](snitch/docs/CODE_QUALITY_INDEX.md) | A registry for tracking the quality and status of all Snitch source code files. |

### 2.3. Gonk-TestUI Module Documentation
| Document | Location | Description |
|---|---|---|
| **README** | [`gonk-testUI/README.md`](gonk-testUI/README.md) | The main README for the Gonk Test UI developer tool. |
| **Architecture** | [`gonk-testUI/docs/ARCHITECTURE.md`](gonk-testUI/docs/ARCHITECTURE.md) | An overview of the `gonk-testUI` architecture. |
| **Changelog** | [`gonk-testUI/docs/CHANGELOG.md`](gonk-testUI/docs/CHANGELOG.md) | A changelog for the `gonk-testUI` module. |
| **Contributing Guide** | [`gonk-testUI/docs/CONTRIBUTING.md`](gonk-testUI/docs/CONTRIBUTING.md) | A guide for contributing to the `gonk-testUI` module. |
| **User Manual** | [`gonk-testUI/docs/USER_MANUAL.md`](gonk-testUI/docs/USER_MANUAL.md) | A detailed user manual for the `gonk-testUI`. |
| **Code Quality Index** | [`gonk-testUI/docs/CODE_QUALITY_INDEX.md`](gonk-testUI/docs/CODE_QUALITY_INDEX.md) | A registry for tracking the quality and status of all Gonk-TestUI source code files. |

---

## 3. Helper Scripts
This section lists standalone scripts that provide developer utility, testing, or code generation capabilities.

| Script | Location | Description |
|---|---|---|
| **Audit API Endpoints** | [`scripts/audit_endpoints.py`](scripts/audit_endpoints.py) | Inspects the FastAPI app to determine if API routes are functional or stubs. |
| **Basic Functional Tests** | [`scripts/functional_test.py`](scripts/functional_test.py) | A `pytest` script that runs basic functional tests against a running API server. |
| **Generate Endpoints Doc** | [`scripts/generate_endpoints_doc.py`](scripts/generate_endpoints_doc.py) | Generates the `project/ENDPOINTS.md` file from the `openapi.json` spec. |
| **Generate OpenAPI Spec** | [`scripts/generate_openapi.py`](scripts/generate_openapi.py) | Generates the `openapi.json` spec from the live FastAPI application. |
| **List API Routes** | [`scripts/list_routes.py`](scripts/list_routes.py) | Lists all registered routes in the FastAPI application. |
| **Run Full Test Suite** | [`scripts/roadmap-test.sh`](scripts/roadmap-test.sh) | A utility script to run the complete `pytest` test suite for the API. |
| **Run E2E Auth Test** | [`scripts/run_e2e_auth_test.sh`](scripts/run_e2e_auth_test.sh) | Runs a full end-to-end integration test for the API and `snitch` authentication flow. |
| **Documentation Linter** | [`scripts/lint-docs.py`](scripts/lint-docs.py) | A pre-commit script that enforces documentation-as-code policies by checking for corresponding doc changes when code is modified. |
| **Doc Lint Rules** | [`scripts/doc-lint-rules.yml`](scripts/doc-lint-rules.yml) | The YAML configuration file for the documentation linter. |
| **Log Work Utility** | [`scripts/log-work.py`](scripts/log-work.py) | A command-line utility to standardize and simplify the process of updating the three core project logs. |
| **Run Linter** | [`scripts/run_lint.sh`](scripts/run_lint.sh) | A utility script to run all linters. |
| **Start Server** | [`scripts/start.sh`](scripts/start.sh) | The main script for starting the API server. |
| **Test Auth Flow** | [`scripts/test_auth_flow.py`](scripts/test_auth_flow.py) | A script for testing the authentication flow. |
| **Run Single Config Test** | [`scripts/test_single_config.sh`](scripts/test_single_config.sh) | A small utility script to run a single, specific test for the config system. |

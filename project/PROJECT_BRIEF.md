# Project Brief

**Project Name:** Gonk API Refactoring and Enhancement  
**Date:** 2025-08-12 
**status:** Live document 

## 1. Project Objectives and Justification

**Objective:** To refactor the existing Zotify-based API into **Gonk**, a professional-grade, multi-service media automation platform. This involves making the system robust, scalable, maintainable, and fully documented, with a clear path toward becoming provider-agnostic.

**Justification:** The original API was tightly coupled to Spotify and suffered from several architectural deficiencies:
- Inconsistent and non-persistent data storage (in-memory queues, JSON files).
- Lack of clear separation between logic layers.
- Incomplete and outdated documentation.
- No abstraction for supporting multiple providers.

This project addresses these issues through a structured audit and a series of architectural refactors, reducing technical debt and enabling future expansion to multiple music/media services.

## 2. Business Case Summary

Primary business drivers:
- **Improved Maintainability:** Clean, well-documented architecture reduces future development and debugging costs.
- **Reliability & Scalability:** Unified database persistence supports more users and larger datasets.
- **Future-Proofing:** Provider-agnostic design enables integration with multiple services, expanding reach and features.
- **Developer Onboarding:** Comprehensive documentation and the `gonk-testUI` tool lower the entry barrier for new contributors.

## 3. Project Scope Outline

**In Scope (Current Phase):**
- Full audit of the existing codebase against documentation.
- Refactoring to a unified, SQLAlchemy-based database persistence layer.
- Creation of a standalone developer testing UI (`gonk-testUI`).
- Complete overhaul of system and project documentation.
- Planning and design of a provider-agnostic abstraction layer.
- Implementation of full two-way sync for Spotify playlists — **Stage 1: Audit & Alignment** completed, **Phase 3 in progress**, **Stage 3: Documentation & Formalization** in progress, **Stage 4: Provider Abstraction** in progress.

**Out of Scope (for current phase, but planned for future):**
- Additional music/media providers beyond Spotify.
- Full implementation of JWT-based authentication or other advanced security layers (strategic vision, to be implemented later).

## 4. High-Level Deliverables

1. **Refactored Gonk API** with a unified persistence layer.
2. **Standalone Developer Testing UI (`gonk-testUI`)** for API testing and DB browsing.
3. **Comprehensive Documentation Set** covering installation, usage, development, and operations.
4. **Living Project Management Documents** (PID, Activity Log, Current State, Roadmap).
5. **Startup Script** for robust API server launch.

## 5. Initial Risks and Constraints

- **Technical Risk:** Development environment instability (file system issues, flaky test runners) may cause delays or require workarounds.
- **Constraint:** Must be backend-agnostic for database and provider-agnostic for services.
- **Constraint:** All work must follow the living documentation policy.

## 6. Key Stakeholders and Roles

- **Project Executive / Senior User:** Primary driver of requirements and vision.
- **Senior Supplier / Lead Developer:** Jules (AI agent) — technical implementation.
- **Project Manager:** The user — direction, approvals, and management.

## 7. High-Level Timeline / Approach

This is an iterative, milestone-based project. Phases:

1. **Audit & Alignment** — Completed.
2. **Unified Database Refactoring** — Completed.
3. **Developer Tooling (`gonk-testUI`)** — Completed.
4. **System Documentation Overhaul** — Completed.
5. **PRINCE2 Documentation Creation** — In progress.
6. **Provider Abstraction Layer Refactoring** — Planned (Next).

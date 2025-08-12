# Project Brief

**Project Name:** Zotify API Refactoring and Enhancement
**Date:** 2025-08-12

## 1. Project Objectives and Justification

**Objective:** To refactor the existing Zotify API to a professional standard of engineering, making it robust, scalable, maintainable, and well-documented. The ultimate goal is to evolve the API into a provider-agnostic platform for music service automation.

**Justification:** The initial version of the Zotify API, while functional, suffered from several architectural deficiencies:
-   Inconsistent and non-persistent data storage (in-memory queues, JSON files).
-   Lack of clear separation between logic layers.
-   Incomplete and outdated documentation.
-   A tight coupling to the Spotify service, preventing future expansion.

This project was initiated to address these issues through a formal audit and a series of architectural refactoring tasks, thereby reducing technical debt and preparing the application for future growth.

## 2. Business Case Summary

The primary business drivers for this project are:
-   **Improved Maintainability:** A cleaner, well-documented architecture reduces the cost and time required for future feature development and bug fixing.
-   **Increased Reliability & Scalability:** Migrating to a unified database system ensures data persistence and provides a foundation for handling more users and data.
-   **Future-Proofing:** The move towards a provider-agnostic architecture opens up new strategic possibilities for integrating with other music services, expanding the application's potential user base and feature set.
-   **Improved Developer Onboarding:** The creation of comprehensive documentation and developer tools (`gonk-testUI`) will reduce the time it takes for new developers to become productive.

## 3. Project Scope Outline

**In Scope:**
-   A full audit of the existing codebase against the documentation.
-   The refactoring of the persistence layer to a unified, SQLAlchemy-based database system.
-   The creation of a standalone developer testing UI (`gonk-testUI`).
-   A complete overhaul of the system and project documentation.
-   The initial planning and design for a provider-agnostic abstraction layer.

**Out of Scope (for the current phase):**
-   The implementation of new music service providers beyond Spotify.
-   The implementation of a full JWT-based authentication system (this is a future enhancement).
-   The implementation of a two-way (write) sync for Spotify playlists.

## 4. High-Level Deliverables (Products)

1.  **A Refactored Zotify API:** With a new, unified database persistence layer.
2.  **A Standalone Developer Testing UI (`gonk-testUI`):** A Flask-based web application for API testing and database browsing.
3.  **A Comprehensive System Documentation Set:** Including installation, user, developer, and operator manuals.
4.  **A Set of "Living" Project Management Documents:** Including this Project Brief, a PID, an Activity Log, and a Current State document.
5.  **A Startup Script:** For robustly launching the API server.

## 5. Initial Risks and Constraints

-   **Technical Risk:** The development environment has shown unreliability in its file system and test runner tools. This could cause delays or require workarounds.
-   **Constraint:** The project must be developed in a way that is "backend-agnostic" for the database and "provider-agnostic" for the music services.
-   **Constraint:** All work must be meticulously documented in accordance with the project's "living document" policy.

## 6. Key Stakeholders and Roles (Inferred)

-   **Project Executive / Senior User:** The primary user driving the project's requirements and vision.
-   **Senior Supplier / Lead Developer:** Jules (the AI agent) is currently filling this role, responsible for the technical implementation.
-   **Project Manager:** The user is also implicitly acting as the Project Manager, providing direction, approving plans, and managing the project flow.

## 7. High-Level Timeline / Approach

The project is being executed in an iterative, milestone-based approach, not a time-based one. The high-level phases have been:
1.  **Audit and Alignment:** Completed.
2.  **Unified Database Refactoring:** Completed.
3.  **Developer Tooling (`gonk-testUI`):** Completed.
4.  **System Documentation Overhaul:** Completed.
5.  **PRINCE2 Documentation Creation:** In Progress.
6.  **Provider Abstraction Layer Refactoring:** Planned (Next).

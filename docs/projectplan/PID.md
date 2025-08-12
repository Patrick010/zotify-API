# Project Initiation Document (PID)

**Project Name:** Zotify API Refactoring and Enhancement
**Date:** 2025-08-12
**Version:** 1.0

---

## 1. Full Business Case

**Justification:** The Zotify API, in its initial state, was not built on a sustainable architecture. It lacked a persistent data layer, had inconsistent documentation, and was tightly coupled to a single provider (Spotify). This project was initiated to rectify these foundational issues, reducing technical debt and enabling future growth.

**Business Benefits:**
-   **Reduced Operational Risk:** By moving to a persistent database, the risk of data loss (e.g., download queues, user tokens) is eliminated.
-   **Increased Development Velocity:** A clean, well-documented, and modular architecture allows for faster and more reliable implementation of new features.
-   **Enhanced Scalability:** The new architecture is designed to support more users, more data, and more integrations.
-   **Strategic Optionality:** The move towards a provider-agnostic design creates future opportunities to expand the service to other platforms, increasing the application's value proposition.

---

## 2. Detailed Project Scope & Product Breakdown

### 2.1. In Scope
-   A full audit of the codebase against documentation.
-   Refactoring of the persistence layer to a unified, SQLAlchemy-based system.
-   Migration of all file-based and in-memory data (playlists, tokens, download jobs) to the new database.
-   Creation of a standalone developer testing UI (`gonk-testUI`) with `sqlite-web` integration.
-   A complete overhaul of the system documentation (`INSTALLATION.md`, `USER_MANUAL.md`, etc.).
-   Creation of formal project management documents (Project Brief, PID).
-   The initial design and planning for a provider-agnostic abstraction layer.

### 2.2. Out of Scope
-   Implementation of any new music service providers.
-   Implementation of a full JWT-based authentication system.
-   Implementation of two-way (write) sync for Spotify playlists.

### 2.3. Main Products (Deliverables)
1.  **Refactored Zotify API (v1.0):** The core API with the new database architecture.
2.  **`gonk-testUI` Module (v0.1.0):** The standalone developer testing tool.
3.  **System Documentation Set:** The new `docs/system/` directory and its contents.
4.  **PRINCE2 Project Documentation:** This PID and the associated Project Brief.
5.  **`scripts/start.sh`:** The new startup script.

---

## 3. Stage Plans (High-Level)

The project has been executed in a series of logical, milestone-based stages rather than time-based stages.

-   **Stage 1: Audit & Alignment (Completed):** The initial phase focused on understanding the codebase and documenting the gaps between the code and the existing documentation.
-   **Stage 2: Core Refactoring (Completed):** This stage involved the two major architectural refactorings: the move to a unified database and the implementation of the `gonk-testUI`.
-   **Stage 3: Documentation & Formalization (Completed):** This stage involved the creation of the new system documentation and these PRINCE2 documents.
-   **Stage 4: Provider Abstraction (Next):** The next stage of the project will be to implement the provider-agnostic abstraction layer.

---

## 4. Project Controls

-   **Reporting:** Progress and status are tracked through the "living documents" in the `docs/projectplan/` directory, specifically `ACTIVITY.md` and `CURRENT_STATE.md`.
-   **Change Control:** All changes are managed through a process of proposing a plan, getting user approval, and then executing the plan. Any significant deviation from an approved plan requires re-approval.
-   **Quality Assurance:** Quality is assured through:
    -   Code reviews (`request_code_review` tool).
    -   Unit and integration testing (though the test runner is currently a known issue).
    -   Meticulous documentation updates to ensure alignment with the code.

---

## 5. Risk, Issue, and Quality Registers

This PID formalizes the known issues into registers.

-   **Risk Register:**
    -   **Risk:** The development environment's tools for file system manipulation and test execution are unreliable.
    -   **Impact:** This can cause delays and require workarounds, impacting development velocity.
    -   **Mitigation:** Rely on external code reviews for validation where tests cannot be run. For file system issues, prefer creating/deleting files over renaming/moving directories.
-   **Issue Register:**
    -   **Issue #1:** The `devtools/` directory exists as a duplicate of `gonk-testUI/`.
    -   **Status:** Open.
    -   **Impact:** Minor codebase clutter. No functional impact.
    -   **Action:** To be removed in a future cleanup task.
-   **Quality Register:**
    -   All code changes must be reviewed.
    -   All documentation must be updated with every change.
    -   The "living documents" (PID, CURRENT_STATE, ACTIVITY) must be kept in sync.

---

## 6. Project Organisation (Roles & Responsibilities)

-   **Project Board / Project Executive:** The primary user, who provides the project mandate, sets the high-level requirements, and approves major plans and stage transitions.
-   **Project Manager:** The user is also fulfilling this role, providing detailed instructions, course corrections, and managing the project flow.
-   **Senior Supplier / Lead Developer:** Jules (the AI agent) is the primary technical resource responsible for design, implementation, testing, and documentation.

---

## 7. Communication Management Approach

-   All communication is handled through the interactive session.
-   Jules provides regular progress updates via the `message_user` tool and by updating the "living documents".
-   The user provides feedback, approvals, and new directives.
-   The `CURRENT_STATE.md` document serves as the primary asynchronous communication tool for project hand-offs.

---

## 8. Configuration Management Approach

-   **Source Code:** Managed in a Git repository. All changes are committed to feature branches.
-   **Documentation:** All documentation is stored as Markdown files within the Git repository and is versioned alongside the code.
-   **Project State:** The "living documents" (`ACTIVITY.md`, `CURRENT_STATE.md`, `PID.md`) serve as the configuration management database for the project's status and direction.

---

## 9. Tailoring Approach

This project adapts the PRINCE2 framework to a highly agile, one-on-one development context between a human project manager and an AI developer.

-   **Principles:** All PRINCE2 principles are adhered to (continued business justification, learn from experience, defined roles, manage by stages, manage by exception, focus on products, tailor to suit).
-   **Themes:** Themes like Quality, Risk, and Change are managed through the interactive process and documented in this PID.
-   **Processes:** Formal processes like "Starting up a Project" and "Initiating a Project" are condensed into the creation of the Project Brief and this PID. "Managing a Stage Boundary" is handled by the user's approval of new high-level plans.
-   **Documents:** The number of management products is minimized to the essential "living documents" to avoid bureaucracy while maintaining clarity and control.

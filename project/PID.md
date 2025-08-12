# Project Initiation Document (PID)

**Project Name:** Zotify API Refactoring and Enhancement  
**Date:** 2025-08-12  
**Version:** 1.0
**Status:** Live Document

---

## 1. Full Business Case

**Justification:**  
The Zotify API was originally built as a lightweight wrapper for a single use case—interacting with Spotify through Zotify/Librespot—but without a sustainable architecture for long-term growth. It lacked persistent storage, modularity, and the flexibility to support multiple providers. This project aims to refactor and expand the API to form a robust, scalable, and provider-agnostic backend for automation, integrations, and developer tooling.

**Strategic Goals:**  
- Transition Zotify from a Spotify-only CLI wrapper into a fully modular API framework capable of integrating with multiple audio content sources.  
- Lay the foundation for a future-ready architecture that supports automation, sync, analytics, and secure multi-user workflows.  
- Deliver an API that is developer-friendly, self-documented, and scalable without major redesigns.  
- Enable both CLI and WebUI-based interactions, giving users and developers a choice of interfaces.  

**Business Benefits:**  
- **Reduced Operational Risk:** Persistent database eliminates data loss for queues, tokens, and state.  
- **Faster Development:** Cleaner, modular architecture accelerates new feature delivery.  
- **Better Scalability:** Prepared for higher load, more data, and multiple integrations.  
- **Future Expansion:** Provider-agnostic design allows easy addition of new streaming platforms.  
- **Enhanced Feature Set:** Full two-way playlist sync and advanced automation unlock entirely new workflows.  

---

## 2. Detailed Project Scope & Product Breakdown

### 2.1 In Scope
- Full audit of the codebase against documentation. *(In Progress)*  
- Refactoring to a unified, SQLAlchemy-based persistence layer.  
- Migration of all file-based and in-memory data (playlists, tokens, download jobs) to the new database.  
- Creation of a standalone developer testing UI (`gonk-testUI`) with `sqlite-web` integration.  
- Complete overhaul of system documentation (`INSTALLATION.md`, `USER_MANUAL.md`, etc.). *(In Progress)*  
- Creation of formal project management documents (Project Brief, PID).  
- Initial design and implementation of a provider-agnostic abstraction layer. *(In Progress)*  
- **Full two-way sync for Spotify playlists** as a core API feature.  

### 2.2 Out of Scope (Current Phase)
- None of the features are permanently out of scope. However, some items (e.g., **full JWT-based authentication** and other advanced security layers) are **strategic goals** for later phases, after the core architecture and sync features are complete.  

### 2.3 Main Products (Deliverables)
1. **Refactored Zotify API (v1.0):** New database architecture with modular design.  
2. **`gonk-testUI` Module (v0.1.0):** Developer testing tool with SQLite inspection.  
3. **System Documentation Set:** Fully updated `docs/system/` directory.  
4. **PRINCE2 Project Documentation:** PID, Project Brief, and supporting docs.  
5. **`scripts/start.sh`:** Unified startup script.  
6. **Spotify Two-Way Sync Module:** Bidirectional playlist sync, with conflict resolution.  

---

## 3. Stage Plans (High-Level)

- **Stage 1: Audit & Alignment** *(In Progress)* — Code/documentation gap analysis and alignment.  
- **Stage 2: Core Refactoring** *(Completed)* — Unified database, new dev UI.  
- **Stage 3: Documentation & Formalization** *(In Progress)* — Full system documentation, formal project docs.  
- **Stage 4: Provider Abstraction** *(In Progress)* — Design and partial implementation of multi-provider layer.  

---

## 4. Project Controls

- **Reporting:** Progress tracked in `project/` (`ACTIVITY.md`, `CURRENT_STATE.md`).  
- **Change Control:** All changes require proposal, approval, and re-approval if scope deviates.  
- **Quality Assurance:**  
  - Code reviews before merge.  
  - Unit/integration testing (test runner stability is a known issue).  
  - Continuous documentation updates in sync with code changes.  

---

## 5. Risk, Issue, and Quality Registers

- **Risk Register:**  
  - *Risk:* Development tools for filesystem manipulation/testing are unreliable.  
  - *Impact:* Delays and workarounds reduce efficiency.  
  - *Mitigation:* External code review, safe file operations instead of rename/move.  

- **Issue Register:**  
  - *Issue #1:* Duplicate `devtools/` directory exists alongside `gonk-testUI/`.  
  - *Status:* Open.  
  - *Impact:* Minor clutter, no functional risk.  
  - *Action:* Cleanup in future refactor.  

- **Quality Register:**  
  - All code must be reviewed.  
  - All docs must be updated with every change.  
  - PID, `CURRENT_STATE.md`, `ACTIVITY.md` remain in sync.  

---

## 6. Project Organisation (Roles & Responsibilities)

- **Project Board / Project Executive:** Primary user — provides mandate, sets requirements, approves plans.  
- **Project Manager:** Primary user — manages flow, gives detailed direction.  
- **Senior Supplier / Lead Developer:** Jules (AI agent) — responsible for technical design, implementation, testing, and documentation.  

---

## 7. Communication Management Approach

- All communication via interactive session.  
- Jules provides regular updates and `CURRENT_STATE.md` hand-offs.  
- User provides approvals and new directives.  

---

## 8. Configuration Management Approach

- **Source Code:** Managed in Git with feature branches.  
- **Documentation:** Markdown in repo, versioned alongside code.  
- **Project State:** Tracked in living docs (`ACTIVITY.md`, `CURRENT_STATE.md`, `PID.md`).  

---

## 9. Tailoring Approach

- PRINCE2 principles applied in a minimal, agile form for a one-on-one AI/human workflow.  
- Quality, risk, and change managed through interactive process and living documentation.  
- Stage boundaries managed via user approval of new high-level plans.  

---

Appendix / References

    project/ROADMAP.md

    project/EXECUTION_PLAN.md

    project/TRACEABILITY_MATRIX.md

    project/PROJECT_REGISTRY.md

    docs/providers/spotify.md (starter)

    project/ACTIVITY.md (live)

    project/CURRENT_STATE.md (live)

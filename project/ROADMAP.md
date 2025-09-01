# Zotify API Platform Roadmap

**Date:** 2025-08-18
**Status:** Live Document

## 1. Introduction

This document provides a high-level, strategic roadmap for the Zotify API Platform. It is organized by major themes and outlines the development trajectory from the current stable state to future enhancements.

This document is not a detailed task tracker. For a log of completed work, see [`ACTIVITY.md`](./logs/ACTIVITY.md). For the immediate next steps, see [`CURRENT_STATE.md`](./logs/CURRENT_STATE.md). For a list of all potential long-term ideas, see [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md).

---

## 2. Core Platform Stability & Security (✅ Done)

This phase focused on refactoring the core architecture, resolving critical regressions, and hardening the platform's security and observability features.

-   **Unified Database Layer:** Migrated all data persistence to a unified SQLAlchemy backend.
-   **Provider Abstraction Layer (v1):** Decoupled the application from a hardcoded Spotify implementation.
-   **`snitch` Application Repair:** Resolved a critical build issue and refactored the application for stability.
-   **Flexible Logging Framework:** Implemented and hardened a feature-rich logging system with capabilities for:
    -   Tag-based routing to multiple sinks.
    -   Dedicated security and audit logging.
    -   Automatic redaction of sensitive data in production environments.
-   **Comprehensive Documentation Overhaul:** Brought all key project documents up to a high standard of quality and accuracy.

---

## 3. Platform Extensibility (Next Up)

This next major phase of work will focus on making the Zotify API a truly extensible platform, allowing the community to build and share new functionality.

-   **Archive Cleanup & Documentation Consolidation:** Clean up the `project/archive/` directory by reviewing old `.md` files, extracting anything still relevant, and discarding what is obsolete. The goal is to reduce noise while preserving useful material without corrupting the authoritative documentation.
-   **Dynamic Plugin System:** Implement a dynamic plugin system based on the `entry_points` mechanism, allowing developers to create custom logging sinks.
    -   **Source:** [`DYNAMIC_PLUGIN_PROPOSAL.md`](./proposals/DYNAMIC_PLUGIN_PROPOSAL.md)
-   **Refactor Providers as Plugins:** As a proof-of-concept, refactor the existing Spotify provider to be a standalone plugin, solidifying the new architectural pattern.
-   **Low-Code/No-Code Integration:** Create a reference implementation for Node-RED integration, making the API accessible to non-programmers.
    -   **Source:** [`LOW_CODE_PROPOSAL.md`](./proposals/LOW_CODE_PROPOSAL.md)
-   **Home Automation Integration:** Create a reference implementation for Home Assistant integration, bringing Zotify into the smart home ecosystem.
    -   **Source:** [`HOME_AUTOMATION_PROPOSAL.md`](./proposals/HOME_AUTOMATION_PROPOSAL.md)

---

## 4. Future Vision

Beyond the next major phase, development will focus on expanding the core feature set and improving the user experience.

-   **API Baseline Implementation:** Diff the implemented OpenAPI spec vs. the `endpoints.yaml` baseline and implement all missing, planned endpoints.
-   **Full Two-Way Sync:** Implement write-sync capabilities for Spotify and other providers.
-   **Advanced API Governance:** Introduce rate limiting, usage quotas, and more sophisticated security controls.
-   **Enhanced User Interface:** Develop a more feature-rich web UI for managing all aspects of the platform.

# Future Enhancements & Product Vision

> **Note:** See the [`TRACEABILITY_MATRIX.md`](./TRACEABILITY_MATRIX.md) for status and implementation tracking of these enhancements.

**Date:** 2025-08-11
**Status:** Living Document

## 1. Purpose

This document serves as a dedicated "parking lot" for new ambitions and feature ideas that have emerged during development but are not part of the current, committed roadmap. It is meant to capture long-term vision without disrupting the alignment and verification process of the active development phases.

---

## 2. Planned Technical Enhancements

This section lists specific technical features and improvements that are candidates for future development phases.

*   **Advanced Admin Endpoint Security:**
    *   Transition from a static admin API key to a more robust, layered security model, including rate limiting, JWT/OAuth2 for user-level endpoints, and dynamic key rotation.
*   **Role-Based Access Control (RBAC):**
    *   Implement a full RBAC system to support multi-user environments with different permission levels. This is a prerequisite for any significant multi-user functionality.
*   **Persistent & Distributed Job Queue:**
    *   Replace the current in-memory download queue with a persistent, database or Redis-backed system to ensure job durability across restarts and to support distributed workers.
*   **Full Spotify OAuth2 Integration & Library Sync:**
    *   Expand the Spotify integration to include full, two-way synchronization (write-sync) for playlists.
    *   Implement full library management, including the ability to read and modify a user's saved albums and liked tracks.
*   **Enhanced Download & Job Management:**
    *   Implement detailed, real-time progress reporting for download jobs.
    *   Introduce user notifications for job completion or failure.
    *   Develop sophisticated retry policies with exponential backoff and error classification.
*   **API Governance:**
    *   Implement API rate limiting and usage quotas per user or API key to ensure fair usage and prevent abuse.
*   **Observability:**
    *   Improve the audit trail with more detailed event logging.
    *   Add real-time monitoring hooks for integration with external monitoring systems.
*   **Standardized Error Handling & Logging:**
    *   Implement a standardized error schema for all API responses.
    *   Refactor the service layer to raise domain-specific exceptions instead of `HTTPException`s.
    *   Establish a consistent logging format and convention across all services.
*   **Comprehensive Health Checks:**
    *   Expand the system info endpoints to include detailed process stats, disk/network health, and dependency checks.
*   **Unified Configuration Management:**
    *   Unify the two configuration systems (`config.py` and `config_service.py`). This would likely involve migrating the settings from `config.json` into the main database and providing a single, consistent API for managing all application settings at runtime.
*   **Snitch Module Enhancement:**
    *   Investigate the further development of the conceptual `Snitch` module.
    *   Potential enhancements include running it as a persistent background service, developing it into a browser plugin for seamless integration, or expanding it to handle multi-service authentication flows.
*   **Dynamic Logging Sink Plugin System:**
    *   Implement a dynamic plugin system for the Flexible Logging Framework, based on Python's `entry_points`. This will allow third-party developers to create and install their own custom sink types without modifying the core API code. See the full proposal at [`DYNAMIC_PLUGIN_PROPOSAL.md`](./DYNAMIC_PLUGIN_PROPOSAL.md).
*   **Plugin-Driven Multi-Source Metadata System:**
    *   Implement a new core service that leverages the Dynamic Plugin System to ingest, normalize, and query metadata from multiple, arbitrary sources (e.g., Spotify, local files, other services).
    *   Each source will be a self-contained, installable plugin.
    *   The system will use a document-oriented database for flexible metadata storage and a vector store to enable powerful semantic search capabilities across all sources.
    *   This feature is a major step towards making the platform truly provider-agnostic and will serve as the foundation for advanced cross-source library management and content discovery. See the full proposal at [`MULTI_SOURCE_METADATA_PROPOSAL.md`](./MULTI_SOURCE_METADATA_PROPOSAL.md).
*   **Home Automation Integration:**
    *   Develop a dedicated integration for home automation platforms like Home Assistant. This would expose Zotify as a `media_player` entity and provide services for triggering downloads and other actions from within home automations. See the full proposal at [`HOME_AUTOMATION_PROPOSAL.md`](./HOME_AUTOMATION_PROPOSAL.md).

---

## 3. API Adoption & Usability Philosophy

Beyond technical features, the long-term success of the API depends on making it irresistibly easy and valuable for developers to adopt. The following principles will guide future development.

### 3.1. Crazy Simple Usage
*   **Goal:** Minimize setup and authentication friction. Ensure the API works out-of-the-box with sensible defaults.
*   **Actions:**
    *   Provide ready-made SDKs or client libraries for popular languages (e.g., Python, JavaScript, Go).
    *   Develop a collection of example apps, recipes, and templates for common use cases.
    *   Maintain a clear, concise, and consistent API design and error handling schema.

### 3.2. Feature-Rich Beyond Spotify API
*   **Goal:** Provide capabilities that the standard Spotify API lacks, making our API more powerful for specific use cases.
*   **Actions:**
    *   Build out advanced download management features (progress, retry, queue control).
    *   Support bulk operations for efficient management of tracks and playlists.
    *   Integrate caching and local state synchronization to improve performance and resilience.

### 3.3. Competitive Differentiators
*   **Goal:** Focus on features that make our API stand out in terms of reliability, security, and performance.
*   **Actions:**
    *   **Transparency:** Provide clear audit logs and job state visibility.
    *   **Security:** Start with strong security defaults and provide a clear roadmap to advanced, layered authentication.
    *   **Performance:** Offer background processing for long-running tasks and intelligent rate limits.
    *   **Extensibility:** Design for extensibility with features like webhooks and a plugin system.

### 3.4. Pragmatic Documentation & Support
*   **Goal:** Create documentation that is practical, example-driven, and helps developers solve real-world problems quickly.
*   **Actions:**
    *   Focus on "how-to" guides and tutorials over purely theoretical references.
    *   Establish a developer community channel (e.g., Discord, forum) for feedback, support, and collaboration.

### 3.5. Low-Code / No-Code Platform Integration

*   **Goal:** To make the API's power accessible to non-programmers and citizen developers through visual, flow-based programming environments.
*   **Vision:** While the Python plugin system extends the API's backend, integration with platforms like Node-RED or Zapier would extend its reach. This would involve creating a dedicated package of nodes or modules for that platform (e.g., `node-red-contrib-zotify`).
*   **Synergy:** These nodes would act as well-designed clients for the Zotify API. The more powerful the backend API becomes (through Python plugins), the more powerful these visual building blocks become. This creates a synergistic ecosystem for both developers and power users. See the full proposal at [`LOW_CODE_PROPOSAL.md`](./LOW_CODE_PROPOSAL.md).

---

# Future Enhancements: Framework & Multi-Service Accessibility

## Web UI
- Clean, responsive HTML/CSS/JS templates that let users browse, search, queue downloads, manage playlists, view statuses—all without writing code.

## Query Language
- A beginner-friendly, expressive query syntax or DSL for filtering and manipulating tracks/playlists. Not just simple filters but advanced ops like:
  - Create, edit, delete playlists
  - Merge playlists with rules (e.g., remove duplicates, reorder by popularity)
  - Import/export playlists in multiple formats (Spotify, M3U, JSON, CSV)
  - Search by genre, artist, album, release year, popularity, explicit content flags
  - Bulk actions (tag editing, batch downloads)
  - Smart dynamic playlists (auto-update by criteria)
- Investigate and prototype integration of AI-driven natural language processing (NLP) to allow users to express queries and commands in everyday language.
  - Enable transforming human-readable requests into precise API queries or playlist manipulations without requiring formal syntax knowledge.
  - Examples:
    - "Create a playlist of upbeat rock songs from the 90s."
    - "Merge my jazz and blues playlists but remove duplicates."
    - "Show me tracks by artists similar to Radiohead released after 2010."
  - This would drastically lower the entry barrier and make advanced functionality accessible to casual users.
  - Research options include embedding pre-trained language models, or interfacing with cloud NLP APIs, with focus on privacy and performance.

## Scripting / Automation Hooks
- A lightweight embedded scripting layer or API clients with abstractions for complex workflows (e.g., periodic sync, trigger downloads on new releases).

## Metadata Editing & Enrichment
- Allow users to edit track metadata locally (tags, cover art), and pull enriched data from third-party sources (e.g., lyrics, credits).

## User Profiles & Sharing
- Basic multi-user support with saved settings, playlist sharing, favorites, and history.

## Notifications & Progress UI
- Push notifications or UI alerts for download completions, failures, quota warnings, etc.

## Mobile-friendly Design
- So users can manage and interact on phones or tablets smoothly.

## Comprehensive Documentation & Examples
- Usage guides, recipes, and code samples for all common tasks to flatten the learning curve.

---

If we deliver this whole ecosystem tightly integrated with the API, it won’t just be “another Spotify API clone” but a full-fledged platform that’s accessible to casual users and power users alike—and that’s how you drive adoption and stand out in a crowded market.

---

## Unified Database Layer Adoption

The recent architectural refactor introducing a backend-agnostic database layer using SQLAlchemy lays the groundwork for more scalable, maintainable data management across all services. While currently focused on core entities (downloads, playlists, tokens), future enhancements should:

- Expand this unified layer to support multi-service integrations and provider-specific data.
- Implement advanced querying, caching, and transactional features.
- Ensure smooth migration paths for any additional persistence needs.
- Maintain strict separation between API logic and data storage for flexibility in swapping backend databases if needed.

**Note:** This foundation is critical and should be a key consideration in any upcoming feature developments, especially multi-provider support and API expansion, but the core refactor is complete and in use. New features must build on top of this layer rather than circumvent it.


## Unified Provider Abstraction Layer

To enable multi-provider support for music services without creating endpoint bloat, a unified abstraction layer will be developed. This layer will translate standardized API requests into provider-specific API calls through connectors.

**Key objectives:**
- Define a core, normalized set of API endpoints and data models that cover common operations across providers.
- Implement lightweight translation matrices or connector modules to handle provider-specific API differences.
- Support pluggable authentication and token management per provider.
- Avoid duplicating full API gateway solutions like WSO2 by embedding the translation logic within the application layer.
- Ensure extensibility for easy addition of new music service providers.

This is a medium- to long-term goal and must be factored into future architectural decisions and design plans.

---

### Provider-Agnostic Feature Specification Extension

**Objective:** Extend the Unified Provider Abstraction Layer by establishing a structured, detailed, and discoverable feature specification process. This ensures all provider-agnostic and provider-specific features are fully documented and tracked.

**Reference:** [Provider-Agnostic Extensions Feature Specification](docs/reference/features/provider_agnostic_extensions.md)

**Key Actions:**
- Maintain a **metadata integration matrix** for all supported providers, tracking feature coverage, compatibility, and limitations.
- Define a **Provider Adapter Interface** template to standardize connector modules and simplify integration of new services.
- Enforce pre-merge checks to ensure new provider-specific or provider-agnostic features have completed spec entries.
- Retroactively document existing provider integrations in the same structured format.
- Cross-link specs to `ENDPOINTS.md`, `SYSTEM_SPECIFICATIONS.md`, `ROADMAP.md`, and `AUDIT_TRACEABILITY_MATRIX.md`.

**Outcome:** Every provider-agnostic or provider-specific feature is discoverable, understandable, and traceable. Developers, maintainers, and auditors can confidently extend or troubleshoot functionality without reverse-engineering code.

**Status:** Proposed – tracked under `docs/reference/features/provider_agnostic_extensions.md`.

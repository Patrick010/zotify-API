<!-- ID: DOC-047 -->
# Proposal: Dynamic dbstudio Plugin for Database Browsing

**Date:** 2025-09-23
**Author:** Jules
**Status:** Proposed

## 1. Problem Statement

Currently, database inspection for the Zotify API is handled by `sqlite-web`, which is integrated directly into the `Gonk/GonkUI` Flask application. This approach has several limitations:

-   **Development-Only & SQLite-Specific:** The tool is designed for local development and only works with the SQLite database backend. It offers no solution for inspecting a production database like PostgreSQL.
-   **Lack of Modularity:** The database browser is tightly coupled to the `GonkUI` application. There is no way to enable or disable it independently, or to replace it with a different tool.
-   **Limited Access Control:** Access to the database browser is tied to access to the `GonkUI` itself. There is no granular, role-based access control to differentiate between a developer who needs to see API endpoints and a database administrator who needs to inspect the data.

## 2. Proposed Solution

This document proposes the creation of a **dynamic `dbstudio` plugin**. This plugin will provide a modular, backend-agnostic, and role-aware database browser that can be dynamically mounted on the core FastAPI application.

### 2.1. How It Will Work

1.  **Plugin Architecture:** The `dbstudio` will be built as a self-contained FastAPI application or router that can be discovered and mounted by the main Zotify API. It will follow the same plugin pattern proposed for logging sinks, using an entry point like `zotify.dev.plugins`.

2.  **Runmode-Based Access Control:** The plugin's visibility and access rules will be strictly controlled by the application's runmode, determined by the `APP_ENV` variable.
    -   **DEV Mode (`APP_ENV=development`):** In development mode, the plugin's router will be mounted. Access will be restricted to authenticated users with `admin` or `dba` roles.
    -   **PROD Mode (`APP_ENV=production`):** In production mode, the plugin's router will also be mounted, but access will be more restrictive. It will be available to users with `admin`, `dba`, or a new, dedicated `dbstudio_user` role. For the initial implementation, this could default to all authenticated users, with the understanding that full RBAC is a future enhancement.

3.  **Agnostic Database Backend Support:** The plugin will not be tied to SQLite. It will use the core API's established SQLAlchemy session to interact with the database, allowing it to work seamlessly with any backend supported by the main application (SQLite, PostgreSQL, MySQL/MariaDB, etc.).

4.  **Decoupling:** The `dbstudio` plugin will be entirely decoupled from the core API's business logic and from the `GonkUI`. It will be a standalone developer tool that can be installed and enabled optionally.

## 3. Benefits

-   **Modularity:** The database browser becomes an optional, installable component, not a hardcoded feature.
-   **RBAC-Ready:** The design introduces role-based access control, preparing the architecture for a full RBAC implementation in the future.
-   **Multi-DB Support:** The tool will work with any database backend configured for the main API, making it useful in both development and production environments.
-   **Dev/Prod Separation:** The runmode-based controls ensure that developer tools are exposed safely and appropriately depending on the environment.

## 4. High-Level Implementation Plan

1.  **Create Plugin Entry Point:** Establish a new entry point group, `zotify.dev.plugins`, for discovering developer tool plugins.
2.  **Develop `dbstudio` Router:** Create the core `dbstudio` as a FastAPI router. This router will contain the endpoints and logic for browsing database tables and records.
3.  **Dynamic Discovery and Mounting:** Modify the main Zotify API's startup sequence. It will scan for `zotify.dev.plugins`, and if the `dbstudio` plugin is found, it will mount its router, likely under a path like `/dev/dbstudio`.
4.  **Implement Authentication Hooks:** The `dbstudio` router will use FastAPI dependencies to enforce the authentication and role-based access checks described in the "Proposed Solution." This will involve checking the user's roles and the application's current `APP_ENV`.
5.  **Documentation:** Create documentation for the `dbstudio` plugin, explaining how to install, enable, and use it, and detailing the access control rules.

## 5. Security Considerations

-   **Authentication is Mandatory:** All endpoints within the `dbstudio` plugin must be protected by the Zotify API's standard authentication dependencies. No public access will be permitted.
-   **Runmode Enforcement:** The plugin must strictly enforce the DEV vs. PROD access rules. The logic for checking the `APP_ENV` must be robust.
-   **Separated Exposure:** The plugin should be designed such that it can be completely disabled in a production environment via configuration, even if the package is installed. This provides an additional layer of security.

## 6. Architectural Impact

-   **Decouples Dev Tools:** This proposal represents a significant step towards decoupling developer tooling from the core API. It moves the database browser from being a feature *of* the `GonkUI` to being a standalone tool *available to* the platform.
-   **Prepares for Plugin Ecosystem:** It establishes the pattern and infrastructure for a future ecosystem of optional developer and administrative plugins.

## 7. Future Possibilities

-   **Full RBAC Integration:** Once a full Role-Based Access Control system is implemented in the core API, the `dbstudio` plugin can be updated to use more granular permissions.
-   **Database Snapshots & Auditing:** The plugin could be extended to support creating database snapshots or providing a UI for viewing audit logs.
-   **Integration with Other Dev Tools:** The `dbstudio` could be designed to interact with other future developer plugins, such as a log viewer or a configuration editor.

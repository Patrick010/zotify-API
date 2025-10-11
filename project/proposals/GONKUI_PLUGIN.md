<!-- ID: DOC-049 -->
# Proposal: Dynamic GonkUI Plugin for Developer UI

**Date:** 2025-09-23
**Author:** Jules
**Status:** Proposed

## 1. Problem Statement

The current `Gonk/GonkUI` is a standalone Flask application that serves as a developer-focused testing UI. While functional, this implementation has several architectural drawbacks:

-   **Tight Coupling:** It exists as a separate, monolithic application within the main repository. It is not modular and cannot be easily updated or replaced without modifying the core project structure.
-   **Inconsistent Architecture:** It uses Flask, while the main API uses FastAPI. This requires developers to understand and run two different web frameworks.
-   **Siloed Development:** As a separate application, it cannot easily or safely interact with other potential developer tools, such as a database browser or a log viewer, without complex and insecure workarounds.

## 2. Proposed Solution

This document proposes that the existing `Gonk/GonkUI` Flask application be converted into a **dynamic `GonkUI` plugin**. This plugin will be a self-contained FastAPI router that can be discovered and mounted by the core API, serving a modern, framework-agnostic web UI.

### 2.1. How It Will Work

1.  **Plugin Architecture:** The `GonkUI` will be refactored into a package that provides a FastAPI router. It will register itself using the `zotify.dev.plugins` entry point, allowing the main API to discover it at startup.

2.  **Dev-Only Visibility:** The plugin will be strictly a developer tool. The main API will only mount the `GonkUI` router if the application's runmode is `development` (`APP_ENV=development`), as determined by the `/api/system/runmode` endpoint or an internal check. In production, the UI will not be exposed.

3.  **Role-Based Access:** Access to the mounted UI will be protected by authentication and role-based checks. Initially, this will be restricted to users with `admin` or `developer` roles.

4.  **Integration with Other Dev Tools:** As a native FastAPI router within the main application, the `GonkUI` plugin can be designed to safely and securely integrate with other developer plugins, such as the proposed `dbstudio` plugin, by providing links or embedding components.

## 3. Benefits

-   **Separation of Concerns:** The development UI is fully decoupled from the core API's production code, improving security and maintainability.
-   **Modular Dev Tools:** This continues the path of creating a modular ecosystem for developer tools, allowing them to be added, removed, or updated independently.
-   **Future Expandability:** A plugin-based UI can be more easily expanded to include new developer-focused features and integrations.
-   **Architectural Consistency:** It aligns the developer UI with the main application's FastAPI framework.

## 4. High-Level Implementation Plan

1.  **Convert Flask to FastAPI Router:** Refactor the existing `Gonk/GonkUI` `app.py` from a Flask application into a FastAPI router that serves the static HTML, CSS, and JS files.
2.  **Create Plugin Entry Point:** Package the refactored `GonkUI` so that it registers its router with the `zotify.dev.plugins` entry point.
3.  **Implement Dynamic Discovery:** The main API's startup logic will scan for `zotify.dev.plugins`. If the `GonkUI` plugin is found and the `APP_ENV` is `development`, it will mount the plugin's router at a path like `/dev/ui`.
4.  **Add Authentication:** The `GonkUI` router will be protected with a FastAPI dependency that checks for an authenticated user and verifies they have the required `admin` or `developer` role.
5.  **Documentation:** Create a guide for developers explaining how to install and enable the `GonkUI` plugin for their local development environment.

## 5. Security Considerations

-   **Strict Dev-Only Exposure:** The primary security mitigation is ensuring the plugin is only ever mounted in a `development` environment. This check must be robust and infallible.
-   **Role-Based Access Control:** All endpoints served by the plugin must be protected by authentication and role checks to prevent unauthorized access, even in a development environment.
-   **No Production Data Leakage:** The UI should be designed to interact with the API through official, authenticated endpoints, and should not have any direct access to production configurations or data.

## 6. Architectural Impact

-   **Decouples Dev UI:** This proposal fully decouples the developer UI from the core API, treating it as an optional, installable tool rather than a built-in feature.
-   **Modular Dev Tooling:** It solidifies the architectural pattern for a modular developer tool ecosystem, where the UI, database browser, and other future tools are all independent plugins.

## 7. Future Possibilities

-   **Include Additional Dev Tools:** The `GonkUI` plugin could serve as a dashboard or container for other developer tool plugins, providing a unified interface for development and debugging.
-   **Optional `dbstudio` Integration:** If both plugins are installed, the `GonkUI` could provide a direct link to or even embed the `dbstudio` interface.
-   **Extensible Dashboard:** The UI itself could be made extensible, allowing other plugins to add their own tabs or widgets to the main developer dashboard.

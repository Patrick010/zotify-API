<!-- ID: DOC-068 -->
# Zotify API Platform

"Phases 3–5 deliver the full core API, user authentication with JWT, endpoint protection, notifications preference, and comprehensive testing. Users can manage profiles, preferences, liked tracks, playback history, and interact with all content endpoints. The Gonk CLI and GonkUI provide an interface for all these actions, with the ability to toggle between simulated and real API testing. Documentation, examples, and OpenAPI specs are fully updated."

Welcome to the Zotify API Platform, a powerful, extensible, and provider-agnostic backend for managing and interacting with your music library. This platform is designed for developers, automators, and power-users who want to build sophisticated workflows for their music collections.

## 1. Core Philosophy

The Zotify API is built on a set of core principles:

-   **Extensibility:** The platform is designed to be extended. A dynamic plugin system allows developers to add new music providers, logging capabilities, and other features without modifying the core codebase.
-   **Configuration over Code:** As much as possible, the behavior of the system is controlled by clear, declarative configuration files, not by hardcoded logic.
-   **Living Documentation:** This project adheres to a strict "living documentation" policy. All documentation is versioned alongside the code and is continuously updated to reflect the reality of the implementation.
-   **Developer-Centric Design:** The API and its surrounding tools are designed to be intuitive and powerful for developers, with features like a flexible logging framework and a standalone testing UI.

## 2. Platform Components

The Zotify ecosystem consists of several key components:

-   **The Core API:** A robust FastAPI application that provides a RESTful interface for all platform features.
-   **`snitch`:** A secure helper application for managing OAuth2 callback flows for CLI-based clients.
-   **`Gonk/GonkUI`:** A standalone web UI for testing and interacting with the API during development.

## 3. Getting Started

To get started with the Zotify API, please refer to the comprehensive guides in our documentation.

-   **For a full installation guide:** See the [**Installation Guide**](./api/docs/system/INSTALLATION.md).
-   **To understand the API's features:** See the [**User Manual**](./api/docs/manuals/USER_MANUAL.md).
-   **For developers integrating our API:** See the [**System Integration Guide**](./api/docs/manuals/SYSTEM_INTEGRATION_GUIDE.md).
-   **For developers contributing to this project:** See the [**API Developer Guide**](./api/docs/manuals/API_DEVELOPER_GUIDE.md).

### Quick Start

A startup script is provided to get the API server running quickly in a development environment.

From the root of the project, run:
```bash
./scripts/start.sh
```
This script will handle installing dependencies, creating necessary directories, and launching the server with the correct settings for development. The API will be available at `http://localhost:8000`.

## 4. Documentation

This project uses a comprehensive, tiered documentation system. For a master list of all project documents, please see the [**Project Registry**](./project/PROJECT_REGISTRY.md).

## 5. Project Status

This project is under active development. For a detailed view of the current status, recent activities, and future plans, please see the following documents:

-   [**CURRENT_STATE.md**](./project/CURRENT_STATE.md)
-   [**ACTIVITY.md**](./project/ACTIVITY.md)
-   [**FUTURE_ENHANCEMENTS.md**](./project/FUTURE_ENHANCEMENTS.md)

# Zotify API: System Integration Guide

This document provides essential information for developers who need to integrate with or consume the Zotify API. It covers project setup, testing procedures, core architectural principles, and documentation conventions.

For developers looking to contribute to the Zotify API itself, please see the [`API_DEVELOPER_GUIDE.md`](./API_DEVELOPER_GUIDE.md).

## 1. Architectural Overview

It is critical to understand that the Zotify API is **not** a reimplementation of the Spotify Web API. Instead, it is a developer-centric framework built around the original Zotify CLI client, which itself uses Librespot for authentication and media retrieval.

The primary purpose of this API is to expose powerful, automation-oriented functionality that Spotify’s own Web API either does not offer or makes difficult to script. This includes:

*   **Direct Media Downloads**: Programmatically download tracks, albums, or playlists.
*   **Offline Caching**: Manage a local cache of media content.
*   **Advanced Automation**: Hook into a robust queueing and download management system.
*   **Raw Librespot Access**: Provide a safe, scriptable, and scalable interface to Librespot's underlying capabilities.

Think of the Zotify API as a developer platform for building systems on top of Spotify's content ecosystem, with a strong focus on media acquisition and local library management.

---

## Table of Contents
1.  [Architectural Overview](#1-architectural-overview)
2.  [Project Setup](#2-project-setup)
3.  [Authentication](#3-authentication)
4.  [Running the Test Suite](#4-running-the-test-suite)
5.  [Core Architectural Principles](#5-core-architectural-principles)
6.  [Code & Documentation Conventions](#6-code--documentation-conventions)

---

## 2. Project Setup

This section guides you through setting up and running the Zotify API from the source code.

### Prerequisites

-   **Python 3.10 or greater**
-   **pip**: The Python package installer.
-   **Git**: For cloning the repository.

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Patrick010/zotify-API.git
    cd zotify-API
    ```

2.  **Install Dependencies (Virtual Environment Recommended):**
    ```bash
    # Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate

    # Install dependencies from the project root
    pip install -e ./api
    ```

3.  **Run the API Server:**
    The application is run using `uvicorn`. For development and integration testing, it's recommended to run in `development` mode to use a default admin API key.
    ```bash
    # Run from the /api directory
    cd api

    # Start the server
    APP_ENV=development uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    The `--reload` flag enables hot-reloading for development.

---

## 3. Authentication

The Zotify API uses the **OAuth 2.0 Authorization Code Flow with PKCE** to securely connect to a user's Spotify account. This process is designed for both interactive and headless environments and is orchestrated by the API and the `snitch` helper application.

The flow is as follows:
1.  **Initiate Login**: A client sends a `GET` request to `/api/spotify/login`.
2.  **User Authorization**: The API returns a Spotify authorization URL. The user must open this URL in a browser and grant permission to the application.
3.  **Callback to Snitch**: After the user grants permission, Spotify redirects the browser to `http://127.0.0.1:4381/login`, where the `snitch` application is listening. Snitch captures the authorization `code` and `state` token from the request.
4.  **Secure Handoff**: Snitch makes a `POST` request to the Zotify API's `/api/auth/spotify/callback` endpoint, sending the `code` and `state` in a secure JSON body.
5.  **Token Exchange**: The main API validates the `state` token, then securely exchanges the `code` for a permanent refresh token and a short-lived access token from Spotify using the PKCE verifier. The tokens are then persisted.

This process ensures that credentials and secrets are never exposed in the browser.

---

## 4. Running the Test Suite

The project maintains a high standard of test coverage. Follow these steps to run the test suite.

1.  **Create Required Directories:**
    The API requires `storage` and `logs` directories. From the project root, run:
    ```bash
    mkdir api/storage
    mkdir api/logs
    ```

2.  **Run Pytest:**
    The test suite requires the `APP_ENV` environment variable to be set to `test`.
    ```bash
    # Run from inside the /api directory
    cd api
    APP_ENV=test python3 -m pytest
    ```

---

## 5. Core Architectural Principles

The Zotify API is built on a set of core principles to ensure it is maintainable, testable, and extensible.

-   **Layered Architecture:** The system is divided into distinct layers (Routes, Services, Schemas, Persistence) to enforce separation of concerns. Business logic resides in the service layer, independent of the FastAPI framework.
-   **Provider Abstraction Layer:** Decouples the core application from specific music service providers (e.g., Spotify). This allows for future extension to other providers without major refactoring.
-   **Centralized Error Handling:** A global error handling module intercepts all exceptions, ensuring consistent and standardized error responses to clients.
-   **Flexible Logging Framework:** A developer-centric logging service that uses tag-based routing and an external configuration file to provide flexible and powerful observability.
-   **Authentication Provider Interface:** Standardizes how authentication flows like OAuth2 are handled, encapsulating provider-specific logic within the provider's connector.

---

## 6. Code & Documentation Conventions

This project operates under a "living documentation" model.

-   **Reality First:** The codebase is the single source of truth. All documentation must reflect the actual, verified behavior of the application.
-   **Continuous Alignment:** All code changes must be accompanied by corresponding documentation updates in the same commit.
-   **Centralized Logging:** All work must be logged in the official project logs (`ACTIVITY.md`, `AUDIT-PHASE-*.md`) to maintain a clear, traceable history.
-   **Project Registry:** All markdown documentation must be registered in `project/PROJECT_REGISTRY.md` to be discoverable.

For a detailed checklist of tasks required for every change, please refer to `project/TASK_CHECKLIST.md`.

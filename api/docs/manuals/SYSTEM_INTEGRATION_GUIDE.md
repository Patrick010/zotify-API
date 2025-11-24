# Zotify API: System Integration Guide

This document provides essential information for developers who need to integrate with or consume the Zotify API. It covers project setup, testing procedures, core architectural principles, and documentation conventions.

For developers looking to contribute to the Zotify API itself, please see the [`API_DEVELOPER_GUIDE.md`](./API_DEVELOPER_GUIDE.md).

## Table of Contents
1.  [Project Setup](#1-project-setup)
2.  [Running the Test Suite](#2-running-the-test-suite)
3.  [Core Architectural Principles](#3-core-architectural-principles)
4.  [Code & Documentation Conventions](#4-code--documentation-conventions)

---

## 1. Project Setup

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

## 2. Running the Test Suite

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

## 3. Core Architectural Principles

The Zotify API is built on a set of core principles to ensure it is maintainable, testable, and extensible.

-   **Layered Architecture:** The system is divided into distinct layers (Routes, Services, Schemas, Persistence) to enforce separation of concerns. Business logic resides in the service layer, independent of the FastAPI framework.
-   **Provider Abstraction Layer:** Decouples the core application from specific music service providers (e.g., Spotify). This allows for future extension to other providers without major refactoring.
-   **Centralized Error Handling:** A global error handling module intercepts all exceptions, ensuring consistent and standardized error responses to clients.
-   **Flexible Logging Framework:** A developer-centric logging service that uses tag-based routing and an external configuration file to provide flexible and powerful observability.
-   **Authentication Provider Interface:** Standardizes how authentication flows like OAuth2 are handled, encapsulating provider-specific logic within the provider's connector.

---

## 4. Code & Documentation Conventions

This project operates under a "living documentation" model.

-   **Reality First:** The codebase is the single source of truth. All documentation must reflect the actual, verified behavior of the application.
-   **Continuous Alignment:** All code changes must be accompanied by corresponding documentation updates in the same commit.
-   **Centralized Logging:** All work must be logged in the official project logs (`ACTIVITY.md`, `AUDIT-PHASE-*.md`) to maintain a clear, traceable history.
-   **Project Registry:** All markdown documentation must be registered in `project/PROJECT_REGISTRY.md` to be discoverable.

For a detailed checklist of tasks required for every change, please refer to `project/TASK_CHECKLIST.md`.

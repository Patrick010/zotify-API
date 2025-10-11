<!-- ID: API-197 -->
# System Requirements

This document lists the system and software requirements for running the Zotify API and its related tools.

## Core API (`api/`)

### Software Requirements

-   **Python**: Version 3.10 or greater.
-   **pip**: The Python package installer, for managing dependencies.
-   **Git**: For cloning the source code repository.
-   **Database**: A SQLAlchemy-compatible database backend. For development, **SQLite** is sufficient. For production, a more robust database like **PostgreSQL** is recommended.
-   **FFmpeg**: (Optional) Required for some audio processing and download features.

### Operating System

The application is developed and tested on Linux. It should be compatible with other Unix-like systems (including macOS) and Windows, but these are not officially supported environments.

## Developer Testing UI (`Gonk/GonkUI/`)

### Software Requirements

-   **Python**: Version 3.10 or greater.
-   **pip**: The Python package installer.
-   **A modern web browser**: For accessing the UI.

All other dependencies (`Flask`, `sqlite-web`) are installed via `pip`.

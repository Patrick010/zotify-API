# Snitch Module Documentation

**Status:** Active
**Date:** 2025-08-18

## 1. Application Structure

The `snitch` application has been refactored into a single, self-contained Go file to resolve a persistent build issue.

### `snitch.go`

-   **Purpose**: This single file contains the entire implementation for the `snitch` executable.
-   **Responsibilities**:
    -   Reading the `SNITCH_API_CALLBACK_URL` environment variable.
    -   Validating the provided URL.
    -   Starting and configuring the local HTTP server.
    -   Handling the `/login` callback request from the OAuth provider.
    -   Forwarding the authentication code to the main Zotify API via a `GET` request.

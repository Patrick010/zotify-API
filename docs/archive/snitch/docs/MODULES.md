# Snitch Module Documentation

This document provides an overview of the internal packages within the `snitch` module.

## Package Structure

```
snitch/
├── cmd/snitch/
└── internal/listener/
```

### `cmd/snitch`

-   **Purpose**: This is the main entry point for the `snitch` executable.
-   **Responsibilities**:
    -   Parsing command-line flags (e.g., `-state`).
    -   Validating required flags.
    -   Calling the `listener` package to start the server.
    -   Handling fatal errors on startup.

### `internal/listener`

-   **Purpose**: This package contains the core logic for the OAuth callback listener. It is considered `internal` to the `snitch` module, meaning its API is not intended to be imported by other modules.
-   **Files**:
    -   `server.go`: Contains the logic for initializing, running, and gracefully shutting down the `http.Server`. It defines the port and endpoint path.
    -   `handler.go`: Contains the `http.HandlerFunc` for the `/snitch/oauth-code` endpoint. It is responsible for validating the `POST` request method, decoding the JSON payload, checking the `state` token, printing the `code` to stdout, and signaling the server to shut down.

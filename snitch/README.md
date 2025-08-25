# Snitch

Snitch is a short-lived, local OAuth callback HTTP listener written in Go. It is a subproject of Zotify-API.

## Purpose

The primary purpose of Snitch is to solve the Spotify authentication redirect problem for headless or CLI-based Zotify-API usage. When a user needs to authenticate with Spotify, they are redirected to a URL. Snitch runs a temporary local web server on `localhost:4381` to catch this redirect, extract the authentication `code` and `state`, and securely forward them to the main Zotify API backend.

## Usage

Snitch is intended to be run as a standalone process during the authentication flow. It is configured via an environment variable.

-   **`SNITCH_API_CALLBACK_URL`**: This environment variable must be set to the **full URL** of the backend API's callback endpoint. The application will validate this on startup and will exit if the URL does not start with `http://` or `https://`.
    -   Example: `export SNITCH_API_CALLBACK_URL="http://localhost:8000/api/auth/spotify/callback"`
-   **`APP_ENV`**: Set to `production` to enable redaction of sensitive data in the log output.

When started, Snitch listens on `http://localhost:4381/login`. After receiving a callback from Spotify, it will make a `GET` request to the configured callback URL with the `code` and `state` as query parameters.

## Build

The application has been simplified to a single file and has no external dependencies. To build the executable, run the following command from within the `snitch` directory:
```bash
go build snitch.go
```

## Implementation

The entire implementation is contained within `snitch.go`. It is a self-contained Go application.

## Security Enhancements (Phase 2)

To ensure the security of the authentication flow, the Snitch listener will be hardened with the following features:
- **Localhost Binding:** The server will only bind to `127.0.0.1` to prevent external access.
- **State & Nonce Validation:** The listener will enforce `state` and `nonce` validation to protect against CSRF and replay attacks.
- **Secure Secret Handling:** The received authentication `code` is handled only in memory and never logged or persisted to disk.

For full details, see the [`PHASE_2_SECURE_CALLBACK.md`](./docs/PHASE_2_SECURE_CALLBACK.md) design document.

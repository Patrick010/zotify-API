# Snitch

Snitch is a short-lived, local OAuth callback HTTP listener written in Go. It is a subproject of Zotify-API.

## Purpose

The primary purpose of Snitch is to solve the Spotify authentication redirect problem for headless or CLI-based Zotify-API usage. When a user needs to authenticate with Spotify, they are redirected to a URL. Snitch runs a temporary local web server on `localhost:4381` to catch this redirect, extract the authentication `code` and `state`, and securely forward them to the main Zotify API backend.

## Usage

Snitch is intended to be run as a standalone process during the authentication flow. It is configured via an environment variable.

-   **`SNITCH_API_CALLBACK_URL`**: This environment variable must be set to the full URL of the backend API's callback endpoint.
    -   Example: `export SNITCH_API_CALLBACK_URL="http://localhost:8000/api/auth/spotify/callback"`

When started, Snitch listens on `http://localhost:4381/login`. After receiving a callback from Spotify, it will make a `POST` request with a JSON body (`{"code": "...", "state": "..."}`) to the configured callback URL.

## Implementation

The entire implementation is contained within `snitch.go`. It is a self-contained Go application with no external dependencies, and can be built and run using standard Go tooling.

# Snitch

Snitch is a short-lived, local OAuth callback HTTP listener written in Go. It is a subproject of Zotify-API.

## Purpose

The primary purpose of Snitch is to solve the Spotify authentication redirect problem for headless Zotify-API usage. When a user needs to authenticate with Spotify, they are redirected to a URL. Snitch runs a temporary local web server to catch this redirect, extract the authentication `code`, print it to standard output, and then shut down.

## Usage

To run Snitch, execute the following command from the `snitch` directory, providing the required `state` token:

```bash
go run ./cmd/snitch -state="your-secret-state-token"
```

This starts a web server on `http://127.0.0.1:56789`. The server waits for a single `POST` request to the `/snitch/oauth-code` endpoint.

To provide the code, send a POST request with a JSON body like this:
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"code": "your-auth-code", "state": "your-secret-state-token"}' \
  http://127.0.0.1:56789/snitch/oauth-code
```

Upon receiving a valid request, Snitch prints the `code` to standard output and shuts down.

## Architecture

The Snitch module follows a standard Go project layout:

-   `cmd/snitch/main.go`: The application's entry point. It handles command-line flag parsing and starts the listener.
-   `internal/listener/`: The core logic for the web server.
    -   `server.go`: Creates, runs, and shuts down the HTTP server.
    -   `handler.go`: Contains the HTTP handler for the `/snitch/oauth-code` endpoint, which validates the POST request and JSON payload.

This tool is intended to be used as part of the Zotify-API authentication flow and is not designed for standalone use.

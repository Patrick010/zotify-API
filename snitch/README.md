# Snitch

Snitch is a short-lived, local OAuth callback HTTP listener written in Go. It is a subproject of Zotify-API.

## Purpose

The primary purpose of Snitch is to solve the Spotify authentication redirect problem for headless Zotify-API usage. When a user needs to authenticate with Spotify, they are redirected to a URL. Snitch runs a temporary local web server to catch this redirect, extract the authentication `code`, print it to standard output, and then shut down.

## Usage

To run Snitch, execute the following command from the `snitch` directory, providing the required `state` token:

```bash
go run ./cmd/snitch -state="your-secret-state-token"
```

This will start a web server on `http://localhost:21371`. The server will wait for a request to the `/callback` endpoint. After receiving a request with a valid `code` and `state` query parameter, it will print the code to the console and exit. The server will automatically time out and shut down after 2 minutes if no valid request is received.

## Architecture

The Snitch module follows a standard Go project layout to separate concerns:

-   `cmd/snitch/main.go`: The entry point of the application. It handles command-line flag parsing and initializes the listener.
-   `internal/listener/`: This package contains the core logic of the web server.
    -   `server.go`: Responsible for creating, running, and shutting down the HTTP server.
    -   `handler.go`: Contains the HTTP handler logic for the `/callback` endpoint, including state validation and code extraction.

This structure ensures that the web server logic is decoupled from the command-line interface, making it more maintainable and testable.

This tool is intended to be used as part of the Zotify-API authentication flow and is not designed for standalone use.

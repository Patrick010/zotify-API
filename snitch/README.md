# Snitch

Snitch is a short-lived, local OAuth callback HTTP listener written in Go. It is a subproject of Zotify-API.

## Purpose

The primary purpose of Snitch is to solve the Spotify authentication redirect problem for headless Zotify-API usage. When a user needs to authenticate with Spotify, they are redirected to a URL. Snitch runs a temporary local web server to catch this redirect, extract the authentication `code`, print it to standard output, and then shut down.

## Usage

Snitch is not intended to be run manually. It is launched as a subprocess by the main Zotify API during the OAuth authentication flow.

It is configured via command-line flags:
- `-state`: The CSRF token to validate the browser redirect.
- `-ipc-port`: The port of the main Zotify API's IPC server.
- `-ipc-token`: The bearer token for authenticating with the IPC server.

## Architecture

Snitch has two main roles:

1.  **HTTP Listener**: It runs a local server on `127.0.0.1:21371` to receive the `GET /callback` redirect from Spotify's authentication flow in the user's browser.
2.  **IPC Client**: After capturing and validating the `code` and `state` from the redirect, it makes a `POST` request to a secondary IPC server running within the main Zotify API process. This securely transmits the captured code back to the application.

This tool is intended to be used as part of the Zotify-API authentication flow and is not designed for standalone use.

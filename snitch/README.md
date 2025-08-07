# Snitch

Snitch is a short-lived, local OAuth callback HTTP listener written in Go. It is a subproject of Zotify-API.

## Purpose

The primary purpose of Snitch is to solve the Spotify authentication redirect problem for headless Zotify-API usage. When a user needs to authenticate with Spotify, they are redirected to a URL. Snitch runs a temporary local web server to catch this redirect, extract the authentication `code`, print it to standard output, and then shut down.

## Usage

To run Snitch, execute the following command from the `snitch` directory:

```bash
go run ./cmd/snitch
```

This will start a web server on `http://localhost:21371`. The server will wait for a request to the `/callback` endpoint. After receiving a request with a `code` query parameter, it will print the code to the console and exit. The server will automatically time out and shut down after 2 minutes if no request is received.

This tool is intended to be used as part of the Zotify-API authentication flow and is not designed for standalone use.

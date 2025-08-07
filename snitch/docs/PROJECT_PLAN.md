# Project Plan: Snitch

## 1. Purpose of Snitch

Snitch is a lightweight, single-purpose command-line tool designed to act as a temporary local OAuth 2.0 callback listener. Its sole function is to capture the authorization `code` sent by Spotify's authentication server during the authorization code flow.

## 2. Problem Being Solved

When command-line applications like Zotify-API need to perform user-level authentication with Spotify, they must use an OAuth 2.0 flow. This typically involves redirecting the user to a Spotify URL in their browser. After the user grants permission, Spotify redirects the browser back to a `redirect_uri`.

For a headless or CLI application, there is no persistent web server to receive this callback. Snitch solves this by spinning up a short-lived HTTP server on a known port (21371 in Phase 1) to listen for this one-time redirect, capture the necessary `code`, and then immediately terminate.

## 3. How it Integrates with Zotify-API

Snitch will be invoked by the Zotify-API backend or a related CLI tool when user authentication is required. The flow is as follows:

1.  Zotify-API determines that a new Spotify OAuth token is needed.
2.  It launches the Snitch binary as a subprocess.
3.  It opens a browser window pointing to the Spotify authorization URL, with `redirect_uri` set to `http://localhost:21371/callback`.
4.  The user authorizes the application in their browser.
5.  Spotify redirects the browser to the Snitch listener.
6.  Snitch captures the `code` from the query parameters, prints it to `stdout`, and exits.
7.  Zotify-API reads the `code` from Snitch's `stdout`.
8.  Zotify-API exchanges the `code` for an access token and refresh token with Spotify's backend.

## 4. Security Constraints and Assumptions

- **Localhost Only**: Snitch must only bind to the localhost interface (`127.0.0.1`) to prevent external network exposure.
- **Short-Lived**: The listener is designed to be ephemeral. It will automatically shut down after a short timeout (2 minutes) to minimize its attack surface.
- **No State**: Snitch does not store any tokens or sensitive information. Its only job is to pass the received `code` to its parent process via `stdout`.
- **Secure IPC (Future Phases)**: While Phase 1 uses `stdout`, later phases will implement a more secure Inter-Process Communication (IPC) handshake to ensure that Snitch is communicating with the legitimate Zotify-API process. This will involve a secret passed at startup.
- **Randomized Port (Future Phases)**: To prevent other applications from squatting on the known port, future phases will use a randomized port for the listener, with the port number communicated back to the parent process.

## Phase 2: Secure Callback Handling

Phase 2 introduces a critical security enhancement: **state validation**.

- **State Token**: The Zotify-API process now starts Snitch with a `--state` flag, providing a unique, unguessable token.
- **Validation Logic**: The HTTP handler in Snitch validates that the `state` parameter in the callback URL from Spotify exactly matches the expected token.
- **Conditional Shutdown**:
    - If the `state` is valid, Snitch captures the `code`, prints it to stdout, and triggers a graceful shutdown.
    - If the `state` is missing or invalid, Snitch rejects the request with a `400 Bad Request` error and, crucially, **does not shut down**. It continues to listen for a valid request until the timeout is reached. This prevents a malicious or malformed request from terminating the authentication process prematurely.

## Phase 3: Code and Structure Refactor

Phase 3 focuses on improving the internal code structure for maintainability and testability, without changing existing functionality.

- **Goal**: Refactor the codebase into a standard Go project layout.
- **Outcome**: The code is now organized into two main packages:
    - `cmd/snitch`: The main application entry point.
    - `internal/listener`: The core package containing all HTTP listener and request handling logic.
- **Benefit**: This separation of concerns makes the code easier to understand, maintain, and test in the future. The application's entry point is decoupled from its core business logic.

## Phase 4: Secure POST Endpoint

Phase 4 transitions Snitch from a `GET` callback listener to a more robust and secure `POST` endpoint. This improves cross-platform compatibility and removes the need for a user-facing browser redirect.

- **Endpoint**: The listener now runs on `http://127.0.0.1:56789` and only accepts `POST` requests to `/snitch/oauth-code`.
- **Payload**: The `code` and `state` are now passed in a JSON body, which is more secure and flexible than query parameters.
- **Strict Validation**: The handler strictly validates the request method, path, and JSON payload before processing the authentication code.
- **Testing**: Unit tests have been introduced to verify the handler's logic for various success and failure scenarios.

# Design Specification: Snitch Phase 2 - Secure Callback

**Status:** Proposed
**Author:** Jules
**Date:** 2025-08-16

## 1. Purpose

This document provides the full design and implementation specification for hardening the Snitch OAuth callback listener. The objective is to move the existing prototype to a production-safe mechanism by implementing security best practices for handling OAuth callbacks locally.

## 2. Requirements Addressed

This design directly addresses the following security and functionality requirements:

- **Listener Binding:** Must only bind to `127.0.0.1`.
- **State and Nonce Validation:** Must enforce cryptographically strong `state` and `nonce` parameters.
- **Secret Handling:** Must not persist or leak tokens or secrets.
- **Input Validation:** Must strictly validate all incoming query parameters.
- **Error Handling:** Must provide minimal, non-leaky error messages.
- **Audit & Traceability:** Must produce structured, non-sensitive logs.
- **Extensibility:** Must be self-contained and reusable.

## 3. Implementation Design

The implementation will involve modifying the existing Go source files in `snitch/internal/listener/`.

### 3.1. Listener Binding
- **File:** `snitch/internal/listener/server.go`
- **Change:** The `http.ListenAndServe` call will be modified.
- **Current:** `http.ListenAndServe(s.Addr, handler)` (Binds to all interfaces)
- **Proposed:** `http.ListenAndServe("127.0.0.1:"+s.Port, handler)` (Binds to IPv4 localhost only). The `Server` struct will be updated to hold a `Port` string instead of a full `Addr` string.

### 3.2. State and Nonce Validation
- **File:** `snitch/internal/listener/handler.go`
- **Change:** The `LoginHandler` will be significantly enhanced.
- **Logic:**
    1.  Before the user is redirected to Spotify, the Zotify API will be responsible for generating a cryptographically random `state` string and storing it temporarily (e.g., in a short-lived database record or a secure cookie).
    2.  The `LoginHandler` in Snitch will receive the `state` from Spotify's callback.
    3.  The handler will now need a way to verify this `state` value. This requires a new IPC mechanism or an API call back to the main Zotify API to ask "Is this state valid?".
    4.  A `nonce` parameter can be included in the state token (e.g. as part of a JWT) to mitigate replay attacks. The Zotify API will be responsible for validating the nonce.
    5.  If the `state` or `nonce` is invalid, the handler will immediately return a `400 Bad Request` error with a generic message.

### 3.3. Secret Handling & Input Validation
- **File:** `snitch/internal/listener/handler.go`
- **Change:**
    - All received parameters (`code`, `state`, `error`, etc.) will be strictly validated. An allow-list of expected characters and lengths will be used.
    - All logging within the handler will be reviewed to ensure no sensitive parts of the request (like the `code`) are logged in plain text. They will be masked or redacted.
    - The `code` will be passed directly to the Zotify API in the POST request body and never stored on disk by Snitch.

### 3.4. Error Handling
- **File:** `snitch/internal/listener/handler.go`
- **Change:** All error paths within the handler will be standardized to return a generic, minimal error page or message to the user's browser.
- **Example Response:** `<html><body><h1>Authentication failed.</h1><p>Please close this window and try again.</p></body></html>`
- No stack traces or internal error details will ever be exposed to the browser.

### 3.5. Audit Logging
- **File:** `snitch/internal/listener/handler.go`
- **Change:** The handler will be updated to produce structured logs for key events.
- **Events to Log:**
    - `callback.received`: When a request hits the handler.
    - `callback.validation.success`: When state/nonce validation passes.
    - `callback.validation.failure`: When state/nonce validation fails.
    - `callback.handoff.success`: When the code is successfully passed to the Zotify API.
    - `callback.handoff.failure`: When the call to the Zotify API fails.
- **Log Format:** These will be simple, non-sensitive logs compatible with the new `LoggingService` design (e.g., `logger.Info("callback.validation.success", details={"state_len": len(state)})`).

## 4. Extensibility
The handler logic will be kept self-contained. The dependency on the Zotify API for state validation will be via a configurable URL, allowing the handler to be reused for other OAuth providers in the future by pointing it to a different validation endpoint.

## 5. Testing
The `handler_test.go` file will be updated with new test cases to cover:
- Requests with a missing `state` parameter.
- Requests with an invalid `state` parameter (requires mocking the validation call to the Zotify API).
- Requests that contain an `error` parameter from the OAuth provider.
- Successful requests.

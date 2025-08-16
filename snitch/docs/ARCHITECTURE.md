# Snitch Architecture

**Status:** Active
**Date:** 2025-08-16

## 1. Core Design

Snitch is designed as a minimal, self-contained Go application with a single responsibility: to act as a temporary, local callback listener for OAuth 2.0 authentication flows.

Its architecture consists of three main parts:
1.  **Main Application (`cmd/snitch/main.go`):** The entry point of the application. It is responsible for reading configuration from environment variables and starting the HTTP server.
2.  **HTTP Server (`internal/listener/server.go`):** A standard Go HTTP server that is hardcoded to bind only to the localhost interface (`127.0.0.1`). This is a critical security feature to prevent any external network access.
3.  **Callback Handler (`internal/listener/handler.go`):** The logic that handles the incoming redirect from the OAuth provider. It extracts the `code` and `state` parameters, performs basic validation, and securely forwards them to the main Zotify API backend.

## 2. Security Model

The security of Snitch relies on a defense-in-depth approach appropriate for a local helper utility. It is not designed to be a publicly exposed, hardened web server.

### 2.1. Localhost Binding
The single most important security feature is that the HTTP server only listens on the `127.0.0.1` IP address. This means that only processes running on the same machine as Snitch can connect to it. It is not accessible from the local network or the internet, which drastically reduces its attack surface.

### 2.2. No Direct User Authentication
Snitch itself does **not** have any concept of users or authentication. It does not handle passwords or sessions. It is an unauthenticated, transient listener.

### 2.3. State Validation (CSRF Protection)
The primary mechanism for authenticating a callback request is the `state` parameter. The workflow is as follows:
1.  The **Zotify API** (not Snitch) generates a unique, unpredictable `state` token before redirecting the user to the OAuth provider.
2.  The OAuth provider must return this exact `state` token back to Snitch in the callback URL.
3.  Snitch forwards this `state` token to the Zotify API.
4.  The **Zotify API** is responsible for validating that the received `state` matches the one it originally generated.

This process ensures that the request came from the legitimate user session that started the flow, protecting against Cross-Site Request Forgery (CSRF) attacks. Snitch's role is simply to be a secure conduit for this parameter.

### 2.4. Snitch-to-API Communication Channel
A critical security assumption of the current design is that the communication channel between Snitch and the Zotify API is secure. Both processes are expected to be running on the same local machine (`localhost`).

**Future Enhancement:** For a true zero-trust environment, this channel could be further secured using mutual TLS (mTLS) to ensure that Snitch only talks to a trusted Zotify API instance, and vice-versa. This is currently tracked as a future enhancement.

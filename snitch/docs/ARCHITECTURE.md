# Snitch Architecture

**Status:** Active
**Date:** 2025-08-16

## 1. Core Design & Workflow

Snitch is designed as a minimal, self-contained Go application with a single responsibility: to act as a temporary, local callback listener for OAuth 2.0 authentication flows, specifically for headless or CLI-based clients.

The standard workflow is as follows:
1.  A user on a **client machine** initiates an action that requires OAuth 2.0 authentication (e.g., logging into the Zotify API from a command line).
2.  The remote **Zotify API server** generates a unique authorization URL (with a `state` token) and sends it to the client.
3.  The client application launches the local **Snitch process** and opens the authorization URL in the user's web browser.
4.  The user authenticates with the OAuth provider (e.g., Spotify).
5.  The provider redirects the user's browser to Snitch's local listener address (`http://127.0.0.1:4381/login`), including the authorization `code` and the original `state`.
6.  Snitch receives this request, extracts the `code` and `state`, and makes a `POST` request over the network to the remote **Zotify API server's** callback endpoint.
7.  The Zotify API validates the `state` and exchanges the `code` for an access token.

## 2. Security Model

The security of Snitch relies on a defense-in-depth approach. It's critical to understand which parts of the communication are secured and which parts have security assumptions.

### 2.1. Browser-to-Snitch Channel (Local)
This channel is between the user's browser and the Snitch listener, both on the same client machine.
-   **Security Mechanism:** The Snitch HTTP server is hardcoded to bind **only to the localhost interface (`127.0.0.1`)**.
-   **Protection:** This prevents any other device on the local network from connecting to or sniffing the traffic of the Snitch listener. While the connection is HTTP (not encrypted), the traffic never leaves the local machine, which is considered a secure boundary in this context.

### 2.2. Snitch-to-API Channel (Remote)
This channel is between the Snitch process on the client machine and the Zotify API on the remote server.
-   **Security Status:** **INSECURE**.
-   **Vulnerability:** This communication currently happens over plain HTTP. The authorization `code` is sent in the body of a POST request without encryption. This means it could be intercepted by a malicious actor with access to the network path between the client and the server (e.g., on a public Wi-Fi network).

### 2.3. Authentication and CSRF Protection
-   **Snitch Authentication:** Snitch itself has **no user authentication mechanism**. It is an open, transient listener.
-   **CSRF Protection:** The security of the overall flow is guaranteed by the `state` parameter. The remote Zotify API generates a unique, unpredictable `state` token and is responsible for validating it. This ensures that only a legitimate, user-initiated flow can be completed, protecting against Cross-Site Request Forgery attacks.

### 2.4. Future Security Enhancements
-   **Critical Priority:** The insecure Snitch-to-API channel must be secured before this feature is considered production-ready. The recommended solution is to implement **mutual TLS (mTLS)**. This would involve both Snitch and the Zotify API presenting certificates to each other, ensuring that the communication is encrypted and that both parties are trusted. This is tracked as a future enhancement.

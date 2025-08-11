# Zotify API Security

**Date:** 2025-08-11 (Updated)
**Status:** Live Document
**Original Version:** [`docs/archive/docs/projectplan/security.md`](../../archive/docs/projectplan/security.md)

---

## 1. Current Security Model

This section describes the security model as it is currently implemented in the codebase.

### 1.1. Admin Endpoint Authentication
The most significant security control is the use of a single, **static admin API key** for all administrative operations.

*   **Mechanism:** Clients must provide the pre-configured admin API key in the `X-API-Key` HTTP header.
*   **Configuration:** The API key is set via the `ADMIN_API_KEY` environment variable or an `.admin_api_key` file.
*   **Threat Model:** This approach is sufficient to prevent unauthorized access in a trusted, internal-only environment. It is **not** intended to be secure enough for a public-facing service.

### 1.2. Spotify Authentication & Token Storage
User-level authentication with the Spotify API is handled via a standard OAuth2 flow.

*   **Risk:** Spotify OAuth tokens (access and refresh) are currently stored in a plain text JSON file (`api/storage/spotify_tokens.json`).
*   **Mitigation Status:** This is a known high-priority issue. A proper, secure storage solution (e.g., encrypted database or secrets manager) is a requirement for any production-ready deployment.

### 1.3. Transport Security
All communication with the API is encrypted using TLS. Certificate management is handled by the hosting provider.

---

## 2. Future Enhancements & Security Roadmap

This section outlines security features that are planned or designed but **not yet implemented**.

### 2.1. Authentication & Authorization
*   **Dynamic Admin Key Generation:** Replace the static admin API key with a system for dynamic, auto-generated keys to mitigate risks of a compromised static secret.
*   **OAuth2 for User Authentication:** Implement a full OAuth2/JWT-based system for end-users of the API, moving beyond the single-admin model.
*   **2FA (Two-Factor Authentication):** Add an extra layer of security for user accounts.
*   **Role-Based Access Control (RBAC):** Create different roles (e.g., admin, user, read-only) with different levels of access.

### 2.2. Secrets Management
*   **Secure Credential Storage:** Implement secure, encrypted storage for Spotify tokens and other application secrets, replacing the plain text JSON files.

### 2.3. General Hardening
*   **Rate Limiting:** Introduce rate limiting on sensitive endpoints (e.g., login, playlist creation) to prevent abuse.
*   **Comprehensive Audit Logging:** Implement a detailed audit logging system to track all security-sensitive events.
*   **Security Testing:** Establish a process for regular penetration testing and vulnerability scanning.

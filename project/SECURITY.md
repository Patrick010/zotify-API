# Zotify API Security

**Date:** 2025-08-18
**Status:** Live Document

## 1. Security Philosophy

The Zotify API platform is designed with a "secure by default" philosophy, which is balanced with the flexibility required for a developer-centric tool. Our approach is to provide a secure baseline out-of-the-box, while giving administrators explicit control over security-related configurations.

## 2. Implemented Security Features

This section describes the security model as it is currently implemented in the codebase.

### 2.1. Administrative Access

Access to all administrative and system-level API endpoints is protected by a static API key.

-   **Mechanism:** Clients must provide the pre-configured admin API key in the `X-API-Key` HTTP header.
-   **Configuration:** The key is set via the `ADMIN_API_KEY` environment variable. For convenience in development (`APP_ENV=development`), a default key (`test_key`) is used if the variable is not set. In a production environment, this variable is mandatory.
-   **Threat Model:** This provides a strong baseline of protection for a service run in a trusted environment (e.g., a private network or personal server). It is not intended for multi-tenant, public-facing deployments without additional layers (like a WAF or API gateway).

### 2.2. Spotify Authentication & Token Storage

The platform uses a standard OAuth2 PKCE flow to authenticate with the Spotify API.

-   **Credential Storage:** Spotify OAuth tokens (access and refresh) are stored in the central `zotify.db` SQLite database, within the `spotify_tokens` table. This is a significant improvement over the previous plain text file storage.
-   **Database Security:** The security of these tokens is dependent on the security of the database file itself. Administrators should ensure that the `storage/` directory has appropriate file permissions.

### 2.3. Secure Logging

The Flexible Logging Framework includes several features to enhance security.

-   **Automatic Data Redaction:** When running in a production environment (`APP_ENV=production`), the logging framework automatically filters all log messages to find and redact sensitive data, such as `access_token`, `refresh_token`, and the OAuth `code`. This prevents accidental leakage of credentials into log files.
-   **Dedicated Security Log:** A dedicated `security.log` is configured by default. The framework uses tag-based routing to direct all security-relevant events (e.g., successful and failed authentication attempts) to this log file, providing a clear audit trail for security monitoring.

### 2.4. The `snitch` Helper Application

The `snitch` application, used for CLI-based authentication, has been refactored for simplicity and security. While its design documents outline a Zero Trust model with end-to-end encryption as a future goal, the current implementation securely forwards the OAuth code over HTTP on the local machine only.

## 3. Security Roadmap (Future Enhancements)

This section outlines security features that are planned but not yet implemented. For full details, see the [`FUTURE_ENHANCEMENTS.md`](./FUTURE_ENHANCEMENTS.md) document.

-   **Dynamic Plugin System Security:** The proposal for the plugin system includes a detailed section on security considerations, including administrator warnings and safe-loading practices. See [`DYNAMIC_PLUGIN_PROPOSAL.md`](./DYNAMIC_PLUGIN_PROPOSAL.md).
-   **Full JWT-Based User Authentication:** The long-term vision is to replace the static admin API key with a full JWT-based authentication system, allowing for multiple users with different roles and permissions.
-   **Encrypted Secrets:** A future enhancement will be to encrypt sensitive data (like the Spotify tokens) within the database itself, providing an additional layer of protection.
-   **API Governance:** Implementing rate limiting and other governance features to prevent abuse.

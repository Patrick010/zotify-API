# Zotify API Security

## 1. Introduction

This document outlines the security architecture, principles, and roadmap for the Zotify API project. It serves as the definitive security reference for developers, operators, and stakeholders.

## 2. Security Objectives and Scope

The primary security objectives for the Zotify API are:

*   **Confidentiality:** Protect sensitive data, such as user credentials and API keys, from unauthorized access.
*   **Integrity:** Ensure that data is not tampered with or modified by unauthorized parties.
*   **Availability:** Ensure that the API is available to authorized users when they need it.

The scope of this security plan covers the entire Zotify API, including the application code, infrastructure, and operational procedures.

## 3. Key Design Principles

*   **Zero Trust:** We assume that no user or system is inherently trustworthy. All requests are authenticated and authorized before being processed.
*   **Least Privilege:** Users and systems are granted the minimum level of access necessary to perform their functions.
*   **Environment-Specific Configurations:** Security configurations are tailored to each environment (e.g., development, testing, production) to ensure that security controls are appropriate for the level of risk.

## 4. Risks and Mitigations

### Admin API Key

The most significant security risk in the current implementation is the use of a single admin API key for all administrative operations. This risk is documented in detail in the [Admin API Key Mitigation Strategy](./admin_api_key_mitigation.md) document.

The current mitigation for this risk is a dynamic, auto-generated admin API key system. However, this is still a temporary solution, and a more robust authentication mechanism will be implemented in a future phase of the project.

## 5. Planned Security Features

The following security features are planned for future phases of the project:

*   **Random Admin Key Generation:** The current implementation already includes this feature.
*   **OAuth2:** For user-level authentication and authorization.
*   **2FA (Two-Factor Authentication):** For an extra layer of security on user accounts.
*   **Credential Storage:** Secure storage of user credentials using industry-standard hashing and encryption algorithms.
*   **Client Certificates:** For authenticating clients in a machine-to-machine communication scenario.
*   **Auditing:** Detailed audit logging of all security-sensitive events.

## 6. Authentication Services

*   **Admin API Key:** A dynamic, auto-generated API key is used to protect administrative endpoints.
*   **OAuth2 (Planned):** Will be used for user-level authentication.

## 7. Secrets Management

*   **Admin API Key:** Stored in the `.admin_api_key` file with restricted permissions. Can be overridden by the `ADMIN_API_KEY` environment variable.
*   **Other Secrets:** All other secrets, such as database credentials and third-party API keys, are managed through environment variables.

## 8. Transport Security

*   **TLS (Transport Layer Security):** All communication with the API is encrypted using TLS.
*   **Certificate Management:** Certificates are managed automatically by the hosting provider.

## 9. Middleware and Error Handling

*   **Authentication Middleware:** The `require_admin_api_key` dependency is used to protect administrative endpoints.
*   **Error Handling:** The API returns appropriate HTTP status codes for authentication and authorization failures (e.g., `401 Unauthorized`, `403 Forbidden`, `503 Service Unavailable`).

## 10. Audit Logging

A comprehensive audit logging strategy will be implemented in a future phase of the project. This will include logging all security-sensitive events, such as:

*   User login attempts (successful and failed)
*   Administrative actions
*   Changes to security configurations

## 11. Security Testing and Monitoring

*   **Security Testing:** Regular security testing, including penetration testing and vulnerability scanning, will be performed to identify and address security vulnerabilities.
*   **Monitoring:** The API is monitored for suspicious activity, and alerts are generated for potential security incidents.

## 12. Subsystem-Specific Security Notes

### Privacy & GDPR Compliance Notes

- Notification, user profile, and preferences endpoints must respect user privacy rights and data protection laws.
- All personal data access is logged via audit trails for accountability.
- Unauthenticated access to sensitive endpoints is forbidden (to be implemented as a high-priority fix).
- Privacy by design principles guide API architecture and implementation.
- GDPR compliance is validated during every development cycle, including during Step 19 privacy integration.

### Playlists Subsystem

*   **Data Privacy:** The current implementation does not have a concept of private playlists. All playlists are public. This is a potential privacy issue that should be addressed in a future iteration by adding a `private` flag to the playlist model and enforcing access control based on user ownership.
*   **Rate Limiting:** There is no rate limiting on the playlist endpoints. This could be a potential issue if the API is exposed to the public, as it could be abused to create a large number of playlists. This should be addressed in a future iteration by adding rate limiting to the playlist creation endpoint.
*   **Logging & Monitoring:** The service logs database errors, but it does not log security-sensitive events like playlist creation or deletion. This should be improved by adding audit logging for these events.

### User Profile Subsystem

*   **Data Privacy:** User profile data is stored in a JSON file. While this is a temporary solution, it is important to ensure that the file has restricted permissions and is not publicly accessible. In a production environment, user data should be stored in a secure, encrypted database.
*   **Role-Based Access Control (RBAC):** The current implementation does not have a concept of users or roles, so RBAC cannot be implemented at this time. This is a high-priority feature that will be implemented in a future phase of the project.
*   **Rate Limiting:** There is no rate limiting on the profile update endpoints. This could be a potential issue if the API is exposed to the public, as it could be abused to update profiles repeatedly. This should be addressed in a future iteration by adding rate limiting to the profile update endpoints.
*   **Audit Logging:** The service now logs all profile and preference updates.

### Notifications Subsystem

*   **Authentication and Authorization:** The notification endpoints are not authenticated. This is a major security flaw, as it allows any user to create, view, and manage notifications for any other user. This will be addressed in a future iteration when a proper user authentication and authorization system is implemented.
*   **Data Privacy:** Notification data is stored in the `user_data.json` file. As with the user profile data, this file should have restricted permissions.
*   **Rate Limiting:** There is no rate limiting on the notification endpoints. This could be a potential issue if the API is exposed to the public. This should be addressed in a future iteration.

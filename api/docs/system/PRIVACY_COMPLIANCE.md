# Privacy Compliance Overview

This document outlines how the Zotify API project complies with data protection laws, specifically the EU General Data Protection Regulation (GDPR).

## User Privacy Compliance Statement

Zotify respects user privacy and commits to protecting personal data by:

- Collecting only necessary data for functionality and services.
- Obtaining explicit user consent where required.
- Providing users with full access to their personal data, including export and deletion options.
- Ensuring data security through access control, encryption, and audit logging.
- Processing data transparently and lawfully, with clearly documented purposes.
- Supporting users’ rights to data correction, portability, and consent withdrawal.
- Conducting regular privacy impact assessments.

## API Compliance & Data Handling

### Data Storage and Security
The primary piece of Personally Identifiable Information (PII) handled by the Zotify API is the user's **Spotify OAuth Token** (access and refresh tokens).

- **Storage Location:** These tokens are stored in the main application database, a SQLite file located at `api/storage/zotify.db`.
- **Security:** The security of this sensitive data is dependent on the security of the database file itself. Access to all API endpoints is protected by a static administrative API key.

### Operator Responsibilities
The operator of the Zotify API instance is responsible for the security of the data at rest.
- **File Permissions:** Ensure the `api/storage/` directory and the `zotify.db` file within it have appropriate, restrictive file system permissions.
- **Backups:** Perform regular, secure backups of the database file.
- For detailed instructions on performing backups and other maintenance tasks, see the [`OPERATOR_MANUAL.md`](../manuals/OPERATOR_MANUAL.md).

### Implemented Endpoints for Data Rights
While dedicated `/privacy/data` endpoints for data export and deletion are planned for a future release, the following existing endpoints can be used to exercise some GDPR-related data rights:

- **Right of Access:** User data can be accessed via the various `/api/user/*` endpoints.
- **Right to Erasure ('Right to be Forgotten'):** A user's Spotify token can be deleted from the database by calling `POST /api/auth/logout`. This effectively disconnects the user's account from the Zotify instance.

## Future Enhancements

- **Dedicated GDPR Endpoints:** Implementation of `/privacy/data/export` and `/privacy/data/delete` endpoints.
- **Role-Based Access Control (RBAC):** Implementation of RBAC for more fine-grained data access permissions.
- **Rate Limiting:** Adding rate limiting to prevent abuse of personal data endpoints.
- **Continuous Monitoring:** Ongoing improvements based on security reviews and audits.

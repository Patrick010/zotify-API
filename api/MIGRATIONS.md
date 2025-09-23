# Migrations

This file tracks the database migrations for the Zotify API.

## Revisions

-   **Revision ID**: `5f96175ff7c9`
    -   **Date**: 2025-09-20
    -   **Description**: Add `notifications_enabled` boolean column to the `user_preferences` table. This adds a `server_default` of `true` to handle existing rows.

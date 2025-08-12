# Developer Guide

This guide provides instructions for setting up the Zotify API for local development and contributing to the project.

## Getting Started

For a complete guide on how to install the project and run it for the first time, please see the [Installation Guide](./INSTALLATION.md).

In summary, the main steps are:
1.  Clone the repository.
2.  Install dependencies with `pip install -e ./api`.
3.  Configure the `DATABASE_URI` in `api/.env`.
4.  Run the application with `./scripts/start.sh`.

## Core Architecture

The Zotify API is built on a modern, service-oriented architecture using Python and FastAPI. Key architectural principles include:

-   **Unified Database**: All application data is stored in a single, unified database managed by SQLAlchemy. This provides a consistent and scalable persistence layer. The database models are defined in `api/src/zotify_api/database/models.py`.
-   **Service Layer**: Business logic is encapsulated in stateless service functions. These services are responsible for interacting with the database via a dedicated CRUD layer.
-   **Provider Abstraction**: The application is being designed to be provider-agnostic. All interactions with external services (like Spotify) should be done through a provider interface layer.

## API Endpoints

The API provides a comprehensive set of endpoints for managing downloads, playlists, authentication, and more.

For a complete and up-to-date list of all available endpoints, their parameters, and their request/response schemas, please refer to the live OpenAPI schema, which is available at the `/openapi.json` endpoint of the running application.

The recommended way to explore and test the API is by using the **`gonk-testUI`** developer tool, which provides a user-friendly interface for interacting with all API endpoints.

## Admin API Key

Some administrative endpoints are protected and require an admin API key.

To use these endpoints during development, you can set the `ADMIN_API_KEY` in your `api/.env` file:
```
ADMIN_API_KEY="your-secret-key"
```
When making requests to protected endpoints, include the API key in the `X-API-Key` header.

## Contributing

If you wish to contribute to the project, please start by reading the `CONTRIBUTING.md` file in the root of the project.

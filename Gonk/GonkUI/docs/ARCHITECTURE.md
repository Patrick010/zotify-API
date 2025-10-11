<!-- ID: API-013 -->
# Gonk Test UI - Architecture

## Overview

The `Gonk/GonkUI` is a standalone web application built with Flask. It is designed to be completely independent of the main Zotify API application, acting only as an external client.

## Components

### 1. Flask Backend (`app.py`)

-   **Web Server**: A simple Flask application serves as the backend for the UI.
-   **Static File Serving**: It serves the main `index.html` page and its associated static assets (`app.js`, `styles.css`).
-   **Process Management**: It contains two API endpoints (`/launch-sqlite-web` and `/stop-sqlite-web`) that are responsible for launching and terminating the `sqlite-web` server as a background subprocess. This allows the UI to control the lifecycle of the database browser.

### 2. Frontend (`static/`)

-   **`index.html`**: The main HTML file that provides the structure for the user interface.
-   **`styles.css`**: Provides basic styling to make the UI usable.
-   **`app.js`**: The core of the frontend logic.
    -   It is a single-page application that dynamically renders content.
    -   On load, it fetches the OpenAPI schema (`/openapi.json`) from the Zotify API. This makes the UI automatically adapt to any changes in the API's endpoints.
    -   It uses the schema to build interactive forms for each endpoint.
    -   It uses the `fetch` API to send requests to the Zotify API and displays the JSON response.
    -   It interacts with the `Gonk/GonkUI` backend to manage the `sqlite-web` process.

### 3. `sqlite-web` Integration

-   `sqlite-web` is a third-party tool that is installed as a dependency.
-   It is launched as a completely separate process by the Flask backend.
-   The main UI embeds the `sqlite-web` interface using an `<iframe>`. This provides a seamless user experience, but the two applications remain decoupled.

# Gonk Test UI

A standalone developer tool for testing the Zotify API.

## Overview

Gonk Test UI is a lightweight, web-based tool designed to make testing and interacting with the Zotify API as simple as possible. It is a completely separate application from the main Zotify API and is intended for development purposes only.

## Features

-   **Dynamic API Endpoint Discovery**: Automatically fetches the OpenAPI schema from a running Zotify API instance and displays a list of all available endpoints.
-   **Interactive API Forms**: Generates web forms for each endpoint, allowing you to easily provide parameters and request bodies.
-   **Real-time API Responses**: Displays the full JSON response from the API immediately after a request is made.
-   **Spotify Authentication Helper**: Provides a simple button to initiate the Spotify OAuth2 login flow.
-   **Integrated Database Browser**: Includes an embedded `sqlite-web` interface, allowing you to browse and query the development database directly from the UI.

## Quick Start

### 1. Installation

This tool has its own set of dependencies, which need to be installed separately from the main Zotify API.

```bash
# Navigate to the gonk-testUI directory
cd gonk-testUI

# Install dependencies from its pyproject.toml
pip install -e .
```
*(Note: The `-e .` command will install the project in editable mode and handle the dependencies from `pyproject.toml`)*

### 2. Configuration

The tool needs to know the location of the Zotify API's database to launch the `sqlite-web` browser. Set the following environment variable before running the tool:

```bash
# Example for Linux/macOS
export DATABASE_URI="sqlite:///../api/storage/zotify.db"

# Example for Windows
set DATABASE_URI=sqlite:///../api/storage/zotify.db
```

### 3. Running the Tool

Make sure the main Zotify API is running (usually on `http://localhost:8000`). Then, run the Gonk Test UI:

```bash
python gonk-testUI/app.py
```

The UI will be available at **`http://localhost:8082`**.

### 4. Using the UI

-   **API Testing**: Click on an endpoint from the list on the left to generate a testing form. Fill out the form and click "Send Request". The API response will appear in the response panel.
-   **Database Browsing**: Click the "Launch sqlite-web" button. This will start the `sqlite-web` server on port 8081, and it will be displayed in the iframe on the right side of the page.

# Gonk Test UI

## Overview

Gonk Test UI is a standalone developer tool for testing the Zotify API. It is a lightweight, web-based tool designed to make testing and interacting with the Zotify API as simple as possible. It runs as a completely separate application from the main Zotify API and is intended for development purposes only.

## Features

-   **Dynamic API Endpoint Discovery**: Automatically fetches the OpenAPI schema from a running Zotify API instance and displays a list of all available endpoints.
-   **Interactive API Forms**: Generates web forms for each endpoint, allowing you to easily provide parameters and request bodies.
-   **Real-time API Responses**: Displays the full JSON response from the API immediately after a request is made.
-   **State-Aware Spotify Authentication**: Provides a dynamic button to initiate the Spotify OAuth2 login flow in a popup window. The button's state (Login/Logout) is automatically updated based on the API's true authentication status.
-   **Integrated Database Browser**: Includes an embedded `sqlite-web` interface, allowing you to browse and query the development database directly from the UI.

## Getting Started

This guide will walk you through the setup and usage of the Gonk Test UI.

### Prerequisites

-   Python 3.10+
-   The main Zotify API application must be running (usually on `http://localhost:8000`).

### 1. Installation

This tool has its own set of dependencies, which need to be installed separately from the main Zotify API.

First, navigate to the `Gonk/GonkUI` directory in your terminal:
```bash
cd Gonk/GonkUI
```

Next, install the required Python packages using its `pyproject.toml` file. The recommended way to do this is with `pip` in editable mode:
```bash
pip install -e .
```
This command will install the packages listed in `pyproject.toml` (`Flask` and `sqlite-web`) into your Python environment.

### 2. Configuration

The tool needs to know the location of the Zotify API's database to launch the `sqlite-web` browser. This is configured via an environment variable.

Before running the tool, set the `DATABASE_URI` environment variable to point to the Zotify API's database file.

**For Linux/macOS:**
```bash
export DATABASE_URI="sqlite:///../api/storage/zotify.db"
```

**For Windows (Command Prompt):**
```bash
set DATABASE_URI=sqlite:///../api/storage/zotify.db
```
*Note: The path is relative to the `Gonk/GonkUI` directory.*

### 3. Running the Application

Once the dependencies are installed and the environment variable is set, you can run the application.

The server can be started with a configurable IP, port, and Zotify API URL:
```bash
# Run with all defaults
# Server on 0.0.0.0:8082, connects to API at http://localhost:8000
python app.py

# Run on a specific IP and port
python app.py --ip 127.0.0.1 --port 8083

# Point to a specific Zotify API instance
python app.py --api-url http://192.168.1.100:8000
```
*(Make sure you are still inside the `Gonk/GonkUI` directory when running this command.)*

**Command-Line Arguments:**
-   `--ip`: The IP address to bind the UI server to. Defaults to `0.0.0.0`.
-   `--port`: The port to run the UI server on. Defaults to `8082`.
-   `--api-url`: The base URL of the Zotify API instance you want to test. Defaults to `http://localhost:8000`.

You can then access the Gonk Test UI in your web browser at the address the server is running on (e.g., `http://localhost:8082`).

### 4. Code Quality

The quality and documentation status of the source code in this module is tracked in a dedicated index. Developers should consult this index to understand the current state of the code and identify areas for improvement.

-   **[View the Gonk-TestUI Code Quality Index](./docs/CODE_QUALITY_INDEX.md)**

### 5. How to Use the UI

For detailed instructions on how to use the features of the UI, please refer to the [User Manual](./docs/USER_MANUAL.md).

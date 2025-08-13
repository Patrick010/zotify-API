# Gonk Test UI - User Manual

## Getting Started

This section will guide you through the setup and launch of the Gonk Test UI application.

### Prerequisites

-   You must have Python 3.10 or higher installed on your system.
-   The main Zotify API application must be running, as the Gonk Test UI interacts with it. By default, the Zotify API runs on `http://localhost:8000`.

### 1. Installation

The Gonk Test UI is a standalone application with its own set of dependencies. These must be installed before running the tool.

First, open your terminal or command prompt and navigate to the `gonk-testUI` directory, which is located at the root of the project.
```bash
cd path/to/project/gonk-testUI
```

Next, install the required Python packages. The dependencies are listed in the `pyproject.toml` file. You can install them using `pip`:
```bash
pip install -e .
```
This command installs the necessary packages (`Flask` and `sqlite-web`) and also installs the `gonk-testUI` project in "editable" mode, which is good for development.

### 2. Configuration

For the integrated database browser (`sqlite-web`) to work, the tool needs to know where the Zotify API's database file is located. This is configured by setting an environment variable.

Before running the application, you must set the `DATABASE_URI` environment variable.

**On Linux or macOS:**
```bash
export DATABASE_URI="sqlite:///../api/storage/zotify.db"
```

**On Windows (Command Prompt):**
```bash
set DATABASE_URI=sqlite:///../api/storage/zotify.db
```
This path points to the default location of the database file relative to the `gonk-testUI` directory. If your database is located elsewhere, you will need to adjust the path accordingly.

### 3. Running the Application

Once the installation and configuration are complete, you can start the Gonk Test UI server.

From within the `gonk-testUI` directory, run the following command:
```bash
# Run on the default IP (0.0.0.0) and port (8082)
python app.py

# Or, run on a specific IP and port
python app.py --ip 127.0.0.1 --port 8083
```

You should see output indicating that the Flask server is running. By default, the server runs on `0.0.0.0:8082`, but you can use the optional `--ip` and `--port` flags to run it on a different address.

### 4. Accessing the UI

Open your web browser and navigate to the address the server is running on (e.g., `http://localhost:8082` or `http://127.0.0.1:8083`).

You should now see the Gonk Test UI interface.

---

## Using the UI

### Main Interface

The UI is divided into two main sections:
-   **API Section (Left)**: For interacting with the Zotify API endpoints.
-   **Database Section (Right)**: For browsing the development database using `sqlite-web`.

### Using the API Tester

1.  **Loading Endpoints**: When you first load the page, the UI automatically fetches the OpenAPI schema from the running Zotify API. The list of all available API endpoints is then displayed in the "API Endpoints" panel on the left.

2.  **Generating an API Form**: Click on any endpoint button in the list. A form will be dynamically generated for that specific endpoint, with fields for all necessary parameters (path, query, request body) and an optional field for the Admin API Key.

3.  **Sending a Request**: Fill out the form with the desired values and click the "Send Request" button.

4.  **Viewing the Response**: The JSON response from the API will be displayed in the "API Response" panel.

### Using the Database Browser

1.  **Launching sqlite-web**: To browse the database, you must first start the `sqlite-web` server. Click the **"Launch sqlite-web"** button at the top of the page. This will start the server in the background on port **8081**.

2.  **Browsing the Database**: After a few seconds, the `sqlite-web` interface will load in the `<iframe>` on the right. You can now browse tables, run queries, and manage data.

3.  **Stopping sqlite-web**: When you are finished, click the **"Stop sqlite-web"** button to shut down the database browser server.

### Spotify Authentication

To test endpoints that require Spotify authentication, click the **"Login with Spotify"** button. This will open a new tab for the Spotify authorization flow. Once you complete it, the application will be able to make authenticated requests.

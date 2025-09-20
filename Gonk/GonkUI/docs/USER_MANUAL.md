# Gonk Test UI - User Manual

## Getting Started

This section will guide you through the setup and launch of the Gonk Test UI application.

### Prerequisites

-   You must have Python 3.10 or higher installed on your system.
-   The main Zotify API application must be running, as the Gonk Test UI interacts with it. By default, the Zotify API runs on `http://localhost:8000`.

### 1. Installation

The Gonk Test UI is a standalone application with its own set of dependencies. These must be installed before running the tool.

First, open your terminal or command prompt and navigate to the `Gonk/GonkUI` directory, which is located at the root of the project.
```bash
cd path/to/project/Gonk/GonkUI
```

Next, install the required Python packages. The dependencies are listed in the `pyproject.toml` file. You can install them using `pip`:
```bash
pip install -e .
```
This command installs the necessary packages (`Flask` and `sqlite-web`) and also installs the `Gonk/GonkUI` project in "editable" mode, which is good for development.

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
This path points to the default location of the database file relative to the `Gonk/GonkUI` directory. If your database is located elsewhere, you will need to adjust the path accordingly.

### 3. Running the Application

Once the installation and configuration are complete, you can start the Gonk Test UI server.

From within the `Gonk/GonkUI` directory, run the following command:
```bash
# Run with all defaults
# Server on 0.0.0.0:8082, connects to API at http://localhost:8000
python app.py

# Run on a specific IP and port
python app.py --ip 127.0.0.1 --port 8083

# Point to a specific Zotify API instance
python app.py --api-url http://192.168.1.100:8000
```

You should see output indicating that the Flask server is running. You can use the following optional flags:
-   `--ip`: The IP address to bind the UI server to (default: `0.0.0.0`).
-   `--port`: The port to run the UI server on (default: `8082`).
-   `--api-url`: The base URL of the Zotify API to test (default: `http://localhost:8000`).

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

### Spotify Authentication and Session Management

The UI provides a dynamic button in the header to manage the Spotify authentication session.

#### Checking Login Status
On page load, the UI automatically checks with the Zotify API to see if you are already authenticated with Spotify. This requires a valid **Admin API Key** to be present in one of the generated forms on the page. If no key is provided, the login button will be disabled.

#### Logging In
1.  Ensure you have entered your Admin API Key in at least one of the API forms. The login button should now be enabled.
2.  If the button says **"Login with Spotify"**, clicking it will open a small popup window with the Spotify authorization page.
3.  Log in to your Spotify account in the popup.
4.  After you approve the permissions, the popup will communicate with the Zotify API backend, save your credentials, and then close automatically.
5.  The main UI page will detect the successful login, and the button will change to say **"Logout"**.

#### Logging Out
1.  If the button says **"Logout"**, clicking it will send a request to the Zotify API to clear your stored Spotify credentials from the database.
2.  This requires a valid **Admin API Key** to be present in one of the API forms.
3.  Upon success, the button will change back to **"Login with Spotify"**.

---

### GonkUI – JWT Mock Panel

1. Open GonkUI in browser.
2. Navigate to the JWT CLI Panel.
3. Enter username/password and click "Login".
   - Verbose mode will display JWT payload and API request details.
4. Click "Get Profile" to fetch profile info.
5. Update preferences using the form and click "Update Preferences".
6. Fetch liked tracks by clicking "Fetch Liked".
7. Fetch listening history by clicking "Fetch History".
8. Clear history by clicking "Clear History".
9. Verbose output panel displays request/response details for all actions.

---

## GonkCLI

The Gonk project also includes a command-line interface (CLI) for interacting with the Zotify API.

### Authentication

Before using most commands, you must log in:
```bash
python Gonk/GonkCLI/main.py login <username> <password>
```

### Commands

-   **Get User Profile:** `python Gonk/GonkCLI/main.py get-profile`
-   **Update Preferences:** `python Gonk/GonkCLI/main.py update-prefs --theme <theme> --language <lang> --notifications <true|false>`
-   **Get Liked Tracks:** `python Gonk/GonkCLI/main.py get-liked`
-   **Get History:** `python Gonk/GonkCLI/main.py get-history`
-   **Clear History:** `python Gonk/GonkCLI/main.py clear-history`

For more details, see the `Gonk/GonkCLI/README.md` file.

# Gonk Test UI - User Manual

## Introduction

Welcome to the Gonk Test UI, a developer tool designed to make testing the Zotify API easy and efficient. This manual will guide you through the features of the UI.

## Main Interface

The UI is divided into two main sections:
-   **API Section (Left)**: For interacting with the Zotify API endpoints.
-   **Database Section (Right)**: For browsing the development database using `sqlite-web`.

## Using the API Tester

### 1. Loading Endpoints

When you first load the page, the UI will automatically try to fetch the OpenAPI schema from the running Zotify API (at `http://localhost:8000/openapi.json`). The list of all available API endpoints will be displayed in the "API Endpoints" panel.

### 2. Generating an API Form

Click on any endpoint button in the list. A form will be dynamically generated for that specific endpoint. The form will include fields for:
-   **Path parameters**: Any parameters that are part of the URL path (e.g., `playlist_id`).
-   **Query parameters**: Any parameters that are appended to the URL.
-   **Request Body**: A textarea for providing a JSON body for `POST`, `PUT`, or `PATCH` requests.
-   **Admin API Key**: A field to provide the admin API key if the endpoint requires authentication.

### 3. Sending a Request

Fill out the form with the desired values and click the "Send Request" button. The UI will send the request to the Zotify API.

### 4. Viewing the Response

The JSON response from the API will be displayed in the "API Response" panel. If there is an error, the error message will be displayed instead.

## Using the Database Browser

The database browser is powered by `sqlite-web`.

### 1. Launching sqlite-web

Before you can use the database browser, you must launch it. Click the **"Launch sqlite-web"** button at the top of the page. This will start the `sqlite-web` server in the background.

*Note: You must have the `DATABASE_URI` environment variable set correctly for this to work.*

### 2. Browsing the Database

After a few seconds, the `sqlite-web` interface will load in the `<iframe>` on the right side of the page. You can now use it to:
-   Browse the data in all tables.
-   Run custom SQL queries.
-   Insert, update, or delete rows.

### 3. Stopping sqlite-web

When you are finished with the database browser, you can stop the server by clicking the **"Stop sqlite-web"** button.

## Spotify Authentication

To test endpoints that require Spotify authentication, you will need to log in.

Click the **"Login with Spotify"** button. This will open a new tab with the Spotify authorization page. Follow the prompts to log in and authorize the application. After you are redirected back, the application will have stored the necessary tokens to make authenticated requests to Spotify.

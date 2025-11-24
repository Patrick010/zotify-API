# Snitch User Manual

**Status:** Active
**Date:** 2025-08-18

## 1. What is Snitch?

Snitch is a small helper application designed to securely handle the final step of an OAuth 2.0 authentication flow for command-line or headless applications.

When an application needs a user to authenticate with a service like Spotify, it typically opens a web browser and sends the user to a login page. After the user logs in, the service redirects the browser back to a special "callback URL". Snitch's job is to run a temporary web server on the user's local machine to *be* that callback URL. It catches the redirect, grabs the secret authentication code, and securely passes it back to the main application.

## 2. How to Build Snitch

The application has been simplified to a single Go file and has no external dependencies. To build the executable, navigate to the `snitch` directory and run the following command:
```bash
go build snitch.go
```
This will create a `snitch.exe` (or `snitch` on Linux/macOS) executable in the same directory.

## 3. How to Use Snitch

Snitch is not meant to be run constantly. It should be launched by your main application (e.g., the Zotify API) just before it needs to authenticate a user.

### 3.1. Configuration

Snitch is configured with a single environment variable:

-   **`SNITCH_API_CALLBACK_URL`**: This **must** be set to the **full URL** of your main application's callback endpoint. The application will validate this on startup and will exit with a clear error message if the URL does not start with `http://` or `https://`.
    -   **Example:** `export SNITCH_API_CALLBACK_URL="http://localhost:8000/api/auth/spotify/callback"`

### 3.2. Initiating the Authentication Flow (Example)

The main application is responsible for starting the OAuth flow. A simplified example in a web browser context would look like this:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Login with Spotify</title>
</head>
<body>
    <h1>Login to Zotify</h1>
    <p>Click the button below to authorize with Spotify. This will open a new window.</p>
    <button onclick="login()">Login with Spotify</button>

    <script>
        // In a real application, this URL would be fetched from the Zotify API
        // itself, which would generate the correct state parameter.
        const spotifyAuthUrl = "https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://127.0.0.1:4381/login&scope=playlist-read-private&state=SOME_UNIQUE_STATE_STRING";

        function login() {
            // The Zotify API would first start the Snitch process on the server.
            // Then, it would provide the client with the URL to open.
            window.open(spotifyAuthUrl, 'Spotify Login', 'width=500,height=600');
        }
    </script>
</body>
</html>
```

**Workflow:**
1.  The user clicks the "Login with Spotify" button.
2.  Before this, your main application should have started the Snitch process.
3.  The browser opens a popup to the Spotify authorization URL. Note that the `redirect_uri` is hardcoded to `http://127.0.0.1:4381/login`, which is where Snitch is listening.
4.  The user logs in and grants permission on the Spotify page.
5.  Spotify redirects the user's browser to `http://127.0.0.1:4381/login?code=...&state=...`.
6.  Snitch "catches" this request, extracts the `code` and `state`, and securely forwards them to the main Zotify API via a `GET` request.
7.  The browser window will then show a success or failure message and can be closed.

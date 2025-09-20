document.addEventListener("DOMContentLoaded", () => {
    const endpointsList = document.getElementById("endpoints-list");
    // The global apiResponse is no longer needed
    // const apiResponse = document.getElementById("api-response");

    const spotifyLoginBtn = document.getElementById("spotify-login");
    const launchSqliteBtn = document.getElementById("launch-sqlite");
    const stopSqliteBtn = document.getElementById("stop-sqlite");
    const sqliteIframe = document.getElementById("sqlite-iframe");
    const themeToggleBtn = document.getElementById("theme-toggle");

    const ZOTIFY_API_BASE = window.ZOTIFY_API_URL || "http://localhost:8000";

    // --- Theme Handling ---
    if (themeToggleBtn) {
        function applyTheme(theme) {
            if (theme === 'dark') {
                document.body.classList.add('dark-mode');
            } else {
                document.body.classList.remove('dark-mode');
            }
        }

        themeToggleBtn.addEventListener('click', () => {
            const isDarkMode = document.body.classList.contains('dark-mode');
            if (isDarkMode) {
                localStorage.setItem('theme', 'light');
                applyTheme('light');
            } else {
                localStorage.setItem('theme', 'dark');
                applyTheme('dark');
            }
        });

        // Apply saved theme on load
        const savedTheme = localStorage.getItem('theme') || 'light';
        applyTheme(savedTheme);
    }

    // Fetch OpenAPI schema and build the UI
    async function loadEndpoints() {
        try {
            const response = await fetch(`${ZOTIFY_API_BASE}/openapi.json`);
            const schema = await response.json();
            endpointsList.innerHTML = ""; // Clear existing

            for (const path in schema.paths) {
                for (const method in schema.paths[path]) {
                    const endpoint = schema.paths[path][method];
                    const button = document.createElement("button");
                    button.textContent = `${method.toUpperCase()} ${path}`;
                    button.dataset.path = path;
                    button.dataset.method = method;
                    button.addEventListener("click", (event) => renderForm(event, path, method, endpoint));
                    endpointsList.appendChild(button);
                }
            }
        } catch (error) {
            endpointsList.innerHTML = "Error loading API schema. Is the Zotify API running?";
            console.error("Error loading endpoints:", error);
        }
    }

    // Render the form for a specific endpoint
    function renderForm(event, path, method, endpoint) {
        // Remove any existing form
        const existingForm = document.getElementById("api-form");
        if (existingForm) {
            existingForm.remove();
        }

        const clickedButton = event.currentTarget;
        const form = document.createElement("form");
        form.id = "api-form";
        form.dataset.path = path;
        form.dataset.method = method;

        let formHtml = `<h3>${method.toUpperCase()} ${path}</h3>`;
        formHtml += `<p>${endpoint.summary || ""}</p>`;

        // Path parameters
        if (endpoint.parameters) {
            for (const param of endpoint.parameters) {
                if (param.in === "path") {
                    formHtml += `<div><label>${param.name} (path):</label><input type="text" name="${param.name}" required></div>`;
                }
                if (param.in === "query") {
                    formHtml += `<div><label>${param.name} (query):</label><input type="text" name="${param.name}"></div>`;
                }
            }
        }

        // Request body
        if (endpoint.requestBody) {
            formHtml += `<div><label>Request Body (JSON):</label><textarea name="requestBody" rows="5"></textarea></div>`;
        }

        formHtml += `<button type="submit">Send Request</button>`;
        form.innerHTML = formHtml;

        clickedButton.after(form);

        form.addEventListener("submit", handleFormSubmit);
    }

    // Handle form submission
    async function handleFormSubmit(event) {
        event.preventDefault();
        const form = event.target;
        const method = form.dataset.method;
        let path = form.dataset.path;

        // Remove previous response from this form, if it exists
        const existingResponse = form.querySelector('.api-response-output');
        if (existingResponse) {
            existingResponse.remove();
        }

        const responseOutput = document.createElement('pre');
        responseOutput.className = 'api-response-output';
        form.appendChild(responseOutput);

        const headers = { "Content-Type": "application/json" };
        const adminKey = getAdminApiKey(); // Use the global getter
        if (adminKey) {
            headers["X-API-Key"] = adminKey;
        }

        const queryParams = new URLSearchParams();
        const formData = new FormData(form);

        for (const [key, value] of formData.entries()) {
            if (path.includes(`{${key}}`)) {
                path = path.replace(`{${key}}`, encodeURIComponent(value));
            } else if (key !== "requestBody" && value) { // No longer need to check for adminApiKey here
                queryParams.set(key, value);
            }
        }

        const url = `${ZOTIFY_API_BASE}${path}?${queryParams.toString()}`;

        const options = { method: method.toUpperCase(), headers };
        if (form.elements.requestBody && form.elements.requestBody.value) {
            options.body = form.elements.requestBody.value;
        }

        try {
            const response = await fetch(url, options);
            const data = await response.json();
            responseOutput.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            responseOutput.textContent = `Error: ${error.message}`;
            console.error("API call error:", error);
        }
    }

    // --- Control Button Handlers ---

    // --- Auth Flow ---

    function getAdminApiKey() {
        const apiKeyInput = document.getElementById('global-admin-api-key');
        return apiKeyInput ? apiKeyInput.value : null;
    }

    async function updateLoginButtonState() {
        if (!spotifyLoginBtn) return;

        // Login button should always be enabled.
        spotifyLoginBtn.disabled = false;
        spotifyLoginBtn.title = "Login with your Spotify account.";

        const apiKey = getAdminApiKey();
        // A key is still needed to check status and to logout.
        // If no key, we assume "Login" state and don't try to fetch status.
        if (!apiKey) {
            spotifyLoginBtn.textContent = "Login with Spotify";
            return;
        }

        try {
            const response = await fetch(`${ZOTIFY_API_BASE}/api/auth/status`, {
                headers: { "X-API-Key": apiKey }
            });
            const data = await response.json();
            if (data.authenticated) {
                spotifyLoginBtn.textContent = "Logout";
            } else {
                spotifyLoginBtn.textContent = "Login with Spotify";
            }
        } catch (error) {
            spotifyLoginBtn.textContent = "Login (Status Error)";
            console.error("Error fetching auth status:", error);
        }
    }

    if (spotifyLoginBtn) {
        let loginPopup;
        let pollingInterval;

        spotifyLoginBtn.addEventListener("click", async () => {
            if (spotifyLoginBtn.textContent === "Logout") {
                const apiKey = getAdminApiKey();
                if (!apiKey) {
                    alert("Admin API Key is required to logout.");
                    return;
                }
                try {
                    await fetch(`${ZOTIFY_API_BASE}/api/auth/logout`, {
                        method: "POST",
                        headers: { "X-API-Key": apiKey }
                    });
                    updateLoginButtonState();
                } catch (error) {
                    alert(`Error during logout: ${error.message}`);
                }
            } else {
                // Login logic using polling
                try {
                    const response = await fetch(`${ZOTIFY_API_BASE}/api/auth/spotify/login`);
                    const data = await response.json();
                    if (data.auth_url) {
                        loginPopup = window.open(data.auth_url, "spotify_login", "width=500,height=600");

                        // Start polling to check auth status
                        pollingInterval = setInterval(async () => {
                            await updateLoginButtonState();
                            if (spotifyLoginBtn.textContent === "Logout") {
                                clearInterval(pollingInterval);
                                if (loginPopup) {
                                    loginPopup.close();
                                }
                            }
                            // Also check if popup was closed manually
                            if (loginPopup && loginPopup.closed) {
                                clearInterval(pollingInterval);
                            }
                        }, 2000); // Poll every 2 seconds
                    }
                } catch (error) {
                    alert(`Error during login: ${error.message}`);
                }
            }
        });
    }

    if (launchSqliteBtn) {
        launchSqliteBtn.addEventListener("click", async () => {
            try {
                const response = await fetch("/launch-sqlite-web", { method: "POST" });
                const data = await response.json();
                alert(data.message);
                if (response.ok) {
                    // Give it a moment to start up, then load it
                    setTimeout(() => {
                        sqliteIframe.src = "http://localhost:8081";
                    }, 1000);
                }
            } catch (error) {
                alert(`Error: ${error.message}`);
            }
        });
    }

    if (stopSqliteBtn) {
        stopSqliteBtn.addEventListener("click", async () => {
            try {
                const response = await fetch("/stop-sqlite-web", { method: "POST" });
                const data = await response.json();
                alert(data.message);
                if (response.ok) {
                    sqliteIframe.src = "about:blank";
                }
            } catch (error) {
                alert(`Error: ${error.message}`);
            }
        });
    }

    // Initial load
    loadEndpoints();
    updateLoginButtonState();

    // Listen for changes in the global admin key input to re-evaluate button state
    const globalApiKeyInput = document.getElementById('global-admin-api-key');
    if (globalApiKeyInput) {
        globalApiKeyInput.addEventListener('input', updateLoginButtonState);
    }

    // --- JWT CLI Panel Handlers ---

    function displayOutput(panelId, data, isVerbose = false) {
        const outputEl = document.getElementById(panelId);
        const verboseEl = document.getElementById("verbose-output");
        if (outputEl) {
            outputEl.textContent = JSON.stringify(data, null, 2);
        }
        if (isVerbose) {
            verboseEl.textContent += `\n\n--- ${new Date().toISOString()} ---\n${JSON.stringify(data, null, 2)}`;
        }
    }

    window.login = async function() {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const verbose = document.getElementById("verbose").checked;
        const statusEl = document.getElementById("login-status");

        try {
            const response = await fetch("/jwt/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();
            if (response.ok) {
                statusEl.textContent = "Login successful!";
                statusEl.style.color = "green";
            } else {
                statusEl.textContent = `Login failed: ${data.message}`;
                statusEl.style.color = "red";
            }
            displayOutput("login-status", data, verbose);
        } catch (error) {
            statusEl.textContent = `Error: ${error.message}`;
            statusEl.style.color = "red";
        }
    }

    window.getProfile = async function() {
        const verbose = document.getElementById("verbose").checked;
        try {
            const response = await fetch("/jwt/profile");
            const data = await response.json();
            displayOutput("profile-output", data, verbose);
        } catch (error) {
            displayOutput("profile-output", { error: error.message }, verbose);
        }
    }

    window.updatePreferences = async function() {
        const theme = document.getElementById("theme").value;
        const notifications = document.getElementById("notifications").checked;
        const verbose = document.getElementById("verbose").checked;

        try {
            const response = await fetch("/jwt/preferences", {
                method: "PATCH",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ theme: theme, notifications_enabled: notifications }),
            });
            const data = await response.json();
            displayOutput("preferences-output", data, verbose);
        } catch (error) {
            displayOutput("preferences-output", { error: error.message }, verbose);
        }
    }

    window.getLiked = async function() {
        const verbose = document.getElementById("verbose").checked;
        try {
            const response = await fetch("/jwt/liked");
            const data = await response.json();
            displayOutput("liked-output", data, verbose);
        } catch (error) {
            displayOutput("liked-output", { error: error.message }, verbose);
        }
    }

    window.getHistory = async function() {
        const verbose = document.getElementById("verbose").checked;
        try {
            const response = await fetch("/jwt/history");
            const data = await response.json();
            displayOutput("history-output", data, verbose);
        } catch (error) {
            displayOutput("history-output", { error: error.message }, verbose);
        }
    }

    window.clearHistory = async function() {
        const verbose = document.getElementById("verbose").checked;
        try {
            const response = await fetch("/jwt/history", { method: "DELETE" });
            const data = await response.json();
            displayOutput("history-output", data, verbose);
        } catch (error) {
            displayOutput("history-output", { error: error.message }, verbose);
        }
    }
});

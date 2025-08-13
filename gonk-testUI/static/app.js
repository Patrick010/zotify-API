document.addEventListener("DOMContentLoaded", () => {
    const endpointsList = document.getElementById("endpoints-list");
    const apiResponse = document.getElementById("api-response");

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

        formHtml += `<div><label>Admin API Key:</label><input type="text" name="adminApiKey"></div>`;
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

        const headers = { "Content-Type": "application/json" };
        const adminKey = form.elements.adminApiKey.value;
        if (adminKey) {
            headers["X-API-Key"] = adminKey;
        }

        const queryParams = new URLSearchParams();
        const formData = new FormData(form);

        for (const [key, value] of formData.entries()) {
            if (path.includes(`{${key}}`)) {
                path = path.replace(`{${key}}`, encodeURIComponent(value));
            } else if (key !== "requestBody" && key !== "adminApiKey" && value) {
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
            apiResponse.textContent = JSON.stringify(data, null, 2);
        } catch (error) {
            apiResponse.textContent = `Error: ${error.message}`;
            console.error("API call error:", error);
        }
    }

    // --- Control Button Handlers ---

    if (spotifyLoginBtn) {
        spotifyLoginBtn.addEventListener("click", async () => {
            try {
                const response = await fetch(`${ZOTIFY_API_BASE}/api/spotify/login`);
                const data = await response.json();
                if (data.auth_url) {
                    window.open(data.auth_url, "_blank");
                }
            } catch (error) {
                apiResponse.textContent = `Error: ${error.message}`;
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
});

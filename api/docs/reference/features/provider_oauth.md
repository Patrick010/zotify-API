# Feature Spec: Provider-Agnostic OAuth2 Authentication

**Status:** In Design

---

**1. Feature Name:**
Provider-Agnostic OAuth2 Authentication Flow

**2. Module/Component:**
Provider Abstraction Layer (`/api/src/zotify_api/providers/`)

**3. Purpose / Business Value:**
To establish a standardized, extensible, and provider-agnostic mechanism for handling user authentication via the OAuth2 Authorization Code Flow. This allows the API to support authentication with multiple music service providers (e.g., Spotify, and future providers) without requiring changes to the core API routes, ensuring architectural consistency and scalability.

**4. Description of Functionality:**
The system provides a generic set of endpoints to initiate and complete the OAuth2 login process for any supported provider. The API delegates the provider-specific implementation details (such as constructing the correct authorization URL and handling the callback parameters) to the currently active provider connector. This decouples the API's routing layer from the specific authentication requirements of each provider.

**5. Technical Details:**
- The `BaseProvider` interface is extended with abstract methods for `get_oauth_login_url` and `handle_oauth_callback`.
- Each provider connector (e.g., `SpotifyConnector`) implements these methods with its service-specific logic.
- Generic API routes (`/api/auth/{provider}/login` and `/api/auth/{provider}/callback`) are used to handle the flow.
- A dependency injector (`get_provider`) dynamically loads the correct provider connector based on the `{provider}` path parameter.
- The callback endpoint returns a simple HTML response to the user's browser (in the popup window) to provide feedback and trigger the window to close.

**6. Associated Endpoints or Functions:**
- `GET /api/auth/{provider}/login`: Initiates the login flow for the specified provider.
- `GET /api/auth/{provider}/callback`: Handles the redirect from the provider after the user grants or denies authorization.
- `zotify_api.providers.base.BaseProvider.get_oauth_login_url`
- `zotify_api.providers.base.BaseProvider.handle_oauth_callback`

**7. Inputs:**
- **`login` endpoint:** None (state is generated server-side).
- **`callback` endpoint (Query Parameters):**
    - `state: str` (required)
    - `code: Optional[str]` (on success)
    - `error: Optional[str]` (on failure)

**8. Outputs:**
- **`login` endpoint:** A JSON response containing the `auth_url` to redirect the user to.
- **`callback` endpoint:** An `HTMLResponse` containing a page with a success or failure message, and JavaScript to close the popup window.

**9. Dependencies:**
- **Modules:** `zotify_api.providers`, `zotify_api.routes.auth`

**10. Supported Configurations:**
- Each provider connector will require its own configuration (e.g., client ID, client secret) to be added to the central application settings.

**11. Edge Cases / Limitations:**
- This flow is designed for user-interactive logins via a web browser popup.
- It assumes the provider supports the OAuth2 Authorization Code Flow with PKCE.

**12. Testing & Validation Notes:**
- Unit tests for each provider connector must mock the external OAuth endpoints and test the `handle_oauth_callback` method for both success (`code`) and failure (`error`) cases.
- API-level tests must verify that the generic routes correctly delegate to the provider and return the expected `HTMLResponse`.

**13. Related Documentation:**
- `project/HIGH_LEVEL_DESIGN.md`
- `project/LOW_LEVEL_DESIGN.md`
- `project/TRACEABILITY_MATRIX.md` (links to `FE-03`)

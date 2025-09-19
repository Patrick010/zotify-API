# Feature Spec: Authentication - Admin API Key

**Status:** Implemented & Live

---

**1. Feature Name:**
Authentication via Static Admin API Key

**2. Module/Component:**
Core API

**3. Purpose / Business Value:**
Provides a simple, effective security mechanism to protect all API endpoints from unauthorized access. This ensures that only trusted clients or users can interact with the API, preventing public abuse and unauthorized data access.

**4. Description of Functionality:**
The system protects all API endpoints by requiring a valid, secret API key to be passed in the `X-API-Key` HTTP header of every request. If the key is missing or invalid, the API returns a `401 Unauthorized` error.

**5. Technical Details:**
- The API uses FastAPI's `APIKeyHeader` dependency to define the security scheme.
- A global dependency, `require_admin_api_key`, is applied to all necessary routes (or globally).
- This dependency checks the provided `X-API-Key` header against the `admin_api_key` value stored in the application's configuration.
- For developer convenience, if the application is run in `development` mode without an `ADMIN_API_KEY` set in the environment, a default key (`test_key`) is used automatically. In `production` mode, the key must be explicitly set, or the application will fail to start.

**6. Associated Endpoints or Functions:**
- This security scheme is applied globally to all endpoints under the `/api/` prefix.
- Key function: `zotify_api.services.auth.require_admin_api_key`

**7. Inputs:**
- **Header:** `X-API-Key`
- **Data Type:** `string`
- **Constraints:** Must be a non-empty string matching the configured server-side key.

**8. Outputs:**
- **Success:** The request is processed normally.
- **Error:** HTTP `401 Unauthorized` with `{"detail": "Invalid or missing API Key"}`.

**9. Dependencies:**
- **External Libraries:** `fastapi`
- **Modules:** `zotify_api.config`, `zotify_api.services.auth`

**10. Supported Configurations:**
- The API key can be configured via an environment variable (`ADMIN_API_KEY`).
- In production, it can also be read from a file (`.admin_api_key`).

**11. Examples:**
**Example cURL Request:**
```bash
curl -X GET "http://localhost:8000/api/system/uptime" -H "X-API-Key: your_secret_api_key"
```

**12. Edge Cases / Limitations:**
- This is a static, shared-secret system. It does not provide user-level authentication or role-based access control.
- The key is transmitted in a header and relies on TLS for protection against snooping.
- There is no built-in mechanism for key rotation; the key must be changed manually in the environment or config file.

**13. Testing & Validation Notes:**
- Tests for protected endpoints should include cases with a valid key, an invalid key, and no key to verify that the `401` error is returned correctly.
- The `api/tests/conftest.py` likely contains fixtures for providing the test client with a valid API key.

**14. Related Documentation:**
- `project/SECURITY.md` (describes the overall security model)
- `project/LOW_LEVEL_DESIGN.md` (mentions the dependency injection for security)
- `project/FUTURE_ENHANCEMENTS.md` (lists JWT as a future improvement)

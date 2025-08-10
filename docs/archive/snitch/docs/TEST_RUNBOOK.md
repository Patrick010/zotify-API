# Snitch Test Runbook

This document provides instructions for testing the Snitch listener.

## Testing Strategy

As of Phase 5, Snitch is tightly integrated with the main Zotify API application and is no longer intended to be run manually. The primary method for testing its logic is through the automated unit tests.

### Running Unit Tests

The core logic of the HTTP handler, including state validation and the IPC client call, is tested in `handler_test.go`.

To run the tests, navigate to the listener directory and use the standard Go test command:

```bash
cd snitch/internal/listener
go test
```

A successful run will output `PASS`, indicating that the handler correctly processes both valid and invalid requests.

### Manual End-to-End Testing

Manual testing of the complete flow requires running the main Zotify API and initiating the authentication process through its `/auth/login` endpoint.

1.  **Build Snitch**: Ensure the `snitch` binary is built (`cd snitch && go build -o snitch ./cmd/snitch`).
2.  **Run Zotify API**: Start the main Python API server from the `api/` directory.
3.  **Trigger Auth**: Make a `POST` request to the `/auth/login` endpoint of the Zotify API.
4.  **Open URL**: Open the `spotify_auth_url` returned by the API in a browser.
5.  **Authenticate**: Log in to Spotify and approve the request. The browser will be redirected to Snitch.
6.  **Verify**: Check the Zotify API logs to confirm the OAuth code was received and the flow completed successfully.

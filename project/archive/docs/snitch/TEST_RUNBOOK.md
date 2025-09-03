# Snitch Test Runbook

This document provides instructions for manually testing the Snitch listener.

## Phase 2: Secure Callback Testing

These tests verify the `state` validation logic.

### Prerequisites

1.  The `snitch` application is built. From the `snitch/` directory, run:
    ```bash
    go build -o snitch ./cmd/snitch
    ```
2.  Choose a secret `state` token for testing. For these examples, we will use `test-state-123`.

### Test 1: Valid Request

This test ensures that Snitch processes a request with the correct `state` token.

1.  **Start Snitch** with the chosen state:
    ```bash
    ./snitch -state="test-state-123"
    ```
    Expected output:
    ```
    Snitch is listening on http://localhost:21371/callback
    Waiting for Spotify to redirect... The listener will time out in 2 minutes.
    ```

2.  **Simulate the callback** in a separate terminal:
    ```bash
    curl "http://localhost:21371/callback?code=AUTH_CODE_HERE&state=test-state-123"
    ```

3.  **Verify the output**:
    -   The `curl` command should return: `Authentication successful! You can close this window now.`
    -   The Snitch terminal should print the code and then shut down:
        ```
        AUTH_CODE_HERE
        Successfully received OAuth code with valid state token.
        Shutdown signal received, stopping listener...
        Snitch has shut down.
        ```

### Test 2: Invalid State

This test ensures that Snitch rejects a request with an incorrect `state` token.

1.  **Start Snitch** with the chosen state:
    ```bash
    ./snitch -state="test-state-123"
    ```

2.  **Simulate the callback** with a wrong state:
    ```bash
    curl -v "http://localhost:21371/callback?code=AUTH_CODE_HERE&state=wrong-state"
    ```

3.  **Verify the output**:
    -   The `curl` command should show an HTTP 400 Bad Request response.
    -   The Snitch terminal should log an error and remain running:
        ```
        OAuth callback received with invalid state token. Expected: test-state-123, Got: wrong-state
        ```
    -   The listener should eventually time out after 2 minutes if no valid request is sent.

### Test 3: Missing State

This test ensures that Snitch rejects a request with no `state` token.

1.  **Start Snitch** as before.

2.  **Simulate the callback** without the state parameter:
    ```bash
    curl -v "http://localhost:21371/callback?code=AUTH_CODE_HERE"
    ```

3.  **Verify the output**:
    -   The `curl` command should show an HTTP 400 Bad Request response.
    -   The Snitch terminal should log an error and remain running:
        ```
        OAuth callback received without a state token.
        ```

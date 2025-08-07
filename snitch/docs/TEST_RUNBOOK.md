# Snitch Test Runbook

This document provides instructions for manually testing the Snitch listener.

## Phase 4: Secure POST Endpoint Testing

These tests verify the `POST` endpoint and JSON payload validation.

### Prerequisites

1.  The `snitch` application is built. From the `snitch/` directory, run:
    ```bash
    go build -o snitch ./cmd/snitch
    ```
2.  Choose a secret `state` token for testing. For these examples, we will use `test-state-123`.

### Test 1: Valid Request

This test ensures Snitch processes a valid `POST` request.

1.  **Start Snitch** with the chosen state:
    ```bash
    ./snitch -state="test-state-123"
    ```
    Expected output:
    ```
    Snitch is listening for a POST request on http://127.0.0.1:56789/snitch/oauth-code
    The listener will time out in 2 minutes.
    ```

2.  **Simulate the callback** in a separate terminal:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
      -d '{"code": "AUTH_CODE_HERE", "state": "test-state-123"}' \
      http://127.0.0.1:56789/snitch/oauth-code
    ```

3.  **Verify the output**:
    -   The `curl` command should return: `{"status":"ok"}`
    -   The Snitch terminal should print the code and then shut down:
        ```
        AUTH_CODE_HERE
        Successfully received and validated OAuth code from...
        Shutdown signal received, stopping listener...
        Snitch has shut down.
        ```

### Test 2: Invalid State

This test ensures Snitch rejects a request with an incorrect `state`.

1.  **Start Snitch** as above.

2.  **Send a `POST` with a wrong state**:
    ```bash
    curl -v -X POST -H "Content-Type: application/json" \
      -d '{"code": "AUTH_CODE_HERE", "state": "wrong-state"}' \
      http://127.0.0.1:56789/snitch/oauth-code
    ```

3.  **Verify the output**:
    -   The `curl` command should show an HTTP 400 Bad Request.
    -   The Snitch terminal should log an "invalid state" error and remain running.

### Test 3: Invalid Method (GET)

This test ensures Snitch rejects non-POST requests.

1.  **Start Snitch** as above.

2.  **Send a `GET` request**:
    ```bash
    curl -v http://127.0.0.1:56789/snitch/oauth-code
    ```

3.  **Verify the output**:
    -   The `curl` command should show an HTTP 405 Method Not Allowed.
    -   The Snitch terminal should log a "non-POST request" error and remain running.

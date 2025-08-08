# API Tests

This directory contains tests for the Zotify API.

## Unit Tests

Unit tests for specific services and modules can be found in the `unit/` subdirectory.

## Integration Tests

Integration tests that test the interaction of different components can be found in this directory (e.g., `test_auth_flow.py`). These tests typically use a `TestClient` to interact with the API in-memory.

## End-to-End (E2E) Tests

End-to-end tests validate the full application stack, including external services or dependent applications like Snitch.

### Spotify Authentication E2E Test

This test verifies the complete Spotify authentication flow, from the API to the Snitch service and back.

- **Test Script:** `test_e2e_auth.py`
- **Orchestrator:** `../../run_e2e_auth_test.sh`

To run the test, execute the runner script from the root of the repository:
```bash
./run_e2e_auth_test.sh
```

The script will handle starting the API server, building and starting the Snitch service, running the `pytest` script, and reporting the results based on the service logs.

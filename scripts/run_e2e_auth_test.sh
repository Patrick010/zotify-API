# ID: OPS-026
#!/bin/bash

# A script to run a full end-to-end test of the Spotify authentication flow,
# involving both the Python API and the Go Snitch service.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Project Root Calculation ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- Configuration ---
API_HOST="127.0.0.1"
API_PORT="8000"
API_URL="http://${API_HOST}:${API_PORT}"
# NOTE: The user's logs show the API running without the /api prefix.
# We will match that behavior for the test.
API_CALLBACK_URL="${API_URL}/auth/spotify/callback"
API_PID_FILE="/tmp/zotify_api.pid"
API_LOG_FILE="/tmp/zotify_api.log"

SNITCH_DIR="snitch"
SNITCH_PID_FILE="/tmp/snitch.pid"
SNITCH_LOG_FILE="/tmp/snitch.log"
SNITCH_BINARY="/tmp/snitch"

# --- Helper Functions ---

function start_api() {
    echo "--- Starting Zotify API server ---"
    (
        cd "$PROJECT_ROOT/api" && \
        uvicorn src.zotify_api.main:app --host ${API_HOST} --port ${API_PORT} &> ${API_LOG_FILE} & \
        echo $! > ${API_PID_FILE}
    )
    # Wait for the server to start
    sleep 3
    echo "API server started with PID $(cat ${API_PID_FILE}). Log: ${API_LOG_FILE}"
}

function stop_api() {
    if [ -f ${API_PID_FILE} ]; then
        PID=$(cat ${API_PID_FILE})
        echo "--- Stopping Zotify API server (PID: ${PID}) ---"
        kill ${PID} || true
        rm ${API_PID_FILE}
    fi
}

function build_and_start_snitch() {
    echo "--- Building and Starting Snitch Service ---"

    echo "Building Snitch binary..."
    (cd "$PROJECT_ROOT/${SNITCH_DIR}" && go build -o ${SNITCH_BINARY} .)

    echo "Starting Snitch service with callback URL: ${API_CALLBACK_URL}"
    (
        export SNITCH_API_CALLBACK_URL="${API_CALLBACK_URL}"
        ${SNITCH_BINARY} &> ${SNITCH_LOG_FILE} &
        echo $! > ${SNITCH_PID_FILE}
    )
    sleep 1
    echo "Snitch service started with PID $(cat ${SNITCH_PID_FILE}). Log: ${SNITCH_LOG_FILE}"
}

function stop_snitch() {
    if [ -f ${SNITCH_PID_FILE} ]; then
        PID=$(cat ${SNITCH_PID_FILE})
        echo "--- Stopping Snitch Service (PID: ${PID}) ---"
        kill ${PID} || true
        rm ${SNITCH_PID_FILE}
    fi
}

function run_e2e_test() {
    echo ""
    echo "========================================="
    echo "         RUNNING E2E AUTH TEST"
    echo "========================================="
    # It's better to run pytest from the root of the api project
    (cd "$PROJECT_ROOT/api" && python -m pytest tests/test_e2e_auth.py)
}

function check_logs_for_success() {
    echo ""
    echo "========================================="
    echo "         CHECKING LOGS FOR SUCCESS"
    echo "========================================="

    # Check Snitch log for successful forwarding
    if grep -q "Backend responded with: 200 OK" ${SNITCH_LOG_FILE}; then
        echo "✅ [SUCCESS] Snitch log shows a 200 OK response from the backend."
    else
        echo "❌ [FAILURE] Snitch log does not show a 200 OK from the backend."
        exit 1
    fi

    # Check API log for the callback being received
    if grep -q "POST /auth/spotify/callback received for state" ${API_LOG_FILE}; then
        echo "✅ [SUCCESS] API log shows callback was received by the auth endpoint."
    else
        echo "❌ [FAILURE] API log does not show callback was received."
        exit 1
    fi

    echo "✅ All checks passed!"
}


# --- Main Execution ---

# Ensure cleanup happens on script exit
trap '{ stop_api; stop_snitch; }' EXIT

# Clean up any old logs
rm -f ${API_LOG_FILE} ${SNITCH_LOG_FILE}

# Start services
start_api
build_and_start_snitch

# Run the test
run_e2e_test

# Check the results
check_logs_for_success

echo ""
echo "E2E TEST SUCCEEDED"
echo ""
echo "--- API Log ---"
cat ${API_LOG_FILE}
echo ""
echo "--- Snitch Log ---"
cat ${SNITCH_LOG_FILE}

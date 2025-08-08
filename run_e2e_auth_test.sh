#!/bin/bash

# A script to run a full end-to-end test of the Spotify authentication flow,
# involving both the Python API and the Go Snitch service.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
API_HOST="127.0.0.1"
API_PORT="8000"
API_URL="http://${API_HOST}:${API_PORT}"
API_CALLBACK_URL="${API_URL}/api/auth/spotify/callback"
API_PID_FILE="/tmp/zotify_api.pid"
API_LOG_FILE="/tmp/zotify_api.log"

SNITCH_DIR="snitch"
SNITCH_SOURCE_FILE="${SNITCH_DIR}/internal/listener/handler.go"
SNITCH_PID_FILE="/tmp/snitch.pid"
SNITCH_LOG_FILE="/tmp/snitch.log"
SNITCH_BINARY="/tmp/snitch"

# --- Helper Functions ---

function start_api() {
    echo "--- Starting Zotify API server ---"
    (
        cd api && \
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

    # IMPORTANT: Temporarily modify the hardcoded API URL in Snitch's source
    echo "Temporarily modifying Snitch source to point to test API URL: ${API_CALLBACK_URL}"
    # Use a backup file for restoration
    cp "${SNITCH_SOURCE_FILE}" "${SNITCH_SOURCE_FILE}.bak"
    sed -i "s|http://192.168.20.5/auth/spotify/callback|${API_CALLBACK_URL}|g" "${SNITCH_SOURCE_FILE}"

    echo "Building Snitch binary..."
    (cd ${SNITCH_DIR} && go build -o ${SNITCH_BINARY} ./cmd/snitch)

    # Restore the original source file
    mv "${SNITCH_SOURCE_FILE}.bak" "${SNITCH_SOURCE_FILE}"
    echo "Restored original Snitch source file."

    echo "Starting Snitch service..."
    (
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
    (cd api && pytest tests/test_e2e_auth.py)
}

function check_logs_for_success() {
    echo ""
    echo "========================================="
    echo "         CHECKING LOGS FOR SUCCESS"
    echo "========================================="

    # Check Snitch log for successful forwarding
    if grep -q "Forwarded callback data to backend" ${SNITCH_LOG_FILE}; then
        echo "✅ [SUCCESS] Snitch log shows data was forwarded."
    else
        echo "❌ [FAILURE] Snitch log does not show data was forwarded."
        exit 1
    fi

    # Check API log for the callback being received
    if grep -q "Received callback from Snitch" ${API_LOG_FILE}; then
        echo "✅ [SUCCESS] API log shows callback was received from Snitch."
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

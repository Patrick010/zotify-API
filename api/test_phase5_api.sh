#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
API_HOST="127.0.0.1"
API_PORT="8080"
BASE_URL="http://${API_HOST}:${API_PORT}/api"
PID_FILE="/tmp/zotify_api_phase5.pid"

# --- Helper Functions ---
function start_server() {
    if lsof -i -P -n | grep -q ":${API_PORT}"; then
        echo "Port ${API_PORT} is already in use. Assuming server is running."
    else
        echo "Starting Zotify API server in the background..."
        (cd src && uvicorn zotify_api.main:app --host ${API_HOST} --port ${API_PORT} & echo $! > ${PID_FILE})
        # Wait for the server to start
        sleep 3
        echo "Server started with PID $(cat ${PID_FILE})"
    fi
}

function stop_server() {
    if [ -f ${PID_FILE} ]; then
        PID=$(cat ${PID_FILE})
        echo "Stopping Zotify API server (PID: ${PID})..."
        kill ${PID} || true # Ignore error if process is already gone
        rm ${PID_FILE}
        echo "Server stopped."
    else
        echo "PID file not found. No server to stop."
    fi
}

function run_test() {
    echo ""
    echo "--- Running Test: $1 ---"
    echo "COMMAND: $2"
    echo "OUTPUT:"
    eval $2
    echo "------------------------"
}

# --- Main Script ---

# Trap EXIT signal to ensure the server is stopped
trap stop_server EXIT

# Start the server
start_server

# --- API Tests ---

echo "=== Logging ==="
run_test "Get Logging" \
    "curl -s '$BASE_URL/logging' | jq ."
run_test "Update Logging" \
    "curl -s -X PATCH '$BASE_URL/logging' -H 'Content-Type: application/json' -d '{\"level\": \"DEBUG\"}' | jq ."

echo "=== Cache ==="
run_test "Get Cache" \
    "curl -s '$BASE_URL/cache' | jq ."
run_test "Clear Cache All" \
    "curl -s -X DELETE '$BASE_URL/cache' -H 'Content-Type: application/json' -d '{}' | jq ."
run_test "Clear Cache by Type" \
    "curl -s -X DELETE '$BASE_URL/cache' -H 'Content-Type: application/json' -d '{\"type\": \"search\"}' | jq ."

echo "=== Network ==="
run_test "Update Network" \
    "curl -s -X PATCH '$BASE_URL/network' -H 'Content-Type: application/json' -d '{\"proxy_enabled\": true, \"http_proxy\": \"http://proxy.local:3128\", \"https_proxy\": \"https://secure.proxy:443\"}' | jq ."
run_test "Get Network" \
    "curl -s '$BASE_URL/network' | jq ."

# --- End of Tests ---
echo ""
echo "All tests completed."

# The 'trap' will handle stopping the server.

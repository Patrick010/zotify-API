#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
API_HOST="127.0.0.1"
API_PORT="8080"
BASE_URL="http://${API_HOST}:${API_PORT}/api/spotify"
PID_FILE="/tmp/zotify_api_phase8.pid"

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

echo "=== Spotify OAuth Login URL ==="
run_test "Spotify Login URL" \
    "curl -s '$BASE_URL/login' | jq ."

echo "Visit the above URL to authorize and get code, then run:"
echo "curl -s \"$BASE_URL/callback?code=YOUR_CODE\" | jq ."

echo "=== Token Status ==="
run_test "Token Status" \
    "curl -s '$BASE_URL/token_status' | jq ."

echo "=== Sync Playlists (manual trigger) ==="
run_test "Sync Playlists" \
    "curl -s -X POST '$BASE_URL/sync_playlists' | jq ."

echo "=== Fetch Track Metadata Example ==="
# Replace with a valid Spotify track ID
TRACK_ID="3n3Ppam7vgaVa1iaRUc9Lp"
run_test "Fetch Track Metadata" \
    "curl -s '$BASE_URL/metadata/$TRACK_ID' | jq ."


# --- End of Tests ---
echo ""
echo "All tests completed."

# The 'trap' will handle stopping the server.

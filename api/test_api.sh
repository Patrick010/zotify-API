#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
API_HOST="127.0.0.1"
API_PORT="8080"
BASE_URL="http://${API_HOST}:${API_PORT}"
PID_FILE="/tmp/zotify_api.pid"

# --- Helper Functions ---
function start_server() {
    echo "Starting Zotify API server in the background..."
    (cd src && uvicorn zotify_api.main:app --host ${API_HOST} --port ${API_PORT} & echo $! > ${PID_FILE})
    # Wait for the server to start
    sleep 3
    echo "Server started with PID $(cat ${PID_FILE})"
}

function stop_server() {
    if [ -f ${PID_FILE} ]; then
        PID=$(cat ${PID_FILE})
        echo "Stopping Zotify API server (PID: ${PID})..."
        kill ${PID}
        rm ${PID_FILE}
        echo "Server stopped."
    else
        echo "PID file not found. Is the server running?"
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

# Test 1: Ping the server
run_test "Ping Server" \
    "curl -s -X GET '${BASE_URL}/ping'"

# Test 2: Get all playlists
run_test "Get All Playlists" \
    "curl -s -X GET '${BASE_URL}/playlists' -H 'accept: application/json'"

# Test 3: Create a new playlist
run_test "Create New Playlist" \
    "curl -s -X POST '${BASE_URL}/playlists' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{\"name\": \"My Test Playlist\"}'"

# Test 4: Get all playlists again to see the new one
run_test "Get All Playlists After Create" \
    "curl -s -X GET '${BASE_URL}/playlists' -H 'accept: application/json'"

# Test 5: Try to create a playlist with a bad payload (e.g., missing name)
run_test "Create Playlist with Bad Payload" \
    "curl -s -w '%{http_code}' -X POST '${BASE_URL}/playlists' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{}'"


# --- End of Tests ---
echo ""
echo "All tests completed."

# The 'trap' will handle stopping the server.

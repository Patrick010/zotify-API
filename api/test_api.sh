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

function cleanup() {
    echo ""
    echo "--- Cleaning up created resources ---"
    curl -s -X DELETE "${BASE_URL}/playlists" -H "accept: */*"
    echo "All playlists deleted."
    echo "-----------------------------------"
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

# Cleanup before tests
cleanup

# --- API Tests ---

# Test 1: Ping the server
run_test "Ping Server" \
    "curl -s -X GET '${BASE_URL}/ping'"

# Test 2: Get all playlists (should be empty now)
run_test "Get All Playlists (should be empty)" \
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

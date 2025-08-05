#!/bin/bash
set -e

BASE_URL="http://127.0.0.1:8080"

echo "--- Running Health Checks ---"

# Check root
echo "Pinging API root..."
curl -sS --fail "$BASE_URL/ping" | grep -q '"pong":true'
echo "API root is responsive."

# Check config
echo "Checking /config endpoint..."
curl -sS --fail "$BASE_URL/api/config" | grep -q 'library_path'
echo "/config is available."

echo "--- Health Checks Passed ---"

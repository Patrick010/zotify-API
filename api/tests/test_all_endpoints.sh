#!/bin/bash
set -e

BASE_URL="http://127.0.0.1:8080/api"
ROUTES=(config playlists tracks logging cache network sync downloads metadata spotify stubs user system)

echo "--- Testing All Endpoints ---"

for route in "${ROUTES[@]}"; do
    echo "Checking /${route}..."
    curl -sS --fail "${BASE_URL}/${route}" > /dev/null
    echo "/${route} is available."
done

echo "--- All Endpoints Tests Passed ---"

#!/bin/bash

# --- Configuration ---
API_HOST="127.0.0.1"
API_PORT="8000" # Corrected port
BASE_URL="http://${API_HOST}:${API_PORT}/api"
ROUTES=(config playlist tracks logging cache network sync downloads metadata spotify stubs user system)
OUTPUT_FILE="/tmp/api_all_routes.json" # Use /tmp to avoid clutter

echo "Fetching API routes and combining JSON responses into $OUTPUT_FILE"
echo "NOTE: This script requires the API server to be running."

# Start JSON array
echo "[" > "$OUTPUT_FILE"

first=true
for route in "${ROUTES[@]}"; do
    if [ "$first" = true ]; then
        first=false
    else
        echo "," >> "$OUTPUT_FILE"
    fi

    # -f, --fail: Fail silently (no output at all) on server errors.
    response=$(curl -s -f "$BASE_URL/$route")

    # If curl fails or returns an empty response, use "null" for valid JSON
    if [ -z "$response" ]; then
        response="null"
    fi

    # Wrap each route's response in an object with route name
    echo "{\"route\":\"$route\", \"data\": $response}" >> "$OUTPUT_FILE"
done

# End JSON array
echo "]" >> "$OUTPUT_FILE"

echo "Done fetching routes. Report written to $OUTPUT_FILE"

# Now run the audit with Python
python3 - <<EOF
import json
import sys

def summarize_routes(file_path):
    try:
        with open(file_path) as f:
            routes = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from {file_path}.", file=sys.stderr)
        print(f"JSON Error: {e}", file=sys.stderr)
        print("This can happen if the API server is not running or not responding correctly.", file=sys.stderr)
        sys.exit(1)


    missing_routes = []
    empty_data_routes = []
    null_data_routes = []

    for route in routes:
        data = route.get("data")
        if data is None:
            null_data_routes.append(route["route"])
        elif not data or data == {}:
            empty_data_routes.append(route["route"])
        elif isinstance(data, dict) and data.get("detail") == "Not Found":
            missing_routes.append(route["route"])

    print("\n--- API Audit Summary ---")
    if missing_routes:
        print("Routes missing (404 or 'Not Found'):")
        for r in missing_routes:
            print(f" - {r}")

    if null_data_routes:
        print("\nRoutes that did not respond (or server down):")
        for r in null_data_routes:
            print(f" - {r}")

    if empty_data_routes:
        print("\nRoutes with empty data:")
        for r in empty_data_routes:
            print(f" - {r}")

    if not missing_routes and not empty_data_routes and not null_data_routes:
        print("All checked routes responded with data.")

summarize_routes("$OUTPUT_FILE")
EOF

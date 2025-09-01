#!/bin/bash

BASE_URL="http://127.0.0.1:8080/api"
ROUTES=(config playlist tracks logging cache network sync downloads metadata spotify stubs user system)
OUTPUT_FILE="api_all_routes.json"

echo "Fetching API routes and combining JSON responses into $OUTPUT_FILE"

# Start JSON array
echo "[" > "$OUTPUT_FILE"

first=true
for route in "${ROUTES[@]}"; do
    if [ "$first" = true ]; then
        first=false
    else
        echo "," >> "$OUTPUT_FILE"
    fi

    response=$(curl -s "$BASE_URL/$route")
    # Wrap each route's response in an object with route name
    echo "{\"route\":\"$route\", \"data\": $response}" >> "$OUTPUT_FILE"
done

# End JSON array
echo "]" >> "$OUTPUT_FILE"

echo "Done fetching routes."

# Now run the audit with Python
python3 - <<EOF
import json

def summarize_routes(file_path):
    with open(file_path) as f:
        routes = json.load(f)

    missing_routes = []
    empty_data_routes = []

    for route in routes:
        data = route.get("data")
        if not data or data == {}:
            empty_data_routes.append(route["route"])
        elif isinstance(data, dict) and data.get("detail") == "Not Found":
            missing_routes.append(route["route"])

    print("Summary Report:")
    if missing_routes:
        print("Routes missing (404 or 'Not Found'):")
        for r in missing_routes:
            print(f" - {r}")
    else:
        print("No missing routes detected.")

    if empty_data_routes:
        print("\nRoutes with empty data:")
        for r in empty_data_routes:
            print(f" - {r}")
    else:
        print("No routes with empty data.")

summarize_routes("$OUTPUT_FILE")
EOF

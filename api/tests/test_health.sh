#!/bin/bash
BASE_URL="http://localhost:8000/api"

echo "Checking API root..."
curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:8000/ping" | grep -q 200 && echo "API root OK" || { echo "API root FAIL"; exit 1; }

echo "Checking /config endpoint..."
curl -s -o /dev/null -w "%{http_code}\n" "$BASE_URL/config" | grep -q 200 && echo "/config OK" || { echo "/config FAIL"; exit 1; }

#!/bin/bash
BASE_URL="http://localhost:8000/api"

for endpoint in user system; do
  echo "Testing /$endpoint endpoint..."
  http_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$endpoint")
  [[ "$http_code" == "200" ]] && echo "  GET /$endpoint OK" || { echo "  GET /$endpoint FAIL ($http_code)"; exit 1; }
done

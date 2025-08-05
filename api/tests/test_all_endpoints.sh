#!/bin/bash
BASE_URL="http://localhost:8000/api"
ENDPOINTS=(config playlists tracks user system downloads metadata spotify sync cache logging stubs)

for ep in "${ENDPOINTS[@]}"; do
  echo "Checking /$ep"
  code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$ep")
  [[ "$code" == "200" ]] && echo "  OK" || { echo "  FAIL ($code)"; exit 1; }
done

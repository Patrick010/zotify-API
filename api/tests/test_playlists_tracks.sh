#!/bin/bash
BASE_URL="http://localhost:8000/api"

for endpoint in playlists tracks; do
  echo "Testing /$endpoint endpoint..."
  http_code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$endpoint")
  [[ "$http_code" == "200" ]] && echo "  GET /$endpoint OK" || { echo "  GET /$endpoint FAIL ($http_code)"; exit 1; }

  resp=$(curl -s "$BASE_URL/$endpoint")
  echo "$resp" | grep -q '"data"' || { echo "  Missing data field"; exit 1; }
  echo "$resp" | grep -q '"meta"' || { echo "  Missing meta field"; exit 1; }

  resp_limit=$(curl -s "$BASE_URL/$endpoint?limit=1")
  data_count=$(echo "$resp_limit" | grep -o '"id":' | wc -l)
  [[ "$data_count" == 1 ]] && echo "  limit=1 works" || { echo "  limit=1 failed (returned $data_count)"; exit 1; }
done

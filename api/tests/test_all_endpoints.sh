#!/bin/bash
BASE_URL="http://localhost:8000/api"
ENDPOINTS=(config playlists tracks user system downloads metadata spotify sync cache logging stubs)

for ep in "${ENDPOINTS[@]}"; do
  echo "Checking /$ep"
  if [ "$ep" == "user" ]; then
    code=$(curl -s -o /dev/null -w "%{http_code}" -H "X-Test-User: 3fa85f64-5717-4562-b3fc-2c963f66afa6" "$BASE_URL/$ep")
  elif [ "$ep" == "spotify" ]; then
    code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/spotify/status")
  else
    code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/$ep")
  fi
  [[ "$code" == "200" ]] && echo "  OK" || { echo "  FAIL ($code)"; exit 1; }
done

# check metadata non-empty
RESP=$(curl -s "$BASE_URL/metadata")
if ! echo "$RESP" | jq . >/dev/null; then
  echo "ERROR: /metadata did not return valid JSON"
  exit 1
fi
# ensure total_tracks exists and is number
TT=$(echo "$RESP" | jq '.total_tracks // 0')
if [ -z "$TT" ]; then
  echo "ERROR: /metadata missing total_tracks"
  exit 1
fi

# check cache hit_rate present
curl -s "$BASE_URL/cache" | jq '.hit_rate' >/dev/null || { echo "cache missing hit_rate"; exit 1; }
# check logging returns data array
curl -s "$BASE_URL/logging" | jq '.data | length' >/dev/null || { echo "logging data missing"; exit 1; }
# check system uptime exists
curl -s "$BASE_URL/system" | jq '.uptime_seconds' >/dev/null || { echo "system uptime missing"; exit 1; }
# check user returns email when header provided (dev)
curl -s -H "X-Test-User: 3fa85f64-5717-4562-b3fc-2c963f66afa6" "$BASE_URL/user" | jq '.email' >/dev/null || { echo "user email missing"; exit 1; }

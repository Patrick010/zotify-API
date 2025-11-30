#!/bin/bash
set -e

OUTDIR="./api_dumps"
OUTFILE="$OUTDIR/all_routes.jsonl"
mkdir -p "$OUTDIR"
> "$OUTFILE"

ROUTES=(
  "config"
  "playlist"
  "tracks"
  "logging"
  "cache"
  "network"
  "sync"
  "downloads"
  "metadata"
  "spotify"
  "stubs"
  "user"
  "system"
)

echo "Dumping all API routes to $OUTFILE"

for route in "${ROUTES[@]}"; do
  echo -n "[GET] http://127.0.0.1:8080/api/$route -> $OUTFILE"
  # Get response, add route info and append as a JSON line
  curl -s "http://127.0.0.1:8080/api/$route" | jq --arg route "$route" '{route: $route, data: .}' >> "$OUTFILE"
done

echo "Done."

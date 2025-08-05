#!/bin/bash
set -e

BASE_URL="http://127.0.0.1:8080/api"

echo "--- Testing Playlists and Tracks Endpoints ---"

# Test GET /playlists
echo "Fetching /playlists..."
curl -sS --fail "$BASE_URL/playlists" | grep -q '"data":'
echo "/playlists responded correctly."

# Test GET /playlists with query params
echo "Fetching /playlists with limit=1..."
curl -sS --fail "$BASE_URL/playlists?limit=1" | grep -q '"limit":1'
echo "/playlists with limit is working."

# Test GET /tracks
echo "Fetching /tracks..."
curl -sS --fail "$BASE_URL/tracks" | grep -q '"data":'
echo "/tracks responded correctly."

# Test GET /tracks with search
echo "Fetching /tracks with search=Artist..."
curl -sS --fail "$BASE_URL/tracks?search=Artist" | grep -q '"total":2'
echo "/tracks with search is working."

echo "--- Playlists and Tracks Tests Passed ---"

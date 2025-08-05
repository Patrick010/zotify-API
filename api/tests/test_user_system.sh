#!/bin/bash
set -e

BASE_URL="http://127.0.0.1:8080/api"

echo "--- Testing User and System Endpoints ---"

# Test GET /user
echo "Fetching /user..."
curl -sS --fail "$BASE_URL/user" | grep -q '"username":"dummy_user"'
echo "/user responded correctly."

# Test GET /system
echo "Fetching /system..."
curl -sS --fail "$BASE_URL/system" | grep -q '"status":"System is operational"'
echo "/system responded correctly."

echo "--- User and System Tests Passed ---"

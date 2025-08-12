#!/bin/bash
set -e

# Check if DATABASE_URI is set
if [ -z "$DATABASE_URI" ]; then
    echo "Error: DATABASE_URI environment variable is not set."
    echo "Please set it to a valid database connection string (e.g., sqlite:///./api/storage/zotify.db)"
    exit 1
fi

echo "Starting Zotify API server..."

# Run the uvicorn server
# We assume this script is run from the root of the project.
cd api/ && uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

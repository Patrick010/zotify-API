#!/bin/bash
set -e

# The DATABASE_URI check has been removed.
# The application now uses a sensible default for local development if the
# environment variable is not set. See api/src/zotify_api/config.py.

echo "Installing/updating dependencies (including dev dependencies)..."
# Correctly install from the project root to include the 'api' package and its 'dev' extras.
pip install -e ".[dev]"

# Create required directories if they don't exist
echo "Ensuring required directories exist..."
mkdir -p api/storage
mkdir -p api/logs

echo "Starting Zotify API server..."

# Set the application environment to "development" to disable production checks
export APP_ENV=development

# Start the documentation server in the background
echo "Starting documentation server on http://0.0.0.0:8008..."
mkdocs serve --dev-addr 0.0.0.0:8008 &

# Run the uvicorn server
# We assume this script is run from the root of the project.
cd api/ && PYTHONPATH=./src uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

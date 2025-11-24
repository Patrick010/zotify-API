#!/bin/bash
set -e

# The DATABASE_URI check has been removed.
# The application now uses a sensible default for local development if the
# environment variable is not set. See api/src/zotify_api/config.py.

# Create required directories if they don't exist from the root
echo "Ensuring required directories exist..."
mkdir -p api/storage
mkdir -p api/logs

# Start the documentation server from the root in the background
echo "Starting documentation server on http://0.0.0.0:8008..."
mkdocs serve --dev-addr 0.0.0.0:8008 &

# Move into the API directory for all subsequent python-related tasks
cd api/

echo "Installing/updating dependencies (including dev dependencies)..."
# Install the package in editable mode from within the api directory
pip install -e ".[dev]"

echo "Starting Zotify API server..."

# Set the application environment to "development" to disable production checks
export APP_ENV=development

# Run the uvicorn server from within the api/ directory
PYTHONPATH=./src uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

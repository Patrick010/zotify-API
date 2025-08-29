#!/bin/bash
set -e

# The DATABASE_URI check has been removed.
# The application now uses a sensible default for local development if the
# environment variable is not set. See api/src/zotify_api/config.py.

echo "Installing/updating dependencies (including dev dependencies)..."
pip install -e './api[dev]'

echo "Starting Zotify API server..."

# Set the application environment to "development" to disable production checks
export APP_ENV=development

# Start the documentation server in the background
echo "Starting documentation server on http://0.0.0.0:8008..."
mkdocs serve --dev-addr 0.0.0.0:8008 &

# Run the uvicorn server
# We assume this script is run from the root of the project.
cd api/ && mkdir -p storage && mkdir -p logs && PYTHONPATH=./src uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

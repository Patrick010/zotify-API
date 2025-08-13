#!/bin/bash
set -e

# The DATABASE_URI check has been removed.
# The application now uses a sensible default for local development if the
# environment variable is not set. See api/src/zotify_api/config.py.

echo "Starting Zotify API server..."

# Run the uvicorn server
# We assume this script is run from the root of the project.
# We set PYTHONPATH to include the `src` directory so that the local,
# editable source code is used instead of a globally installed package.
cd api/ && mkdir -p storage && PYTHONPATH=./src uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

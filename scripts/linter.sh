#!/usr/bin/env bash
set -euo pipefail

echo "Running Unified Linter..."
echo "=========================="

# Default to not running the checks
RUN_PYTEST=false
RUN_MKDOCS=false

# Get list of staged files
# We need to be in the git repository root for this to work correctly.
cd /app

STAGED_FILES=$(git diff --name-only --cached)

if [ -z "$STAGED_FILES" ]; then
    echo "No staged files to check."
fi

echo "Checking staged files:"
echo "$STAGED_FILES"
echo "--------------------------"

# Check for code changes
if echo "$STAGED_FILES" | grep -q -E '\.py$|\.go$'; then
    echo "Code changes detected. Flagging pytest to run."
    RUN_PYTEST=true
fi

# Check for documentation changes in api/docs
if echo "$STAGED_FILES" | grep -q -E '^api/docs/'; then
    echo "API documentation changes detected. Flagging mkdocs to run."
    RUN_MKDOCS=true
fi

# --- Execution Phase ---
echo "=========================="
echo "Executing checks..."

# Always run the documentation cross-reference linter
# This script needs to be run from the api directory
echo "Running doc linter..."
(cd api && PRE_COMMIT=true python3 ../scripts/lint-docs.py)


# Run pytest if flagged
if [ "$RUN_PYTEST" = true ]; then
    echo "--------------------------"
    echo "Running pytest..."
    (cd api && APP_ENV=test pytest)
else
    echo "--------------------------"
    echo "Skipping pytest: No code changes detected."
fi

# Run mkdocs build if flagged
if [ "$RUN_MKDOCS" = true ]; then
    echo "--------------------------"
    echo "Running mkdocs build..."
    mkdocs build --clean
else
    echo "--------------------------"
    echo "Skipping mkdocs build: No relevant documentation changes detected."
fi

echo "=========================="
echo "Unified Linter finished successfully."

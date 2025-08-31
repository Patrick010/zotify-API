#!/usr/bin/env bash
set -euo pipefail

# repo root -> script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Activate venv if present (adjust path if your venv lives elsewhere)
if [[ -f "$PROJECT_ROOT/api/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1090
    source "$PROJECT_ROOT/api/.venv/bin/activate"
fi

cd "$PROJECT_ROOT/api"

echo "=== Running full test suite ==="
echo

# Set the application environment to "development" to disable production checks
# and provide a default API key for tests.
export APP_ENV=development

# Create the storage directory if it doesn't exist, so the SQLite DB can be created.
mkdir -p storage

# Run pytest from api/ so pytest finds tests via testpaths in pyproject.toml
if python3 -m pytest -v --maxfail=5 --disable-warnings; then
    echo
    echo "✅ All tests passed"
    exit 0
else
    echo
    echo "❌ Tests failed"
    exit 1
fi

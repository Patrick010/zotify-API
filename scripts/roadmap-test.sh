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

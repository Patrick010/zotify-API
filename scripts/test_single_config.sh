#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/api/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1090
    source "$SCRIPT_DIR/api/.venv/bin/activate"
fi
cd "$SCRIPT_DIR/api"
echo "=== Running single config reset test ==="
python3 -m pytest -q tests/test_config.py::test_reset_config -q

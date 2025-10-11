# ID: OPS-030
#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
if [[ -f "$PROJECT_ROOT/api/.venv/bin/activate" ]]; then
    # shellcheck disable=SC1090
    source "$PROJECT_ROOT/api/.venv/bin/activate"
fi
cd "$PROJECT_ROOT/api"
echo "=== Running single config reset test ==="
python3 -m pytest -q tests/test_config.py::test_reset_config -q

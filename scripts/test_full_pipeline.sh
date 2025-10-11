#!/usr/bin/env bash
set -euo pipefail

echo "=== Starting full pipeline test (dry-run) ==="

# Step 1: Backup TRACE_INDEX.yml
TRACE_INDEX="/root/zotify-API/project/reports/TRACE_INDEX.yml"
BACKUP_TRACE_INDEX="/root/zotify-API/project/reports/TRACE_INDEX.yml.bak"
if [ -f "$TRACE_INDEX" ]; then
    echo "[Step 1] Backing up TRACE_INDEX.yml"
    cp "$TRACE_INDEX" "$BACKUP_TRACE_INDEX"
fi

# Step 2: Run inventory script in test mode
echo "[Step 2] Running repo_inventory_and_governance.py in test mode"
python3 scripts/repo_inventory_and_governance.py --full --debug || { echo "Inventory script failed"; exit 1; }

# Step 3: Check for missing DOC-/API- IDs in TRACE_INDEX.yml
echo "[Step 3] Checking for missing DOC-/API- IDs"
MISSING_IDS=$(python3 - <<EOF
import yaml
trace_index_path = "$TRACE_INDEX"
data = yaml.safe_load(open(trace_index_path))
missing = [item['path'] for item in data.get('artifacts', []) if 'id' not in item or not item['id']]
print(",".join(missing))
EOF
)
if [ -n "$MISSING_IDS" ]; then
    echo "Missing IDs for files: $MISSING_IDS"
    exit 1
fi

# Step 4: Run alignment verification
echo "[Step 4] Running verify_alignment_migration.py"
python3 scripts/verify_alignment_migration.py || { echo "Alignment verification failed"; exit 1; }

# Step 5: Run governance linter
echo "[Step 5] Running lint_governance_links.py"
python3 scripts/lint_governance_links.py || { echo "Linter failed"; exit 1; }

# Step 6: (Optional) Check for unregistered files in indexes
echo "[Step 6] Checking for unregistered files in indexes"
# Could be extended with extra logic if needed

# Step 7: Final report
echo "=== Full pipeline test completed successfully ==="

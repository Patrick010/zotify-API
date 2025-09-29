#!/bin/bash
set -e

echo "=== Running Linter Regression Test ==="
BRANCH=test-linter-regression

git checkout -b $BRANCH
python3 scripts/linter.py

echo "=== Regression Test Completed ==="
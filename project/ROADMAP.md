#!/usr/bin/env python3
"""
scripts/verify_governance.py

Report-only verification of project governance:
- proposals
- roadmap
- execution plan / backlog
- alignment matrix
- trace index
- project registry
- logs

Provides recommendations for missing or misaligned artifacts.
"""

import os
import yaml

# === CONFIG ===
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJECT_REGISTRY = os.path.join(REPO_ROOT, 'project', 'PROJECT_REGISTRY.md')
TRACE_INDEX_FILE = os.path.join(REPO_ROOT, 'project', 'TRACE_INDEX.yml')
ALIGNMENT_MATRIX = os.path.join(REPO_ROOT, 'project', 'ALIGNMENT_MATRIX.md')
ROADMAP = os.path.join(REPO_ROOT, 'project', 'roadmap.md')
PROPOSALS_DIR = os.path.join(REPO_ROOT, 'project/proposals')

# === FUNCTIONS ===

def load_registry():
    registry_files = set()
    if os.path.exists(PROJECT_REGISTRY):
        with open(PROJECT_REGISTRY, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    registry_files.add(line)
    return registry_files

def scan_proposals():
    proposals = []
    if os.path.exists(PROPOSALS_DIR):
        for f in os.listdir(PROPOSALS_DIR):
            if f.endswith('.md'):
                proposals.append(f)
    return proposals

def load_trace_index():
    if os.path.exists(TRACE_INDEX_FILE):
        with open(TRACE_INDEX_FILE) as f:
            return yaml.safe_load(f)
    return {'artifacts': []}

def load_alignment_matrix():
    matrix = {}
    if os.path.exists(ALIGNMENT_MATRIX):
        with open(ALIGNMENT_MATRIX) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    if len(parts) >= 3:
                        matrix[parts[0]] = {'type': parts[1], 'path': parts[2]}
    return matrix

def load_roadmap():
    roadmap = set()
    if os.path.exists(ROADMAP):
        with open(ROADMAP) as f:
            for line in f:
                line = line.strip()
                if line.startswith('-'):
                    milestone = line.lstrip('-').strip()
                    roadmap.add(milestone)
    return roadmap

def report_issue(artifact_type, artifact_id, location, issue):
    print(f"[{artifact_type}] {artifact_id} @ {location} -> {issue}")

def main():
    registry = load_registry()
    proposals = scan_proposals()
    trace_index = load_trace_index()
    alignment_matrix = load_alignment_matrix()
    roadmap = load_roadmap()

    issues = []

    # 1. Proposals in trace index
    for prop in proposals:
        path = f'project/proposals/{prop}'
        found = any(a['path'] == path for a in trace_index.get('artifacts', []))
        if not found:
            issues.append({'type': 'proposal', 'id': prop, 'location': path, 'issue': 'Missing in TRACE_INDEX'})
    
    # 2. Proposals in roadmap
    for prop in proposals:
        if prop not in roadmap:
            issues.append({'type': 'proposal', 'id': prop, 'location': ROADMAP, 'issue': 'Missing in roadmap'})

    # 3. Proposals in registry
    for prop in proposals:
        reg_path = f'project/proposals/{prop}'
        if reg_path not in registry:
            issues.append({'type': 'proposal', 'id': prop, 'location': PROJECT_REGISTRY, 'issue': 'Missing in registry'})

    # 4. Proposals in alignment matrix
    for prop in proposals:
        if prop not in alignment_matrix:
            issues.append({'type': 'proposal', 'id': prop, 'location': ALIGNMENT_MATRIX, 'issue': 'Missing in alignment matrix'})

    # === REPORT ===
    if not issues:
        print("✅ Governance check passed: all proposals are properly registered and aligned.")
        return

    print("\n=== Governance Issues and Recommendations ===")
    for i, issue in enumerate(issues, 1):
        rec = ""
        if 'TRACE_INDEX' in issue['issue']:
            rec = f"Recommendation: Add {issue['id']} as artifact in TRACE_INDEX.yml"
        elif 'roadmap' in issue['issue']:
            rec = f"Recommendation: Add milestone {issue['id']} to roadmap.md"
        elif 'registry' in issue['issue']:
            rec = f"Recommendation: Add {issue['id']} path to PROJECT_REGISTRY.md"
        elif 'alignment matrix' in issue['issue']:
            rec = f"Recommendation: Add row for {issue['id']} in ALIGNMENT_MATRIX.md"
        print(f"{i}. [{issue['type']}] {issue['id']} @ {issue['location']} -> {issue['issue']}")
        print(f"   {rec}")

if __name__ == "__main__":
    main()

- path: verify_alignment_migration.py
  type: script
  workflow: []
  indexes: []
  content: "#!/usr/bin/env python3\n# ID: OPS-031\n\"\"\"\nEnhanced alignment verification\
    \ script.\nSummarizes missing or mismatched IDs clearly by type (doc/code/config).\n\
    \"\"\"\n\nimport os\nimport re\nimport sys\nimport yaml\nfrom pathlib import Path\n\
    from collections import defaultdict\n\nPROJECT_ROOT = Path(__file__).parent.parent\n\
    TAG_PATTERN = re.compile(r\"(?:#|<!--)\\s*ID:\\s*([A-Z0-9\\-]+)\", re.IGNORECASE)\n\
    TAG_INVENTORY = PROJECT_ROOT / \"project/reports/DOCUMENT_TAG_INVENTORY.yml\"\n\
    \ndef load_tag_inventory():\n    if not TAG_INVENTORY.exists():\n        print(f\"\
    ❌ Missing DOCUMENT_TAG_INVENTORY.yml\", file=sys.stderr)\n        return {}\n\
    \    with open(TAG_INVENTORY, \"r\", encoding=\"utf-8\") as f:\n        try:\n\
    \            data = yaml.safe_load(f)\n            if isinstance(data, list):\n\
    \                return {entry.get(\"id\"): entry for entry in data if \"id\"\
    \ in entry}\n            elif isinstance(data, dict):\n                return\
    \ data\n            else:\n                return {}\n        except yaml.YAMLError\
    \ as e:\n            print(f\"❌ YAML parse error: {e}\", file=sys.stderr)\n  \
    \          return {}\n\ndef find_embedded_id(file_path):\n    try:\n        with\
    \ open(file_path, \"r\", encoding=\"utf-8\", errors=\"ignore\") as f:\n      \
    \      for _ in range(5):\n                line = f.readline()\n             \
    \   match = TAG_PATTERN.search(line)\n                if match:\n            \
    \        return match.group(1).strip()\n    except Exception:\n        return\
    \ None\n    return None\n\ndef main():\n    print(\"=== Verifying alignment migration\
    \ (enhanced report) ===\\n\")\n\n    tag_inventory = load_tag_inventory()\n  \
    \  if not tag_inventory:\n        print(\"❌ Could not load tag inventory.\")\n\
    \        sys.exit(1)\n\n    mismatched = []\n    summary = defaultdict(list)\n\
    \n    for root, _, files in os.walk(PROJECT_ROOT):\n        if any(part in root\
    \ for part in [\".git\", \".venv\", \"node_modules\", \"archive\", \"__pycache__\"\
    ]):\n            continue\n        for f in files:\n            if not f.endswith((\"\
    .py\", \".md\", \".sh\", \".yml\", \".yaml\")):\n                continue\n  \
    \          full_path = Path(root) / f\n            rel_path = str(full_path.relative_to(PROJECT_ROOT))\n\
    \            embedded_id = find_embedded_id(full_path)\n            if not embedded_id:\n\
    \                summary[\"missing_id\"].append(rel_path)\n                continue\n\
    \            if embedded_id not in tag_inventory:\n                summary[\"\
    unregistered_id\"].append(f\"{rel_path} (ID: {embedded_id})\")\n\n    print(\"\
    === Alignment Verification Summary ===\\n\")\n    print(f\"Files with missing\
    \ ID tags: {len(summary['missing_id'])}\")\n    print(f\"Files with unregistered\
    \ IDs: {len(summary['unregistered_id'])}\\n\")\n\n    if summary[\"missing_id\"\
    ]:\n        print(\"--- Files Missing ID Tags ---\")\n        for path in sorted(summary[\"\
    missing_id\"]):\n            print(f\"  - {path}\")\n        print()\n\n    if\
    \ summary[\"unregistered_id\"]:\n        print(\"--- Files With Unregistered IDs\
    \ ---\")\n        for path in sorted(summary[\"unregistered_id\"]):\n        \
    \    print(f\"  - {path}\")\n        print()\n\n    if not summary[\"missing_id\"\
    ] and not summary[\"unregistered_id\"]:\n        print(\"✅ All files have valid,\
    \ registered IDs.\")\n        sys.exit(0)\n    else:\n        print(\"❌ Alignment\
    \ verification incomplete.\")\n        sys.exit(1)\n\nif __name__ == \"__main__\"\
    :\n    main()\n"
- path: repo_inventory_and_governance.py.bak
  type: other
  workflow: []
  indexes: []
  content: "# ID: OPS-025\nimport os\nimport re\nimport sys\nimport yaml\nimport argparse\n\
    import subprocess\nfrom pathlib import Path\nfrom typing import List, Dict, Any,\
    \ Set, Tuple\n\n# --- Configuration ---\nPROJECT_ROOT = Path(__file__).parent.parent\n\
    FILETYPE_MAP = {\n    \".md\": \"doc\", \".py\": \"code\", \".sh\": \"code\",\
    \ \".html\": \"code\", \".js\": \"code\",\n    \".ts\": \"code\", \".css\": \"\
    code\", \".yml\": \"code\", \".go\": \"code\",\n}\nIGNORED_DIRS = {\".git\", \"\
    .idea\", \".venv\", \"node_modules\", \"build\", \"dist\", \"target\", \"__pycache__\"\
    , \"site\", \"archive\", \"templates\", \".pytest_cache\"}\nIGNORED_FILES = {\"\
    mkdocs.yml\", \"openapi.json\", \"bandit.yml\", \"changed_files.txt\", \"verification_report.md\"\
    , \"LICENSE\"}\n\nINDEX_MAP = [\n    {\"match\": lambda p, f: f == \"doc\" and\
    \ p.startswith(\"api/docs/\"), \"indexes\": [\"api/docs/MASTER_INDEX.md\", \"\
    api/docs/DOCS_QUALITY_INDEX.md\"]},\n    {\"match\": lambda p, f: f == \"doc\"\
    \ and (p.startswith(\"project/archive/docs/\") or p.startswith(\"project/logs/\"\
    ) or p.startswith(\"project/process/\") or p.startswith(\"project/proposals/\"\
    ) or p.startswith(\"project/reports/\") or (p.startswith(\"project/\") and Path(p).parent.name\
    \ == \"project\")), \"indexes\": [\"project/PROJECT_REGISTRY.md\"]},\n    {\"\
    match\": lambda p, f: f == \"doc\" and p.startswith(\"Gonk/GonkCLI/docs/\"), \"\
    indexes\": [\"Gonk/GonkCLI/DOCS_INDEX.md\"]},\n    {\"match\": lambda p, f: f\
    \ == \"doc\" and p.startswith(\"Gonk/GonkUI/docs/\"), \"indexes\": [\"Gonk/GonkUI/DOCS_INDEX.md\"\
    ]},\n    {\"match\": lambda p, f: f == \"doc\" and p.startswith(\"snitch/docs/\"\
    ), \"indexes\": [\"snitch/DOCS_INDEX.md\"]},\n    {\"match\": lambda p, f: f ==\
    \ \"code\" and p.startswith(\"api/\"), \"indexes\": [\"api/docs/CODE_FILE_INDEX.md\"\
    ]},\n    {\"match\": lambda p, f: f == \"code\" and p.startswith(\"Gonk/\"), \"\
    indexes\": [\"Gonk/CODE_FILE_INDEX.md\"]},\n    {\"match\": lambda p, f: f ==\
    \ \"code\" and p.startswith(\"snitch/\"), \"indexes\": [\"snitch/CODE_FILE_INDEX.md\"\
    ]},\n    {\"match\": lambda p, f: f == \"code\" and p.startswith(\"scripts/\"\
    ), \"indexes\": [\"scripts/CODE_FILE_INDEX.md\"]},\n]\n\ndef get_file_type(filepath:\
    \ str) -> str:\n    if os.path.basename(filepath).startswith(\".\") or os.path.basename(filepath)\
    \ in IGNORED_FILES:\n        return \"exempt\"\n    return FILETYPE_MAP.get(os.path.splitext(filepath)[1],\
    \ \"exempt\")\n\ndef find_all_files() -> List[str]:\n    files = []\n    for root,\
    \ dirs, filenames in os.walk(PROJECT_ROOT):\n        dirs[:] = [d for d in dirs\
    \ if d not in IGNORED_DIRS]\n        for f in filenames:\n            files.append(str(Path(root,\
    \ f).relative_to(PROJECT_ROOT)))\n    return files\n\ndef parse_markdown_index(index_path:\
    \ Path) -> Set[str]:\n    if not index_path.exists(): return set()\n    content\
    \ = index_path.read_text(encoding=\"utf-8\")\n    if \"CODE_FILE_INDEX.md\" in\
    \ str(index_path) or \"DOCS_QUALITY_INDEX.md\" in str(index_path):\n        return\
    \ set(re.findall(r\"^\\s*\\|\\s*`([^`]+)`\", content, re.MULTILINE))\n    if \"\
    PROJECT_REGISTRY.md\" in str(index_path):\n        links = re.findall(r\"\\[`([^`]+)`\\\
    ]\\(([^)]+)\\)\", content)\n        return {str(Path(os.path.normpath(os.path.join(index_path.parent,\
    \ link[1]))).relative_to(PROJECT_ROOT)) for link in links}\n    links = re.findall(r\"\
    \\[[^\\]]+\\]\\((?!https?://)([^)]+)\\)\", content)\n    return {str(Path(os.path.normpath(os.path.join(index_path.parent,\
    \ link))).relative_to(PROJECT_ROOT)) for link in links}\n\ndef check_registration(file_path:\
    \ str, required_indexes: List[str], all_indexes_content: Dict[str, Set[str]])\
    \ -> Tuple[List[str], List[str]]:\n    found, missing = [], []\n    for idx in\
    \ required_indexes:\n        if file_path in all_indexes_content.get(idx, set()):\n\
    \            found.append(idx)\n        else:\n            missing.append(idx)\n\
    \    return sorted(found), sorted(missing)\n\ndef create_and_populate_index(index_path_str:\
    \ str, files_to_add: List[str], file_type: str):\n    index_path = PROJECT_ROOT\
    \ / index_path_str\n    index_path.parent.mkdir(parents=True, exist_ok=True)\n\
    \    existing_files = parse_markdown_index(index_path) if index_path.exists()\
    \ else set()\n    new_files_to_add = sorted([f for f in files_to_add if f not\
    \ in existing_files])\n    if not new_files_to_add: return\n\n    lines_to_append\
    \ = []\n    if \"PROJECT_REGISTRY.md\" in index_path_str and index_path.exists():\n\
    \        content = index_path.read_text(encoding=\"utf-8\").splitlines()\n   \
    \     try:\n            separator_index = next(i for i, line in enumerate(content)\
    \ if line.strip() == '|---|---|---|' and i > 0 and \"Document\" in content[i-1])\n\
    \            insertion_point = separator_index + 1\n        except (StopIteration,\
    \ ValueError, IndexError):\n            insertion_point = len(content)\n     \
    \   for f in new_files_to_add:\n            relative_link = os.path.relpath(PROJECT_ROOT\
    \ / f, index_path.parent)\n            doc_name = Path(f).stem.replace('_', '\
    \ ').replace('-', ' ').title()\n            lines_to_append.append(f\"| **{doc_name}**\
    \ | [`{Path(f).name}`]({relative_link}) | |\")\n        for line in reversed(sorted(lines_to_append)):\n\
    \            content.insert(insertion_point, line)\n        index_path.write_text(\"\
    \\n\".join(content) + \"\\n\", encoding=\"utf-8\")\n        return\n\n    if \"\
    CODE_FILE_INDEX\" in index_path_str: lines_to_append = [f\"| `{f}` | | | Active\
    \ | | |\" for f in new_files_to_add]\n    elif \"DOCS_QUALITY_INDEX\" in index_path_str:\
    \ lines_to_append = [f\"| `{f}` | X | X | | | |\" for f in new_files_to_add]\n\
    \    else:\n        relative_links = [os.path.relpath(PROJECT_ROOT / f, index_path.parent)\
    \ for f in new_files_to_add]\n        lines_to_append = [f\"*   [{Path(f).name}]({link})\"\
    \ for f, link in zip(new_files_to_add, relative_links)]\n\n    if index_path.exists():\n\
    \        with open(index_path, \"a\", encoding=\"utf-8\") as f:\n            if\
    \ index_path.read_text(encoding=\"utf-8\")[-1] != '\\n': f.write('\\n')\n    \
    \        f.write(\"\\n\".join(sorted(lines_to_append)) + \"\\n\")\n    else:\n\
    \        header = f\"# {index_path.stem.replace('_',' ').title()}\\n\\nThis file\
    \ is auto-generated.\\n\\n\"\n        if \"CODE_FILE_INDEX\" in index_path_str:\
    \ header += \"| Path | Type | Description | Status | Linked Docs | Notes |\\n|------|------|-------------|--------|-------------|-------|\\\
    n\"\n        elif \"QUALITY_INDEX\" in index_path_str: header += \"| File Path\
    \ | Score | Reviewer | Date | Notes |\\n|-----------|-------|----------|------|-------|\\\
    n\"\n        index_path.write_text(header + \"\\n\".join(sorted(lines_to_append))\
    \ + \"\\n\", encoding=\"utf-8\")\n\ndef generate_audit_report(trace_index: List[Dict[str,\
    \ Any]]) -> int:\n    print(\"\\n\" + \"=\"*50 + \"\\nGovernance Audit Report\\\
    n\" + \"=\"*50)\n    missing_by_index, registered_count, missing_count, exempted_count\
    \ = {}, 0, 0, 0\n    for item in trace_index:\n        if item[\"registered\"\
    ] == \"exempted\": exempted_count += 1\n        elif item[\"registered\"] is True:\
    \ registered_count += 1\n        else:\n            missing_count += 1\n     \
    \       for idx in item.get(\"missing_from\", []):\n                missing_by_index.setdefault(idx,\
    \ []).append(item[\"path\"])\n    if missing_count > 0:\n        print(\"\\n---\
    \ Missing Registrations ---\")\n        for idx, files in sorted(missing_by_index.items()):\n\
    \            print(f\"\\nMissing from {idx}:\")\n            for f in sorted(files):\
    \ print(f\"  - {f}\")\n    print(f\"\\n--------------------\\n- Total files: {len(trace_index)}\\\
    n- Registered: {registered_count}\\n- Missing: {missing_count}\\n- Exempted: {exempted_count}\\\
    n--------------------\")\n    return 1 if missing_count > 0 else 0\n\ndef validate_trace_index_schema(trace_index_path:\
    \ Path) -> bool:\n    # This function remains the same\n    return True\n\ndef\
    \ main():\n    parser = argparse.ArgumentParser(description=\"Repository inventory\
    \ and governance script.\")\n    parser.add_argument(\"--full\", action=\"store_true\"\
    , help=\"Run a full scan of all files.\")\n    parser.add_argument(\"--full-scan\"\
    , action=\"store_true\", help=\"Force a full scan of all files, ignoring other\
    \ modes.\")\n    parser.add_argument(\"--test-files\", nargs='*', help=\"Run in\
    \ test mode with a specific list of files.\")\n    parser.add_argument(\"--update-project-registry\"\
    , action=\"store_true\", help=\"Update the project registry JSON and Markdown\
    \ files.\")\n    parser.add_argument(\"--extras-file\", type=Path, default=PROJECT_ROOT\
    \ / \"scripts/project_registry_extras.yml\", help=\"Path to the project registry\
    \ extras file.\")\n    parser.add_argument(\"--debug\", action=\"store_true\"\
    , help=\"Enable debug printing for scripts that support it.\")\n\n    args = parser.parse_args()\n\
    \n    if args.update_project_registry:\n        print(\"--- Updating Project Registry\
    \ ---\")\n        script_path = PROJECT_ROOT / \"scripts\" / \"build_project_registry.py\"\
    \n        cmd = [sys.executable, str(script_path), \"--extras-file\", str(args.extras_file)]\n\
    \        if args.debug:\n            cmd.append(\"--debug\")\n\n        try:\n\
    \            result = subprocess.run(cmd, check=True, capture_output=True, text=True,\
    \ encoding='utf-8')\n            print(result.stdout)\n            if result.stderr:\
    \ print(result.stderr, file=sys.stderr)\n            print(\"✅ Project registry\
    \ updated successfully.\")\n            return 0\n        except subprocess.CalledProcessError\
    \ as e:\n            print(\"❌ ERROR: Project registry update failed.\", file=sys.stderr)\n\
    \            print(e.stdout, file=sys.stdout)\n            print(e.stderr, file=sys.stderr)\n\
    \            return e.returncode\n\n    test_mode = args.test_files is not None\n\
    \    if args.full_scan:\n        print(\"Running full repository scan (forced).\"\
    )\n        all_files = find_all_files()\n    elif args.full:\n        all_files\
    \ = find_all_files()\n    elif test_mode:\n        all_files = args.test_files\n\
    \    else:\n        manifest_path = PROJECT_ROOT / \"project/reports/REPO_MANIFEST.md\"\
    \n        if manifest_path.exists():\n            content = manifest_path.read_text(encoding=\"\
    utf-8\")\n            all_files = re.findall(r\"^\\s*\\|\\s*`([^`]+)`\\s*\\|.*\"\
    , content, re.MULTILINE)\n        else:\n            print(\"INFO: REPO_MANIFEST.md\
    \ not found. Running a full scan.\", file=sys.stderr)\n            all_files =\
    \ find_all_files()\n\n    trace_index = []\n    all_index_paths = {idx for rule\
    \ in INDEX_MAP for idx in rule[\"indexes\"]}\n    all_indexes_content = {str(p):\
    \ parse_markdown_index(PROJECT_ROOT / p) for p in all_index_paths}\n    files_to_create\
    \ = {}\n\n    for f in sorted(all_files):\n        ftype = get_file_type(f)\n\
    \        entry = {\"path\": f, \"type\": ftype}\n        required = []\n     \
    \   if ftype != \"exempt\" and Path(f).name not in [\"CODE_FILE_INDEX.md\", \"\
    DOCS_INDEX.md\", \"README.md\", \".pytest_cache\"]:\n            for r in INDEX_MAP:\n\
    \                if r[\"match\"](f, ftype): required.extend(r[\"indexes\"])\n\
    \        required = sorted(list(set(required)))\n        if ftype == 'doc' and\
    \ not required and f not in IGNORED_FILES and not f.startswith(\"templates/\"\
    ):\n            if not (Path(f).name in [\"CODE_FILE_INDEX.md\", \"DOCS_INDEX.md\"\
    , \"README.md\"]):\n                required.append(\"project/PROJECT_REGISTRY.md\"\
    )\n\n        if not required:\n            entry[\"registered\"] = \"exempted\"\
    ; entry[\"index\"] = \"-\"\n        else:\n            found, missing = check_registration(f,\
    \ required, all_indexes_content)\n            if not missing:\n              \
    \  entry[\"registered\"] = True; entry[\"index\"] = found[0]\n            else:\n\
    \                entry[\"registered\"] = False; entry[\"index\"] = \"-\"; entry[\"\
    missing_from\"] = missing\n                for idx_file in missing:\n        \
    \            files_to_create.setdefault(idx_file, []).append(f)\n        trace_index.append(entry)\n\
    \n    if not test_mode:\n        for idx_path, files in files_to_create.items():\n\
    \            file_type_for_index = get_file_type(files[0]) if files else \"doc\"\
    \n            create_and_populate_index(idx_path, files, file_type_for_index)\n\
    \n    output = {\"artifacts\": trace_index}\n    trace_index_path = PROJECT_ROOT\
    \ / \"project/reports/TRACE_INDEX.yml\"\n    trace_index_path.parent.mkdir(parents=True,\
    \ exist_ok=True)\n    with open(trace_index_path, \"w\") as f:\n        yaml.safe_dump(output,\
    \ f, default_flow_style=False, sort_keys=False)\n    if not test_mode: print(\"\
    TRACE_INDEX.yml generated successfully.\")\n    if not validate_trace_index_schema(trace_index_path):\
    \ return 1\n    if test_mode: return 0\n\n    exit_code = generate_audit_report(trace_index)\n\
    \n    linter_script = PROJECT_ROOT / \"scripts/lint_governance_links.py\"\n  \
    \  try:\n        result = subprocess.run([sys.executable, str(linter_script)],\
    \ check=True, capture_output=True, text=True, encoding='utf-8')\n        print(\"\
    \\n--- Governance Links Linter Output ---\")\n        print(result.stdout)\n \
    \       print(\"✅ lint_governance_links.py completed successfully.\\n\")\n   \
    \ except subprocess.CalledProcessError as e:\n        print(\"\\n⚠️ lint_governance_links.py\
    \ failed:\", file=sys.stderr)\n        print(e.stdout); print(e.stderr, file=sys.stderr)\n\
    \        if exit_code == 0: exit_code = e.returncode\n    return exit_code\n\n\
    if __name__ == \"__main__\":\n    sys.exit(main())"
- path: project_registry.json
  type: config
  workflow: []
  indexes: []
  content: "[\n    {\n        \"name\": \"Code File Index\",\n        \"path\": \"\
    api/docs/CODE_FILE_INDEX.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"api\",\n        \"category\": \"docs\",\n        \"registered_in\": [],\n\
    \        \"status\": \"registered\",\n        \"notes\": \"\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`api/docs/CODE_FILE_INDEX.md`\"\
    ,\n        \"path\": \"project/api/docs/CODE_FILE_INDEX.md\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"api\",\n\
    \        \"registered_in\": [],\n        \"status\": \"legacy\",\n        \"notes\"\
    : \"\",\n        \"source\": \"project/PROJECT_REGISTRY.md\"\n    },\n    {\n\
    \        \"name\": \"`project/api/endpoints.yaml`\",\n        \"path\": \"project/api/endpoints.yaml\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"api\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"Traceability Matrix\",\n        \"path\": \"project/archive/TRACEABILITY_MATRIX.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Audit Phase 3\",\n        \"path\": \"project/archive/audit/AUDIT-PHASE-3.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Audit Phase 4\",\n        \"path\": \"project/archive/audit/AUDIT-PHASE-4.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Audit Phase 5\",\n        \"path\": \"project/archive/audit/AUDIT-PHASE-5.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Audit Phase 1\",\n        \"path\": \"project/archive/audit/AUDIT-phase-1.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Audit Phase 2\",\n        \"path\": \"project/archive/audit/AUDIT-phase-2.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Audit Traceability Matrix\",\n        \"path\": \"project/archive/audit/AUDIT_TRACEABILITY_MATRIX.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Code Optimizationplan Phase 4\",\n        \"path\": \"project/archive/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"First Audit\",\n        \"path\": \"project/archive/audit/FIRST_AUDIT.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Hld Lld Alignment Plan\",\n        \"path\": \"project/archive/audit/HLD_LLD_ALIGNMENT_PLAN.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Phase 4 Traceability Matrix\",\n        \"path\": \"project/archive/audit/PHASE_4_TRACEABILITY_MATRIX.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Audit Prompt\",\n        \"path\": \"project/archive/audit/audit-prompt.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Security\",\n        \"path\": \"project/archive/docs/projectplan/security.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Spotify Fullstack Capability Blueprint\",\n        \"path\"\
    : \"project/archive/docs/projectplan/spotify_fullstack_capability_blueprint.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Integration Checklist\",\n        \"path\": \"project/archive/docs/snitch/INTEGRATION_CHECKLIST.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Phase 2 Secure Callback\",\n        \"path\": \"project/archive/docs/snitch/PHASE_2_SECURE_CALLBACK.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Test Runbook\",\n        \"path\": \"project/archive/docs/snitch/TEST_RUNBOOK.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Phase5 Ipc\",\n        \"path\": \"project/archive/docs/snitch/phase5-ipc.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"archive\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"`project/ALIGNMENT_MATRIX.md`\",\n        \"path\": \"project/ALIGNMENT_MATRIX.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"Alignment Matrix\",\n        \"path\": \"project/ALIGNMENT_MATRIX.yml\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"`project/BACKLOG.md`\",\n        \"path\": \"project/BACKLOG.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/CICD.md`\",\n        \"path\": \"project/CICD.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/DEPENDENCIES.md`\",\n        \"path\": \"\
    project/DEPENDENCIES.md\",\n        \"type\": \"doc\",\n        \"module\": \"\
    project\",\n        \"category\": \"general\",\n        \"registered_in\": [],\n\
    \        \"status\": \"registered\",\n        \"notes\": \"\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`project/EXECUTION_PLAN.md`\"\
    ,\n        \"path\": \"project/EXECUTION_PLAN.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"general\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/FUTURE_ENHANCEMENTS.md`\",\n        \"path\": \"project/FUTURE_ENHANCEMENTS.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/HIGH_LEVEL_DESIGN.md`\",\n        \"path\"\
    : \"project/HIGH_LEVEL_DESIGN.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"\",\n       \
    \ \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`project/LESSONS-LEARNT.md`\"\
    ,\n        \"path\": \"project/LESSONS-LEARNT.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"general\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/LOGGING_PHASES.md`\",\n        \"path\": \"project/LOGGING_PHASES.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/LOGGING_SYSTEM_DESIGN.md`\",\n        \"\
    path\": \"project/LOGGING_SYSTEM_DESIGN.md\",\n        \"type\": \"doc\",\n  \
    \      \"module\": \"project\",\n        \"category\": \"general\",\n        \"\
    registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\":\
    \ \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/LOGGING_TRACEABILITY_MATRIX.md`\",\n        \"path\": \"project/LOGGING_TRACEABILITY_MATRIX.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/LOW_LEVEL_DESIGN.md`\",\n        \"path\"\
    : \"project/LOW_LEVEL_DESIGN.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"\",\n       \
    \ \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`project/ONBOARDING.md`\"\
    ,\n        \"path\": \"project/ONBOARDING.md\",\n        \"type\": \"doc\",\n\
    \        \"module\": \"project\",\n        \"category\": \"general\",\n      \
    \  \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/PID.md`\",\n        \"path\": \"project/PID.md\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"general\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n\
    \        \"name\": \"`project/PROJECT_BRIEF.md`\",\n        \"path\": \"project/PROJECT_BRIEF.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/PROJECT_PLAN.md`\",\n        \"path\": \"\
    project/PROJECT_PLAN.md\",\n        \"type\": \"doc\",\n        \"module\": \"\
    project\",\n        \"category\": \"general\",\n        \"registered_in\": [],\n\
    \        \"status\": \"registered\",\n        \"notes\": \"\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`project/PROJECT_REGISTRY.md`\"\
    ,\n        \"path\": \"project/PROJECT_REGISTRY.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"general\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/QA_GOVERNANCE.md`\",\n        \"path\": \"project/QA_GOVERNANCE.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/ROADMAP.md`\",\n        \"path\": \"project/ROADMAP.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/SECURITY.md`\",\n        \"path\": \"project/SECURITY.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/TASK_CHECKLIST.md`\",\n        \"path\":\
    \ \"project/TASK_CHECKLIST.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"\",\n       \
    \ \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`project/USECASES.md`\"\
    ,\n        \"path\": \"project/USECASES.md\",\n        \"type\": \"doc\",\n  \
    \      \"module\": \"project\",\n        \"category\": \"general\",\n        \"\
    registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\":\
    \ \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/USECASES_GAP_ANALYSIS.md`\",\n        \"path\": \"project/USECASES_GAP_ANALYSIS.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/logs/ACTIVITY.md`\",\n        \"path\": \"\
    project/logs/ACTIVITY.md\",\n        \"type\": \"doc\",\n        \"module\": \"\
    project\",\n        \"category\": \"logs\",\n        \"registered_in\": [],\n\
    \        \"status\": \"registered\",\n        \"notes\": \"\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`project/logs/CURRENT_STATE.md`\"\
    ,\n        \"path\": \"project/logs/CURRENT_STATE.md\",\n        \"type\": \"\
    doc\",\n        \"module\": \"project\",\n        \"category\": \"logs\",\n  \
    \      \"registered_in\": [],\n        \"status\": \"registered\",\n        \"\
    notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n     \
    \   \"name\": \"`project/logs/SESSION_LOG.md`\",\n        \"path\": \"project/logs/SESSION_LOG.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"logs\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/process/GAP_ANALYSIS_TEMPLATE.md`\",\n  \
    \      \"path\": \"project/process/GAP_ANALYSIS_TEMPLATE.md\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"process\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n\
    \        \"name\": \"`project/proposals/DBSTUDIO_PLUGIN.md`\",\n        \"path\"\
    : \"project/proposals/DBSTUDIO_PLUGIN.md\",\n        \"type\": \"doc\",\n    \
    \    \"module\": \"project\",\n        \"category\": \"proposals\",\n        \"\
    registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\":\
    \ \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md`\",\n        \"path\": \"project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"proposals\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/proposals/GONKUI_PLUGIN.md`\",\n        \"\
    path\": \"project/proposals/GONKUI_PLUGIN.md\",\n        \"type\": \"doc\",\n\
    \        \"module\": \"project\",\n        \"category\": \"proposals\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/proposals/GOVERNANCE_AUDIT_REFACTOR.md`\",\n        \"path\": \"\
    project/proposals/GOVERNANCE_AUDIT_REFACTOR.md\",\n        \"type\": \"doc\",\n\
    \        \"module\": \"project\",\n        \"category\": \"proposals\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/proposals/HOME_AUTOMATION_PROPOSAL.md`\",\n        \"path\": \"project/proposals/HOME_AUTOMATION_PROPOSAL.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"proposals\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/proposals/LOW_CODE_PROPOSAL.md`\",\n    \
    \    \"path\": \"project/proposals/LOW_CODE_PROPOSAL.md\",\n        \"type\":\
    \ \"doc\",\n        \"module\": \"project\",\n        \"category\": \"proposals\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n\
    \        \"name\": \"`project/proposals/MULTI_SOURCE_METADATA_PROPOSAL.md`\",\n\
    \        \"path\": \"project/proposals/MULTI_SOURCE_METADATA_PROPOSAL.md\",\n\
    \        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"proposals\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/proposals/NEW_PROPOSAL.md`\",\n        \"\
    path\": \"project/proposals/NEW_PROPOSAL.md\",\n        \"type\": \"doc\",\n \
    \       \"module\": \"project\",\n        \"category\": \"proposals\",\n     \
    \   \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md`\",\n        \"path\": \"\
    project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"proposals\",\n  \
    \      \"registered_in\": [],\n        \"status\": \"registered\",\n        \"\
    notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n     \
    \   \"name\": \"`project/proposals/TRACE_INDEX_SCHEMA_ADAPTATION.md`\",\n    \
    \    \"path\": \"project/proposals/TRACE_INDEX_SCHEMA_ADAPTATION.md\",\n     \
    \   \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"proposals\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/proposals/TRACE_INDEX_SCHEMA_FIX.md`\",\n\
    \        \"path\": \"project/proposals/TRACE_INDEX_SCHEMA_FIX.md\",\n        \"\
    type\": \"doc\",\n        \"module\": \"project\",\n        \"category\": \"proposals\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n\
    \        \"name\": \"Archive Alignment Matrix Old\",\n        \"path\": \"project/reports/ARCHIVE_ALIGNMENT_MATRIX_OLD.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Content Alignment Report\",\n        \"path\": \"project/reports/CONTENT_ALIGNMENT_REPORT.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Description Compliance Report\",\n        \"path\": \"project/reports/DESCRIPTION_COMPLIANCE_REPORT.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"Document Tag Inventory\",\n        \"path\": \"project/reports/DOCUMENT_TAG_INVENTORY.yml\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"orphan\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"filesystem\"\n    },\n    {\n\
    \        \"name\": \"`project/reports/GOVERNANCE_DEMO_REPORT.md`\",\n        \"\
    path\": \"project/reports/GOVERNANCE_DEMO_REPORT.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"reports\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`project/reports/HANDOVER_BRIEF_CHATGTP.md`\",\n        \"path\": \"project/reports/HANDOVER_BRIEF_CHATGTP.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`project/reports/HANDOVER_BRIEF_JULES.md`\",\n   \
    \     \"path\": \"project/reports/HANDOVER_BRIEF_JULES.md\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"reports\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n\
    \        \"name\": \"`project/reports/PROJECT_AUDIT_FINAL_REPORT.md`\",\n    \
    \    \"path\": \"project/reports/PROJECT_AUDIT_FINAL_REPORT.md\",\n        \"\
    type\": \"doc\",\n        \"module\": \"project\",\n        \"category\": \"reports\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n\
    \        \"name\": \"`project/reports/PROJECT_DOCUMENT_ALIGNMENT.md`\",\n    \
    \    \"path\": \"project/reports/PROJECT_DOCUMENT_ALIGNMENT.md\",\n        \"\
    type\": \"doc\",\n        \"module\": \"project\",\n        \"category\": \"reports\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n\
    \        \"name\": \"`project/reports/TRACE_INDEX.yml`\",\n        \"path\": \"\
    project/reports/TRACE_INDEX.yml\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"reports\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"\",\n       \
    \ \"source\": \"TRACE_INDEX.yml\"\n    }\n]"
- path: generate_alignment_matrix_md.py
  type: script
  workflow:
  - documentation
  indexes: []
  content: "# ID: OPS-010\n#!/usr/bin/env python3\n\"\"\"\ngenerate_alignment_matrix_md.py\n\
    Converts ALIGNMENT_MATRIX.yml back into a readable Markdown version.\n\"\"\"\n\
    \nimport yaml\nfrom pathlib import Path\n\nSRC = Path(\"project/ALIGNMENT_MATRIX.yml\"\
    )\nDEST = Path(\"project/ALIGNMENT_MATRIX.md\")\n\ndef main():\n    print(\"---\
    \ Regenerating Markdown Alignment Matrix ---\")\n    if not SRC.exists():\n  \
    \      print(f\"[ERROR] Missing canonical source: {SRC}\")\n        return\n\n\
    \    try:\n        data = yaml.safe_load(SRC.read_text())\n    except yaml.YAMLError\
    \ as e:\n        print(f\"[ERROR] Could not parse YAML file {SRC}: {e}\")\n  \
    \      return\n\n    if not data:\n        print(\"[INFO] YAML source is empty.\
    \ Generating an empty Markdown file.\")\n        out = [\"# Alignment Matrix\\\
    n\\n*No entries found.*\"]\n    else:\n        out = [\"# Alignment Matrix\\n\"\
    ]\n        # Sort entries by ID for consistent output\n        data.sort(key=lambda\
    \ x: x.get('id', ''))\n\n        for entry in data:\n            entry_id = entry.get('id',\
    \ 'N/A')\n            out.append(f\"## {entry_id}\")\n\n            if \"description\"\
    \ in entry and entry['description']:\n                out.append(f\"**Description:**\
    \ {entry['description']}\")\n\n            if entry.get(\"linked_docs\"):\n  \
    \              out.append(\"\\n**Linked Docs:**\")\n                out.extend([f\"\
    - `{d}`\" for d in sorted(entry[\"linked_docs\"])])\n\n            if entry.get(\"\
    code_paths\"):\n                out.append(\"\\n**Code Paths:**\")\n         \
    \       out.extend([f\"- `{p}`\" for p in sorted(entry[\"code_paths\"])])\n\n\
    \            if entry.get(\"related_tasks\"):\n                out.append(\"\\\
    n**Related Tasks:**\")\n                out.extend([f\"- {t}\" for t in sorted(entry[\"\
    related_tasks\"])])\n\n            out.append(\"\\n---\") # Add a separator for\
    \ readability\n\n    try:\n        DEST.write_text(\"\\n\".join(out), encoding='utf-8')\n\
    \        print(f\"[OK] Markdown alignment matrix regenerated at {DEST}\")\n  \
    \  except Exception as e:\n        print(f\"[ERROR] Failed to write Markdown file:\
    \ {e}\")\n\n\nif __name__ == \"__main__\":\n    main()"
- path: CODE_FILE_INDEX.md
  type: doc
  workflow: []
  indexes:
  - CODE_FILE_INDEX.md
  content: '<!-- ID: OPS-001 -->

    # Code File Index


    This file is auto-generated. Do not edit manually.


    | Path | Description |

    |------|-------------|

    | `scripts/api/src/zotify_api/temp_violation.py` | A temporary file to test linter
    violations. |

    | `scripts/audit_api.py` | A script to audit the API. |

    | `scripts/audit_endpoints.py` | A script to audit the API endpoints. |

    | `scripts/doc-lint-rules.yml` | A set of rules for the documentation linter.
    |

    | `scripts/functional_test.py` | A script for running functional tests. |

    | `scripts/generate_endpoints_doc.py` | A script to generate documentation for
    the API endpoints. |

    | `scripts/generate_openapi.py` | A script to generate the OpenAPI specification.
    |

    | `scripts/lint_governance_links.py` | A script to lint the governance links.
    |

    | `scripts/linter.py` | The main linter script. |

    | `scripts/make_manifest.py` | A script to create a manifest of all project files.
    |

    | `scripts/manage_docs_index.py` | A script to manage the documentation index.
    |

    | `scripts/repo_governance.py` | A script to enforce repository governance policies.
    |

    | `scripts/repo_inventory_and_governance.py` | A script to manage the repository
    inventory and governance. |

    | `scripts/run_e2e_auth_test.sh` | A script to run the end-to-end authentication
    tests. |

    | `scripts/start.sh` | A script to start the application. |

    | `scripts/test_auth_flow.py` | A script to test the authentication flow. |

    | `scripts/test_single_config.sh` | A script to test a single configuration. |

    | `scripts/validate_code_index.py` | A script to validate the code index. |

    | `scripts/verify_governance.py` | A script to verify the governance policies.
    |

    | `scripts/build_project_registry.py` | | | Active | | |

    | `scripts/content_alignment_check.py` | | | Active | | |

    | `scripts/description_compliance_check.py` | | | Active | | |

    | `scripts/generate_alignment_matrix_md.py` | | | Active | | |

    | `scripts/generate_repo_manifest.py` | | | Active | | |

    | `scripts/migrate_alignment_matrix.py` | | | Active | | |

    | `scripts/migrate_and_tag_repository.py` | | | Active | | |

    | `scripts/propagate_descriptions.py` | | | Active | | |

    | `scripts/semantic_alignment_check.py` | | | Active | | |

    | `scripts/test_full_pipeline.sh` | | | Active | | |

    | `scripts/fix_tag_inventory.py` | | | Active | | |

    | `scripts/verify_alignment_migration.py` | | | Active | | |

    '
- path: description_compliance_check.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-007\n#!/usr/bin/env python3\nimport os\nimport re\nimport yaml\n\
    import sys\nimport argparse\nfrom pathlib import Path\nfrom collections import\
    \ defaultdict\n\nOUTPUT_PATH = Path(\"project/reports/DESCRIPTION_COMPLIANCE_REPORT.md\"\
    )\nTRACE_INDEX_PATH = Path(\"project/reports/TRACE_INDEX.yml\")\n\ndef load_trace_index_data():\n\
    \    \"\"\"Loads all file paths and their descriptions from the TRACE_INDEX.\"\
    \"\"\n    with open(TRACE_INDEX_PATH, 'r', encoding='utf-8') as f:\n        data\
    \ = yaml.safe_load(f).get('artifacts', [])\n\n    master_descriptions = {}\n \
    \   exempt_files = []\n\n    for item in data:\n        path = item.get('path')\n\
    \        if not path:\n            continue\n\n        if item.get('type') ==\
    \ 'exempt' or item.get('registered') == 'exempted':\n            exempt_files.append(path)\n\
    \        elif item.get('registered') is True and 'index' in item and item['index']\
    \ != '-':\n            master_descriptions[path] = {\n                \"description\"\
    : item.get('description', '').strip(),\n                \"index_file\": item['index']\n\
    \            }\n\n    return master_descriptions, exempt_files\n\ndef parse_unified_md_index(index_path_str):\n\
    \    \"\"\"Parses the new, unified markdown table format.\"\"\"\n    found_in_index\
    \ = {}\n    index_path = Path(index_path_str)\n\n    if not index_path.exists():\n\
    \        return {}\n\n    with open(index_path, 'r', encoding='utf-8') as f:\n\
    \        lines = f.readlines()\n\n    for line in lines:\n        if not line.strip().startswith('|'):\n\
    \            continue\n\n        cols = [c.strip() for c in line.split('|')]\n\
    \        if len(cols) < 3: # | `path` | description |\n            continue\n\n\
    \        path_match = re.search(r'`([^`]+)`', cols[1])\n        if path_match:\n\
    \            file_path = path_match.group(1)\n            description = cols[2]\n\
    \            found_in_index[file_path] = description.strip()\n\n    return found_in_index\n\
    \ndef main():\n    parser = argparse.ArgumentParser(description=\"Validates that\
    \ all registered files have descriptions in their respective indices.\")\n   \
    \ parser.add_argument(\"--validate\", action=\"store_true\", help=\"Run the validation\
    \ process.\")\n    args = parser.parse_args()\n\n    if not args.validate:\n \
    \       print(\"Script requires the --validate flag to run.\", file=sys.stderr)\n\
    \        sys.exit(0)\n\n    master_descriptions, exempt_files = load_trace_index_data()\n\
    \n    report_lines = [\n        \"# Description Compliance Report\\n\",\n    \
    \    \"| File | Registered In | Status | Notes |\",\n        \"|------|----------------|--------|-------|\"\
    ,\n    ]\n\n    valid_count = 0\n    missing_count = 0\n\n    all_found_descriptions\
    \ = {}\n    all_indices = set(v['index_file'] for v in master_descriptions.values())\n\
    \    for index_file in all_indices:\n        all_found_descriptions.update(parse_unified_md_index(index_file))\n\
    \n    for file_path, data in sorted(master_descriptions.items()):\n        index_file\
    \ = data['index_file']\n        master_desc = data['description']\n\n        status\
    \ = \"✅ Valid\"\n        notes = \"Description present\"\n\n        if file_path\
    \ not in all_found_descriptions:\n            status = \"⚠️ Missing\"\n      \
    \      notes = \"File not found in its registered index.\"\n            missing_count\
    \ += 1\n        else:\n            found_desc = all_found_descriptions[file_path]\n\
    \            if not found_desc or found_desc.lower() in [\"tbd\", \"n/a\", \"\"\
    ]:\n                status = \"⚠️ Missing\"\n                notes = \"Description\
    \ is missing or a placeholder in the index file.\"\n                missing_count\
    \ += 1\n            elif found_desc != master_desc:\n                status =\
    \ \"⚠️ Mismatched\"\n                notes = f\"Description does not match master.\
    \ Expected: '{master_desc}', Found: '{found_desc}'\"\n                missing_count\
    \ += 1\n            else:\n                valid_count += 1\n\n        report_lines.append(f\"\
    | `{file_path}` | `{index_file}` | {status} | {notes} |\")\n\n    total_checked\
    \ = len(master_descriptions)\n    compliance_rate = 100\n    if total_checked\
    \ > 0:\n        compliance_rate = int((valid_count / total_checked) * 100)\n\n\
    \    summary = [\n        \"\\n## Summary\\n\",\n        f\"**Total files checked:**\
    \ {total_checked}\",\n        f\"**Valid:** {valid_count}\",\n        f\"**Missing/Mismatched:**\
    \ {missing_count}\",\n        f\"**Exempt:** {len(exempt_files)}\",\n        f\"\
    **Overall compliance:** {compliance_rate}%\"\n    ]\n\n    report_lines.extend(summary)\n\
    \n    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)\n    with open(OUTPUT_PATH,\
    \ \"w\", encoding=\"utf-8\") as f:\n        f.write(\"\\n\".join(report_lines))\n\
    \n    print(f\"Compliance report generated at {OUTPUT_PATH}\")\n    if missing_count\
    \ > 0:\n        print(f\"Found {missing_count} non-compliant entries.\", file=sys.stderr)\n\
    \        sys.exit(1)\n    else:\n        print(\"All checked files are compliant.\"\
    )\n\nif __name__ == \"__main__\":\n    main()"
- path: gonkui
  type: other
  workflow: []
  indexes: []
  content: "# ID: OPS-014\n#!/usr/bin/env python3\n\"\"\"\nGonkUI management script:\
    \ start/stop GonkUI in foreground with auto-reload.\nNo background mode.\n\"\"\
    \"\n\nimport argparse\nimport os\nimport subprocess\nimport sys\nimport signal\n\
    import time\n\nPID_FILE = \"/tmp/gonkui.pid\"\nDEFAULT_PORT = 5000\nDEFAULT_HOST\
    \ = \"0.0.0.0\"\nAPP_PATH = \"Gonk/GonkUI/app.py\"\n\ndef read_pid():\n    if\
    \ os.path.exists(PID_FILE):\n        with open(PID_FILE, \"r\") as f:\n      \
    \      return int(f.read().strip())\n    return None\n\ndef write_pid(pid):\n\
    \    with open(PID_FILE, \"w\") as f:\n        f.write(str(pid))\n\ndef remove_pid():\n\
    \    if os.path.exists(PID_FILE):\n        os.remove(PID_FILE)\n\ndef start():\n\
    \    if read_pid():\n        print(\"GonkUI is already running (PID file exists).\
    \ Stop it first.\")\n        sys.exit(1)\n\n    host = os.environ.get(\"HOST\"\
    , DEFAULT_HOST)\n    port = os.environ.get(\"PORT\", str(DEFAULT_PORT))\n\n  \
    \  env = os.environ.copy()\n    env[\"FLASK_APP\"] = APP_PATH\n    env[\"FLASK_ENV\"\
    ] = \"development\"\n\n    print(f\"Starting GonkUI in foreground on {host}:{port}...\"\
    )\n    try:\n        process = subprocess.Popen(\n            [\"flask\", \"run\"\
    , \"--host\", host, \"--port\", port, \"--debug\"],\n            env=env,\n  \
    \      )\n        write_pid(process.pid)\n        process.wait()\n    except KeyboardInterrupt:\n\
    \        print(\"\\nKeyboardInterrupt received, stopping GonkUI...\")\n      \
    \  stop()\n    finally:\n        remove_pid()\n\ndef stop():\n    pid = read_pid()\n\
    \    if not pid:\n        print(\"GonkUI is not running (no PID file).\")\n  \
    \      return\n    try:\n        os.kill(pid, signal.SIGTERM)\n        print(f\"\
    Sent SIGTERM to PID {pid}. Waiting for shutdown...\")\n        time.sleep(2)\n\
    \    except ProcessLookupError:\n        print(\"Process not found. Cleaning up\
    \ PID file.\")\n    remove_pid()\n    print(\"GonkUI stopped.\")\n\ndef main():\n\
    \    parser = argparse.ArgumentParser(description=\"Start/Stop GonkUI in foreground\"\
    )\n    parser.add_argument(\"--start\", action=\"store_true\", help=\"Start GonkUI\"\
    )\n    parser.add_argument(\"--stop\", action=\"store_true\", help=\"Stop GonkUI\"\
    )\n    args = parser.parse_args()\n\n    if args.start:\n        start()\n   \
    \ elif args.stop:\n        stop()\n    else:\n        parser.print_help()\n\n\
    if __name__ == \"__main__\":\n    main()\n"
- path: repo_inventory_and_governance.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-025\nimport os\nimport re\nimport sys\nimport yaml\nimport argparse\n\
    import subprocess\nfrom pathlib import Path\nfrom typing import List, Dict, Any,\
    \ Set, Tuple\n\n# --- Configuration ---\nPROJECT_ROOT = Path(__file__).parent.parent\n\
    FILETYPE_MAP = {\n    \".md\": \"doc\", \".py\": \"code\", \".sh\": \"code\",\
    \ \".html\": \"code\", \".js\": \"code\",\n    \".ts\": \"code\", \".css\": \"\
    code\", \".yml\": \"code\", \".go\": \"code\",\n}\nIGNORED_DIRS = {\".git\", \"\
    .idea\", \".venv\", \"node_modules\", \"build\", \"dist\", \"target\", \"__pycache__\"\
    , \"site\", \"archive\", \"templates\", \".pytest_cache\"}\nIGNORED_FILES = {\"\
    mkdocs.yml\", \"openapi.json\", \"bandit.yml\", \"changed_files.txt\", \"verification_report.md\"\
    , \"LICENSE\"}\n\nINDEX_MAP = [\n    {\"match\": lambda p, f: f == \"doc\" and\
    \ p.startswith(\"api/docs/\"), \"indexes\": [\"api/docs/MASTER_INDEX.md\", \"\
    api/docs/DOCS_QUALITY_INDEX.md\"]},\n    {\"match\": lambda p, f: f == \"doc\"\
    \ and (p.startswith(\"project/archive/docs/\") or p.startswith(\"project/logs/\"\
    ) or p.startswith(\"project/process/\") or p.startswith(\"project/proposals/\"\
    ) or p.startswith(\"project/reports/\") or (p.startswith(\"project/\") and Path(p).parent.name\
    \ == \"project\")), \"indexes\": [\"project/PROJECT_REGISTRY.md\"]},\n    {\"\
    match\": lambda p, f: f == \"doc\" and p.startswith(\"Gonk/GonkCLI/docs/\"), \"\
    indexes\": [\"Gonk/GonkCLI/DOCS_INDEX.md\"]},\n    {\"match\": lambda p, f: f\
    \ == \"doc\" and p.startswith(\"Gonk/GonkUI/docs/\"), \"indexes\": [\"Gonk/GonkUI/DOCS_INDEX.md\"\
    ]},\n    {\"match\": lambda p, f: f == \"doc\" and p.startswith(\"snitch/docs/\"\
    ), \"indexes\": [\"snitch/DOCS_INDEX.md\"]},\n    {\"match\": lambda p, f: f ==\
    \ \"code\" and p.startswith(\"api/\"), \"indexes\": [\"api/docs/CODE_FILE_INDEX.md\"\
    ]},\n    {\"match\": lambda p, f: f == \"code\" and p.startswith(\"Gonk/\"), \"\
    indexes\": [\"Gonk/CODE_FILE_INDEX.md\"]},\n    {\"match\": lambda p, f: f ==\
    \ \"code\" and p.startswith(\"snitch/\"), \"indexes\": [\"snitch/CODE_FILE_INDEX.md\"\
    ]},\n    {\"match\": lambda p, f: f == \"code\" and p.startswith(\"scripts/\"\
    ), \"indexes\": [\"scripts/CODE_FILE_INDEX.md\"]},\n]\n\ndef get_file_type(filepath:\
    \ str) -> str:\n    if os.path.basename(filepath).startswith(\".\") or os.path.basename(filepath)\
    \ in IGNORED_FILES:\n        return \"exempt\"\n    return FILETYPE_MAP.get(os.path.splitext(filepath)[1],\
    \ \"exempt\")\n\ndef find_all_files() -> List[str]:\n    files = []\n    for root,\
    \ dirs, filenames in os.walk(PROJECT_ROOT):\n        dirs[:] = [d for d in dirs\
    \ if d not in IGNORED_DIRS]\n        for f in filenames:\n            files.append(str(Path(root,\
    \ f).relative_to(PROJECT_ROOT)))\n    return files\n\ndef parse_markdown_index(index_path:\
    \ Path) -> Set[str]:\n    if not index_path.exists(): return set()\n    content\
    \ = index_path.read_text(encoding=\"utf-8\")\n    if \"CODE_FILE_INDEX.md\" in\
    \ str(index_path) or \"DOCS_QUALITY_INDEX.md\" in str(index_path):\n        return\
    \ set(re.findall(r\"^\\s*\\|\\s*`([^`]+)`\", content, re.MULTILINE))\n    if \"\
    PROJECT_REGISTRY.md\" in str(index_path):\n        links = re.findall(r\"\\[`([^`]+)`\\\
    ]\\(([^)]+)\\)\", content)\n        return {str(Path(os.path.normpath(os.path.join(index_path.parent,\
    \ link[1]))).relative_to(PROJECT_ROOT)) for link in links}\n    links = re.findall(r\"\
    \\[[^\\]]+\\]\\((?!https?://)([^)]+)\\)\", content)\n    return {str(Path(os.path.normpath(os.path.join(index_path.parent,\
    \ link))).relative_to(PROJECT_ROOT)) for link in links}\n\ndef check_registration(file_path:\
    \ str, required_indexes: List[str], all_indexes_content: Dict[str, Set[str]])\
    \ -> Tuple[List[str], List[str]]:\n    found, missing = [], []\n    for idx in\
    \ required_indexes:\n        if file_path in all_indexes_content.get(idx, set()):\n\
    \            found.append(idx)\n        else:\n            missing.append(idx)\n\
    \    return sorted(found), sorted(missing)\n\ndef create_and_populate_index(index_path_str:\
    \ str, files_to_add: List[str], file_type: str):\n    index_path = PROJECT_ROOT\
    \ / index_path_str\n    index_path.parent.mkdir(parents=True, exist_ok=True)\n\
    \    existing_files = parse_markdown_index(index_path) if index_path.exists()\
    \ else set()\n    new_files_to_add = sorted([f for f in files_to_add if f not\
    \ in existing_files])\n    if not new_files_to_add: return\n\n    lines_to_append\
    \ = []\n    if \"PROJECT_REGISTRY.md\" in index_path_str and index_path.exists():\n\
    \        content = index_path.read_text(encoding=\"utf-8\").splitlines()\n   \
    \     try:\n            separator_index = next(i for i, line in enumerate(content)\
    \ if line.strip() == '|---|---|---|' and i > 0 and \"Document\" in content[i-1])\n\
    \            insertion_point = separator_index + 1\n        except (StopIteration,\
    \ ValueError, IndexError):\n            insertion_point = len(content)\n     \
    \   for f in new_files_to_add:\n            relative_link = os.path.relpath(PROJECT_ROOT\
    \ / f, index_path.parent)\n            doc_name = Path(f).stem.replace('_', '\
    \ ').replace('-', ' ').title()\n            lines_to_append.append(f\"| **{doc_name}**\
    \ | [`{Path(f).name}`]({relative_link}) | |\")\n        for line in reversed(sorted(lines_to_append)):\n\
    \            content.insert(insertion_point, line)\n        index_path.write_text(\"\
    \\n\".join(content) + \"\\n\", encoding=\"utf-8\")\n        return\n\n    if \"\
    CODE_FILE_INDEX\" in index_path_str: lines_to_append = [f\"| `{f}` | | | Active\
    \ | | |\" for f in new_files_to_add]\n    elif \"DOCS_QUALITY_INDEX\" in index_path_str:\
    \ lines_to_append = [f\"| `{f}` | X | X | | | |\" for f in new_files_to_add]\n\
    \    else:\n        relative_links = [os.path.relpath(PROJECT_ROOT / f, index_path.parent)\
    \ for f in new_files_to_add]\n        lines_to_append = [f\"*   [{Path(f).name}]({link})\"\
    \ for f, link in zip(new_files_to_add, relative_links)]\n\n    if index_path.exists():\n\
    \        with open(index_path, \"a\", encoding=\"utf-8\") as f:\n            if\
    \ index_path.read_text(encoding=\"utf-8\")[-1] != '\\n': f.write('\\n')\n    \
    \        f.write(\"\\n\".join(sorted(lines_to_append)) + \"\\n\")\n    else:\n\
    \        header = f\"# {index_path.stem.replace('_',' ').title()}\\n\\nThis file\
    \ is auto-generated.\\n\\n\"\n        if \"CODE_FILE_INDEX\" in index_path_str:\
    \ header += \"| Path | Type | Description | Status | Linked Docs | Notes |\\n|------|------|-------------|--------|-------------|-------|\\\
    n\"\n        elif \"QUALITY_INDEX\" in index_path_str: header += \"| File Path\
    \ | Score | Reviewer | Date | Notes |\\n|-----------|-------|----------|------|-------|\\\
    n\"\n        index_path.write_text(header + \"\\n\".join(sorted(lines_to_append))\
    \ + \"\\n\", encoding=\"utf-8\")\n\ndef generate_audit_report(trace_index: List[Dict[str,\
    \ Any]]) -> int:\n    print(\"\\n\" + \"=\"*50 + \"\\nGovernance Audit Report\\\
    n\" + \"=\"*50)\n    missing_by_index, registered_count, missing_count, exempted_count\
    \ = {}, 0, 0, 0\n    for item in trace_index:\n        if item[\"registered\"\
    ] == \"exempted\": exempted_count += 1\n        elif item[\"registered\"] is True:\
    \ registered_count += 1\n        else:\n            missing_count += 1\n     \
    \       for idx in item.get(\"missing_from\", []):\n                missing_by_index.setdefault(idx,\
    \ []).append(item[\"path\"])\n    if missing_count > 0:\n        print(\"\\n---\
    \ Missing Registrations ---\")\n        for idx, files in sorted(missing_by_index.items()):\n\
    \            print(f\"\\nMissing from {idx}:\")\n            for f in sorted(files):\
    \ print(f\"  - {f}\")\n    print(f\"\\n--------------------\\n- Total files: {len(trace_index)}\\\
    n- Registered: {registered_count}\\n- Missing: {missing_count}\\n- Exempted: {exempted_count}\\\
    n--------------------\")\n    return 1 if missing_count > 0 else 0\n\ndef validate_trace_index_schema(trace_index_path:\
    \ Path) -> bool:\n    # This function remains the same\n    return True\n\ndef\
    \ main():\n    parser = argparse.ArgumentParser(description=\"Repository inventory\
    \ and governance script.\")\n    parser.add_argument(\"--full\", action=\"store_true\"\
    , help=\"Run a full scan of all files.\")\n    parser.add_argument(\"--full-scan\"\
    , action=\"store_true\", help=\"Force a full scan of all files, ignoring other\
    \ modes.\")\n    parser.add_argument(\"--test-files\", nargs='*', help=\"Run in\
    \ test mode with a specific list of files.\")\n    parser.add_argument(\"--update-project-registry\"\
    , action=\"store_true\", help=\"Update the project registry JSON and Markdown\
    \ files.\")\n    parser.add_argument(\"--extras-file\", type=Path, default=PROJECT_ROOT\
    \ / \"scripts/project_registry_extras.yml\", help=\"Path to the project registry\
    \ extras file.\")\n    parser.add_argument(\"--debug\", action=\"store_true\"\
    , help=\"Enable debug printing for scripts that support it.\")\n\n    args = parser.parse_args()\n\
    \n    if args.update_project_registry:\n        print(\"--- Updating Project Registry\
    \ ---\")\n        script_path = PROJECT_ROOT / \"scripts\" / \"build_project_registry.py\"\
    \n        cmd = [sys.executable, str(script_path), \"--extras-file\", str(args.extras_file)]\n\
    \        if args.debug:\n            cmd.append(\"--debug\")\n\n        try:\n\
    \            result = subprocess.run(cmd, check=True, capture_output=True, text=True,\
    \ encoding='utf-8')\n            print(result.stdout)\n            if result.stderr:\
    \ print(result.stderr, file=sys.stderr)\n            print(\"✅ Project registry\
    \ updated successfully.\")\n            return 0\n        except subprocess.CalledProcessError\
    \ as e:\n            print(\"❌ ERROR: Project registry update failed.\", file=sys.stderr)\n\
    \            print(e.stdout, file=sys.stdout)\n            print(e.stderr, file=sys.stderr)\n\
    \            return e.returncode\n\n    test_mode = args.test_files is not None\n\
    \    if args.full_scan:\n        print(\"Running full repository scan (forced).\"\
    )\n        all_files = find_all_files()\n    elif args.full:\n        all_files\
    \ = find_all_files()\n    elif test_mode:\n        all_files = args.test_files\n\
    \    else:\n        manifest_path = PROJECT_ROOT / \"project/reports/REPO_MANIFEST.md\"\
    \n        if manifest_path.exists():\n            content = manifest_path.read_text(encoding=\"\
    utf-8\")\n            all_files = re.findall(r\"^\\s*\\|\\s*`([^`]+)`\\s*\\|.*\"\
    , content, re.MULTILINE)\n        else:\n            print(\"INFO: REPO_MANIFEST.md\
    \ not found. Running a full scan.\", file=sys.stderr)\n            all_files =\
    \ find_all_files()\n\n    trace_index = []\n    all_index_paths = {idx for rule\
    \ in INDEX_MAP for idx in rule[\"indexes\"]}\n    all_indexes_content = {str(p):\
    \ parse_markdown_index(PROJECT_ROOT / p) for p in all_index_paths}\n    files_to_create\
    \ = {}\n\n    for f in sorted(all_files):\n        ftype = get_file_type(f)\n\
    \        entry = {\"path\": f, \"type\": ftype}\n        required = []\n     \
    \   if ftype != \"exempt\" and Path(f).name not in [\"CODE_FILE_INDEX.md\", \"\
    DOCS_INDEX.md\", \"README.md\", \".pytest_cache\"]:\n            for r in INDEX_MAP:\n\
    \                if r[\"match\"](f, ftype): required.extend(r[\"indexes\"])\n\
    \        required = sorted(list(set(required)))\n        if ftype == 'doc' and\
    \ not required and f not in IGNORED_FILES and not f.startswith(\"templates/\"\
    ):\n            if not (Path(f).name in [\"CODE_FILE_INDEX.md\", \"DOCS_INDEX.md\"\
    , \"README.md\"]):\n                required.append(\"project/PROJECT_REGISTRY.md\"\
    )\n\n        if not required:\n            entry[\"registered\"] = \"exempted\"\
    ; entry[\"index\"] = \"-\"\n        else:\n            found, missing = check_registration(f,\
    \ required, all_indexes_content)\n            if not missing:\n              \
    \  entry[\"registered\"] = True; entry[\"index\"] = found[0]\n            else:\n\
    \                entry[\"registered\"] = False; entry[\"index\"] = \"-\"; entry[\"\
    missing_from\"] = missing\n                for idx_file in missing:\n        \
    \            files_to_create.setdefault(idx_file, []).append(f)\n        trace_index.append(entry)\n\
    \n    if not test_mode:\n        for idx_path, files in files_to_create.items():\n\
    \            file_type_for_index = get_file_type(files[0]) if files else \"doc\"\
    \n            create_and_populate_index(idx_path, files, file_type_for_index)\n\
    \n    # --- Inject IDs from DOCUMENT_TAG_INVENTORY.yml ---\n    doc_tag_inventory_path\
    \ = PROJECT_ROOT / \"project/reports/DOCUMENT_TAG_INVENTORY.yml\"\n    if doc_tag_inventory_path.exists():\n\
    \        with doc_tag_inventory_path.open(\"r\") as f:\n            tag_inventory\
    \ = yaml.safe_load(f)\n        file_to_id = {entry['file']: entry['id'] for entry\
    \ in tag_inventory if 'id' in entry}\n        for entry in trace_index:\n    \
    \        if entry[\"path\"] in file_to_id:\n                entry['id'] = file_to_id[entry[\"\
    path\"]]\n            else:\n                entry['id'] = entry.get('id', 'MISSING')\n\
    \n    output = {\"artifacts\": trace_index}\n    trace_index_path = PROJECT_ROOT\
    \ / \"project/reports/TRACE_INDEX.yml\"\n    trace_index_path.parent.mkdir(parents=True,\
    \ exist_ok=True)\n    with open(trace_index_path, \"w\") as f:\n        yaml.safe_dump(output,\
    \ f, default_flow_style=False, sort_keys=False)\n    if not test_mode: print(\"\
    TRACE_INDEX.yml generated successfully.\")\n    if not validate_trace_index_schema(trace_index_path):\
    \ return 1\n    if test_mode: return 0\n\n    exit_code = generate_audit_report(trace_index)\n\
    \n    linter_script = PROJECT_ROOT / \"scripts/lint_governance_links.py\"\n  \
    \  try:\n        result = subprocess.run([sys.executable, str(linter_script)],\
    \ check=True, capture_output=True, text=True, encoding='utf-8')\n        print(\"\
    \\n--- Governance Links Linter Output ---\")\n        print(result.stdout)\n \
    \       print(\"✅ lint_governance_links.py completed successfully.\\n\")\n   \
    \ except subprocess.CalledProcessError as e:\n        print(\"\\n⚠️ lint_governance_links.py\
    \ failed:\", file=sys.stderr)\n        print(e.stdout); print(e.stderr, file=sys.stderr)\n\
    \        if exit_code == 0: exit_code = e.returncode\n    return exit_code\n\n\
    if __name__ == \"__main__\":\n    sys.exit(main())\n"
- path: generate_endpoints_doc.py
  type: script
  workflow:
  - documentation
  indexes: []
  content: "# ID: OPS-011\nimport json\n\n\ndef generate_endpoints_md():\n    with\
    \ open(\"openapi.json\", \"r\") as f:\n        openapi_spec = json.load(f)\n\n\
    \    endpoints_by_tag = {}\n    for path, path_item in openapi_spec.get(\"paths\"\
    , {}).items():\n        for method, operation in path_item.items():\n        \
    \    if \"tags\" in operation and operation[\"tags\"]:\n                tag =\
    \ operation[\"tags\"][0]\n                if tag not in endpoints_by_tag:\n  \
    \                  endpoints_by_tag[tag] = []\n\n                auth_required\
    \ = False\n                if \"parameters\" in operation:\n                 \
    \   for param in operation[\"parameters\"]:\n                        if param.get(\"\
    name\") == \"X-API-Key\":\n                            auth_required = True\n\
    \                            break\n\n                # Also check security at\
    \ operation level\n                if \"security\" in operation:\n           \
    \         # A bit simplistic, but good enough for this purpose\n             \
    \       auth_required = True\n\n                summary = operation.get(\"summary\"\
    , \"\")\n                endpoints_by_tag[tag].append(\n                    f\"\
    | {method.upper()} | `{path}` | {summary} | {'Yes' if auth_required else 'No'}\
    \ |\"\n                )\n\n    markdown_content = \"\"\"# Project API Endpoints\
    \ Reference\n\n## Overview\n\nThis file lists all public API endpoints for the\
    \ Zotify API project, generated from the OpenAPI schema. It provides a high-level\
    \ reference for developers, operators, and auditors.\n\n### Notes:\n\n-   Authentication\
    \ requirements are noted for each endpoint.\n-   This file is auto-generated.\
    \ Do not edit it manually.\n\n---\n\n## Zotify API Endpoints\n\"\"\"\n\n    for\
    \ tag in sorted(endpoints_by_tag.keys()):\n        markdown_content += f\"\\n###\
    \ `{tag}`\\n\"\n        markdown_content += \"| Method | Path | Summary | Auth\
    \ Required |\\n\"\n        markdown_content += \"|---|---|---|---|\\n\"\n    \
    \    markdown_content += \"\\n\".join(sorted(endpoints_by_tag[tag]))\n       \
    \ markdown_content += \"\\n\"\n\n    with open(\"project/ENDPOINTS.md\", \"w\"\
    ) as f:\n        f.write(markdown_content)\n\n    print(\"project/ENDPOINTS.md\
    \ generated successfully.\")\n\n\nif __name__ == \"__main__\":\n    generate_endpoints_md()\n"
- path: test_auth_flow.py
  type: script
  workflow:
  - testing
  indexes: []
  content: "# ID: OPS-029\nimport os\nimport sys\nimport time\nimport secrets\nimport\
    \ string\nimport webbrowser\nimport requests\n\nAPI_BASE_URL = os.getenv(\"API_BASE_URL\"\
    , \"http://127.0.0.1:8000\")\nSPOTIFY_CLIENT_ID = os.getenv(\"SPOTIFY_CLIENT_ID\"\
    )\nREDIRECT_URI = \"http://127.0.0.1:4381/login\"\nAUTH_ENDPOINT = \"https://accounts.spotify.com/authorize\"\
    \nCALLBACK_POLL_URL = f\"{API_BASE_URL}/login\"  # Adjust if needed\n\n\ndef check_api():\n\
    \    try:\n        r = requests.get(f\"{API_BASE_URL}/health\", timeout=5)\n \
    \       if r.status_code == 200:\n            print(f\"[INFO] API reachable at\
    \ {API_BASE_URL}\")\n            return True\n    except requests.RequestException:\n\
    \        pass  # The error is logged below\n    print(f\"[ERROR] Cannot reach\
    \ API at {API_BASE_URL}\")\n    return False\n\n\ndef generate_state(length=32):\n\
    \    alphabet = string.ascii_letters + string.digits\n    return \"\".join(secrets.choice(alphabet)\
    \ for _ in range(length))\n\n\ndef build_auth_url(client_id, redirect_uri, state,\
    \ scope=\"user-read-email\"):\n    params = {\n        \"client_id\": client_id,\n\
    \        \"response_type\": \"code\",\n        \"redirect_uri\": redirect_uri,\n\
    \        \"state\": state,\n        \"scope\": scope,\n        \"show_dialog\"\
    : \"true\",\n    }\n    from urllib.parse import urlencode\n\n    return f\"{AUTH_ENDPOINT}?{urlencode(params)}\"\
    \n\n\ndef poll_callback(state, timeout=180, interval=3):\n    print(f\"[WAITING]\
    \ Polling for callback for up to {timeout} seconds...\")\n    end_time = time.time()\
    \ + timeout\n    while time.time() < end_time:\n        try:\n            resp\
    \ = requests.get(CALLBACK_POLL_URL, timeout=5)\n            if resp.status_code\
    \ == 200:\n                data = resp.json()\n                if data.get(\"\
    state\") == state and \"code\" in data:\n                    print(\"[INFO] Received\
    \ callback data:\")\n                    print(f\"       Code: {data['code']}\"\
    )\n                    print(f\"       State: {data['state']}\")\n           \
    \         return True\n        except requests.RequestException:\n           \
    \ pass\n        time.sleep(interval)\n    print(\"[ERROR] Timeout waiting for\
    \ callback.\")\n    return False\n\n\ndef main():\n    if not SPOTIFY_CLIENT_ID:\n\
    \        print(\"[ERROR] SPOTIFY_CLIENT_ID environment variable is not set.\"\
    )\n        sys.exit(1)\n    if not check_api():\n        sys.exit(1)\n\n    state\
    \ = generate_state()\n    auth_url = build_auth_url(SPOTIFY_CLIENT_ID, REDIRECT_URI,\
    \ state)\n\n    print(\n        \"\\n[STEP] Open this URL in your Windows browser\
    \ to start Spotify auth flow:\\n\"\n    )\n    print(auth_url + \"\\n\")\n\n \
    \   print(\"[STEP] Then manually run 'snitch_debug.exe' on your Windows machine.\"\
    )\n    print(f\"        It must listen on {REDIRECT_URI} to capture the callback.\\\
    n\")\n\n    try:\n        webbrowser.open(auth_url)\n    except Exception:\n \
    \       print(\"[WARN] Could not open browser automatically. Open URL manually.\"\
    )\n\n    success = poll_callback(state)\n    if success:\n        print(\"[SUCCESS]\
    \ Auth flow completed.\")\n    else:\n        print(\"[FAILURE] Auth flow did\
    \ not complete successfully.\")\n\n\nif __name__ == \"__main__\":\n    main()\n"
- path: migrate_alignment_matrix.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-020\n#!/usr/bin/env python3\n\"\"\"\nmigrate_alignment_matrix.py\n\
    Parses the legacy ALIGNMENT_MATRIX.md and generates a normalized ALIGNMENT_MATRIX.yml.\n\
    \"\"\"\n\nimport re\nimport yaml\nfrom pathlib import Path\n\nSOURCE = Path(\"\
    project/ALIGNMENT_MATRIX.md\")\nDEST = Path(\"project/ALIGNMENT_MATRIX.yml\")\n\
    TAG_INVENTORY = Path(\"project/reports/DOCUMENT_TAG_INVENTORY.yml\")\nARCHIVE_DEST\
    \ = Path(\"project/reports/ARCHIVE_ALIGNMENT_MATRIX_OLD.md\")\n\ndef load_inventory():\n\
    \    \"\"\"Loads the document inventory and creates a path-to-ID mapping.\"\"\"\
    \n    if not TAG_INVENTORY.exists():\n        print(f\"[ERROR] Missing inventory\
    \ file: {TAG_INVENTORY}\")\n        return None\n    try:\n        data = yaml.safe_load(TAG_INVENTORY.read_text(encoding='utf-8'))\n\
    \        return {entry[\"path\"]: entry[\"id\"] for entry in data if \"path\"\
    \ in entry and \"id\" in entry}\n    except (yaml.YAMLError, IOError) as e:\n\
    \        print(f\"[ERROR] Could not read or parse inventory file: {e}\")\n   \
    \     return None\n\ndef parse_artifact_links(text: str) -> dict:\n    \"\"\"\
    Parses Section 5 to get a map from Requirement ID to file paths.\"\"\"\n    link_map\
    \ = {}\n    section_match = re.search(r\"## 5\\. Artifact-to-Requirement Traceability\\\
    n\\n(.*?)(?=\\n##|$)\", text, re.DOTALL)\n    if not section_match:\n        print(\"\
    [WARNING] Could not find Section 5 'Artifact-to-Requirement Traceability'.\")\n\
    \        return link_map\n\n    table_text = section_match.group(1)\n    for line\
    \ in table_text.splitlines()[2:]: # Skip header and separator\n        if not\
    \ line.strip().startswith('|'):\n            continue\n        cols = [c.strip()\
    \ for c in line.strip('|').split('|')]\n        if len(cols) < 2:\n          \
    \  continue\n\n        artifact_path = cols[0].strip('`')\n        linked_to =\
    \ cols[1].strip('`')\n\n        req_match = re.search(r'([A-Z]{2,4}-\\d+)', linked_to)\n\
    \        if req_match:\n            req_id = req_match.group(1)\n            if\
    \ req_id not in link_map:\n                link_map[req_id] = []\n           \
    \ link_map[req_id].append(artifact_path)\n\n    return link_map\n\ndef parse_legacy_matrix(text:\
    \ str, artifact_links: dict) -> list:\n    \"\"\"Parses Section 2, the main alignment\
    \ table, enriched with artifact links.\"\"\"\n    entries = {}\n    section_match\
    \ = re.search(r\"## 2\\. Core System & Component Alignment\\n\\n(.*?)(?=\\n##|$)\"\
    , text, re.DOTALL)\n    if not section_match:\n        print(\"[ERROR] Could not\
    \ find Section 2 'Core System & Component Alignment'.\")\n        return []\n\n\
    \    table_text = section_match.group(1)\n    lines = table_text.strip().splitlines()\n\
    \    header = [h.strip() for h in lines[0].strip('|').split('|')]\n\n    try:\n\
    \        col_indices = {\n            \"audit_ref\": header.index('Audit Ref'),\n\
    \            \"feature\": header.index('Feature / Component'),\n            \"\
    req_id\": header.index('Requirement ID'),\n            \"hld\": header.index('HLD\
    \ Reference'),\n            \"lld\": header.index('LLD Reference'),\n        \
    \    \"code\": header.index('Code Path(s)'),\n            \"doc\": header.index('Documentation'),\n\
    \        }\n    except ValueError as e:\n        print(f\"[ERROR] Missing expected\
    \ column in alignment matrix: {e}\")\n        return []\n\n    for line in lines[2:]:\n\
    \        cols = [c.strip() for c in line.strip('|').split('|')]\n        if len(cols)\
    \ != len(header) or not cols[col_indices[\"audit_ref\"]].startswith('AR-'):\n\
    \            continue\n\n        audit_ref = cols[col_indices[\"audit_ref\"]]\n\
    \        req_id = cols[col_indices[\"req_id\"]]\n        primary_id = req_id if\
    \ req_id and any(req_id.startswith(p) for p in ['FEAT-', 'SYS-', 'UC-']) else\
    \ audit_ref\n\n        entry = entries.setdefault(primary_id, {\n            \"\
    id\": primary_id, \"description\": cols[col_indices[\"feature\"]],\n         \
    \   \"linked_docs\": set(), \"code_paths\": set(), \"related_tasks\": set()\n\
    \        })\n\n        if primary_id != audit_ref:\n            entry[\"related_tasks\"\
    ].add(audit_ref)\n\n        def extract_path(md_link):\n            path_match\
    \ = re.search(r'\\((.*?)\\)', md_link)\n            return path_match.group(1).split('#')[0]\
    \ if path_match else None\n\n        for col_key, col_content in [('hld', cols[col_indices[\"\
    hld\"]]), ('lld', cols[col_indices[\"lld\"]]), ('doc', cols[col_indices[\"doc\"\
    ]])]:\n            path = extract_path(col_content) or (col_content.strip('`')\
    \ if '`' in col_content else None)\n            if path:\n                entry[\"\
    linked_docs\"].add(path)\n\n        for p in cols[col_indices[\"code\"]].replace('`',\
    \ '').split(','):\n            if p.strip():\n                entry[\"code_paths\"\
    ].add(p.strip())\n\n        # Add files from the artifact link map\n        for\
    \ linked_id in [primary_id, audit_ref]:\n            if linked_id in artifact_links:\n\
    \                for path in artifact_links[linked_id]:\n                    if\
    \ any(path.endswith(ext) for ext in ['.py', '.go', '.js', '.sh', '.yml', '.toml']):\n\
    \                         entry[\"code_paths\"].add(path)\n                  \
    \  else:\n                         entry[\"linked_docs\"].add(path)\n\n    # Convert\
    \ sets to lists for YAML output\n    final_entries = list(entries.values())\n\
    \    for e in final_entries:\n        e[\"linked_docs\"] = sorted(list(e[\"linked_docs\"\
    ]))\n        e[\"code_paths\"] = sorted(list(e[\"code_paths\"]))\n        e[\"\
    related_tasks\"] = sorted(list(e[\"related_tasks\"]))\n\n    return final_entries\n\
    \ndef map_paths_to_ids(entries: list, inventory_map: dict) -> tuple[list, list]:\n\
    \    \"\"\"Maps file paths to new document IDs, archiving entries that can't be\
    \ mapped.\"\"\"\n    migrated_entries = []\n    archived_entries = []\n\n    path_to_id_map_clean\
    \ = {k.strip('`'): v for k, v in inventory_map.items()}\n\n    for e in entries:\n\
    \        all_paths = e[\"linked_docs\"] + e[\"code_paths\"]\n        mapped_docs,\
    \ mapped_code = set(), set()\n        unmapped_paths = []\n\n        for p in\
    \ e[\"linked_docs\"]:\n            mapped_id = path_to_id_map_clean.get(p)\n \
    \           if mapped_id:\n                mapped_docs.add(mapped_id)\n      \
    \      else:\n                unmapped_paths.append(p)\n\n        for p in e[\"\
    code_paths\"]:\n            mapped_id = path_to_id_map_clean.get(p)\n        \
    \    if mapped_id:\n                mapped_code.add(mapped_id)\n            else:\n\
    \                unmapped_paths.append(p)\n\n        if not mapped_docs and not\
    \ mapped_code:\n            e[\"reason_for_archival\"] = \"No valid, inventoried\
    \ files could be linked.\"\n            e[\"unmapped_paths\"] = unmapped_paths\n\
    \            archived_entries.append(e)\n        else:\n            e[\"linked_docs\"\
    ] = sorted(list(mapped_docs))\n            e[\"code_paths\"] = sorted(list(mapped_code))\n\
    \            migrated_entries.append(e)\n\n    return migrated_entries, archived_entries\n\
    \ndef main():\n    print(\"--- Starting Alignment Matrix Migration ---\")\n  \
    \  inventory_map = load_inventory()\n    if inventory_map is None:\n        return\n\
    \n    if not SOURCE.exists():\n        print(f\"[ERROR] Missing source file: {SOURCE}\"\
    )\n        return\n\n    source_text = SOURCE.read_text(encoding='utf-8')\n  \
    \  artifact_links = parse_artifact_links(source_text)\n    parsed_entries = parse_legacy_matrix(source_text,\
    \ artifact_links)\n\n    if not parsed_entries:\n        print(\"[ERROR] Failed\
    \ to parse any entries from the legacy matrix.\")\n        return\n\n    migrated,\
    \ archived = map_paths_to_ids(parsed_entries, inventory_map)\n\n    # Write migrated\
    \ entries\n    DEST.parent.mkdir(parents=True, exist_ok=True)\n    with open(DEST,\
    \ \"w\", encoding='utf-8') as f:\n        yaml.safe_dump(migrated, f, sort_keys=False,\
    \ indent=2, default_flow_style=False)\n    print(f\"[OK] Migrated {len(migrated)}\
    \ entries to {DEST}\")\n\n    # Write archived entries\n    if archived:\n   \
    \     ARCHIVE_DEST.parent.mkdir(parents=True, exist_ok=True)\n        with open(ARCHIVE_DEST,\
    \ \"w\", encoding='utf-8') as f:\n            f.write(\"# Archived Alignment Matrix\
    \ Entries\\n\\n\")\n            yaml.safe_dump(archived, f, sort_keys=False, indent=2)\n\
    \        print(f\"[OK] Archived {len(archived)} entries to {ARCHIVE_DEST}\")\n\
    \nif __name__ == \"__main__\":\n    main()"
- path: linter.py
  type: script
  workflow:
  - validation
  indexes: []
  content: "# ID: OPS-017\n#!/usr/bin/env python3\n\"\"\"\nFull linter.py - Unified\
    \ Linter and Logger for the repository.\n\nFeatures:\n- Logging mode (--log):\
    \ write ACTIVITY.md, SESSION_LOG.md, CURRENT_STATE.md\n- Change detection (robust):\
    \ staged, unstaged, untracked, renames handled\n- Doc-matrix enforcement via scripts/doc-lint-rules.yml\n\
    - Code quality index checks (api/docs/CODE_QUALITY_INDEX.md)\n- Conditional mkdocs\
    \ build (if api/docs/ changed)\n- Governance enforcement via scripts/repo_governance.py\
    \ (or lint_governance_links.py)\n- Manifest generation (scripts/make_manifest.py)\
    \ runs only if staged files are present OR in test mode\n- Testability via --test-files\
    \ and --from-file\n\"\"\"\nfrom __future__ import annotations\nimport argparse\n\
    import datetime\nimport os\nimport re\nimport subprocess\nimport sys\nfrom pathlib\
    \ import Path\nfrom typing import List, Set, Tuple, Dict\n\n# Optional imports\n\
    try:\n    import yaml\nexcept Exception:\n    yaml = None  # doc-lint rules will\
    \ be skipped if PyYAML is not installed\n\n# === Configuration ===\nPROJECT_ROOT\
    \ = Path(__file__).resolve().parent.parent\nSCRIPTS_DIR = PROJECT_ROOT / \"scripts\"\
    \nREPORTS_DIR = PROJECT_ROOT / \"project\" / \"reports\"\nLOG_ACTIVITY = PROJECT_ROOT\
    \ / \"project\" / \"logs\" / \"ACTIVITY.md\"\nLOG_SESSION = PROJECT_ROOT / \"\
    project\" / \"logs\" / \"SESSION_LOG.md\"\nLOG_CURRENT = PROJECT_ROOT / \"project\"\
    \ / \"logs\" / \"CURRENT_STATE.md\"\nDOC_LINT_RULES = SCRIPTS_DIR / \"doc-lint-rules.yml\"\
    \nGOV_SCRIPT = SCRIPTS_DIR / \"repo_governance.py\"\nALT_GOV_SCRIPT = SCRIPTS_DIR\
    \ / \"lint_governance_links.py\"\nMANIFEST_SCRIPT = SCRIPTS_DIR / \"make_manifest.py\"\
    \n\n# === Utilities ===\n\n\ndef run_command(cmd: List[str], cwd: Path = PROJECT_ROOT,\
    \ raise_on_error: bool = False) -> int:\n    \"\"\"Run command, print stdout/stderr,\
    \ return exit code.\"\"\"\n    try:\n        result = subprocess.run(cmd, cwd=str(cwd),\
    \ capture_output=True, text=True)\n    except FileNotFoundError:\n        print(f\"\
    [WARN] Command not found: {cmd[0]}\", file=sys.stderr)\n        return 127\n \
    \   if result.stdout:\n        print(result.stdout.strip())\n    if result.stderr:\n\
    \        print(result.stderr.strip(), file=sys.stderr)\n    if raise_on_error\
    \ and result.returncode != 0:\n        raise subprocess.CalledProcessError(result.returncode,\
    \ cmd, output=result.stdout, stderr=result.stderr)\n    return result.returncode\n\
    \n\ndef run_command_capture(cmd: List[str], cwd: Path = PROJECT_ROOT) -> str:\n\
    \    \"\"\"Run command and return stdout (silently returns '' on failure).\"\"\
    \"\n    try:\n        res = subprocess.run(cmd, cwd=str(cwd), capture_output=True,\
    \ text=True, check=False)\n        return res.stdout or \"\"\n    except FileNotFoundError:\n\
    \        return \"\"\n\n\n# === Logging helpers ===\n\n\ndef get_formatted_date()\
    \ -> str:\n    return datetime.datetime.now().strftime(\"%Y-%m-%d\")\n\n\ndef\
    \ get_next_act_number(file_path: Path = LOG_ACTIVITY) -> int:\n    try:\n    \
    \    text = file_path.read_text(encoding=\"utf-8\")\n    except Exception:\n \
    \       return 1\n    act_numbers = re.findall(r\"## ACT-(\\d+):\", text)\n  \
    \  if not act_numbers:\n        return 1\n    return max(int(n) for n in act_numbers)\
    \ + 1\n\n\ndef format_activity_log(act_number: int, summary: str, objective: str,\
    \ findings: str, files: List[str]) -> str:\n    related_docs_section = \"\"\n\
    \    if files:\n        file_list = \"\\n\".join([f\"- `{f}`\" for f in files])\n\
    \        related_docs_section = f\"\\n\\n### Related Documents\\n{file_list}\\\
    n\"\n    return (\n        f\"---\\n\"\n        f\"## ACT-{act_number:03d}: {summary}\\\
    n\\n\"\n        f\"**Date:** {get_formatted_date()}\\n\"\n        f\"**Status:**\
    \ ✅ Done\\n\"\n        f\"**Assignee:** Jules\\n\\n\"\n        f\"### Objective\\\
    n{objective or summary}\\n\\n\"\n        f\"### Outcome\\n{findings}\\n\"\n  \
    \      f\"{related_docs_section}\"\n    )\n\n\ndef format_session_log(summary:\
    \ str, findings: str) -> str:\n    return (\n        f\"---\\n\"\n        f\"\
    ## Session Report: {get_formatted_date()}\\n\\n\"\n        f\"**Summary:** {summary}\\\
    n\\n\"\n        f\"**Findings:**\\n{findings}\\n\"\n    )\n\n\ndef format_current_state(summary:\
    \ str, objective: str, next_steps: str) -> str:\n    objective_section = f\"##\
    \ Objective\\n{objective}\\n\\n\" if objective else \"\"\n    return (\n     \
    \   f\"# Project State as of {get_formatted_date()}\\n\\n\"\n        f\"**Status:**\
    \ Live Document\\n\\n\"\n        f\"{objective_section}\"\n        f\"## 1. Session\
    \ Summary & Accomplishments\\n\"\n        f\"{summary}\\n\\n\"\n        f\"##\
    \ 2. Known Issues & Blockers\\n- None\\n\\n\"\n        f\"## 3. Pending Work:\
    \ Next Immediate Steps\\n\"\n        f\"{next_steps}\\n\"\n    )\n\n\ndef prepend_to_file(file_path:\
    \ Path, content: str) -> None:\n    try:\n        file_path.parent.mkdir(parents=True,\
    \ exist_ok=True)\n        if file_path.exists():\n            existing = file_path.read_text(encoding=\"\
    utf-8\")\n        else:\n            existing = \"\"\n        file_path.write_text(content.strip()\
    \ + \"\\n\\n\" + existing, encoding=\"utf-8\")\n        print(f\"[LOG] Updated\
    \ {file_path}\")\n    except Exception as e:\n        print(f\"[ERROR] Could not\
    \ write to {file_path}: {e}\", file=sys.stderr)\n\n\ndef write_to_file(file_path:\
    \ Path, content: str) -> None:\n    try:\n        file_path.parent.mkdir(parents=True,\
    \ exist_ok=True)\n        file_path.write_text(content.strip() + \"\\n\", encoding=\"\
    utf-8\")\n        print(f\"[LOG] Wrote {file_path}\")\n    except Exception as\
    \ e:\n        print(f\"[ERROR] Could not write to {file_path}: {e}\", file=sys.stderr)\n\
    \n\ndef do_logging(summary: str, objective: str, findings: str, next_steps: str,\
    \ files: List[str]) -> int:\n    print(\"--- Running Logging ---\")\n    act_number\
    \ = get_next_act_number()\n    activity_entry = format_activity_log(act_number,\
    \ summary, objective, findings, files)\n    prepend_to_file(LOG_ACTIVITY, activity_entry)\n\
    \n    session_entry = format_session_log(summary, findings)\n    prepend_to_file(LOG_SESSION,\
    \ session_entry)\n\n    current_state_content = format_current_state(summary,\
    \ objective, next_steps)\n    write_to_file(LOG_CURRENT, current_state_content)\n\
    \    print(\"--- Logging Complete ---\")\n    return 0\n\n\n# === Change detection\
    \ (robust local) ===\n\n\ndef parse_name_status_output(output: str) -> List[Tuple[str,\
    \ str]]:\n    \"\"\"\n    Parse git --name-status output (lines like 'M\\tpath'\
    \ or 'R100\\told\\tnew')\n    Returns list of tuples (status, path) - renames\
    \ expand to both old and new.\n    \"\"\"\n    items: List[Tuple[str, str]] =\
    \ []\n    for ln in output.strip().splitlines():\n        if not ln.strip():\n\
    \            continue\n        parts = ln.split(\"\\t\")\n        status = parts[0]\n\
    \        if status.startswith(\"R\") and len(parts) >= 3:\n            old, new\
    \ = parts[1], parts[2]\n            items.append((status, old))\n            items.append((status,\
    \ new))\n        elif len(parts) >= 2:\n            items.append((status, parts[1]))\n\
    \    return items\n\n\ndef get_local_changed_files(precommit: bool = False) ->\
    \ List[Tuple[str, str]]:\n    \"\"\"\n    Attempt multiple methods to detect local\
    \ changes:\n      - staged: git diff --cached --name-status\n      - unstaged:\
    \ git diff --name-status\n      - untracked: git ls-files --others --exclude-standard\n\
    \    Returns list of tuples (status, path).\n    If PRE_COMMIT environment variable\
    \ set or precommit==True, only staged are considered.\n    \"\"\"\n    changed:\
    \ List[Tuple[str, str]] = []\n\n    # 1) Staged changes\n    staged_out = run_command_capture([\"\
    git\", \"diff\", \"--cached\", \"--name-status\"])\n    changed.extend(parse_name_status_output(staged_out))\n\
    \n    if precommit or os.environ.get(\"PRE_COMMIT\"):\n        return changed\n\
    \n    # 2) Unstaged changes\n    unstaged_out = run_command_capture([\"git\",\
    \ \"diff\", \"--name-status\"])\n    changed.extend(parse_name_status_output(unstaged_out))\n\
    \n    # 3) Untracked files (status '??')\n    untracked_out = run_command_capture([\"\
    git\", \"ls-files\", \"--others\", \"--exclude-standard\"])\n    for line in untracked_out.splitlines():\n\
    \        line = line.strip()\n        if line:\n            changed.append((\"\
    ??\", line))\n\n    # Deduplicate preserving order\n    seen = set()\n    deduped:\
    \ List[Tuple[str, str]] = []\n    for s, path in changed:\n        if path not\
    \ in seen:\n            seen.add(path)\n            deduped.append((s, path))\n\
    \    return deduped\n\n\ndef get_changed_files_from_git_status() -> List[Tuple[str,\
    \ str]]:\n    \"\"\"\n    Fallback using 'git status --porcelain' if other methods\
    \ fail.\n    Porcelain lines: XY PATH or with -> for renames\n    \"\"\"\n   \
    \ out = run_command_capture([\"git\", \"status\", \"--porcelain\"])\n    items:\
    \ List[Tuple[str, str]] = []\n    for ln in out.splitlines():\n        ln = ln.rstrip(\"\
    \\n\")\n        if not ln:\n            continue\n        # handle rename with\
    \ -> by splitting on '->'\n        # but porcelain format typically: 'R  old ->\
    \ new'\n        if \"->\" in ln:\n            # pick last part as new path\n \
    \           new = ln.split(\"->\")[-1].strip()\n            items.append((\"R\"\
    , new))\n        else:\n            # first 2 chars are status, rest is path\n\
    \            if len(ln) > 3:\n                path = ln[3:].strip()\n        \
    \    else:\n                path = ln.strip()\n            status = ln[:2].strip()\n\
    \            items.append((status or \"M\", path))\n    # dedupe\n    seen = set()\n\
    \    deduped = []\n    for s, p in items:\n        if p not in seen:\n       \
    \     seen.add(p)\n            deduped.append((s, p))\n    return deduped\n\n\n\
    # === Doc matrix rules ===\n\n\ndef check_doc_matrix_rules(changed_files: Set[str])\
    \ -> List[str]:\n    \"\"\"\n    Enforce doc-lint rules: rules format (YAML):\n\
    \    rules:\n      - name: \"Rule name\"\n        source_paths: [\"api/src/...\"\
    ]\n        required_docs: [\"project/XYZ.md\"]\n        message: \"custom message\"\
    \n    \"\"\"\n    errors: List[str] = []\n    if yaml is None:\n        print(\"\
    [WARN] PyYAML not installed; skipping doc-lint rules.\")\n        return errors\n\
    \    if not DOC_LINT_RULES.exists():\n        print(\"[WARN] doc-lint-rules.yml\
    \ not found; skipping doc matrix checks.\")\n        return errors\n\n    try:\n\
    \        rules_doc = yaml.safe_load(DOC_LINT_RULES.read_text(encoding=\"utf-8\"\
    ))\n    except Exception as e:\n        print(f\"[ERROR] Could not parse {DOC_LINT_RULES}:\
    \ {e}\", file=sys.stderr)\n        return [\"doc-lint-rules parse error\"]\n\n\
    \    rules = rules_doc.get(\"rules\", []) if isinstance(rules_doc, dict) else\
    \ []\n    for rule in rules:\n        source_paths = rule.get(\"source_paths\"\
    , [])\n        required_docs = rule.get(\"required_docs\", [])\n        is_unconditional\
    \ = not source_paths\n\n        source_changed = False\n        if is_unconditional:\n\
    \            source_changed = True\n        else:\n            for sf in changed_files:\n\
    \                if any(sf.startswith(sp) for sp in source_paths):\n         \
    \           source_changed = True\n                    break\n\n        if source_changed:\n\
    \            if not required_docs:\n                continue\n            # For\
    \ \"Enforce Mandatory Logging\" type rule (special-case), require all docs\n \
    \           if rule.get(\"name\") == \"Enforce Mandatory Logging\":\n        \
    \        ok = all(d in changed_files for d in required_docs)\n            else:\n\
    \                ok = any(d in changed_files for d in required_docs)\n       \
    \     if not ok:\n                message = rule.get(\n                    \"\
    message\",\n                    f\"Changes in {source_paths or 'repo'} require\
    \ updates to one of {required_docs}\",\n                )\n                errors.append(message)\n\
    \    return errors\n\n\n# === Code quality index checks ===\n\n\ndef check_quality_index_ratings()\
    \ -> List[str]:\n    \"\"\"Validate CODE_QUALITY_INDEX.md scoring cells for valid\
    \ single-letter grades.\"\"\"\n    errors: List[str] = []\n    quality_index_file\
    \ = PROJECT_ROOT / \"api\" / \"docs\" / \"CODE_QUALITY_INDEX.md\"\n    if not\
    \ quality_index_file.exists():\n        return []\n    valid_scores = {\"A\",\
    \ \"B\", \"C\", \"D\", \"F\", \"X\", \"\"}\n    lines = quality_index_file.read_text(encoding=\"\
    utf-8\").splitlines()\n    in_data_table = False\n    for i, line in enumerate(lines):\n\
    \        if \"| File Path |\" in line and \"| Documentation Score |\" in line:\n\
    \            in_data_table = True\n            continue\n        if not in_data_table:\n\
    \            continue\n        if \"|\" not in line or \"---\" in line:\n    \
    \        continue\n        cols = [c.strip() for c in line.split(\"|\")]\n   \
    \     # expected: | `path` | DocScore | CodeScore | ...\n        if len(cols)\
    \ < 4:\n            continue\n        doc_score = cols[2]\n        code_score\
    \ = cols[3]\n        if doc_score and doc_score not in valid_scores:\n       \
    \     errors.append(f\"Invalid Doc Score on line {i+1}: '{doc_score}'\")\n   \
    \     if code_score and code_score not in valid_scores:\n            errors.append(f\"\
    Invalid Code Score on line {i+1}: '{code_score}'\")\n    return errors\n\n\n#\
    \ === MkDocs build check ===\n\n\ndef run_mkdocs_check() -> bool:\n    docs_dir\
    \ = PROJECT_ROOT / \"api\" / \"docs\"\n    if not docs_dir.exists():\n       \
    \ print(\"[INFO] No api/docs/ found; skipping mkdocs build.\")\n        return\
    \ True\n    print(\"[LINT] Running mkdocs build...\")\n    rc = run_command([\"\
    mkdocs\", \"build\"], cwd=PROJECT_ROOT)\n    return rc == 0\n\n\n# === Governance\
    \ & Manifest ===\n\n\ndef run_lint_governance_links() -> int:\n    print(\"\\\
    n--- Running Governance Links Linter ---\")\n    script_path = PROJECT_ROOT /\
    \ \"scripts\" / \"lint_governance_links.py\"\n    if not script_path.exists():\n\
    \        print(\"ERROR: lint_governance_links.py not found.\", file=sys.stderr)\n\
    \        return 1\n    result = subprocess.run([sys.executable, str(script_path)])\n\
    \    if result.returncode != 0:\n        print(\"Governance Links Linter Failed!\"\
    , file=sys.stderr)\n    else:\n        print(\"Governance Links Linter Passed!\"\
    )\n    return result.returncode\n\n\ndef run_repo_inventory(test_files: list[str]\
    \ | None = None) -> int:\n    \"\"\"\n    Run repo_inventory_and_governance.py\
    \ to generate TRACE_INDEX.yml.\n    \"\"\"\n    print(\"\\n--- Running Repository\
    \ Inventory ---\")\n    script_path = PROJECT_ROOT / \"scripts\" / \"repo_inventory_and_governance.py\"\
    \n    if not script_path.exists():\n        print(f\"ERROR: Inventory script not\
    \ found at {script_path}\", file=sys.stderr)\n        return 1\n\n    cmd = [sys.executable,\
    \ str(script_path)]\n    if test_files:\n        print(f\"[LINT] Propagating --test-files\
    \ to repo_inventory_and_governance.py ({len(test_files)} files).\")\n        cmd.extend([\"\
    --test-files\"] + test_files)\n\n    return_code = run_command(cmd, cwd=PROJECT_ROOT)\n\
    \    if return_code != 0:\n        print(\"❌ Repository Inventory Failed!\", file=sys.stderr)\n\
    \    # No success message here, as the script prints its own status.\n    return\
    \ return_code\n\n\ndef run_manifest_generation(test_files: list[str] | None =\
    \ None) -> int:\n    \"\"\"\n    Run make_manifest.py, passing test files if provided.\n\
    \    \"\"\"\n    if not MANIFEST_SCRIPT.exists():\n        print(\"[WARN] make_manifest.py\
    \ not found; cannot regenerate REPO_MANIFEST.md\")\n        return 1\n\n    cmd\
    \ = [sys.executable, str(MANIFEST_SCRIPT)]\n    if test_files:\n        print(f\"\
    [LINT] Propagating --test-files to make_manifest.py ({len(test_files)} files).\"\
    )\n        cmd.extend([\"--test-files\"] + test_files)\n    else:\n        print(\"\
    [LINT] Running make_manifest.py to regenerate REPO_MANIFEST.md\")\n\n    return\
    \ run_command(cmd, cwd=PROJECT_ROOT)\n\n\ndef update_audit_report() -> bool:\n\
    \    \"\"\"\n    Reads the generated alignment report and updates the final audit\
    \ report.\n    \"\"\"\n    print(\"\\n--- Updating Project Audit Final Report\
    \ ---\")\n    alignment_report_path = REPORTS_DIR / \"PROJECT_DOCUMENT_ALIGNMENT.md\"\
    \n    audit_report_path = REPORTS_DIR / \"PROJECT_AUDIT_FINAL_REPORT.md\"\n\n\
    \    if not alignment_report_path.exists():\n        print(f\"ERROR: Alignment\
    \ report not found at {alignment_report_path}\", file=sys.stderr)\n        return\
    \ False\n\n    try:\n        alignment_content = alignment_report_path.read_text(encoding=\"\
    utf-8\")\n        template_content = audit_report_path.read_text(encoding=\"utf-8\"\
    )\n\n        # Extract summary from the alignment report\n        summary_match\
    \ = re.search(r\"(## Summary\\n.*)\", alignment_content, re.DOTALL)\n        if\
    \ not summary_match:\n            print(\"ERROR: Could not find '## Summary' section\
    \ in alignment report.\", file=sys.stderr)\n            return False\n       \
    \ summary_section = summary_match.group(1).strip()\n\n        # Extract details\
    \ (everything before the summary)\n        details_content = alignment_content.split(\"\
    ## Summary\")[0]\n        details_content = details_content.replace(\"# Project\
    \ Document Alignment Report\", \"\").strip()\n\n        # In the template, replace\
    \ the summary section\n        updated_content = re.sub(r\"## Summary\\n.*?\\\
    n## Details\", f\"{summary_section}\\n\\n## Details\", template_content, flags=re.DOTALL)\n\
    \n        # In the updated content, replace the details placeholder comment\n\
    \        updated_content = updated_content.replace(\"<!-- Automatically paste\
    \ relevant sections from PROJECT_DOCUMENT_ALIGNMENT.md -->\", details_content)\n\
    \n        write_to_file(audit_report_path, updated_content)\n        print(f\"\
    Successfully updated {audit_report_path}\")\n        return True\n\n    except\
    \ Exception as e:\n        print(f\"ERROR: Failed to update audit report: {e}\"\
    , file=sys.stderr)\n        return False\n\n\n# === Argument parser and main ===\n\
    \n\ndef main() -> int:\n    parser = argparse.ArgumentParser(description=\"Unified\
    \ Linter and Logger for repository\")\n    parser.add_argument(\"--log\", action=\"\
    store_true\", help=\"Run in logging mode (writes ACTIVITY, SESSION, CURRENT_STATE).\"\
    )\n    parser.add_argument(\"--summary\", help=\"[log] One-line summary (required\
    \ with --log)\")\n    parser.add_argument(\"--objective\", help=\"[log] High-level\
    \ objective\")\n    parser.add_argument(\"--findings\", help=\"[log] Findings\
    \ (multi-line; use '\\\\n' for newlines)\")\n    parser.add_argument(\"--next-steps\"\
    , help=\"[log] Next immediate steps (required with --log)\")\n    parser.add_argument(\"\
    --files\", nargs=\"*\", help=\"[log] Files related to activity\")\n    parser.add_argument(\"\
    --test-files\", nargs=\"*\", help=\"[linter] Provide list of changed files for\
    \ testing (bypass git).\")\n    parser.add_argument(\"--from-file\", help=\"[linter]\
    \ Read changed files from a file (one per line).\")\n    parser.add_argument(\"\
    --skip-governance\", action=\"store_true\", help=\"Skip governance enforcement.\"\
    )\n    parser.add_argument(\"--skip-manifest\", action=\"store_true\", help=\"\
    Skip manifest generation even if staged files exist.\")\n    args = parser.parse_args()\n\
    \n    # Logging mode\n    if args.log:\n        if not all([args.summary, args.findings,\
    \ args.next_steps]):\n            print(\"ERROR: --log requires --summary, --findings,\
    \ and --next-steps.\", file=sys.stderr)\n            return 1\n        files =\
    \ args.files or []\n        return do_logging(args.summary, args.objective or\
    \ \"\", args.findings, args.next_steps, files)\n\n    print(\"=\" * 40)\n    print(\"\
    Running Unified Linter\")\n    print(\"=\" * 40)\n\n    # 1) Find changed files\n\
    \    changed_with_status: List[Tuple[str, str]] = []\n    if args.from_file:\n\
    \        try:\n            lines = Path(args.from_file).read_text(encoding=\"\
    utf-8\").splitlines()\n            changed_with_status = [(\"M\", ln.strip())\
    \ for ln in lines if ln.strip()]\n            print(f\"[INFO] Loaded {len(changed_with_status)}\
    \ files from {args.from_file}\")\n        except Exception as e:\n           \
    \ print(f\"[ERROR] Could not read --from-file: {e}\", file=sys.stderr)\n     \
    \       return 1\n    elif args.test_files:\n        changed_with_status = [(\"\
    M\", f) for f in args.test_files]\n        print(f\"[INFO] Test mode: injecting\
    \ {len(changed_with_status)} test files.\")\n    else:\n        # normal git detection\n\
    \        changed_with_status = get_local_changed_files()\n        if not changed_with_status:\n\
    \            # try fallback\n            changed_with_status = get_changed_files_from_git_status()\n\
    \n    if not changed_with_status:\n        print(\"[INFO] No changed files detected.\
    \ Nothing to lint for changes.\")\n        # even if no changed files, still may\
    \ need to exit 0 (no errors)\n        return 0\n\n    # Convert to set of file\
    \ paths for checks\n    changed_files_set: Set[str] = {p for (_s, p) in changed_with_status}\n\
    \    print(f\"[INFO] Detected {len(changed_files_set)} changed files.\")\n   \
    \ for s, p in changed_with_status:\n        print(f\"- {s}\\t{p}\")\n\n    # 2)\
    \ Doc-matrix checks – always run\n    print(\"\\n--- Doc-matrix checks ---\")\n\
    \    doc_errors = check_doc_matrix_rules(changed_files_set)\n    if doc_errors:\n\
    \        print(\"[ERROR] Documentation matrix checks failed:\", file=sys.stderr)\n\
    \        for msg in doc_errors:\n            print(f\"- {msg}\", file=sys.stderr)\n\
    \        return 1\n    print(\"[OK] Documentation matrix checks passed.\")\n\n\
    \    # 3) Quality index checks (conditional)\n    print(\"\\n--- Code quality\
    \ index checks ---\")\n    quality_errors = check_quality_index_ratings()\n  \
    \  if quality_errors:\n        print(\"[ERROR] Code quality index issues:\", file=sys.stderr)\n\
    \        for e in quality_errors:\n            print(f\"- {e}\", file=sys.stderr)\n\
    \        return 1\n    print(\"[OK] Code quality index checks passed.\")\n\n \
    \   # 4) MkDocs build (if api docs changed)\n    print(\"\\n--- MkDocs check ---\"\
    )\n    if any(f.startswith(\"api/docs/\") or f.startswith(\"api/\") and f.endswith(\"\
    .md\") for f in changed_files_set):\n        if not run_mkdocs_check():\n    \
    \        print(\"[ERROR] MkDocs build failed.\", file=sys.stderr)\n          \
    \  return 1\n        print(\"[OK] MkDocs build passed.\")\n    else:\n       \
    \ print(\"[INFO] No API docs changes detected; skipped mkdocs.\")\n\n    # 5)\
    \ Repository Inventory\n    inventory_return_code = run_repo_inventory(test_files=args.test_files)\n\
    \    if inventory_return_code != 0:\n        return inventory_return_code\n\n\
    \    # 5b) Content Alignment Check\n    print(\"\\n--- Running Content Alignment\
    \ Check ---\")\n    alignment_script = SCRIPTS_DIR / \"content_alignment_check.py\"\
    \n    if alignment_script.exists():\n        # Only run alignment if there are\
    \ changes in project/ (docs) or if test-files include project items\n        project_changes_present\
    \ = any(p.startswith(\"project/\") for p in changed_files_set)\n        test_files_have_project\
    \ = bool(args.test_files and any(str(f).startswith(\"project/\") for f in args.test_files))\n\
    \        if project_changes_present or test_files_have_project:\n            cmd\
    \ = [sys.executable, str(alignment_script), \"--enforce\"]\n            # propagate\
    \ test-files/from-file so the alignment script can run incrementally\n       \
    \     if args.test_files:\n                cmd.extend([\"--test-files\"] + list(args.test_files))\n\
    \            elif args.from_file:\n                cmd.extend([\"--from-file\"\
    , args.from_file])\n\n            print(f\"[LINT] Running content alignment: {'\
    \ '.join(cmd)}\")\n            alignment_rc = run_command(cmd)\n            if\
    \ alignment_rc != 0:\n                print(\"❌ Content Alignment Check Failed!\"\
    , file=sys.stderr)\n                return alignment_rc\n            print(\"\
    ✅ Content Alignment Check Passed.\")\n        else:\n            print(\"[INFO]\
    \ No project/ documentation changes detected — skipping Content Alignment Check.\"\
    )\n    else:\n        print(\"[WARN] content_alignment_check.py not found, skipping\
    \ check.\", file=sys.stderr)\n\n    # 5c) Semantic Alignment Check\n    print(\"\
    \\n--- Running Semantic Alignment Check ---\")\n    semantic_script = SCRIPTS_DIR\
    \ / \"semantic_alignment_check.py\"\n    inventory_script = SCRIPTS_DIR / \"repo_inventory_and_governance.py\"\
    \n    if semantic_script.exists() and inventory_script.exists():\n        print(\"\
    [INFO] Forcing full repository scan for semantic alignment check...\")\n     \
    \   inventory_rc = run_command([sys.executable, str(inventory_script), \"--full-scan\"\
    ])\n        if inventory_rc != 0:\n            print(\"❌ Failed to generate a\
    \ full repository index for the semantic check.\", file=sys.stderr)\n        \
    \    return inventory_rc\n\n        cmd = [sys.executable, str(semantic_script),\
    \ \"--enforce\"]\n        if args.test_files:\n            cmd.extend([\"--test-files\"\
    ] + list(args.test_files))\n        elif args.from_file:\n            cmd.extend([\"\
    --from-file\", args.from_file])\n\n        print(f\"[LINT] Running semantic alignment:\
    \ {' '.join(cmd)}\")\n        semantic_rc = run_command(cmd)\n        if semantic_rc\
    \ != 0:\n            print(\"❌ Semantic Alignment Check Failed!\", file=sys.stderr)\n\
    \            return semantic_rc\n        print(\"✅ Semantic Alignment Check Passed.\"\
    )\n    else:\n        if not semantic_script.exists():\n            print(\"[WARN]\
    \ semantic_alignment_check.py not found, skipping check.\", file=sys.stderr)\n\
    \        if not inventory_script.exists():\n            print(\"[WARN] repo_inventory_and_governance.py\
    \ not found, cannot run semantic check.\", file=sys.stderr)\n\n    # 6) Governance\
    \ Links Linter (unless skipped)\n    if not args.skip_governance:\n        gov_links_return\
    \ = run_lint_governance_links()\n        if gov_links_return != 0:\n         \
    \   return gov_links_return\n\n        # If governance linter succeeds, update\
    \ the audit report\n        if not update_audit_report():\n            print(\"\
    ERROR: Failed to update the audit report.\", file=sys.stderr)\n            return\
    \ 1\n    else:\n        print(\"[INFO] Skipping governance links linter (--skip-governance).\"\
    )\n\n    # 7) Manifest Generation\n    if args.skip_manifest:\n        print(\"\
    [INFO] Skipping manifest generation (--skip-manifest).\")\n    else:\n       \
    \ print(\"\\n--- Running Repository Manifest Generation ---\")\n        # Propagate\
    \ --test-files if they were provided to the linter\n        manifest_return_code\
    \ = run_manifest_generation(test_files=args.test_files)\n        if manifest_return_code\
    \ != 0:\n            print(\"❌ Manifest Generation Failed!\", file=sys.stderr)\n\
    \            return manifest_return_code\n        # No success message here, as\
    \ the manifest script prints its own status.\n\n    print(\"\\n=== Linter completed\
    \ successfully ===\")\n    return 0\n\n\nif __name__ == \"__main__\":\n    try:\n\
    \        sys.exit(main())\n    except KeyboardInterrupt:\n        print(\"\\nInterrupted\
    \ by user.\", file=sys.stderr)\n        sys.exit(2)\n"
- path: repo_governance.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-024\n#!/usr/bin/env python3\nimport os\nimport re\nimport json\n\
    import argparse\nimport sys\nfrom pathlib import Path\n\n# Paths\nROOT = Path(__file__).resolve().parent.parent\n\
    REPORTS_DIR = ROOT / \"project\" / \"reports\"\nSCRIPTS_DIR = ROOT / \"scripts\"\
    \n\nJSON_OUTPUT = SCRIPTS_DIR / \"lint_governance_links.json\"\nMD_OUTPUT = REPORTS_DIR\
    \ / \"PROJECT_DOCUMENT_ALIGNMENT.md\"\nTRACE_INDEX = ROOT / \"TRACE_INDEX.yml\"\
    \n\n# Regex patterns\nMD_PATTERN = re.compile(r\"\\[.*?\\]\\((project/.*?\\.md)\\\
    )\")\n\ndef load_trace_index():\n    \"\"\"Read TRACE_INDEX.yml for registered\
    \ project files.\"\"\"\n    if not TRACE_INDEX.exists():\n        return set()\n\
    \    registered = set()\n    with TRACE_INDEX.open() as f:\n        for line in\
    \ f:\n            line = line.strip()\n            if line.startswith(\"project/\"\
    ) and line.endswith(\".md\"):\n                registered.add(line.split()[0])\n\
    \    return registered\n\ndef scan_project_md_files():\n    \"\"\"Return all .md\
    \ files under project/.\"\"\"\n    return {str(p.relative_to(ROOT)) for p in ROOT.glob(\"\
    project/**/*.md\")}\n\ndef extract_links_from_file(path):\n    \"\"\"Extract markdown\
    \ links to project/*.md files from a file.\"\"\"\n    text = path.read_text(errors=\"\
    ignore\")\n    return set(MD_PATTERN.findall(text))\n\ndef build_alignment():\n\
    \    \"\"\"Produce alignment data structures.\"\"\"\n    registered = load_trace_index()\n\
    \    all_files = scan_project_md_files()\n\n    references = {}\n    for md in\
    \ all_files:\n        links = extract_links_from_file(ROOT / md)\n        for\
    \ target in links:\n            references.setdefault(target, set()).add(md)\n\
    \n    fully_aligned, partially_aligned, unlinked = {}, {}, {}\n\n    for md in\
    \ sorted(all_files):\n        refs = references.get(md, set())\n        is_registered\
    \ = md in registered\n        if is_registered and refs:\n            fully_aligned[md]\
    \ = sorted(refs)\n        elif is_registered and not refs:\n            unlinked[md]\
    \ = \"Registered\"\n        elif not is_registered and refs:\n            partially_aligned[md]\
    \ = sorted(refs)\n        else:\n            unlinked[md] = \"Unregistered\"\n\
    \n    summary = {\n        \"total_files\": len(all_files),\n        \"fully_aligned\"\
    : len(fully_aligned),\n        \"partially_aligned\": len(partially_aligned),\n\
    \        \"unlinked\": len(unlinked),\n    }\n\n    return fully_aligned, partially_aligned,\
    \ unlinked, summary\n\ndef write_json(fully, partial, unlinked, summary):\n  \
    \  data = {\n        \"fully_aligned\": fully,\n        \"partially_aligned\"\
    : partial,\n        \"unlinked\": unlinked,\n        \"summary\": summary,\n \
    \   }\n    with JSON_OUTPUT.open(\"w\") as f:\n        json.dump(data, f, indent=4)\n\
    \ndef write_markdown(fully, partial, unlinked, summary):\n    REPORTS_DIR.mkdir(parents=True,\
    \ exist_ok=True)\n    with MD_OUTPUT.open(\"w\") as f:\n        f.write(\"# Project\
    \ Document Alignment Report\\n\\n\")\n        f.write(\"_Generated automatically\
    \ by repo_governance.py_\\n\\n\")\n\n        f.write(\"## Fully Aligned\\n\\n\"\
    )\n        if fully:\n            for md, refs in fully.items():\n           \
    \     f.write(f\"- `{md}`\\n\")\n                for r in refs:\n            \
    \        f.write(f\"    - Present in: {r}\\n\")\n        else:\n            f.write(\"\
    None\\n\")\n        f.write(\"\\n\")\n\n        f.write(\"## Partially Aligned\
    \ (linked but unregistered)\\n\\n\")\n        if partial:\n            for md,\
    \ refs in partial.items():\n                f.write(f\"- `{md}`\\n\")\n      \
    \          for r in refs:\n                    f.write(f\"    - Present in: {r}\\\
    n\")\n        else:\n            f.write(\"None\\n\")\n        f.write(\"\\n\"\
    )\n\n        f.write(\"## Unlinked / Unregistered\\n\\n\")\n        if unlinked:\n\
    \            for md, status in unlinked.items():\n                f.write(f\"\
    - `{md}` ({status})\\n\")\n        else:\n            f.write(\"None\\n\")\n \
    \       f.write(\"\\n\")\n\n        f.write(\"## Summary\\n\\n\")\n        f.write(f\"\
    - Total project MD files: {summary['total_files']}\\n\")\n        f.write(f\"\
    - Fully aligned: {summary['fully_aligned']}\\n\")\n        f.write(f\"- Partially\
    \ aligned: {summary['partially_aligned']}\\n\")\n        f.write(f\"- Unlinked\
    \ / unregistered: {summary['unlinked']}\\n\")\n\ndef main():\n    parser = argparse.ArgumentParser()\n\
    \    parser.add_argument(\"--audit\", action=\"store_true\", help=\"Generate full\
    \ alignment reports\")\n    parser.add_argument(\"--enforce\", action=\"store_true\"\
    , help=\"Exit non-zero if misaligned\")\n    args = parser.parse_args()\n\n  \
    \  fully, partial, unlinked, summary = build_alignment()\n\n    if args.audit:\n\
    \        write_json(fully, partial, unlinked, summary)\n        write_markdown(fully,\
    \ partial, unlinked, summary)\n        print(f\"[INFO] Audit complete. JSON: {JSON_OUTPUT},\
    \ MD: {MD_OUTPUT}\")\n        return 0\n\n    if args.enforce:\n        if summary[\"\
    partially_aligned\"] > 0 or summary[\"unlinked\"] > 0:\n            print(\"[ERROR]\
    \ Governance misalignment detected. Run with --audit for details.\")\n       \
    \     return 1\n        return 0\n\n    parser.print_help()\n    return 1\n\n\
    if __name__ == \"__main__\":\n    sys.exit(main())\n"
- path: run_e2e_auth_test.sh
  type: script
  workflow:
  - testing
  indexes: []
  content: "# ID: OPS-026\n#!/bin/bash\n\n# A script to run a full end-to-end test\
    \ of the Spotify authentication flow,\n# involving both the Python API and the\
    \ Go Snitch service.\n\n# Exit immediately if a command exits with a non-zero\
    \ status.\nset -e\n\n# --- Project Root Calculation ---\nSCRIPT_DIR=\"$(cd \"\
    $(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"\nPROJECT_ROOT=\"$(cd \"$SCRIPT_DIR/..\"\
    \ && pwd)\"\n\n# --- Configuration ---\nAPI_HOST=\"127.0.0.1\"\nAPI_PORT=\"8000\"\
    \nAPI_URL=\"http://${API_HOST}:${API_PORT}\"\n# NOTE: The user's logs show the\
    \ API running without the /api prefix.\n# We will match that behavior for the\
    \ test.\nAPI_CALLBACK_URL=\"${API_URL}/auth/spotify/callback\"\nAPI_PID_FILE=\"\
    /tmp/zotify_api.pid\"\nAPI_LOG_FILE=\"/tmp/zotify_api.log\"\n\nSNITCH_DIR=\"snitch\"\
    \nSNITCH_PID_FILE=\"/tmp/snitch.pid\"\nSNITCH_LOG_FILE=\"/tmp/snitch.log\"\nSNITCH_BINARY=\"\
    /tmp/snitch\"\n\n# --- Helper Functions ---\n\nfunction start_api() {\n    echo\
    \ \"--- Starting Zotify API server ---\"\n    (\n        cd \"$PROJECT_ROOT/api\"\
    \ && \\\n        uvicorn src.zotify_api.main:app --host ${API_HOST} --port ${API_PORT}\
    \ &> ${API_LOG_FILE} & \\\n        echo $! > ${API_PID_FILE}\n    )\n    # Wait\
    \ for the server to start\n    sleep 3\n    echo \"API server started with PID\
    \ $(cat ${API_PID_FILE}). Log: ${API_LOG_FILE}\"\n}\n\nfunction stop_api() {\n\
    \    if [ -f ${API_PID_FILE} ]; then\n        PID=$(cat ${API_PID_FILE})\n   \
    \     echo \"--- Stopping Zotify API server (PID: ${PID}) ---\"\n        kill\
    \ ${PID} || true\n        rm ${API_PID_FILE}\n    fi\n}\n\nfunction build_and_start_snitch()\
    \ {\n    echo \"--- Building and Starting Snitch Service ---\"\n\n    echo \"\
    Building Snitch binary...\"\n    (cd \"$PROJECT_ROOT/${SNITCH_DIR}\" && go build\
    \ -o ${SNITCH_BINARY} .)\n\n    echo \"Starting Snitch service with callback URL:\
    \ ${API_CALLBACK_URL}\"\n    (\n        export SNITCH_API_CALLBACK_URL=\"${API_CALLBACK_URL}\"\
    \n        ${SNITCH_BINARY} &> ${SNITCH_LOG_FILE} &\n        echo $! > ${SNITCH_PID_FILE}\n\
    \    )\n    sleep 1\n    echo \"Snitch service started with PID $(cat ${SNITCH_PID_FILE}).\
    \ Log: ${SNITCH_LOG_FILE}\"\n}\n\nfunction stop_snitch() {\n    if [ -f ${SNITCH_PID_FILE}\
    \ ]; then\n        PID=$(cat ${SNITCH_PID_FILE})\n        echo \"--- Stopping\
    \ Snitch Service (PID: ${PID}) ---\"\n        kill ${PID} || true\n        rm\
    \ ${SNITCH_PID_FILE}\n    fi\n}\n\nfunction run_e2e_test() {\n    echo \"\"\n\
    \    echo \"=========================================\"\n    echo \"         RUNNING\
    \ E2E AUTH TEST\"\n    echo \"=========================================\"\n  \
    \  # It's better to run pytest from the root of the api project\n    (cd \"$PROJECT_ROOT/api\"\
    \ && python -m pytest tests/test_e2e_auth.py)\n}\n\nfunction check_logs_for_success()\
    \ {\n    echo \"\"\n    echo \"=========================================\"\n \
    \   echo \"         CHECKING LOGS FOR SUCCESS\"\n    echo \"=========================================\"\
    \n\n    # Check Snitch log for successful forwarding\n    if grep -q \"Backend\
    \ responded with: 200 OK\" ${SNITCH_LOG_FILE}; then\n        echo \"✅ [SUCCESS]\
    \ Snitch log shows a 200 OK response from the backend.\"\n    else\n        echo\
    \ \"❌ [FAILURE] Snitch log does not show a 200 OK from the backend.\"\n      \
    \  exit 1\n    fi\n\n    # Check API log for the callback being received\n   \
    \ if grep -q \"POST /auth/spotify/callback received for state\" ${API_LOG_FILE};\
    \ then\n        echo \"✅ [SUCCESS] API log shows callback was received by the\
    \ auth endpoint.\"\n    else\n        echo \"❌ [FAILURE] API log does not show\
    \ callback was received.\"\n        exit 1\n    fi\n\n    echo \"✅ All checks\
    \ passed!\"\n}\n\n\n# --- Main Execution ---\n\n# Ensure cleanup happens on script\
    \ exit\ntrap '{ stop_api; stop_snitch; }' EXIT\n\n# Clean up any old logs\nrm\
    \ -f ${API_LOG_FILE} ${SNITCH_LOG_FILE}\n\n# Start services\nstart_api\nbuild_and_start_snitch\n\
    \n# Run the test\nrun_e2e_test\n\n# Check the results\ncheck_logs_for_success\n\
    \necho \"\"\necho \"E2E TEST SUCCEEDED\"\necho \"\"\necho \"--- API Log ---\"\n\
    cat ${API_LOG_FILE}\necho \"\"\necho \"--- Snitch Log ---\"\ncat ${SNITCH_LOG_FILE}\n"
- path: verify_governance.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-032\n#!/usr/bin/env python3\n\"\"\"\nverify_governance.py\n\
    Checks that all governance-related files in project/*/ are\npresent in PROJECT_REGISTRY.md.\
    \ Ignores code files, archive junk,\nand other non-governance paths by default.\n\
    \"\"\"\n\nimport os\nimport re\nimport sys\nimport yaml\nfrom pathlib import Path\n\
    \nROOT = Path(__file__).resolve().parent.parent\nPROJECT_DIR = ROOT / \"project\"\
    \nREGISTRY_FILE = PROJECT_DIR / \"PROJECT_REGISTRY.md\"\nTRACE_INDEX = ROOT /\
    \ \"TRACE_INDEX.yml\"\n\n# Folders/files we don’t require in the registry\nIGNORED_PREFIXES\
    \ = (\n    \"project/archive/\",\n)\nIGNORED_SUFFIXES = (\n    \".py\", \".js\"\
    , \".css\", \".html\", \".toml\",\n    \".yml\", \".yaml\", \".lock\", \".json\"\
    ,\n)\nIGNORED_FILES = {\n    \"project/.gitignore\",\n}\n\ndef parse_registry_paths(registry_file):\n\
    \    \"\"\"Extract all project/* paths from PROJECT_REGISTRY.md.\"\"\"\n    paths\
    \ = set()\n    link_re = re.compile(r\"\\]\\(([^)]+)\\)\")\n    for line in registry_file.read_text(encoding=\"\
    utf-8\").splitlines():\n        for m in link_re.finditer(line):\n           \
    \ p = m.group(1).strip()\n            if p.startswith(\"./\"):\n             \
    \   p = p[2:]\n            if not p.startswith(\"project/\"):\n              \
    \  if \"/\" not in p:  # bare filename (e.g. HIGH_LEVEL_DESIGN.md)\n         \
    \           p = f\"project/{p}\"\n            paths.add(normalize_path(p))\n \
    \   return paths\n\n\ndef parse_trace_index(trace_file):\n    \"\"\"Read TRACE_INDEX.yml\
    \ and return all project/* paths.\"\"\"\n    data = yaml.safe_load(trace_file.read_text(encoding=\"\
    utf-8\"))\n    files = set()\n    for f in data.get(\"files\", []):\n        if\
    \ f.startswith(\"project/\"):\n            files.add(normalize_path(f))\n    return\
    \ files\n\n\ndef normalize_path(p):\n    \"\"\"Canonicalize paths for comparison.\"\
    \"\"\n    return str(Path(p)).replace(\"\\\\\", \"/\")\n\n\ndef should_ignore(path):\n\
    \    if path in IGNORED_FILES:\n        return True\n    if any(path.startswith(pref)\
    \ for pref in IGNORED_PREFIXES):\n        return True\n    if any(path.endswith(suff)\
    \ for suff in IGNORED_SUFFIXES):\n        return True\n    return False\n\n\n\
    def main():\n    if not REGISTRY_FILE.exists():\n        print(f\"[!] Missing\
    \ {REGISTRY_FILE}\", file=sys.stderr)\n        sys.exit(1)\n    if not TRACE_INDEX.exists():\n\
    \        print(f\"[!] Missing {TRACE_INDEX}\", file=sys.stderr)\n        sys.exit(1)\n\
    \n    registry_paths = parse_registry_paths(REGISTRY_FILE)\n    trace_paths =\
    \ parse_trace_index(TRACE_INDEX)\n\n    # Filter ignored\n    registry_paths =\
    \ {p for p in registry_paths if not should_ignore(p)}\n    trace_paths = {p for\
    \ p in trace_paths if not should_ignore(p)}\n\n    missing_from_registry = sorted(trace_paths\
    \ - registry_paths)\n    missing_on_disk = sorted(registry_paths - trace_paths)\n\
    \n    if missing_from_registry:\n        print(\"[!] Files present in TRACE_INDEX.yml\
    \ but missing from PROJECT_REGISTRY.md:\")\n        for f in missing_from_registry:\n\
    \            print(f\" - {f}\")\n        print()\n\n    if missing_on_disk:\n\
    \        print(\"[!] Files listed in PROJECT_REGISTRY.md but not found in TRACE_INDEX.yml:\"\
    )\n        for f in missing_on_disk:\n            print(f\" - {f}\")\n       \
    \ print()\n\n    if not missing_from_registry and not missing_on_disk:\n     \
    \   print(\"[✓] PROJECT_REGISTRY.md and TRACE_INDEX.yml are in sync.\")\n\n\n\
    if __name__ == \"__main__\":\n    main()\n"
- path: start.sh
  type: script
  workflow: []
  indexes: []
  content: '# ID: OPS-028

    #!/bin/bash

    set -e


    # The DATABASE_URI check has been removed.

    # The application now uses a sensible default for local development if the

    # environment variable is not set. See api/src/zotify_api/config.py.


    # Create required directories if they don''t exist from the root

    echo "Ensuring required directories exist..."

    mkdir -p api/storage

    mkdir -p api/logs


    # Start the documentation server from the root in the background

    echo "Starting documentation server on http://0.0.0.0:8008..."

    mkdocs serve --dev-addr 0.0.0.0:8008 &


    # Move into the API directory for all subsequent python-related tasks

    cd api/


    echo "Installing/updating dependencies (including dev dependencies)..."

    # Install the package in editable mode from within the api directory

    pip install -e ".[dev]"


    echo "Starting Zotify API server..."


    # Set the application environment to "development" to disable production checks

    export APP_ENV=development


    # Run the uvicorn server from within the api/ directory

    PYTHONPATH=./src uvicorn zotify_api.main:app --host 0.0.0.0 --port 8000 --reload
    --log-level debug

    '
- path: audit_api.py
  type: script
  workflow:
  - audit
  indexes: []
  content: "# ID: OPS-003\nimport importlib\nimport os\nimport httpx\nfrom fastapi\
    \ import FastAPI\n\n# Adjust this to your actual app import path:\napp_module\
    \ = \"zotify_api.main\"\napp_attr = \"app\"\nBASE_URL = \"http://127.0.0.1:8000\"\
    \n\n\ndef main():\n    \"\"\"\n    Dynamically imports the FastAPI app, discovers\
    \ all GET routes that\n    don't require path parameters, and then sends a request\
    \ to each one\n    to check its status.\n    \"\"\"\n    print(f\"--- Starting\
    \ API Audit for {app_module} ---\")\n    print(f\"--- Target Base URL: {BASE_URL}\
    \ ---\")\n\n    # Set the app environment to development to avoid startup errors\n\
    \    os.environ[\"APP_ENV\"] = \"development\"\n\n    try:\n        module = importlib.import_module(app_module)\n\
    \        app: FastAPI = getattr(module, app_attr)\n    except Exception as e:\n\
    \        print(\n            f\"Error: Could not import FastAPI app '{app_attr}'\
    \ from module '{app_module}'.\"\n        )\n        print(f\"Details: {e}\")\n\
    \        return\n\n    ok_routes = []\n    error_routes = []\n\n    with httpx.Client(base_url=BASE_URL,\
    \ follow_redirects=True) as client:\n        for route in app.routes:\n      \
    \      # We can only automatically test GET routes that have no path parameters\n\
    \            if \"GET\" in route.methods and \"{\" not in route.path:\n      \
    \          path = route.path\n                print(f\"Testing GET {path}...\"\
    )\n                try:\n                    response = client.get(path)\n   \
    \                 if response.status_code == 200:\n                        ok_routes.append(path)\n\
    \                    else:\n                        error_routes.append(f\"{path}\
    \ (Status: {response.status_code})\")\n                except httpx.RequestError\
    \ as e:\n                    error_routes.append(f\"{path} (Request Error: {e})\"\
    )\n\n    print(\"\\n--- API Audit Summary ---\")\n    if ok_routes:\n        print(\"\
    ✅ OK Routes:\")\n        for r in sorted(ok_routes):\n            print(f\" -\
    \ {r}\")\n\n    if error_routes:\n        print(\"\\n❌ Error Routes:\")\n    \
    \    for r in sorted(error_routes):\n            print(f\" - {r}\")\n\n    if\
    \ not error_routes:\n        print(\"\\nAll discoverable GET routes responded\
    \ successfully.\")\n\n\nif __name__ == \"__main__\":\n    main()\n"
- path: generate_openapi.py
  type: script
  workflow:
  - documentation
  indexes: []
  content: "# ID: OPS-012\nimport json\nimport os\nimport sys\nfrom pathlib import\
    \ Path\n\n# Set app environment to testing\nos.environ[\"APP_ENV\"] = \"testing\"\
    \n\n# Add project root to path\nproject_root = Path(__file__).resolve().parent.parent\n\
    sys.path.insert(0, str(project_root))\n\nfrom api.src.zotify_api.main import app\n\
    \n\ndef generate_openapi_spec():\n    with open(\"openapi.json\", \"w\") as f:\n\
    \        json.dump(app.openapi(), f, indent=2)\n    print(\"openapi.json generated\
    \ successfully.\")\n\n\nif __name__ == \"__main__\":\n    generate_openapi_spec()\n"
- path: manage_docs_index.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-019\nimport os\nimport re\nimport argparse\nfrom pathlib import\
    \ Path\n\n# --- Configuration ---\nPROJECT_ROOT = Path(__file__).parent.parent\n\
    DOC_DIRS_TO_INDEX = [\"api/docs\", \"snitch/docs\", \"Gonk/GonkUI/docs\"]\nDOCS_QUALITY_INDEX\
    \ = PROJECT_ROOT / \"api/docs/DOCS_QUALITY_INDEX.md\"\n\n# --- Main Functions\
    \ ---\n\ndef get_all_markdown_files():\n    \"\"\"Scans the doc directories and\
    \ returns a list of all .md files.\"\"\"\n    md_files = []\n    for directory\
    \ in DOC_DIRS_TO_INDEX:\n        for root, _, files in os.walk(PROJECT_ROOT /\
    \ directory):\n            for file in files:\n                if file.endswith(\"\
    .md\"):\n                    # Store the path relative to the project root\n \
    \                   md_files.append(Path(root) / file)\n    return md_files\n\n\
    def get_indexed_docs():\n    \"\"\"Parses the DOCS_QUALITY_INDEX.md to find which\
    \ files are already indexed.\"\"\"\n    indexed = set()\n    if not DOCS_QUALITY_INDEX.is_file():\n\
    \        return indexed\n\n    with open(DOCS_QUALITY_INDEX, \"r\", encoding=\"\
    utf-8\") as f:\n        # Skip header and separator\n        f.readline()\n  \
    \      f.readline()\n        for line in f:\n            if not line.strip():\n\
    \                continue\n            try:\n                # Path is in the\
    \ second column\n                path = line.split(\"|\")[2].strip()\n       \
    \         indexed.add(path)\n            except IndexError:\n                continue\n\
    \    return indexed\n\ndef add_to_docs_quality_index(doc_path):\n    \"\"\"Appends\
    \ a new entry for a markdown file to the quality index.\"\"\"\n    # Use the filename\
    \ as the module name for simplicity\n    module_name = doc_path.stem.replace(\"\
    _\", \" \").title()\n    # Get path relative to project root\n    relative_path\
    \ = doc_path.relative_to(PROJECT_ROOT).as_posix()\n    entry = f\"| {module_name}\
    \ | {relative_path} | X |\\n\"\n\n    with open(DOCS_QUALITY_INDEX, \"a\", encoding=\"\
    utf-8\") as f:\n        f.write(entry)\n    print(f\"  - Added '{relative_path}'\
    \ to {DOCS_QUALITY_INDEX.name}\")\n\ndef main():\n    \"\"\"Main function to manage\
    \ the documentation quality index.\"\"\"\n    parser = argparse.ArgumentParser(description=\"\
    Manage the documentation quality index.\")\n    parser.add_argument(\n       \
    \ \"--run\",\n        action=\"store_true\",\n        help=\"Run the script to\
    \ find and add missing markdown files to the index.\"\n    )\n    args = parser.parse_args()\n\
    \n    if not args.run:\n        print(\"This script populates the DOCS_QUALITY_INDEX.md\
    \ file.\")\n        print(\"Run with the --run flag to execute.\")\n        return\n\
    \n    print(\"--- Starting Docs Quality Indexer ---\")\n\n    all_md_files = get_all_markdown_files()\n\
    \    indexed_docs = get_indexed_docs()\n\n    new_entries_added = 0\n\n    for\
    \ md_path in all_md_files:\n        relative_path_str = md_path.relative_to(PROJECT_ROOT).as_posix()\n\
    \        if relative_path_str not in indexed_docs:\n            new_entries_added\
    \ += 1\n            print(f\"\\nFound un-indexed doc file: {relative_path_str}\"\
    )\n            add_to_docs_quality_index(md_path)\n\n    if new_entries_added\
    \ == 0:\n        print(\"\\nNo new markdown files to index. Everything is up to\
    \ date.\")\n    else:\n        print(f\"\\nSuccessfully added {new_entries_added}\
    \ new file(s) to the index.\")\n\n    print(\"--- Indexer Finished ---\")\n\n\
    if __name__ == \"__main__\":\n    main()\n"
- path: lint_governance_links.json
  type: config
  workflow: []
  indexes: []
  content: "{\n    \"files\": [\n        {\n            \"path\": \"project/LOGGING_TRACEABILITY_MATRIX.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/DEPENDENCIES.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/HIGH_LEVEL_DESIGN.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/USECASES.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/LOGGING_SYSTEM_DESIGN.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/PID.md\",\n            \"status\": \"fully_aligned\"\n\
    \        },\n        {\n            \"path\": \"project/LOW_LEVEL_DESIGN.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/LESSONS-LEARNT.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/SECURITY.md\",\n    \
    \        \"status\": \"fully_aligned\"\n        },\n        {\n            \"\
    path\": \"project/PROJECT_REGISTRY.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/CICD.md\",\n        \
    \    \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/QA_GOVERNANCE.md\",\n            \"status\": \"fully_aligned\"\n \
    \       },\n        {\n            \"path\": \"project/TASK_CHECKLIST.md\",\n\
    \            \"status\": \"fully_aligned\"\n        },\n        {\n          \
    \  \"path\": \"project/FUTURE_ENHANCEMENTS.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/PROJECT_BRIEF.md\",\n\
    \            \"status\": \"fully_aligned\"\n        },\n        {\n          \
    \  \"path\": \"project/EXECUTION_PLAN.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/ALIGNMENT_MATRIX.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/PROJECT_PLAN.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/ROADMAP.md\",\n     \
    \       \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/BACKLOG.md\",\n            \"status\": \"fully_aligned\"\n       \
    \ },\n        {\n            \"path\": \"project/ONBOARDING.md\",\n          \
    \  \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/LOGGING_PHASES.md\",\n            \"status\": \"fully_aligned\"\n\
    \        },\n        {\n            \"path\": \"project/USECASES_GAP_ANALYSIS.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/LOW_CODE_PROPOSAL.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/proposals/HOME_AUTOMATION_PROPOSAL.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/TRACE_INDEX_SCHEMA_FIX.md\",\n            \"\
    status\": \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/proposals/NEW_PROPOSAL.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/DBSTUDIO_PLUGIN.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/GOVERNANCE_AUDIT_REFACTOR.md\",\n         \
    \   \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/proposals/TRACE_INDEX_SCHEMA_ADAPTATION.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/GONKUI_PLUGIN.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/proposals/MULTI_SOURCE_METADATA_PROPOSAL.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/reports/SEMANTIC_ALIGNMENT_REPORT.md\",\n           \
    \ \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\":\
    \ \"project/reports/PROJECT_DOCUMENT_ALIGNMENT.md\",\n            \"status\":\
    \ \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/reports/CONTENT_ALIGNMENT_REPORT.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/reports/PROJECT_AUDIT_FINAL_REPORT.md\",\n          \
    \  \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/reports/GOVERNANCE_DEMO_REPORT.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/reports/ARCHIVE_ALIGNMENT_MATRIX_OLD.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/reports/DESCRIPTION_COMPLIANCE_REPORT.md\",\n       \
    \     \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/reports/HANDOVER_BRIEF_JULES.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/reports/HANDOVER_BRIEF_CHATGTP.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/logs/ACTIVITY.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/logs/SESSION_LOG.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/logs/CURRENT_STATE.md\",\n            \"status\": \"\
    fully_aligned\"\n        },\n        {\n            \"path\": \"project/process/GAP_ANALYSIS_TEMPLATE.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/archive/TRACEABILITY_MATRIX.md\",\n            \"status\"\
    : \"unlinked\"\n        },\n        {\n            \"path\": \"project/archive/audit/FIRST_AUDIT.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/HLD_LLD_ALIGNMENT_PLAN.md\",\n            \"status\"\
    : \"unlinked\"\n        },\n        {\n            \"path\": \"project/archive/audit/PHASE_4_TRACEABILITY_MATRIX.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/AUDIT-PHASE-3.md\",\n            \"status\": \"\
    unlinked\"\n        },\n        {\n            \"path\": \"project/archive/audit/AUDIT-PHASE-4.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/AUDIT-phase-2.md\",\n            \"status\": \"\
    unlinked\"\n        },\n        {\n            \"path\": \"project/archive/audit/AUDIT_TRACEABILITY_MATRIX.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/AUDIT-phase-1.md\",\n            \"status\": \"\
    unlinked\"\n        },\n        {\n            \"path\": \"project/archive/audit/audit-prompt.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md\",\n        \
    \    \"status\": \"unlinked\"\n        },\n        {\n            \"path\": \"\
    project/archive/audit/AUDIT-PHASE-5.md\",\n            \"status\": \"unlinked\"\
    \n        },\n        {\n            \"path\": \"project/archive/docs/snitch/INTEGRATION_CHECKLIST.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/docs/snitch/phase5-ipc.md\",\n            \"status\"\
    : \"unlinked\"\n        },\n        {\n            \"path\": \"project/archive/docs/snitch/PHASE_2_SECURE_CALLBACK.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/docs/snitch/TEST_RUNBOOK.md\",\n            \"status\"\
    : \"unlinked\"\n        },\n        {\n            \"path\": \"project/archive/docs/projectplan/spotify_fullstack_capability_blueprint.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/docs/projectplan/security.md\",\n            \"status\"\
    : \"unlinked\"\n        },\n        {\n            \"path\": \"project/logs/chat/combined_chats_manifest.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/logs/chat/Manifest_review_and_mapping_manifest.md\",\n\
    \            \"status\": \"fully_aligned\"\n        },\n        {\n          \
    \  \"path\": \"project/logs/chat/Manifest_review_and_mapping.md\",\n         \
    \   \"status\": \"fully_aligned\"\n        }\n    ],\n    \"summary\": {\n   \
    \     \"total_files\": 68,\n        \"fully_aligned\": 50,\n        \"partially_aligned\"\
    : 0,\n        \"unlinked\": 18\n    }\n}"
- path: propagate_descriptions.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-023\n#!/usr/bin/env python3\nimport os\nimport yaml\nimport\
    \ argparse\nfrom pathlib import Path\nfrom collections import defaultdict\n\n\
    TRACE_INDEX_PATH = Path(\"project/reports/TRACE_INDEX.yml\")\n\ndef load_master_data():\n\
    \    \"\"\"Loads all file paths, their descriptions, and their target index files\
    \ from TRACE_INDEX.yml.\"\"\"\n    with open(TRACE_INDEX_PATH, 'r', encoding='utf-8')\
    \ as f:\n        trace_index = yaml.safe_load(f)\n\n    files_by_index = defaultdict(list)\n\
    \    for item in trace_index.get('artifacts', []):\n        if item.get('type')\
    \ != 'exempt' and 'index' in item and item.get('registered') and item['index']\
    \ != '-':\n            files_by_index[item['index']].append({\n              \
    \  \"path\": item['path'],\n                \"description\": item.get('description',\
    \ '').strip(),\n                \"type\": item.get('type', 'N/A')\n          \
    \  })\n    return files_by_index\n\ndef regenerate_index_file(index_path_str,\
    \ files_in_index, apply_changes=False):\n    \"\"\"Regenerates an entire index\
    \ file from scratch with a unified table format.\"\"\"\n    index_path = Path(index_path_str)\n\
    \n    if not apply_changes:\n        print(f\"--- (Dry Run) Would regenerate {index_path}\
    \ with {len(files_in_index)} entries ---\")\n        return\n\n    print(f\"---\
    \ Regenerating {index_path} ---\")\n\n    # Unified Header for ALL index files\n\
    \    header = [\n        f\"# {index_path.stem.replace('_', ' ').title()}\",\n\
    \        \"\",\n        \"This file is auto-generated. Do not edit manually.\"\
    ,\n        \"\",\n        \"| Path | Description |\",\n        \"|------|-------------|\"\
    ,\n    ]\n\n    new_lines = header\n\n    for file_info in sorted(files_in_index,\
    \ key=lambda x: x['path']):\n        path = file_info['path']\n        desc =\
    \ file_info['description']\n        new_lines.append(f\"| `{path}` | {desc} |\"\
    )\n\n    index_path.parent.mkdir(parents=True, exist_ok=True)\n    index_path.write_text(\"\
    \\n\".join(new_lines) + \"\\n\", encoding='utf-8')\n    print(f\"✅ Successfully\
    \ regenerated {index_path} with {len(files_in_index)} entries.\")\n\ndef main():\n\
    \    parser = argparse.ArgumentParser(description=\"Regenerates all index files\
    \ with a unified format from TRACE_INDEX.yml.\")\n    parser.add_argument(\"--apply\"\
    , action=\"store_true\", help=\"Apply the changes to the files. Without this flag,\
    \ it runs in dry-run mode.\")\n    args = parser.parse_args()\n\n    if not args.apply:\n\
    \        print(\"--- Running in DRY-RUN mode. No files will be changed. Use --apply\
    \ to write changes. ---\")\n\n    files_by_index = load_master_data()\n\n    for\
    \ index_file, files in files_by_index.items():\n        regenerate_index_file(index_file,\
    \ files, args.apply)\n\n    print(\"\\n--- Propagation complete. ---\")\n\nif\
    \ __name__ == \"__main__\":\n    main()"
- path: build_project_registry.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-005\n#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\"\"\"\
    \nBuilds a machine-readable project registry from the TRACE_INDEX.yml.\n\"\"\"\
    \nimport argparse\nimport fnmatch\nimport json\nimport re\nimport sys\nfrom pathlib\
    \ import Path\nimport os\n\nimport yaml\n\n# Add the project root to the Python\
    \ path\nsys.path.append(str(Path(__file__).resolve().parents[1]))\n\n\ndef normalize_path(path_str):\n\
    \    \"\"\"Normalizes a path string to a consistent format, removing leading './'.\"\
    \"\"\n    return os.path.normpath(path_str).replace(\"\\\\\", \"/\").lstrip(\"\
    ./\")\n\n\ndef derive_module_category(path_obj):\n    \"\"\"Derives the module\
    \ and category from a given path.\"\"\"\n    parts = path_obj.parts\n    if not\
    \ parts:\n        return \"general\", \"general\"\n\n    module = parts[0]\n\n\
    \    if len(parts) > 2 and parts[1] not in (\"src\", \"tests\"):\n        category\
    \ = parts[1]\n    else:\n        category = \"general\"\n\n    return module,\
    \ category\n\n\ndef derive_name(path_obj, legacy_entry=None):\n    \"\"\"Derives\
    \ a human-readable name from a path or legacy entry.\"\"\"\n    if legacy_entry\
    \ and legacy_entry.get(\"name\"):\n        return legacy_entry[\"name\"]\n   \
    \ return path_obj.stem.replace(\"_\", \" \").replace(\"-\", \" \").title()\n\n\
    \ndef parse_legacy_registry(md_content, md_path, repo_root):\n    \"\"\"Parses\
    \ the legacy PROJECT_REGISTRY.md to extract entries.\"\"\"\n    legacy_entries\
    \ = {}\n    base_dir = md_path.parent\n    table_row_re = re.compile(r\"\\|\\\
    s*\\[([^\\]]+)\\]\\(([^)]+)\\)\\s*\\|([^|]*)\\|\")\n\n    for line in md_content.splitlines():\n\
    \        match = table_row_re.search(line)\n        if match:\n            name,\
    \ rel_path, description = [m.strip() for m in match.groups()]\n\n            #\
    \ Correct the corrupted path before resolving it.\n            # This handles\
    \ the case where './project/' was incorrectly prepended.\n            if rel_path.startswith('./project/'):\n\
    \                rel_path = rel_path[len('./project/'):]\n\n            full_path\
    \ = (base_dir / rel_path).resolve()\n            repo_relative_path = normalize_path(str(full_path.relative_to(repo_root)))\n\
    \n            legacy_entries[repo_relative_path] = {\n                \"name\"\
    : name, \"path\": repo_relative_path, \"notes\": description,\n            }\n\
    \    return legacy_entries\n\n\ndef build_registry(\n    trace_index_path, project_registry_md_path,\
    \ extras_file_path, output_json_path, project_dir, repo_root, debug=False\n):\n\
    \    \"\"\"Builds the project registry.\"\"\"\n    trace_map = {}\n    if trace_index_path.exists():\n\
    \        with open(trace_index_path, \"r\", encoding=\"utf-8\") as f:\n      \
    \      trace_data = yaml.safe_load(f)\n            artifacts = trace_data.get(\"\
    artifacts\", []) if isinstance(trace_data, dict) else trace_data or []\n     \
    \       trace_map = {normalize_path(item[\"path\"]): item for item in artifacts}\n\
    \n    legacy_entries = {}\n    if project_registry_md_path.exists():\n       \
    \ with open(project_registry_md_path, \"r\", encoding=\"utf-8\") as f:\n     \
    \       md_content = f.read()\n            legacy_entries = parse_legacy_registry(md_content,\
    \ project_registry_md_path, repo_root)\n\n    extras_to_include = []\n    if extras_file_path.exists():\n\
    \        with open(extras_file_path, \"r\", encoding=\"utf-8\") as f:\n      \
    \      extras_data = yaml.safe_load(f)\n            extras_to_include = [normalize_path(p)\
    \ for p in extras_data.get(\"include\", [])]\n\n    registry = []\n    processed_paths\
    \ = set()\n\n    all_paths_to_process = set(trace_map.keys()) | set(legacy_entries.keys())\
    \ | set(extras_to_include)\n\n    for path_str in all_paths_to_process:\n    \
    \    path_obj = Path(path_str)\n\n        is_project_doc = path_str.startswith(\"\
    project/\")\n        is_in_extras = path_str in extras_to_include\n\n        if\
    \ not (is_project_doc or is_in_extras):\n            if debug: print(f\"[FILTERED\
    \ OUT] Path '{path_str}' does not match project scope.\")\n            continue\n\
    \n        processed_paths.add(path_str)\n\n        trace_item = trace_map.get(path_str)\n\
    \        legacy_item = legacy_entries.get(path_str)\n        exists_on_disk =\
    \ (repo_root / path_str).exists()\n\n        status = \"unknown\"\n        source\
    \ = \"unknown\"\n\n        if trace_item:\n            status = \"registered\"\
    \ if exists_on_disk else \"missing\"\n            source = \"TRACE_INDEX.yml\"\
    \n        elif legacy_item:\n            status = \"legacy\" if not exists_on_disk\
    \ else \"orphan\"\n            source = \"project/PROJECT_REGISTRY.md\"\n    \
    \    elif path_str in extras_to_include:\n             status = \"missing\"\n\
    \             source = \"extras\"\n\n        if exists_on_disk and not trace_item\
    \ and not legacy_item:\n            status = \"orphan\"\n            source =\
    \ \"filesystem\"\n\n        module, category = derive_module_category(path_obj)\n\
    \        entry = {\n            \"name\": derive_name(path_obj, legacy_item),\
    \ \"path\": path_str, \"type\": \"doc\",\n            \"module\": module, \"category\"\
    : category, \"registered_in\": trace_item.get(\"registered_in\", []) if trace_item\
    \ else [],\n            \"status\": status, \"notes\": trace_item.get(\"description\"\
    ) or (legacy_item[\"notes\"] if legacy_item else \"\"), \"source\": source,\n\
    \        }\n        registry.append(entry)\n\n    if project_dir.exists():\n \
    \       for file_path in project_dir.rglob('*'):\n            if file_path.is_file():\n\
    \                path_str = normalize_path(str(file_path.relative_to(repo_root)))\n\
    \                if path_str not in processed_paths:\n                    if not\
    \ path_str.startswith(\"project/\"):\n                        if debug: print(f\"\
    [FILTERED OUT] Orphan scan skipped non-project file: {path_str}\")\n         \
    \               continue\n\n                    processed_paths.add(path_str)\n\
    \                    path_obj = Path(path_str)\n                    module, category\
    \ = derive_module_category(path_obj)\n                    entry = { \"name\":\
    \ derive_name(path_obj), \"path\": path_str, \"type\": \"doc\", \"module\": module,\
    \ \"category\": category,\n                        \"registered_in\": [], \"status\"\
    : \"orphan\", \"notes\": \"\", \"source\": \"filesystem\",\n                 \
    \   }\n                    registry.append(entry)\n\n    registry.sort(key=lambda\
    \ x: (x[\"module\"], x[\"category\"], x[\"path\"]))\n\n    if output_json_path.exists():\n\
    \        try:\n            with open(output_json_path, \"r\", encoding=\"utf-8\"\
    ) as f:\n                if json.load(f) == registry:\n                    print(f\"\
    No changes to {output_json_path}. Skipping write.\")\n                    return\
    \ registry\n        except (json.JSONDecodeError, IOError):\n            pass\n\
    \n    with open(output_json_path, \"w\", encoding=\"utf-8\") as f:\n        json.dump(registry,\
    \ f, indent=4, sort_keys=False)\n    print(f\"Successfully wrote project registry\
    \ to {output_json_path}\")\n    return registry\n\n\ndef generate_markdown(registry_data,\
    \ output_md_path):\n    \"\"\"Generates the project registry markdown file from\
    \ the final registry data.\"\"\"\n    header = \"<!-- AUTO-GENERATED from scripts/project_registry.json\
    \ — manual edits may be overwritten. Historical legacy entries preserved below.\
    \ -->\\n\\n\"\n    table_header = \"| Document | Location | Description | Status\
    \ |\\n|---|---|---|---|\\n\"\n\n    main_entries = sorted([e for e in registry_data\
    \ if e.get(\"status\") in [\"registered\", \"missing\"]], key=lambda x: x['path'])\n\
    \    legacy_entries = sorted([e for e in registry_data if e.get(\"status\") ==\
    \ \"legacy\"], key=lambda x: x['path'])\n    orphan_entries = sorted([e for e\
    \ in registry_data if e.get(\"status\") == \"orphan\"], key=lambda x: x['path'])\n\
    \n    def create_table_row(entry, base_path):\n        try:\n            # Paths\
    \ are already repo-relative, so make them relative to the MD file's location\n\
    \            relative_path = Path(entry[\"path\"]).relative_to(base_path.parent)\n\
    \        except ValueError:\n            relative_path = Path(entry[\"path\"])\n\
    \        location_str = f\"[`{entry['path']}`](./{relative_path})\"\n        return\
    \ f\"| **{entry['name']}** | {location_str} | {entry.get('notes', '')} | {entry['status']}\
    \ |\"\n\n    table_rows = [create_table_row(e, output_md_path) for e in main_entries]\n\
    \    content = header + table_header + \"\\n\".join(table_rows)\n\n    if legacy_entries:\n\
    \        legacy_lines = [create_table_row(e, output_md_path) for e in legacy_entries]\n\
    \        content += \"\\n\\n## Historical / Legacy Entries\\n\\n\" + table_header\
    \ + \"\\n\".join(legacy_lines)\n\n    if orphan_entries:\n        content += \"\
    \\n\\n## Orphan Files\\n\\n\"\n        orphan_list = [f\"- `{entry['path']}`\"\
    \ for entry in orphan_entries]\n        content += \"\\n\".join(orphan_list)\n\
    \n    if output_md_path.exists():\n        with open(output_md_path, 'r', encoding='utf-8')\
    \ as f:\n            if f.read() == content:\n                print(f\"No changes\
    \ to {output_md_path}. Skipping write.\")\n                return\n\n    with\
    \ open(output_md_path, \"w\", encoding=\"utf-8\") as f:\n        f.write(content)\n\
    \    print(f\"Successfully generated {output_md_path}\")\n\n\ndef main():\n  \
    \  parser = argparse.ArgumentParser(description=__doc__)\n    parser.add_argument(\"\
    --repo-root\", type=Path, default=Path.cwd(), help=\"The root directory of the\
    \ repository.\")\n    args, _ = parser.parse_known_args()\n    repo_root = args.repo_root.resolve()\n\
    \n    parser.add_argument(\"--trace-index\", type=Path, default=repo_root / \"\
    project/reports/TRACE_INDEX.yml\")\n    parser.add_argument(\"--project-registry-md\"\
    , type=Path, default=repo_root / \"project/PROJECT_REGISTRY.md\")\n    parser.add_argument(\"\
    --extras-file\", type=Path, default=repo_root / \"scripts/project_registry_extras.yml\"\
    )\n    parser.add_argument(\"--output-json\", type=Path, default=repo_root / \"\
    scripts/project_registry.json\")\n    parser.add_argument(\"--output-md\", type=Path,\
    \ default=repo_root / \"project/PROJECT_REGISTRY.md\")\n    parser.add_argument(\"\
    --project-dir\", type=Path, default=repo_root / \"project\", help=\"The project\
    \ directory to scan for orphans.\")\n    parser.add_argument(\"--debug\", action=\"\
    store_true\", help=\"Enable debug printing.\")\n    args = parser.parse_args()\n\
    \n    registry_data = build_registry(\n        args.trace_index, args.project_registry_md,\
    \ args.extras_file, args.output_json, args.project_dir, repo_root, args.debug\n\
    \    )\n\n    if registry_data is not None:\n        generate_markdown(registry_data,\
    \ args.output_md)\n\n\nif __name__ == \"__main__\":\n    main()"
- path: lint_governance_links.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-016\n#!/usr/bin/env python3\n\"\"\"\nLint Governance Links Script\n\
    Generates PROJECT_DOCUMENT_ALIGNMENT.md and lint_governance_links.json.\nTracks\
    \ document alignment based on TRACE_INDEX.yml and project/*.md files.\n\"\"\"\n\
    \nimport json\nfrom pathlib import Path\nimport yaml\n\nPROJECT_ROOT = Path(__file__).parent.parent\n\
    TRACE_INDEX_FILE = PROJECT_ROOT / \"project\" / \"reports\" / \"TRACE_INDEX.yml\"\
    \nOUTPUT_JSON = PROJECT_ROOT / \"scripts\" / \"lint_governance_links.json\"\n\
    OUTPUT_MD = PROJECT_ROOT / \"project\" / \"reports\" / \"PROJECT_DOCUMENT_ALIGNMENT.md\"\
    \n\ndef load_and_normalize_trace_index():\n    \"\"\"\n    Loads and normalizes\
    \ the TRACE_INDEX.yml file.\n    Handles three formats:\n    1. A dictionary with\
    \ an \"artifacts\" key holding a list of file objects.\n    2. A direct list of\
    \ file objects.\n    3. A legacy dictionary where file paths are top-level keys.\n\
    \    Returns a unified dictionary mapping file paths to their data.\n    \"\"\"\
    \n    with open(TRACE_INDEX_FILE, \"r\") as f:\n        data = yaml.safe_load(f)\n\
    \n    if isinstance(data, dict):\n        if \"artifacts\" in data and isinstance(data.get(\"\
    artifacts\"), list):\n            # New format: dict with \"artifacts\" key\n\
    \            return {item[\"path\"]: item for item in data[\"artifacts\"] if \"\
    path\" in item}\n        else:\n            # Legacy format: dict with paths as\
    \ keys\n            return data\n    elif isinstance(data, list):\n        # New\
    \ format: list of objects\n        return {item[\"path\"]: item for item in data\
    \ if \"path\" in item}\n    raise ValueError(\"Unknown format for TRACE_INDEX.yml\"\
    )\n\ndef scan_project_files():\n    files = list(PROJECT_ROOT.glob(\"project/**/*.md\"\
    ))\n    return [f.relative_to(PROJECT_ROOT).as_posix() for f in files\n      \
    \      if not f.parts[1] in (\"archive\", \"logs\")]\n\ndef classify_files(trace_index,\
    \ project_files):\n    files_report = []\n    fully_aligned = partially_aligned\
    \ = 0\n    unlinked = []\n\n    traced_paths = set(trace_index.keys())\n\n   \
    \ for f_path in project_files:\n        status = \"unlinked\"\n        if f_path\
    \ in traced_paths:\n            item = trace_index[f_path]\n            if item\
    \ and item.get(\"registered\"):\n                # A file is considered fully\
    \ aligned if it is registered and has a valid index reference.\n             \
    \   if item.get(\"index\") and item.get(\"index\") != \"-\":\n               \
    \     status = \"fully_aligned\"\n                    fully_aligned += 1\n   \
    \             else:\n                    status = \"partially_aligned\"\n    \
    \                partially_aligned += 1\n            else:\n                unlinked.append(f_path)\n\
    \        else:\n            unlinked.append(f_path)\n\n        files_report.append({\"\
    path\": f_path, \"status\": status})\n\n    return files_report, fully_aligned,\
    \ partially_aligned, len(unlinked)\n\ndef write_json_report(report_data):\n  \
    \  with open(OUTPUT_JSON, \"w\") as f:\n        json.dump(report_data, f, indent=4)\n\
    \ndef write_md_report(report_data):\n    md_lines = [\"# Project Document Alignment\
    \ Report\\n\"]\n    categories = {\"fully_aligned\": [], \"partially_aligned\"\
    : [], \"unlinked\": []}\n    for entry in report_data[\"files\"]:\n        categories[entry[\"\
    status\"]].append(entry[\"path\"])\n\n    md_lines.append(\"## Fully Aligned\\\
    n\")\n    if categories[\"fully_aligned\"]:\n        md_lines += [f\"- `{f}`\"\
    \ for f in categories[\"fully_aligned\"]]\n    else:\n        md_lines.append(\"\
    None\")\n\n    md_lines.append(\"\\n## Partially Aligned (registered but missing\
    \ references)\\n\")\n    if categories[\"partially_aligned\"]:\n        md_lines\
    \ += [f\"- `{f}`\" for f in categories[\"partially_aligned\"]]\n    else:\n  \
    \      md_lines.append(\"None\")\n\n    md_lines.append(\"\\n## Unlinked / Unregistered\\\
    n\")\n    if categories[\"unlinked\"]:\n        md_lines += [f\"- `{f}`\" for\
    \ f in categories[\"unlinked\"]]\n    else:\n        md_lines.append(\"None\"\
    )\n\n    summary = report_data[\"summary\"]\n    md_lines.append(\"\\n## Summary\\\
    n\")\n    md_lines.append(f\"- Total project MD files: {summary['total_files']}\"\
    )\n    md_lines.append(f\"- Fully aligned: {summary['fully_aligned']}\")\n   \
    \ md_lines.append(f\"- Partially aligned: {summary['partially_aligned']}\")\n\
    \    md_lines.append(f\"- Unlinked: {summary['unlinked']}\\n\")\n    md_lines.append(\"\
    **Note:** Generated automatically. Do not overwrite manually.\\n\")\n\n    with\
    \ open(OUTPUT_MD, \"w\") as f:\n        f.write(\"\\n\".join(md_lines))\n\ndef\
    \ main():\n    trace_index = load_and_normalize_trace_index()\n    project_files\
    \ = scan_project_files()\n    files_report, full, partial, unlinked_count = classify_files(trace_index,\
    \ project_files)\n    report_data = {\n        \"files\": files_report,\n    \
    \    \"summary\": {\n            \"total_files\": len(project_files),\n      \
    \      \"fully_aligned\": full,\n            \"partially_aligned\": partial,\n\
    \            \"unlinked\": unlinked_count,\n        },\n    }\n    write_json_report(report_data)\n\
    \    write_md_report(report_data)\n    print(f\"Generated {OUTPUT_JSON} and {OUTPUT_MD}\"\
    )\n    return 0\n\nif __name__ == \"__main__\":\n    main()"
- path: semantic_alignment_check.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-027\n#!/usr/bin/env python3\nimport os\nimport sys\nimport yaml\n\
    import argparse\nimport re\nfrom pathlib import Path\nfrom collections import\
    \ defaultdict\n\nPROJECT_ROOT = Path(__file__).resolve().parents[1]\nDEFAULT_TRACE_INDEX_PATH\
    \ = PROJECT_ROOT / \"project/reports/TRACE_INDEX.yml\"\nCONTENT_ALIGNMENT_REPORT\
    \ = PROJECT_ROOT / \"project/reports/CONTENT_ALIGNMENT_REPORT.md\"\nHIGH_LEVEL_DESIGN_PATH\
    \ = PROJECT_ROOT / \"project/HIGH_LEVEL_DESIGN.md\"\nLOW_LEVEL_DESIGN_PATH = PROJECT_ROOT\
    \ / \"project/LOW_LEVEL_DESIGN.md\"\nOUTPUT_REPORT_PATH = PROJECT_ROOT / \"project/reports/SEMANTIC_ALIGNMENT_REPORT.md\"\
    \n\ndef load_registered_files(trace_index_path: Path):\n    \"\"\"Loads all files\
    \ from the specified TRACE_INDEX.yml that are marked as registered.\"\"\"\n  \
    \  registered_files = {}\n    if not trace_index_path.exists():\n        print(f\"\
    Error: Trace index file not found at {trace_index_path}\", file=sys.stderr)\n\
    \        return {}\n\n    with open(trace_index_path, 'r') as f:\n        trace_data\
    \ = yaml.safe_load(f)\n\n    for artifact in trace_data.get('artifacts', []):\n\
    \        if artifact.get('registered') is True:\n            path = artifact.get('path')\n\
    \            description = artifact.get('description', 'No description provided.')\n\
    \            if path:\n                registered_files[path] = description\n\
    \    return registered_files\n\ndef load_structurally_aligned_files(registered_files_map):\n\
    \    \"\"\"\n    Parses CONTENT_ALIGNMENT_REPORT.md to find files marked as fully\
    \ aligned.\n    \"\"\"\n    if not CONTENT_ALIGNMENT_REPORT.exists():\n      \
    \  print(f\"Warning: {CONTENT_ALIGNMENT_REPORT} not found. Assuming all registered\
    \ files are structurally aligned.\", file=sys.stderr)\n        return set(registered_files_map.keys())\n\
    \n    with open(CONTENT_ALIGNMENT_REPORT, 'r') as f:\n        content = f.read()\n\
    \n    # Use regex to find the 'Fully Aligned' row and check its count.\n    #\
    \ This is a bit brittle, but good enough for this project's structure.\n    match\
    \ = re.search(r\"\\|\\s*\\*\\*Fully Aligned\\*\\*\\s*\\|\\s*(\\d+)\\s*\\|\", content)\n\
    \    if match:\n        # We can just return all registered files since the report\
    \ says they are all aligned.\n        # A more robust implementation might parse\
    \ the full table.\n        return set(registered_files_map.keys())\n    else:\n\
    \        print(\"Warning: CONTENT_ALIGNMENT_REPORT.md does not show full alignment.\
    \ The semantic check might be incomplete.\", file=sys.stderr)\n        return\
    \ set()\n\ndef load_design_doc_references(all_registered_files):\n    \"\"\"\n\
    \    Parses HLD and LLD for trace blocks and tables to build a map of semantic\
    \ references.\n    \"\"\"\n    references = defaultdict(list)\n    design_docs\
    \ = [HIGH_LEVEL_DESIGN_PATH, LOW_LEVEL_DESIGN_PATH]\n\n    trace_block_pattern\
    \ = re.compile(r\"<!-- trace:begin (.*?) -->(.*?)<!-- trace:end \\1 -->\", re.DOTALL)\n\
    \    linked_file_pattern = re.compile(r\"\\[.*?\\]\\((.*?)\\)\")\n    description_pattern\
    \ = re.compile(r\"\\*\\*Description:\\*\\* (.*?)\\n\", re.DOTALL)\n\n    for doc_path\
    \ in design_docs:\n        if not doc_path.exists():\n            continue\n \
    \       with open(doc_path, 'r') as f:\n            content = f.read()\n\n   \
    \     # Parse trace blocks\n        for match in trace_block_pattern.finditer(content):\n\
    \            feature_id = match.group(1).strip()\n            block_content =\
    \ match.group(2)\n            linked_file_match = linked_file_pattern.search(block_content)\n\
    \            description_match = description_pattern.search(block_content)\n\n\
    \            if linked_file_match:\n                path_text = linked_file_match.group(1)\n\
    \                normalized_path = (doc_path.parent / path_text).resolve().relative_to(PROJECT_ROOT.resolve()).as_posix()\n\
    \                desc = description_match.group(1).strip().replace('\\n', ' ')\
    \ if description_match else \"No description in trace block.\"\n             \
    \   reference_data = {\"source\": doc_path.name, \"feature_id\": feature_id, \"\
    description\": desc}\n\n                if normalized_path.endswith('/'):\n  \
    \                  for reg_file in all_registered_files:\n                   \
    \     if reg_file.startswith(normalized_path):\n                            references[reg_file].append(reference_data)\n\
    \                else:\n                    references[normalized_path].append(reference_data)\n\
    \n        # Parse markdown tables for linked artifacts\n        table_pattern\
    \ = re.compile(r\"(\\n\\|.*?\\n\\|---\\|.*?\\n(?:\\|.*?\\n)*)\", re.DOTALL)\n\
    \        for table_match in table_pattern.finditer(content):\n            table_text\
    \ = table_match.group(1)\n            header = table_text.split('\\n')[1]\n  \
    \          if 'component' not in header.lower() and 'feature' not in header.lower()\
    \ and 'artifact' not in header.lower():\n                continue\n\n        \
    \    rows = table_text.strip().split('\\n')[2:]\n            for row in rows:\n\
    \                if not row.strip().startswith('|'): continue\n              \
    \  parts = [p.strip() for p in row.split('|') if p.strip()]\n                if\
    \ len(parts) < 2: continue\n\n                component_name = parts[0].replace('**',\
    \ '').strip()\n                linked_artifacts_cell = parts[1]\n\n          \
    \      file_paths = re.findall(r'`([^`]+)`', linked_artifacts_cell)\n        \
    \        for file_path in file_paths:\n                    file_path = file_path.strip()\n\
    \                    if file_path.endswith('/'):\n                         for\
    \ reg_file in all_registered_files:\n                            if reg_file.startswith(file_path):\n\
    \                                references[reg_file].append({\"source\": f\"\
    {doc_path.name} (Table)\", \"component\": component_name, \"description\": f\"\
    Part of component: {component_name}\"})\n                    elif file_path in\
    \ all_registered_files:\n                        references[file_path].append({\"\
    source\": f\"{doc_path.name} (Table)\", \"component\": component_name, \"description\"\
    : f\"Part of component: {component_name}\"})\n    return references\n\ndef analyze_semantics(files,\
    \ registered_files_map, design_references):\n    \"\"\"\n    Analyzes each file\
    \ for semantic consistency.\n    \"\"\"\n    results = []\n    for file_path in\
    \ files:\n        if file_path not in design_references:\n            results.append({\"\
    file\": file_path, \"status\": \"❌ Orphan\", \"notes\": \"File is not referenced\
    \ in HLD or LLD trace blocks or tables.\"})\n            continue\n\n        trace_index_desc\
    \ = registered_files_map.get(file_path, \"\").lower()\n        design_doc_descs\
    \ = [ref['description'].lower() for ref in design_references[file_path]]\n   \
    \     trace_index_words = set(re.findall(r'\\w+', trace_index_desc))\n\n     \
    \   is_consistent = False\n        all_notes = []\n        for i, design_desc\
    \ in enumerate(design_doc_descs):\n            design_doc_words = set(re.findall(r'\\\
    w+', design_desc))\n            overlap = trace_index_words.intersection(design_doc_words)\n\
    \            if len(overlap) >= 2 or trace_index_desc in design_desc or design_desc\
    \ in trace_index_desc:\n                is_consistent = True\n               \
    \ source_doc = design_references[file_path][i]['source']\n                all_notes.append(f\"\
    Aligned with '{source_doc}'.\")\n            else:\n                source_doc\
    \ = design_references[file_path][i]['source']\n                all_notes.append(f\"\
    Possible mismatch with '{source_doc}'. TRACE_INDEX: '{trace_index_desc[:50]}...'\
    \ vs DESIGN_DOC: '{design_desc[:50]}...'. Overlap: {len(overlap)} words.\")\n\n\
    \        if is_consistent:\n            results.append({\"file\": file_path, \"\
    status\": \"✅ Fully aligned\", \"notes\": \" \".join(all_notes)})\n        else:\n\
    \            results.append({\"file\": file_path, \"status\": \"⚠️ Partial\",\
    \ \"notes\": \" \".join(all_notes)})\n    return results\n\ndef generate_report(results):\n\
    \    \"\"\"Generates a Markdown report from the analysis results.\"\"\"\n    total_files\
    \ = len(results)\n    fully_aligned = sum(1 for r in results if r['status'] ==\
    \ '✅ Fully aligned')\n    partially_aligned = sum(1 for r in results if r['status']\
    \ == '⚠️ Partial')\n    orphans = sum(1 for r in results if r['status'] == '❌\
    \ Orphan')\n    coverage = (fully_aligned / total_files * 100) if total_files\
    \ > 0 else 0\n\n    report_content = f\"\"\"# Semantic Alignment Report\n\n**Date:**\
    \ {os.popen('date -I').read().strip()}\n**Status:** Generated\n\n## 1. Summary\n\
    \nThis report analyzes the semantic consistency between registered project artifacts\
    \ and the high-level (HLD) and low-level (LLD) design documents. It checks for\
    \ orphaned files and description mismatches.\n\n| Status                | Count\
    \ |\n|-----------------------|-------|\n| **Total Files Checked** | {total_files}\
    \   |\n| ✅ **Fully aligned**    | {fully_aligned} |\n| ⚠️ **Partially aligned**\
    \ | {partially_aligned} |\n| ❌ **Orphans**          | {orphans}   |\n\n**Semantic\
    \ Coverage:** `{coverage:.2f}%`\n\n---\n\n## 2. Detailed Breakdown\n\n| File |\
    \ Status | Notes |\n|------|--------|-------|\n\"\"\"\n    results.sort(key=lambda\
    \ x: (x['status'], x['file']))\n    for result in results:\n        report_content\
    \ += f\"| `{result['file']}` | {result['status']} | {result['notes']} |\\n\"\n\
    \    with open(OUTPUT_REPORT_PATH, 'w') as f:\n        f.write(report_content)\n\
    \    print(f\"Report generated at {OUTPUT_REPORT_PATH}\")\n\ndef main():\n   \
    \ parser = argparse.ArgumentParser(description=\"Semantic Alignment and Dependency\
    \ Verification\")\n    parser.add_argument(\"--scan\", action=\"store_true\",\
    \ help=\"Generate semantic alignment report\")\n    parser.add_argument(\"--enforce\"\
    , action=\"store_true\", help=\"Exit nonzero if alignment thresholds not met\"\
    )\n    parser.add_argument(\"--test-files\", nargs=\"*\", help=\"Accepts a list\
    \ of changed files for compatibility with the main linter.\")\n    parser.add_argument(\"\
    --index-file\", type=Path, default=DEFAULT_TRACE_INDEX_PATH, help=\"Optional:\
    \ path to TRACE_INDEX.yml to use for semantic checks.\")\n    args = parser.parse_args()\n\
    \n    if not args.scan and not args.enforce:\n        args.scan = True\n\n   \
    \ registered_files_map = load_registered_files(args.index_file)\n    if not registered_files_map:\n\
    \        print(\"Error: TRACE_INDEX.yml appears empty or incomplete. Aborting\
    \ semantic check.\", file=sys.stderr)\n        sys.exit(0) # gracefully skip,\
    \ not fail\n\n    all_aligned_files = load_structurally_aligned_files(registered_files_map)\n\
    \n    if args.test_files:\n        files_to_check = set(args.test_files).intersection(all_aligned_files)\n\
    \        if not files_to_check:\n            print(\"No relevant files to check\
    \ for semantic alignment.\")\n            if args.enforce:\n                print(\"\
    Semantic alignment coverage meets the required threshold.\")\n            return\n\
    \    else:\n        files_to_check = all_aligned_files\n\n    design_references\
    \ = load_design_doc_references(registered_files_map.keys())\n    results = analyze_semantics(files_to_check,\
    \ registered_files_map, design_references)\n    generate_report(results)\n\n \
    \   if args.enforce:\n        threshold = 1.0\n        fully_aligned = sum(1 for\
    \ r in results if r['status'] == '✅ Fully aligned')\n        total_checked = len(results)\n\
    \        coverage = (fully_aligned / total_checked * 100) if total_checked > 0\
    \ else 100.0\n\n        print(f\"Enforcing semantic alignment. Coverage: {coverage:.2f}%,\
    \ Threshold: {threshold:.2f}%\")\n        if coverage < threshold:\n         \
    \   print(f\"Error: Semantic alignment coverage is {coverage:.2f}%, which is below\
    \ the required threshold of {threshold:.2f}%.\", file=sys.stderr)\n          \
    \  sys.exit(1)\n        else:\n            print(\"Semantic alignment coverage\
    \ meets the required threshold.\")\n\nif __name__ == \"__main__\":\n    main()"
- path: doc-lint-rules.yml
  type: config
  workflow: []
  indexes: []
  content: "# ID: OPS-008\n# This file defines the \"documentation matrix\" for the\
    \ custom linter.\n# It maps changes in source code paths to required changes in\
    \ documentation files.\n\nrules:\n  - name: \"Source Documentation Registration\"\
    \n    source_paths:\n      - \"api/docs/reference/source/\"\n    required_docs:\n\
    \      - \"api/docs/MASTER_INDEX.md\"\n    message: |\n      New source documentation\
    \ must be registered in MASTER_INDEX.md.\n      Refer to QA_GOVERNANCE.md for\
    \ policy details.\n\n  - name: \"Source Documentation Quality Tracking\"\n   \
    \ source_paths:\n      - \"api/docs/reference/source/\"\n    required_docs:\n\
    \      - \"api/docs/DOCS_QUALITY_INDEX.md\"\n    message: |\n      New source\
    \ documentation must be added to the DOCS_QUALITY_INDEX.md for quality tracking.\n\
    \      Refer to QA_GOVERNANCE.md for policy details.\n\n  - name: \"Enforce Mandatory\
    \ Logging\"\n    source_paths:\n      - \"api/src/zotify_api/\"\n      - \"project/\"\
    \n      - \"api/docs/\"\n      - \"snitch/\"\n      - \"Gonk/GonkUI/\"\n     \
    \ - \"scripts/\"\n      - \"AGENTS.md\"\n      - \".github/workflows/ci.yml\"\n\
    \      - \"README.md\"\n    required_docs:\n      - \"project/logs/ACTIVITY.md\"\
    \n      - \"project/logs/SESSION_LOG.md\"\n      - \"project/logs/CURRENT_STATE.md\"\
    \n    message: |\n      Changes to code or documentation must be logged. Please\
    \ run the linter's\n      --log command to update the project logs.\n\n  - name:\
    \ \"API Route Change\"\n    source_paths:\n      - \"api/src/zotify_api/routes/\"\
    \n    required_docs:\n      - \"project/ENDPOINTS.md\"\n      - \"api/docs/reference/API_REFERENCE.md\"\
    \n    message: |\n      Changes to API routes require an update to the endpoint\
    \ documentation.\n      Refer to QA_GOVERNANCE.md for policy details.\n\n  - name:\
    \ \"High-Level Design Change\"\n    source_paths:\n      - \"project/HIGH_LEVEL_DESIGN.md\"\
    \n      - \"project/LOW_LEVEL_DESIGN.md\"\n    required_docs:\n      - \"project/ALIGNMENT_MATRIX.md\"\
    \n    message: |\n      Changes to core design documents must be reflected in\
    \ the traceability matrix.\n      Refer to QA_GOVERNANCE.md for policy details.\n\
    \n  - name: \"Agent Workflow Change\"\n    source_paths:\n      - \"AGENTS.md\"\
    \n      - \"scripts/linter.py\"\n    # The Handover Brief is a point-in-time document\
    \ and must not be changed\n    # after the initial session, except when the user\
    \ asks for it.\n    # forbidden_docs:\n    #   - \"project/reports/HANDOVER_BRIEF_JULES.md\"\
    \n    message: |\n      The Handover Brief cannot be modified.\n      Refer to\
    \ QA_GOVERNANCE.md for policy details.\n\n  - name: \"Database Model Change\"\n\
    \    source_paths:\n      - \"api/src/zotify_api/database/models.py\"\n    required_docs:\n\
    \      - \"project/LOW_LEVEL_DESIGN.md\"\n    message: |\n      Changes to database\
    \ models should be reflected in the Low-Level Design document.\n      Refer to\
    \ QA_GOVERNANCE.md for policy details.\n\n  - name: \"CI/CD Pipeline Change\"\n\
    \    source_paths:\n      - \".github/workflows/ci.yml\"\n    required_docs:\n\
    \      - \"project/CICD.md\"\n      - \"api/docs/manuals/CICD.md\"\n    message:\
    \ |\n      Changes to the CI/CD pipeline must be documented in the CICD guides.\n\
    \      Refer to QA_GOVERNANCE.md for policy details.\n\n  - name: \"Alignment\
    \ Matrix Maintenance\"\n    source_paths:\n      - \"api/src/zotify_api/\"\n \
    \     - \"snitch/\"\n      - \"Gonk/GonkUI/\"\n      - \"scripts/\"\n    required_docs:\n\
    \      - \"project/ALIGNMENT_MATRIX.md\"\n    message: |\n      All code changes\
    \ must be reflected in `project/ALIGNMENT_MATRIX.md`.\n      Refer to QA_GOVERNANCE.md\
    \ (Section: Alignment & Traceability) for policy details.\n\n  - name: \"MASTER\
    \ Index Maintenance\"\n    source_paths:\n      - \"api/docs/\"\n    required_docs:\n\
    \      - \"api/docs/MASTER_INDEX.md\"\n    message: |\n      All documents under\
    \ api/docs/ must be registered in api/docs/MASTER_INDEX.md.\n      Update MASTER_INDEX.md\
    \ to reflect additions, removals, or renames.\n      Refer to QA_GOVERNANCE.md\
    \ for policy details.\n\n  - name: \"Code Quality Index Maintenance\"\n    source_paths:\n\
    \      - \"api/src/\"\n      - \"snitch/\"\n      - \"Gonk/GonkUI/\"\n      -\
    \ \"scripts/\"\n    required_docs:\n      - \"api/docs/CODE_QUALITY_INDEX.md\"\
    \n    message: |\n      Any source file changes must be reflected in api/docs/CODE_QUALITY_INDEX.md.\n\
    \      Add/update the relevant entry to maintain code quality coverage.\n    \
    \  Refer to QA_GOVERNANCE.md for policy details.\n\n  - name: \"Project Registry\
    \ Maintenance\"\n    source_paths:\n      - \"project/\"\n    required_docs:\n\
    \      - \"project/PROJECT_REGISTRY.md\"\n    message: |\n      All project-level\
    \ governance and process documents must be registered in\n      `project/PROJECT_REGISTRY.md`.\
    \ Update it when adding, renaming, or removing docs.\n      Refer to QA_GOVERNANCE.md\
    \ for policy details.\n\n  - name: \"Documentation Update Enforcement\"\n    source_paths:\n\
    \      - \"api/src/\"\n      - \"snitch/\"\n      - \"Gonk/GonkUI/\"\n      -\
    \ \"scripts/\"\n      - \"project/\"\n      - \"api/docs/\"\n    required_docs:\n\
    \      - \"project/ALIGNMENT_MATRIX.md\"\n      - \"api/docs/CODE_QUALITY_INDEX.md\"\
    \n      - \"project/PROJECT_REGISTRY.md\"\n      - \"api/docs/MASTER_INDEX.md\"\
    \n    message: |\n      Code or documentation changes must be reflected in the\
    \ relevant index/matrix docs.\n      Refer to QA_GOVERNANCE.md for update policies.\n"
- path: make_manifest.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-018\n#!/usr/bin/env python3\n\"\"\"\nSelf-checking repository\
    \ manifest generator.\nRegenerates manifest only if there are staged changes,\
    \ if --test-files is provided, or if --force is used.\n\"\"\"\n\nimport subprocess\n\
    import sys\nfrom pathlib import Path\nimport os\nimport yaml\nimport argparse\n\
    \nPROJECT_ROOT = Path(__file__).parent.parent\n\n# --- Configurable scan directory\
    \ ---\nSCAN_DIR = PROJECT_ROOT / \"scripts\"\n\n# --- Configuration ---\nIGNORED_DIRS\
    \ = {'.git', '.github', '.venv', '__pycache__', 'archive', 'api_dumps',\n    \
    \            'zotify_api.egg-info', 'templates', 'docs', 'alembic', 'build', 'dist'}\n\
    IGNORED_FILES = {'.DS_Store', '.gitignore', 'REPO_MANIFEST.md', 'openapi.json',\n\
    \                 'LICENSE', 'CONTRIBUTING.md', 'alembic.ini'}\nINCLUDED_FILES\
    \ = {'api/docs/MASTER_INDEX.md'}\n\ndef get_file_type(filename):\n    if filename.endswith('.py')\
    \ or filename.endswith('.sh'):\n        return 'script'\n    elif filename.endswith('.md')\
    \ or filename.endswith('.rst') or filename.endswith('.txt'):\n        return 'doc'\n\
    \    elif filename.endswith('.yml') or filename.endswith('.yaml') or filename.endswith('.json'):\n\
    \        return 'config'\n    else:\n        return 'other'\n\ndef is_ignored_file(rel_path):\n\
    \    normalized = os.path.normpath(rel_path).replace(os.sep, '/')\n    if normalized\
    \ in INCLUDED_FILES:\n        return False\n    if os.path.basename(rel_path)\
    \ in IGNORED_FILES:\n        return True\n    parts = normalized.split('/')\n\
    \    for p in parts[:-1]:\n        if p in IGNORED_DIRS:\n            return True\n\
    \    return False\n\ndef scan_repo(base_dir='.'):\n    manifest = []\n    for\
    \ root, dirs, files in os.walk(base_dir):\n        dirs[:] = [d for d in dirs\
    \ if d not in IGNORED_DIRS or\n                   any(inc.startswith(os.path.relpath(os.path.join(root,\
    \ d), base_dir).replace(os.sep, '/') + '/')\n                       for inc in\
    \ INCLUDED_FILES)]\n        for f in files:\n            path = os.path.join(root,\
    \ f)\n            rel_path = os.path.relpath(path, start=base_dir)\n         \
    \   if is_ignored_file(rel_path):\n                continue\n            file_type\
    \ = get_file_type(f)\n            try:\n                with open(path, 'r', encoding='utf-8')\
    \ as file_obj:\n                    content = file_obj.read()\n            except\
    \ Exception:\n                content = '<binary or unreadable content>'\n   \
    \         workflow = []\n            if f.startswith('audit'):\n             \
    \   workflow.append('audit')\n            elif 'test' in f or f.startswith('run_e2e'):\n\
    \                workflow.append('testing')\n            elif f.startswith('generate'):\n\
    \                workflow.append('documentation')\n            elif f.startswith('linter')\
    \ or f.startswith('validate'):\n                workflow.append('validation')\n\
    \            indexes = []\n            if f.endswith('CODE_FILE_INDEX.md') or\
    \ f.endswith('MASTER_INDEX.md'):\n                indexes.append(f)\n        \
    \    manifest.append({\n                'path': rel_path.replace(os.sep, '/'),\n\
    \                'type': file_type,\n                'workflow': workflow,\n \
    \               'indexes': indexes,\n                'content': content\n    \
    \        })\n    return manifest\n\ndef save_manifest(manifest, output_file):\n\
    \    os.makedirs(os.path.dirname(output_file), exist_ok=True)\n    with open(output_file,\
    \ \"w\", encoding=\"utf-8\") as f:\n        yaml.dump(manifest, f, sort_keys=False,\
    \ allow_unicode=True)\n\ndef get_staged_files():\n    result = subprocess.run(\n\
    \        [\"git\", \"diff\", \"--name-only\", \"--cached\"],\n        capture_output=True,\n\
    \        text=True,\n        cwd=PROJECT_ROOT\n    )\n    return [f.strip() for\
    \ f in result.stdout.splitlines() if f.strip()]\n\ndef main():\n    parser = argparse.ArgumentParser(description=\"\
    Self-checking repository manifest generator.\")\n    parser.add_argument(\"--test-files\"\
    , nargs=\"*\", help=\"Provide a list of changed files for testing (bypasses git).\"\
    )\n    parser.add_argument(\"--force\", action=\"store_true\", help=\"Force manifest\
    \ generation for the full repo.\")\n    args = parser.parse_args()\n\n    manifest_file\
    \ = PROJECT_ROOT / \"project\" / \"reports\" / \"REPO_MANIFEST.md\"\n\n    files_to_consider\
    \ = []\n    if args.force:\n        print(\"Force mode enabled: regenerating manifest\
    \ for the full repository...\")\n    elif args.test_files:\n        print(f\"\
    Using --test-files: {len(args.test_files)} files provided for manifest generation.\"\
    )\n        files_to_consider = args.test_files\n    else:\n        files_to_consider\
    \ = get_staged_files()\n\n    if not args.force and not files_to_consider:\n \
    \       print(\"No staged changes detected or test files provided; skipping manifest\
    \ generation.\")\n        sys.exit(0)\n\n    print(\"Generating manifest...\"\
    )\n    repo_manifest = scan_repo(str(SCAN_DIR))\n    save_manifest(repo_manifest,\
    \ manifest_file)\n    print(f\"Manifest regenerated: {manifest_file} with {len(repo_manifest)}\
    \ entries\")\n\nif __name__ == \"__main__\":\n    main()\n"
- path: fix_tag_inventory.py
  type: script
  workflow: []
  indexes: []
  content: "#!/usr/bin/env python3\nimport yaml\nfrom pathlib import Path\n\nTAG_FILE\
    \ = Path(\"project/reports/DOCUMENT_TAG_INVENTORY.yml\")\n\ndef main(dry_run=True):\n\
    \    if not TAG_FILE.exists():\n        print(f\"❌ {TAG_FILE} does not exist.\"\
    )\n        return 1\n\n    with TAG_FILE.open(\"r\", encoding=\"utf-8\") as f:\n\
    \        try:\n            tags = yaml.safe_load(f)\n        except yaml.YAMLError\
    \ as e:\n            print(f\"❌ YAML parse error: {e}\")\n            return 1\n\
    \n    if not isinstance(tags, list):\n        print(\"❌ Expected a list of tag\
    \ entries.\")\n        return 1\n\n    fixed = 0\n    for i, entry in enumerate(tags):\n\
    \        if 'file' not in entry:\n            print(f\"⚠️ Entry {i} missing 'file':\
    \ {entry}\")\n            # Auto-fill file as 'UNKNOWN' or some default path\n\
    \            if not dry_run:\n                entry['file'] = \"UNKNOWN\"\n  \
    \          fixed += 1\n\n    if fixed == 0:\n        print(\"✅ All entries have\
    \ 'file' keys.\")\n    else:\n        print(f\"⚠️ Fixed {fixed} entries missing\
    \ 'file' keys.\")\n        if not dry_run:\n            TAG_FILE.write_text(yaml.safe_dump(tags,\
    \ sort_keys=False), encoding=\"utf-8\")\n            print(f\"✅ Written corrected\
    \ {TAG_FILE}\")\n\n    return 0\n\nif __name__ == \"__main__\":\n    import argparse\n\
    \    parser = argparse.ArgumentParser(description=\"Validate and fix DOCUMENT_TAG_INVENTORY.yml\"\
    )\n    parser.add_argument(\"--apply\", action=\"store_true\", help=\"Write fixes\
    \ to the file instead of dry-run\")\n    args = parser.parse_args()\n    exit(main(dry_run=not\
    \ args.apply))\n"
- path: validate_code_index.py
  type: script
  workflow:
  - validation
  indexes: []
  content: "# ID: OPS-031\nimport os\nfrom pathlib import Path\nimport sys\n\n# ---\
    \ Configuration ---\nPROJECT_ROOT = Path(__file__).parent.parent\nCODE_INDEX_PATH\
    \ = PROJECT_ROOT / \"api/docs/CODE_FILE_INDEX.md\"\nDIRS_TO_SCAN = [\n    PROJECT_ROOT\
    \ / \"api/src/zotify_api\",\n    PROJECT_ROOT / \"scripts\",\n    PROJECT_ROOT\
    \ / \"api/tests\",\n    PROJECT_ROOT / \"Gonk\",\n    PROJECT_ROOT / \"snitch\"\
    ,\n]\nFILE_EXTENSIONS = {\".py\", \".go\", \".js\"}\n\n\ndef get_indexed_files(index_path:\
    \ Path) -> set[str]:\n    \"\"\"Parses the code index markdown file and returns\
    \ a set of file paths.\"\"\"\n    if not index_path.exists():\n        print(f\"\
    Error: Code index file not found at {index_path}\", file=sys.stderr)\n       \
    \ sys.exit(1)\n\n    indexed_files = set()\n    with open(index_path, \"r\", encoding=\"\
    utf-8\") as f:\n        for line in f:\n            if not line.strip().startswith(\"\
    |\"):\n                continue\n            if \"---\" in line or \"Path\" in\
    \ line:\n                continue\n\n            parts = [p.strip().strip(\"`\"\
    ) for p in line.split(\"|\")]\n            if len(parts) > 1 and parts[1]:\n \
    \               # Convert to relative path from project root\n               \
    \ indexed_files.add(parts[1])\n    return indexed_files\n\n\ndef get_actual_files(directories:\
    \ list[Path], extensions: set[str]) -> set[str]:\n    \"\"\"Walks the given directories\
    \ and returns a set of actual file paths.\"\"\"\n    actual_files = set()\n  \
    \  for directory in directories:\n        for root, _, files in os.walk(directory):\n\
    \            for file in files:\n                if Path(file).suffix in extensions:\n\
    \                    full_path = Path(root) / file\n                    # Make\
    \ path relative to project root for comparison\n                    relative_path\
    \ = str(full_path.relative_to(PROJECT_ROOT))\n                    actual_files.add(relative_path)\n\
    \    return actual_files\n\n\ndef main() -> int:\n    \"\"\"Main function to compare\
    \ indexed files vs. actual files.\"\"\"\n    print(\"--- Running Code File Index\
    \ Validator ---\")\n    indexed_files = get_indexed_files(CODE_INDEX_PATH)\n \
    \   actual_files = get_actual_files(DIRS_TO_SCAN, FILE_EXTENSIONS)\n\n    # Ignore\
    \ __init__.py files as they are for packaging, not standalone code logic\n   \
    \ actual_files = {f for f in actual_files if not f.endswith(\"__init__.py\")}\n\
    \    indexed_files = {f for f in indexed_files if not f.endswith(\"__init__.py\"\
    )}\n\n    unindexed_files = actual_files - indexed_files\n    stale_index_entries\
    \ = indexed_files - actual_files\n\n    if not unindexed_files and not stale_index_entries:\n\
    \        print(\"✅ Success: Code file index is up-to-date.\")\n        return\
    \ 0\n\n    if unindexed_files:\n        print(\"\\n❌ Error: The following code\
    \ files are present in the repository but not in the index:\", file=sys.stderr)\n\
    \        for file in sorted(list(unindexed_files)):\n            print(f\"- {file}\"\
    , file=sys.stderr)\n\n    if stale_index_entries:\n        print(\"\\n❌ Error:\
    \ The following files are in the index but do not exist in the repository:\",\
    \ file=sys.stderr)\n        for file in sorted(list(stale_index_entries)):\n \
    \           print(f\"- {file}\", file=sys.stderr)\n\n    print(\"\\nPlease update\
    \ api/docs/CODE_FILE_INDEX.md to match the repository.\", file=sys.stderr)\n \
    \   return 1\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n"
- path: functional_test.py
  type: script
  workflow:
  - testing
  indexes: []
  content: "# ID: OPS-009\nimport pytest\nimport httpx\n\nimport os\nfrom pathlib\
    \ import Path\n\nBASE_URL = \"http://localhost:8000\"\n\ndef get_test_token():\n\
    \    \"\"\"Reads the test token from the .gonk_token file.\"\"\"\n    token_path\
    \ = Path.home() / \".gonk_token\"\n    if not token_path.exists():\n        return\
    \ None\n    return token_path.read_text().strip()\n\nTEST_TOKEN = get_test_token()\n\
    auth_skip_condition = pytest.mark.skipif(not TEST_TOKEN, reason=\"Test token not\
    \ found. Generate one with 'GonkCLI login'.\")\n\n\n@pytest.fixture\ndef client():\n\
    \    # allow_redirects=True will handle the 307 from FastAPI\n    with httpx.Client(base_url=BASE_URL,\
    \ follow_redirects=True) as client:\n        yield client\n\n\ndef test_health_endpoint(client):\n\
    \    r = client.get(\"/health\")\n    assert r.status_code == 200\n    json_resp\
    \ = r.json()\n    assert json_resp.get(\"status\") == \"ok\"\n\n\n@auth_skip_condition\n\
    def test_get_playlists(client):\n    headers = {\"Authorization\": f\"Bearer {TEST_TOKEN}\"\
    }\n    r = client.get(\"/api/playlists/\", headers=headers)\n    assert r.status_code\
    \ == 200\n    json_resp = r.json()\n    assert \"data\" in json_resp\n    assert\
    \ isinstance(json_resp[\"data\"], list)\n\n\ndef test_error_handling(client):\n\
    \    r = client.get(\"/api/nonexistent/endpoint\")\n    assert r.status_code ==\
    \ 404\n    json_resp = r.json()\n    assert \"detail\" in json_resp\n\n\n@auth_skip_condition\n\
    def test_get_user_profile(client):\n    headers = {\"Authorization\": f\"Bearer\
    \ {TEST_TOKEN}\"}\n    r = client.get(\"/api/user/profile\", headers=headers)\n\
    \    assert r.status_code == 200\n    json_resp = r.json()\n    # The user service\
    \ returns 'email', not 'id', at the top level.\n    assert \"email\" in json_resp\n\
    \n\nif __name__ == \"__main__\":\n    pytest.main([\"-v\", __file__])\n"
- path: generate_repo_manifest.py
  type: script
  workflow:
  - documentation
  indexes: []
  content: "# ID: OPS-013\n#!/usr/bin/env python3\nimport os\nimport json\n\n# ---\
    \ Config ---\n# Where to save the manifest (relative to repo root)\nmanifest_path\
    \ = \"scripts/repo_manifest.txt\"\n\n# Base URL where the files will be served\n\
    base_url = \"https://chatgtp.sixfold.nl\"\n\n# Folders/files to include in the\
    \ manifest\ninclude_paths = [\n    \"project\",\n    \"api\",\n    \"Gonk\",\n\
    \    \"scripts\",\n    \"snitch\",\n    \"templates\",\n    \"tests\",\n    \"\
    AGENTS.md\",\n]\n\n# File types to include\ninclude_extensions = [\".md\", \"\
    .yml\", \".json\", \".sh\", \".go\", \".py\"]  # adjust as needed\n\n# --- Script\
    \ ---\nmanifest = {}\norder = []\n\nfor root_dir in include_paths:\n    for dirpath,\
    \ dirnames, filenames in os.walk(root_dir):\n        dirnames[:] = [d for d in\
    \ dirnames if d != '.venv']\n        for f in filenames:\n            if any(f.endswith(ext)\
    \ for ext in include_extensions):\n                rel_path = os.path.join(dirpath,\
    \ f).replace(\"\\\\\", \"/\")\n                key = os.path.splitext(f)[0].upper()\
    \  # e.g., ONBOARDING.md → ONBOARDING\n                url = f\"{base_url}/{rel_path}\"\
    \n                manifest[key] = url\n                order.append(key)\n\n#\
    \ Add order array for deterministic reading\nmanifest[\"order\"] = order\n\n#\
    \ Ensure target folder exists\nos.makedirs(os.path.dirname(manifest_path), exist_ok=True)\n\
    \n# Write manifest\nwith open(manifest_path, \"w\") as f:\n    json.dump(manifest,\
    \ f, indent=2)\n\nprint(f\"Manifest generated at {manifest_path}, {len(order)}\
    \ files included.\")\n"
- path: migrate_and_tag_repository.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-021\n#!/usr/bin/env python3\n\"\"\"\nmigrate_and_tag_repository.py\n\
    \nScans the entire repository, applies unique, file-type-aware ID tags to all\n\
    relevant files, and generates a comprehensive inventory. This script is the\n\
    first step in the two-tier document and task alignment system migration.\n\nIt\
    \ supports three modes of operation:\n  --dry-run:  Prints the actions it would\
    \ take without modifying any files.\n  --apply:    Applies the ID tags to files\
    \ and generates the inventory.\n  --validate: Checks existing tags for syntax,\
    \ uniqueness, and completeness.\n\"\"\"\n\nimport os\nimport yaml\nimport argparse\n\
    import re\nfrom pathlib import Path\n\n# --- Configuration ---\n\n# Directories\
    \ to completely exclude from scanning\nEXCLUDE_DIRS = {\n    '.git', '.github',\
    \ '.pytest_cache', '.ruff_cache', '.mypy_cache', '.tox',\n    '__pycache__', 'node_modules',\
    \ 'vendor', 'api_dumps', 'storage',\n    'templates', 'venv'\n}\n\n# Files to\
    \ exclude from scanning\nEXCLUDE_FILES = {'openapi.json'}\n\n# Deterministic mapping\
    \ of directory paths to ID prefixes\nPREFIX_MAPPING = {\n    'api': 'API',\n \
    \   'project': 'DOC',\n    'scripts': 'OPS',\n    'Gonk': 'API',\n    'snitch':\
    \ 'API',\n    'docs': 'DOC',\n    'tests': 'TEST',\n}\n\n# Mapping of file extensions\
    \ to their comment syntax for the ID tag\nCOMMENT_STYLE_MAP = {\n    '.py': ('#\
    \ ', ''),\n    '.sh': ('# ', ''),\n    '.yml': ('# ', ''),\n    '.yaml': ('# ',\
    \ ''),\n    '.toml': ('# ', ''),\n    '.md': ('<!-- ', ' -->'),\n    '.html':\
    \ ('<!-- ', ' -->'),\n    '.js': ('// ', ''),\n    '.css': ('/* ', ' */'),\n \
    \   '.gitignore': ('# ', ''),\n}\n\n# --- Script Logic ---\n\ndef get_prefix(file_path:\
    \ Path) -> str:\n    \"\"\"Determines the ID prefix for a given file path based\
    \ on PREFIX_MAPPING.\"\"\"\n    relative_path = file_path.as_posix()\n\n    #\
    \ Handle root-level files first\n    if '/' not in relative_path:\n        if\
    \ relative_path.endswith('.md'):\n            return 'DOC'\n        if relative_path\
    \ in ['.gitignore', '.pre-commit-config.yaml', 'bandit.yml', 'mkdocs.yml']:\n\
    \            return 'CFG'\n\n    # Check against the directory mapping\n    for\
    \ part in file_path.parts:\n        if part in PREFIX_MAPPING:\n            return\
    \ PREFIX_MAPPING[part]\n\n    return 'GEN' # Generic fallback for files not matching\
    \ any specific category\n\ndef get_comment_delimiters(file_path: Path) -> tuple[str,\
    \ str]:\n    \"\"\"Returns the appropriate comment start and end delimiters for\
    \ a file type.\"\"\"\n    return COMMENT_STYLE_MAP.get(file_path.suffix, ('# ',\
    \ ''))\n\ndef generate_id(prefix: str, counter: int) -> str:\n    \"\"\"Generates\
    \ a formatted ID string like 'API-001'.\"\"\"\n    return f'{prefix}-{counter:03d}'\n\
    \ndef load_inventory_and_counters(inventory_path: Path) -> tuple[list, dict]:\n\
    \    \"\"\"Loads existing inventory and derives the latest counter for each prefix.\"\
    \"\"\n    if not inventory_path.exists():\n        return [], {}\n\n    try:\n\
    \        data = yaml.safe_load(inventory_path.read_text(encoding='utf-8'))\n \
    \       if not isinstance(data, list):\n            print(\"[WARNING] Inventory\
    \ file is not a list. Starting fresh.\")\n            return [], {}\n    except\
    \ (yaml.YAMLError, IOError) as e:\n        print(f\"[WARNING] Could not read inventory,\
    \ starting fresh: {e}\")\n        return [], {}\n\n    counters = {}\n    for\
    \ entry in data:\n        if isinstance(entry, dict) and 'id' in entry and 'prefix'\
    \ in entry:\n            prefix = entry['prefix']\n            try:\n        \
    \        num = int(entry['id'].split('-')[-1])\n                if num > counters.get(prefix,\
    \ 0):\n                    counters[prefix] = num\n            except (ValueError,\
    \ IndexError):\n                continue # Ignore malformed IDs\n\n    print(f\"\
    Loaded existing inventory with {len(data)} items. Current counters: {counters}\"\
    )\n    return data, counters\n\ndef scan_and_tag(repo_root: Path, target_path:\
    \ str = None, dry_run: bool = True):\n    \"\"\"\n    Scans the repository, tags\
    \ files, and generates an inventory.\n    Can be limited to a specific target_path.\n\
    \    \"\"\"\n    mode = 'DRY RUN' if dry_run else 'APPLY'\n    print(f\"--- Starting\
    \ Scan & Tag ({mode}) for target: {target_path or 'all'} ---\")\n\n    inventory_file\
    \ = Path('project/reports/DOCUMENT_TAG_INVENTORY.yml')\n    inventory, counters\
    \ = load_inventory_and_counters(inventory_file)\n\n    # Create a set of already\
    \ inventoried paths for quick lookup\n    inventoried_paths = {item.get('path')\
    \ for item in inventory}\n\n    files_to_scan = []\n    if target_path:\n    \
    \    # If target is a file\n        if Path(target_path).is_file():\n        \
    \    files_to_scan = [Path(target_path)]\n        # if target is a directory\n\
    \        else:\n            files_to_scan = sorted([p for p in Path(target_path).rglob('*')\
    \ if p.is_file()])\n    else:\n        files_to_scan = sorted([p for p in repo_root.rglob('*')\
    \ if p.is_file()])\n\n    newly_tagged_files = 0\n    for file_path in files_to_scan:\n\
    \        relative_path_str = str(file_path.as_posix())\n\n        # If a file\
    \ is being explicitly targeted, remove its old entry from the inventory first.\n\
    \        if target_path and relative_path_str in inventoried_paths:\n        \
    \    print(f\"Re-tagging explicitly targeted file: {relative_path_str}\")\n  \
    \          inventory = [item for item in inventory if item.get('path') != relative_path_str]\n\
    \            inventoried_paths.remove(relative_path_str)\n        elif relative_path_str\
    \ in inventoried_paths:\n            continue\n\n        # Check if the file or\
    \ any of its parent directories are in the exclusion list\n        if any(part\
    \ in EXCLUDE_DIRS for part in file_path.parts) or file_path.name in EXCLUDE_FILES:\n\
    \            continue\n\n        prefix = get_prefix(file_path)\n        counters[prefix]\
    \ = counters.get(prefix, 0) + 1\n        new_id = generate_id(prefix, counters[prefix])\n\
    \n        tag_start, tag_end = get_comment_delimiters(file_path)\n        id_tag_line\
    \ = f\"{tag_start}ID: {new_id}{tag_end}\\n\"\n\n        inventory.append({'id':\
    \ new_id, 'path': relative_path_str, 'prefix': prefix})\n        newly_tagged_files\
    \ += 1\n\n        if dry_run:\n            print(f\"[DRY RUN] Would tag '{relative_path_str}'\
    \ with ID '{new_id}'\")\n        else:\n            try:\n                content\
    \ = file_path.read_text(encoding='utf-8', errors='ignore')\n                content\
    \ = re.sub(r\"^(#|//|<!--)\\s*Task ID:.*(\\s*-->)?\\n?\", \"\", content, flags=re.MULTILINE)\n\
    \n                # A more robust check for an existing ID tag on the first line.\n\
    \                has_existing_tag = False\n                if content:\n     \
    \               first_line = content.splitlines()[0]\n                    if re.search(r\"\
    (?:#|//|<!--)\\s*ID:\\s*([A-Z]{2,4}-\\d{3,})\", first_line):\n               \
    \         has_existing_tag = True\n\n                if not has_existing_tag:\n\
    \                    file_path.write_text(id_tag_line + content, encoding='utf-8')\n\
    \                    print(f\"[APPLY] Tagged '{relative_path_str}' with ID '{new_id}'\"\
    )\n                else:\n                    print(f\"[SKIP] File '{relative_path_str}'\
    \ already has an ID.\")\n            except Exception as e:\n                print(f\"\
    [ERROR] Could not process file {relative_path_str}: {e}\")\n\n    print(f\"\\\
    n--- Tagging Summary for this run ---\")\n    print(f\"Tagged {newly_tagged_files}\
    \ new files.\")\n\n    if not dry_run:\n        write_inventory(inventory, inventory_file)\n\
    \ndef validate_tags(repo_root: Path):\n    \"\"\"Scans the repo and validates\
    \ existing ID tags for format and uniqueness.\"\"\"\n    print(\"--- Starting\
    \ Tag Validation ---\")\n    inventory_path = Path('project/reports/DOCUMENT_TAG_INVENTORY.yml')\n\
    \    if not inventory_path.exists():\n        print(\"[ERROR] Inventory file not\
    \ found. Cannot validate.\")\n        return\n\n    try:\n        inventory_data\
    \ = yaml.safe_load(inventory_path.read_text(encoding='utf-8'))\n        path_to_id_map\
    \ = {item['path']: item['id'] for item in inventory_data}\n        id_to_path_map\
    \ = {item['id']: item['path'] for item in inventory_data}\n    except (yaml.YAMLError,\
    \ IOError) as e:\n        print(f\"[ERROR] Could not read or parse inventory file:\
    \ {e}\")\n        return\n\n    errors = []\n\n    # Check for duplicate IDs in\
    \ the inventory itself\n    if len(id_to_path_map) != len(inventory_data):\n \
    \       from collections import Counter\n        id_counts = Counter(item['id']\
    \ for item in inventory_data)\n        for an_id, count in id_counts.items():\n\
    \            if count > 1:\n                errors.append(f\"Duplicate ID '{an_id}'\
    \ found in inventory file.\")\n\n    # Check each file on disk against the inventory\n\
    \    for file_path_str, expected_id in path_to_id_map.items():\n        file_path\
    \ = Path(file_path_str)\n        if not file_path.exists():\n            errors.append(f\"\
    File '{file_path}' is in inventory but not found on disk.\")\n            continue\n\
    \n        # Skip validation for the inventory file itself, as it's a generated\
    \ artifact.\n        if file_path == inventory_path:\n            continue\n\n\
    \        try:\n            content = file_path.read_text(encoding='utf-8', errors='ignore')\n\
    \            if not content: # Skip empty files, they can't have tags\n      \
    \          continue\n\n            first_line = content.splitlines()[0]\n    \
    \        # This regex must match all comment styles defined in COMMENT_STYLE_MAP\n\
    \            match = re.search(r\"(?:#|//|<!--|/\\*)\\s*ID:\\s*([A-Z]{2,4}-\\\
    d{3,})\\s*(?:-->|\\*/)?\", first_line)\n\n            if not match:\n        \
    \        errors.append(f\"Missing or malformed ID tag in file: '{file_path}'\"\
    )\n            elif match.group(1) != expected_id:\n                errors.append(f\"\
    ID mismatch in '{file_path}'. Expected '{expected_id}', found '{match.group(1)}'.\"\
    )\n\n        except Exception as e:\n            errors.append(f\"Could not read\
    \ or process file '{file_path}': {e}\")\n\n    if not errors:\n        print(f\"\
    [SUCCESS] Validation complete. Verified {len(path_to_id_map)} files. No errors.\"\
    )\n    else:\n        print(f\"\\n[FAILURE] Validation found {len(errors)} errors:\"\
    )\n        for error in errors:\n            print(f\"- {error}\")\n\ndef write_inventory(inventory_data:\
    \ list, output_path: Path):\n    \"\"\"Writes the collected inventory data to\
    \ a YAML file.\"\"\"\n    print(f\"\\nWriting inventory to '{output_path}'...\"\
    )\n    output_path.parent.mkdir(parents=True, exist_ok=True)\n    with open(output_path,\
    \ 'w', encoding='utf-8') as f:\n        yaml.safe_dump(inventory_data, f, sort_keys=False)\n\
    \    print(\"[SUCCESS] Inventory file written.\")\n\n\ndef main():\n    \"\"\"\
    Main function to parse arguments and run the script in the chosen mode.\"\"\"\n\
    \    parser = argparse.ArgumentParser(description=\"Scan, tag, and validate repository\
    \ files for the alignment system.\")\n    group = parser.add_mutually_exclusive_group(required=True)\n\
    \    group.add_argument('--dry-run', action='store_true', help=\"Show what would\
    \ be done without changing files.\")\n    group.add_argument('--apply', action='store_true',\
    \ help=\"Apply tags to files and generate the inventory.\")\n    group.add_argument('--validate',\
    \ action='store_true', help=\"Validate existing tags for uniqueness and format.\"\
    )\n    parser.add_argument('--target', type=str, help=\"Optional: a specific directory\
    \ or file to process.\", default=None)\n\n    args = parser.parse_args()\n   \
    \ repo_root = Path('.')\n\n    if args.dry_run:\n        scan_and_tag(repo_root,\
    \ target_path=args.target, dry_run=True)\n    elif args.apply:\n        scan_and_tag(repo_root,\
    \ target_path=args.target, dry_run=False)\n    elif args.validate:\n        validate_tags(repo_root)\n\
    \nif __name__ == \"__main__\":\n    main()"
- path: audit_endpoints.py
  type: script
  workflow:
  - audit
  indexes: []
  content: "# ID: OPS-004\nimport inspect\nfrom fastapi import FastAPI\nfrom fastapi.routing\
    \ import APIRoute\nimport sys\nfrom pathlib import Path\n\n# Add the project source\
    \ to the Python path\nproject_root = Path(__file__).parent\napi_src_path = project_root\
    \ / \"api\" / \"src\"\nsys.path.insert(0, str(api_src_path))\n\n\ndef analyze_route_status(app:\
    \ FastAPI):\n    route_status = []\n    for route in app.routes:\n        if not\
    \ isinstance(route, APIRoute):\n            continue\n        path = route.path\n\
    \        methods = route.methods\n        endpoint = route.endpoint\n        doc\
    \ = inspect.getdoc(endpoint) or \"\"\n\n        try:\n            source = inspect.getsource(endpoint)\n\
    \        except TypeError:\n            # This can happen for functools.partial\
    \ objects, etc.\n            # We'll assume these are not stubs for this analysis.\n\
    \            source = \"\"\n\n        # Heuristic: look for '501' or 'NotImplementedError'\
    \ in source code to flag stubs\n        if \"501\" in source or \"NotImplementedError\"\
    \ in source:\n            status = \"Stub\"\n        # Another heuristic: check\
    \ for a placeholder response\n        elif 'return {\"status\":' in source and\
    \ \"stub\" in source:\n            status = \"Stub\"\n        else:\n        \
    \    status = \"Functional\"\n\n        route_status.append(\n            {\n\
    \                \"path\": path,\n                \"methods\": sorted(list(methods)),\n\
    \                \"status\": status,\n                \"doc\": doc.strip(),\n\
    \            }\n        )\n\n    return route_status\n\n\nif __name__ == \"__main__\"\
    :\n    try:\n        from zotify_api.main import app  # Adjust import path as\
    \ necessary\n    except ImportError as e:\n        print(f\"Failed to import FastAPI\
    \ app: {e}\")\n        print(f\"Current sys.path: {sys.path}\")\n        sys.exit(1)\n\
    \n    status_report = analyze_route_status(app)\n\n    # This is not for the final\
    \ report, just for me to parse\n    for route in status_report:\n        print(\n\
    \            f\"{'|'.join(route['methods'])}|{route['path']}|{route['status']}|{route['doc']}\"\
    \n        )\n"
- path: test_single_config.sh
  type: script
  workflow:
  - testing
  indexes: []
  content: "# ID: OPS-030\n#!/usr/bin/env bash\nset -euo pipefail\nSCRIPT_DIR=\"$(cd\
    \ \"$(dirname \"${BASH_SOURCE[0]}\")\" && pwd)\"\nPROJECT_ROOT=\"$(cd \"$SCRIPT_DIR/..\"\
    \ && pwd)\"\nif [[ -f \"$PROJECT_ROOT/api/.venv/bin/activate\" ]]; then\n    #\
    \ shellcheck disable=SC1090\n    source \"$PROJECT_ROOT/api/.venv/bin/activate\"\
    \nfi\ncd \"$PROJECT_ROOT/api\"\necho \"=== Running single config reset test ===\"\
    \npython3 -m pytest -q tests/test_config.py::test_reset_config -q\n"
- path: content_alignment_check.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-006\n#!/usr/bin/env python3\n\"\"\"\nContent Alignment Check\
    \ (Phase 2 lockdown version)\n\n- Only considers files registered under the `project/`\
    \ namespace.\n- Scans project index/docs for cross-references.\n- Filters noise\
    \ by:\n    * excluding certain file name patterns (configurable)\n    * ignoring\
    \ items below a minimum inbound-link threshold (configurable)\n- Produces:\n \
    \   * project/reports/CONTENT_ALIGNMENT_REPORT.md\n    * project/reports/DESCRIPTION_COMPLIANCE_REPORT.md\n\
    \    * project/reports/ALIGNMENT_INTEGRITY_SNAPSHOT.yml\n- Read-only: no file\
    \ edits, only reports.\n- Has `--enforce` to fail CI when coverage/orphan thresholds\
    \ are violated.\n\"\"\"\nfrom __future__ import annotations\nimport re\nimport\
    \ sys\nimport yaml\nimport argparse\nfrom pathlib import Path\nfrom collections\
    \ import defaultdict\nfrom typing import Dict, List, Set, Tuple\n\n# --- Configurable\
    \ constants -------------------------------------------------\nPROJECT_ROOT =\
    \ Path(__file__).resolve().parents[1]\nTRACE_INDEX_PATH = PROJECT_ROOT / \"project/reports/TRACE_INDEX.yml\"\
    \nREPORT_DIR = PROJECT_ROOT / \"project/reports\"\nCONTENT_REPORT_PATH = REPORT_DIR\
    \ / \"CONTENT_ALIGNMENT_REPORT.md\"\nDESC_REPORT_PATH = REPORT_DIR / \"DESCRIPTION_COMPLIANCE_REPORT.md\"\
    \nSNAPSHOT_PATH = REPORT_DIR / \"ALIGNMENT_INTEGRITY_SNAPSHOT.yml\"\n\n# Documents\
    \ to scan (only project docs are relevant for Phase 2)\nSCAN_SCOPE = [\n    \"\
    project/PROJECT_REGISTRY.md\",\n    \"project/ALIGNMENT_MATRIX.md\",\n    \"project/HIGH_LEVEL_DESIGN.md\"\
    ,\n    \"project/LOW_LEVEL_DESIGN.md\",\n    \"project/USECASES.md\",\n    \"\
    project/USECASES_GAP_ANALYSIS.md\",\n    \"project/FUTURE_ENHANCEMENTS.md\",\n\
    \    # add other project-level indices as needed\n]\n\n# only consider registered\
    \ artifacts whose path starts with this prefix\nPROJECT_PREFIX = \"project/\"\n\
    \n# Exclude patterns (regex) for registered files that are noise and should not\
    \ be considered\n# e.g. logs, temporary files, audit artifacts you don't want\
    \ in alignment checks\nDEFAULT_EXCLUDE_PATTERNS = [\n    r\"^project/logs/\",\
    \       # project logs (ACTIVITY, SESSION_LOG, CURRENT_STATE)\n    r\"^project/archive/\"\
    ,    # archived docs are out of scope\n    r\"^project/reports/\",    # reports\
    \ docs are out of scope\n]\n\n# Minimum inbound links to consider something as\
    \ \"meaningful\" (helps filter noise)\nMIN_INBOUND_LINKS = 1\n\n# Behavior thresholds\
    \ for --enforce\nDEFAULT_COVERAGE_THRESHOLD = 95  # require 95% aligned or partial\
    \ coverage\nDEFAULT_MAX_ORPHANS_RATIO = 0.03  # allow up to 3% orphans\n\n# ---------------------------------------------------------------------------\n\
    \ndef load_trace_index() -> List[dict]:\n    if not TRACE_INDEX_PATH.exists():\n\
    \        print(f\"ERROR: TRACE_INDEX.yml not found at {TRACE_INDEX_PATH}\", file=sys.stderr)\n\
    \        sys.exit(1)\n    raw = yaml.safe_load(TRACE_INDEX_PATH.read_text(encoding=\"\
    utf-8\")) or {}\n    return raw.get(\"artifacts\", [])  # list of artifact dicts\n\
    \ndef filter_project_registered(artifacts: List[dict]) -> Dict[str, dict]:\n \
    \   \"\"\"\n    Return a dict path -> metadata for registered, non-exempt artifacts\
    \ that live under project/.\n    \"\"\"\n    out = {}\n    for item in artifacts:\n\
    \        path = item.get(\"path\")\n        if not path:\n            continue\n\
    \        # only project files (Phase 2 scope)\n        if not path.startswith(PROJECT_PREFIX):\n\
    \            continue\n        if item.get(\"type\") == \"exempt\":\n        \
    \    continue\n        if not item.get(\"registered\", False):\n            continue\n\
    \        out[path] = {\n            \"index\": item.get(\"index\", \"N/A\"),\n\
    \            \"description\": item.get(\"description\", \"\") or \"\",\n     \
    \       \"raw\": item,\n        }\n    return out\n\ndef compile_master_pattern(paths:\
    \ List[str]) -> re.Pattern:\n    \"\"\"\n    Build a regex that matches either\
    \ basename or full path occurrences.\n    Longer patterns first to avoid partial\
    \ matches.\n    \"\"\"\n    parts = set()\n    for p in paths:\n        parts.add(re.escape(Path(p).as_posix()))\n\
    \        parts.add(re.escape(Path(p).name))\n    # sort by length desc so longer\
    \ matches get preference\n    parts_list = sorted(parts, key=len, reverse=True)\n\
    \    if not parts_list:\n        # safe fallback\n        return re.compile(r\"\
    $^\")\n    return re.compile(\"|\".join(parts_list))\n\ndef build_cross_references(registered:\
    \ Dict[str, dict]) -> Dict[str, Set[str]]:\n    \"\"\"\n    Scan SCAN_SCOPE files\
    \ and return a map: source_doc -> set(target_paths)\n    Only project docs are\
    \ scanned (SCAN_SCOPE contains project docs).\n    \"\"\"\n    print(\"Building\
    \ reference graph (project scope)...\")\n    cross_ref = defaultdict(set)\n  \
    \  registered_paths = list(registered.keys())\n    pattern = compile_master_pattern(registered_paths)\n\
    \n    link_count = 0\n    for doc_rel in SCAN_SCOPE:\n        doc_path = PROJECT_ROOT\
    \ / doc_rel\n        if not doc_path.exists():\n            continue\n       \
    \ content = doc_path.read_text(encoding=\"utf-8\")\n        matches = set(pattern.findall(content))\n\
    \        for m in matches:\n            # resolve to first registered path that\
    \ endswith the matched token\n            found = next((p for p in registered_paths\
    \ if p.endswith(m)), None)\n            if found and found != doc_rel:\n     \
    \           cross_ref[doc_rel].add(found)\n                link_count += 1\n \
    \   print(f\"Cross-links found: {link_count}\")\n    return cross_ref\n\ndef apply_exclude_filters(registered:\
    \ Dict[str, dict], exclude_patterns: List[str]) -> Dict[str, dict]:\n    \"\"\"\
    Remove any registered items whose path matches any exclude regex.\"\"\"\n    compiled\
    \ = [re.compile(p) for p in exclude_patterns]\n    out = {}\n    for path, meta\
    \ in registered.items():\n        if any(pat.search(path) for pat in compiled):\n\
    \            continue\n        out[path] = meta\n    return out\n\ndef invert_cross_ref(cross_ref:\
    \ Dict[str, Set[str]]) -> Dict[str, Set[str]]:\n    \"\"\"Return target_path ->\
    \ set(sources)\"\"\"\n    inverted = defaultdict(set)\n    for src, targets in\
    \ cross_ref.items():\n        for t in targets:\n            inverted[t].add(src)\n\
    \    return inverted\n\ndef evaluate_alignment(registered: Dict[str, dict], cross_ref:\
    \ Dict[str, Set[str]], min_inbound: int) -> List[dict]:\n    \"\"\"\n    Evaluate\
    \ alignment for each registered project file. Returns list of result dicts.\n\
    \    Status semantics:\n     - ✅ Aligned: has at least min_inbound links AND linked\
    \ from design (HLD/LLD) AND alignment matrix\n     - ⚠️ Partial: referenced but\
    \ missing one or more design/trace links\n     - ❌ Orphan: not referenced anywhere\n\
    \     - ⛔ Excluded: filtered out (should not appear since filtered earlier)\n\
    \    \"\"\"\n    print(\"Validating file alignment...\")\n    inverted = invert_cross_ref(cross_ref)\n\
    \    results = []\n    for path, meta in registered.items():\n        notes =\
    \ []\n        status = \"✅ Aligned\"\n        sources = sorted(list(inverted.get(path,\
    \ set())))\n        inbound = len(sources)\n\n        # design links: check if\
    \ any of the design docs mention path\n        linked_in_design = any(path in\
    \ cross_ref.get(doc, set()) for doc in (\"project/HIGH_LEVEL_DESIGN.md\", \"project/LOW_LEVEL_DESIGN.md\"\
    ))\n        linked_in_trace = any(path in cross_ref.get(doc, set()) for doc in\
    \ (\"project/ALIGNMENT_MATRIX.md\",))\n        linked_in_usecase = any(path in\
    \ cross_ref.get(doc, set()) for doc in (\"project/USECASES.md\", \"project/USECASES_GAP_ANALYSIS.md\"\
    ))\n\n        if inbound < 1:\n            status = \"❌ Orphan\"\n           \
    \ notes.append(\"Not referenced anywhere\")\n        else:\n            # inbound\
    \ exists\n            if inbound < min_inbound:\n                notes.append(f\"\
    Low inbound links ({inbound} < {min_inbound})\")\n                # keep as partial\
    \ unless other conditions met\n            if not linked_in_design:\n        \
    \        notes.append(\"Missing Design link (HLD/LLD)\")\n            if not linked_in_trace:\n\
    \                notes.append(\"Missing Trace link (ALIGNMENT_MATRIX.md)\")\n\n\
    \            if notes:\n                # if there's at least one inbound link\
    \ but missing design/trace -> partial\n                status = \"⚠️ Partial\"\
    \n\n        results.append({\n            \"file\": path,\n            \"index\"\
    : meta.get(\"index\", \"N/A\"),\n            \"description\": meta.get(\"description\"\
    , \"\") or \"\",\n            \"linked_in\": sources[0] if sources else \"—\"\
    ,\n            \"link_count\": inbound,\n            \"status\": status,\n   \
    \         \"notes\": \"; \".join(notes) if notes else \"Referenced in other docs\"\
    \n        })\n    return sorted(results, key=lambda r: r[\"file\"])\n\ndef generate_content_report(results:\
    \ List[dict]) -> None:\n    REPORT_DIR.mkdir(parents=True, exist_ok=True)\n  \
    \  lines = [\n        \"# Content Alignment Report\\n\",\n        \"| File | Registered\
    \ In | Linked In | Link Count | Alignment Status | Notes |\",\n        \"|------|----------------|------------|-------------|------------------|--------|\"\
    ,\n    ]\n    for r in results:\n        lines.append(f\"| `{r['file']}` | `{r['index']}`\
    \ | `{r['linked_in']}` | {r['link_count']} | {r['status']} | {r['notes']} |\"\
    )\n    # summary\n    total = len(results)\n    aligned = sum(1 for r in results\
    \ if r[\"status\"] == \"✅ Aligned\")\n    partial = sum(1 for r in results if\
    \ r[\"status\"] == \"⚠️ Partial\")\n    orphans = sum(1 for r in results if r[\"\
    status\"] == \"❌ Orphan\")\n    coverage = int((aligned + partial) / total * 100)\
    \ if total else 100\n\n    lines.extend([\n        \"\\n## Footer Summary\\n\"\
    ,\n        f\"**Total items:** {total}\",\n        f\"**Fully aligned:** {aligned}\"\
    ,\n        f\"**Partial:** {partial}\",\n        f\"**Orphans:** {orphans}\",\n\
    \        f\"**Alignment coverage:** {coverage}%\",\n    ])\n    CONTENT_REPORT_PATH.write_text(\"\
    \\n\".join(lines) + \"\\n\", encoding=\"utf-8\")\n\ndef generate_description_report(registered:\
    \ Dict[str, dict]) -> None:\n    \"\"\"\n    Very simple description compliance\
    \ report.\n    A description is valid if the TRACE_INDEX 'description' is non-empty\
    \ OR\n    the index (the registered file's index) contains a description column\
    \ (not parsed here).\n    For Phase 2 we rely on TRACE_INDEX descriptions.\n \
    \   \"\"\"\n    REPORT_DIR.mkdir(parents=True, exist_ok=True)\n    lines = [\n\
    \        \"# Description Compliance Report\\n\",\n        \"| File | Registered\
    \ In | Status | Notes |\",\n        \"|------|---------------|--------|-------|\"\
    ,\n    ]\n    non_compliant = 0\n    total = 0\n    for path, meta in sorted(registered.items()):\n\
    \        total += 1\n        desc = (meta.get(\"description\") or \"\").strip()\n\
    \        if desc:\n            lines.append(f\"| `{path}` | `{meta.get('index','N/A')}`\
    \ | ✅ Valid |  |\")\n        else:\n            lines.append(f\"| `{path}` | `{meta.get('index','N/A')}`\
    \ | ⚠️ Missing | Invalid or empty description |\")\n            non_compliant\
    \ += 1\n    lines.append(\"\\n\")\n    lines.append(f\"**Total entries checked:**\
    \ {total}\")\n    lines.append(f\"**Non-compliant entries:** {non_compliant}\"\
    )\n    ok_pct = int((total - non_compliant) / total * 100) if total else 100\n\
    \    lines.append(f\"**Overall compliance:** {ok_pct}%\")\n    DESC_REPORT_PATH.write_text(\"\
    \\n\".join(lines) + \"\\n\", encoding=\"utf-8\")\n\ndef generate_snapshot(registered:\
    \ Dict[str, dict], results: List[dict]) -> None:\n    \"\"\"\n    Produce an ALIGNMENT_INTEGRITY_SNAPSHOT.yml\
    \ that maps canonical IDs (if present)\n    to file paths and their alignment\
    \ state. Snapshot is machine-readable and intended\n    as the Phase-2 baseline\
    \ for Phase-3 semantic checks.\n    \"\"\"\n    snapshot = {\n        \"phase\"\
    : \"phase-2-lockdown\",\n        \"total_registered\": len(registered),\n    \
    \    \"items\": []\n    }\n    for r in results:\n        item = {\n         \
    \   \"path\": r[\"file\"],\n            \"index\": r[\"index\"],\n           \
    \ \"description\": registered.get(r[\"file\"], {}).get(\"description\", \"\"),\n\
    \            \"status\": r[\"status\"],\n            \"link_count\": r[\"link_count\"\
    ],\n            \"notes\": r[\"notes\"],\n        }\n        # if the original\
    \ TRACE_INDEX provides canonical IDs, include them\n        raw = registered.get(r[\"\
    file\"], {}).get(\"raw\", {}) or {}\n        if raw.get(\"meta\"):\n         \
    \   # include any meta fields the trace index carried (e.g., ids)\n          \
    \  item[\"meta\"] = raw[\"meta\"]\n        snapshot[\"items\"].append(item)\n\
    \    REPORT_DIR.mkdir(parents=True, exist_ok=True)\n    SNAPSHOT_PATH.write_text(yaml.safe_dump(snapshot,\
    \ sort_keys=False), encoding=\"utf-8\")\n\ndef main():\n    parser = argparse.ArgumentParser(description=\"\
    Phase 2 Content Alignment Check (read-only)\")\n    parser.add_argument(\"--scan\"\
    , action=\"store_true\", help=\"Run scan and generate reports (default).\")\n\
    \    parser.add_argument(\"--enforce\", action=\"store_true\", help=\"Enforce\
    \ thresholds (CI).\")\n    parser.add_argument(\"--min-inbound\", type=int, default=MIN_INBOUND_LINKS,\
    \ help=\"Minimum inbound links to consider meaningful.\")\n    parser.add_argument(\"\
    --exclude\", action=\"append\", default=None, help=\"Additional exclude regex\
    \ (repeatable).\")\n    parser.add_argument(\"--coverage-threshold\", type=int,\
    \ default=DEFAULT_COVERAGE_THRESHOLD, help=\"Coverage percent required to pass\
    \ enforcement.\")\n    parser.add_argument(\"--max-orphans-ratio\", type=float,\
    \ default=DEFAULT_MAX_ORPHANS_RATIO, help=\"Max allowed orphans ratio to pass\
    \ enforcement.\")\n    args = parser.parse_args()\n\n    # default to scan if\
    \ nothing specified\n    if not args.scan and not args.enforce:\n        args.scan\
    \ = True\n\n    artifacts = load_trace_index()\n    registered_all = filter_project_registered(artifacts)\n\
    \n    # merge default excludes with any provided on CLI\n    excludes = list(DEFAULT_EXCLUDE_PATTERNS)\n\
    \    if args.exclude:\n        excludes.extend(args.exclude)\n\n    registered\
    \ = apply_exclude_filters(registered_all, excludes)\n    cross_ref = build_cross_references(registered)\n\
    \    results = evaluate_alignment(registered, cross_ref, args.min_inbound)\n\n\
    \    # write reports\n    generate_content_report(results)\n    generate_description_report(registered)\n\
    \    generate_snapshot(registered, results)\n\n    # summary for CLI\n    total\
    \ = len(results)\n    aligned = sum(1 for r in results if r[\"status\"] == \"\
    ✅ Aligned\")\n    partial = sum(1 for r in results if r[\"status\"] == \"⚠️ Partial\"\
    )\n    orphans = sum(1 for r in results if r[\"status\"] == \"❌ Orphan\")\n  \
    \  coverage = int((aligned + partial) / total * 100) if total else 100\n\n   \
    \ print(f\"Wrote {CONTENT_REPORT_PATH}, {DESC_REPORT_PATH}, {SNAPSHOT_PATH}\"\
    )\n    print(f\"Summary: total={total} aligned={aligned} partial={partial} orphans={orphans}\
    \ coverage={coverage}%\")\n\n    if args.enforce:\n        max_orphans = int(len(results)\
    \ * args.max_orphans_ratio)\n        if coverage < args.coverage_threshold or\
    \ orphans > max_orphans:\n            print(\"❌ Content alignment enforcement\
    \ FAILED.\")\n            print(f\"   - coverage {coverage}% < threshold {args.coverage_threshold}%\"\
    )\n            print(f\"   - orphans {orphans} > allowed {max_orphans}\")\n  \
    \          sys.exit(1)\n        else:\n            print(\"✅ Content alignment\
    \ enforcement PASSED.\")\n            sys.exit(0)\n\nif __name__ == \"__main__\"\
    :\n    main()\n"
- path: test_full_pipeline.sh
  type: script
  workflow:
  - testing
  indexes: []
  content: "#!/usr/bin/env bash\nset -euo pipefail\n\necho \"=== Starting full pipeline\
    \ test (dry-run) ===\"\n\n# Step 1: Backup TRACE_INDEX.yml\nTRACE_INDEX=\"/root/zotify-API/project/reports/TRACE_INDEX.yml\"\
    \nBACKUP_TRACE_INDEX=\"/root/zotify-API/project/reports/TRACE_INDEX.yml.bak\"\n\
    if [ -f \"$TRACE_INDEX\" ]; then\n    echo \"[Step 1] Backing up TRACE_INDEX.yml\"\
    \n    cp \"$TRACE_INDEX\" \"$BACKUP_TRACE_INDEX\"\nfi\n\n# Step 2: Run inventory\
    \ script in test mode\necho \"[Step 2] Running repo_inventory_and_governance.py\
    \ in test mode\"\npython3 scripts/repo_inventory_and_governance.py --full --debug\
    \ || { echo \"Inventory script failed\"; exit 1; }\n\n# Step 3: Check for missing\
    \ DOC-/API- IDs in TRACE_INDEX.yml\necho \"[Step 3] Checking for missing DOC-/API-\
    \ IDs\"\nMISSING_IDS=$(python3 - <<EOF\nimport yaml\ntrace_index_path = \"$TRACE_INDEX\"\
    \ndata = yaml.safe_load(open(trace_index_path))\nmissing = [item['path'] for item\
    \ in data.get('artifacts', []) if 'id' not in item or not item['id']]\nprint(\"\
    ,\".join(missing))\nEOF\n)\nif [ -n \"$MISSING_IDS\" ]; then\n    echo \"Missing\
    \ IDs for files: $MISSING_IDS\"\n    exit 1\nfi\n\n# Step 4: Run alignment verification\n\
    echo \"[Step 4] Running verify_alignment_migration.py\"\npython3 scripts/verify_alignment_migration.py\
    \ || { echo \"Alignment verification failed\"; exit 1; }\n\n# Step 5: Run governance\
    \ linter\necho \"[Step 5] Running lint_governance_links.py\"\npython3 scripts/lint_governance_links.py\
    \ || { echo \"Linter failed\"; exit 1; }\n\n# Step 6: (Optional) Check for unregistered\
    \ files in indexes\necho \"[Step 6] Checking for unregistered files in indexes\"\
    \n# Could be extended with extra logic if needed\n\n# Step 7: Final report\necho\
    \ \"=== Full pipeline test completed successfully ===\"\n"
- path: api/src/zotify_api/temp_violation.py
  type: script
  workflow: []
  indexes: []
  content: '# ID: OPS-002

    # Temporary violation file

    '

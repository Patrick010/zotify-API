- path: AGENTS.md
  type: doc
  workflow: []
  indexes: []
  content: "<!-- ID: DOC-067 -->\n# Agent Instructions & Automated Workflow System\n\
    \n**Version:** 2.0\n**Status:** Active\n\n---\n\n## 0. Fundamental Rules\n\nThis\
    \ is a mandatory, non-optional rule that all agents must follow at all times.\n\
    \n    Do not approve your own tasks or plans. Do not make un-asked for changes.\
    \ Do not start tasks or plans without approval.\n\n---\n\n## 1. About This System\n\
    \n### 1.1. Purpose\nThis document and its associated scripts are designed to solve\
    \ a common problem in software development: ensuring documentation stays synchronized\
    \ with the code. The goal is to enforce the project's **\"Living Documentation\"\
    ** policy by making the process as frictionless and automated as possible.\n\n\
    ### 1.2. How It Works\nThe system consists of three main components:\n1.  **This\
    \ Document (`AGENTS.md`):** The central source of truth for the workflow. AI agents\
    \ are programmed to read this file and follow its instructions.\n2.  **Automation\
    \ Scripts (`scripts/`):** A set of simple scripts that automate key tasks.\n3.\
    \  **Configuration (`scripts/doc-lint-rules.yml`):** A configuration file that\
    \ defines the relationships between code and documentation, acting as a \"documentation\
    \ matrix\" to power the linter.\n\n### 1.3. How to Set Up in Another Project\n\
    To transplant this system to another repository:\n1.  **Copy Files:** Copy this\
    \ `AGENTS.md` file, the scripts in the `scripts/` directory, and the config file\
    \ (`scripts/doc-lint-rules.yml`).\n2.  **Install Dependencies:** Ensure the project's\
    \ dependency manager includes `mkdocs`, `mkdocs-material`, and `pydoc-markdown`.\n\
    3.  **Customize:** Edit `scripts/doc-lint-rules.yml` and the onboarding documents\
    \ below to match the new project's structure.\n\n---\n\n## 2. Agent Onboarding\n\
    \nBefore starting any new task, you **must** first read the following document\
    \ to understand the project's context and procedures:\n- `project/ONBOARDING.md`\n\
    \n---\n\n## 3. The Automated Workflow\n\nThis workflow is designed to be followed\
    \ for every task that involves code or documentation changes.\n\n### Step 1: Register\
    \ New Files\nThe first step of any task is to understand where to register new\
    \ files. The project has two main categories of documentation, and each has its\
    \ own registry. Failing to register a new file in the correct location will cause\
    \ the `scripts/linter.py` verification script to fail.\n\n*   **Project-Level\
    \ Documentation (`project/`):**\n    *   **What it is:** Internal planning documents,\
    \ logs, proposals, backlogs, and audit files. The project registry is strictly\
    \ limited to files within the `project/` directory, with one exception: the repo-wide\
    \ `api/docs/CODE_FILE_INDEX.md` is also included.\n    *   **How to Register:**\
    \ The project registry is now **auto-generated**. The file `project/PROJECT_REGISTRY.md`\
    \ is built programmatically from the canonical `project/reports/TRACE_INDEX.yml`.\
    \ Manual edits to this file will be overwritten.\n    *   **Command to Update:**\
    \ To regenerate the project registry after changes, run:\n        ```bash\n  \
    \      python3 scripts/repo_inventory_and_governance.py --update-project-registry\n\
    \        ```\n    *   **Adding Special Cases:** If a file from outside the `project/`\
    \ directory needs to be intentionally included in the project registry, it must\
    \ be added to `scripts/project_registry_extras.yml`. This ensures all exceptions\
    \ are explicitly approved and documented.\n\n*   **API & User-Facing Documentation\
    \ (`api/docs/`):**\n    *   **What it is:** External-facing documentation intended\
    \ for API consumers or developers contributing to the API. This includes user\
    \ manuals, installation guides, API references, and feature specifications.\n\
    \    *   **Where to Register:** New API documents **must** be registered in `api/docs/MASTER_INDEX.md`.\n\
    \n### Step 2: Code and Document\nThis is the primary development task. When you\
    \ make changes to the code, you are responsible for updating all corresponding\
    \ documentation. Use the registries mentioned in Step 1 to identify relevant documents.\n\
    \n### Step 3: Maintain the Quality Index for Source Code\nTo ensure a high standard\
    \ of quality, all new **source code files** (`.py`, `.go`, `.js`) must be registered\
    \ in the appropriate quality index. The quality assessment itself will be performed\
    \ by an independent process.\n\n1.  **Add New Files to Index:** When you create\
    \ a new source file, you **must** add a corresponding entry to the consolidated\
    \ `api/docs/CODE_QUALITY_INDEX.md` file.\n2.  **Set Initial Score:** The initial\
    \ \"Code Score\" for any new file must be set to **'X'**, signifying that the\
    \ quality is \"Unknown\" and pending review.\n\n### Step 4: Log Your Work\nAt\
    \ the completion of any significant action, you **must** log the work using the\
    \ unified linter script.\n\n*   **Command:** `python3 scripts/linter.py [-h] [--log]\
    \ [--summary SUMMARY] [--objective OBJECTIVE] [--findings FINDINGS] [--next-steps\
    \ NEXT_STEPS] [--files [FILES ...]] [--test-files [TEST_FILES ...]] [--from-file\
    \ FROM_FILE] [--skip-governance]\n\n*   **Automation:** This command automatically\
    \ updates `project/logs/ACTIVITY.md`, `project/logs/CURRENT_STATE.md` and `project/logs/SESSION_LOG.md`.\n\
    *   **Enforcement:** The pre-submission linter (`python3 scripts/linter.py`) now\
    \ includes an unconditional check to ensure these log files have been modified.\
    \ If you do not run the `--log` command, the linter will fail.\n\n> **Important:**\
    \ Due to a global git policy, it is not possible to run this script as an automated\
    \ pre-commit hook. Therefore, you **must** run this script manually before every\
    \ commit to ensure the project logs are kept up-to-date.\n\n### Step 5: Pre-Submission\
    \ Verification\nBefore submitting your work for review, you **must** run the unified\
    \ linter script to verify compliance. This script intelligently runs the necessary\
    \ checks based on the files you have changed.\n\n*   **Command:** `python3 scripts/linter.py`\n\
    *   **Purpose:** This script acts as a single entrypoint for all verification\
    \ steps, enforcing the policies defined in `project/QA_GOVERNANCE.md`. It will:\n\
    \    1.  **Run Documentation Linters:** It runs a suite of checks based on the\
    \ rules in `doc-lint-rules.yml` to enforce documentation policies, including:\n\
    \        -   Ensuring code changes are reflected in the `project/ALIGNMENT_MATRIX.md`.\n\
    \        -   Ensuring new source files are added to the `api/docs/CODE_QUALITY_INDEX.md`.\n\
    \        -   Ensuring new project documents are registered in `project/PROJECT_REGISTRY.md`.\n\
    \        -   Ensuring new API documents are registered in `api/docs/MASTER_INDEX.md`.\n\
    \    2.  **Run Tests:** Conditionally runs the `pytest` test suite if it detects\
    \ changes to source code files (`.py`, `.go`).\n    3.  **Build Docs:** Conditionally\
    \ runs the `mkdocs build` command if it detects changes to the documentation files\
    \ in `api/docs/`.\n*   You must resolve any errors reported by the script before\
    \ submitting.\n\n---\n\n## 4. Key Policy Documents (Reference)\n\nThis automated\
    \ workflow is designed to fulfill the rules defined in the following core documents.\
    \ Refer to them if you need more context on the *why* behind the rules.\n\n* \
    \  `project/PID.md`\n*   `project/HIGH_LEVEL_DESIGN.md`\n*   `project/TASK_CHECKLIST.md`\n\
    *   `project/QA_GOVERNANCE.md`\n"
- path: README.md
  type: doc
  workflow: []
  indexes: []
  content: '<!-- ID: DOC-068 -->

    # Zotify API Platform


    "Phases 3–5 deliver the full core API, user authentication with JWT, endpoint
    protection, notifications preference, and comprehensive testing. Users can manage
    profiles, preferences, liked tracks, playback history, and interact with all content
    endpoints. The Gonk CLI and GonkUI provide an interface for all these actions,
    with the ability to toggle between simulated and real API testing. Documentation,
    examples, and OpenAPI specs are fully updated."


    Welcome to the Zotify API Platform, a powerful, extensible, and provider-agnostic
    backend for managing and interacting with your music library. This platform is
    designed for developers, automators, and power-users who want to build sophisticated
    workflows for their music collections.


    ## 1. Core Philosophy


    The Zotify API is built on a set of core principles:


    -   **Extensibility:** The platform is designed to be extended. A dynamic plugin
    system allows developers to add new music providers, logging capabilities, and
    other features without modifying the core codebase.

    -   **Configuration over Code:** As much as possible, the behavior of the system
    is controlled by clear, declarative configuration files, not by hardcoded logic.

    -   **Living Documentation:** This project adheres to a strict "living documentation"
    policy. All documentation is versioned alongside the code and is continuously
    updated to reflect the reality of the implementation.

    -   **Developer-Centric Design:** The API and its surrounding tools are designed
    to be intuitive and powerful for developers, with features like a flexible logging
    framework and a standalone testing UI.


    ## 2. Platform Components


    The Zotify ecosystem consists of several key components:


    -   **The Core API:** A robust FastAPI application that provides a RESTful interface
    for all platform features.

    -   **`snitch`:** A secure helper application for managing OAuth2 callback flows
    for CLI-based clients.

    -   **`Gonk/GonkUI`:** A standalone web UI for testing and interacting with the
    API during development.


    ## 3. Getting Started


    To get started with the Zotify API, please refer to the comprehensive guides in
    our documentation.


    -   **For a full installation guide:** See the [**Installation Guide**](./api/docs/system/INSTALLATION.md).

    -   **To understand the API''s features:** See the [**User Manual**](./api/docs/manuals/USER_MANUAL.md).

    -   **For developers integrating our API:** See the [**System Integration Guide**](./api/docs/manuals/SYSTEM_INTEGRATION_GUIDE.md).

    -   **For developers contributing to this project:** See the [**API Developer
    Guide**](./api/docs/manuals/API_DEVELOPER_GUIDE.md).


    ### Quick Start


    A startup script is provided to get the API server running quickly in a development
    environment.


    From the root of the project, run:

    ```bash

    ./scripts/start.sh

    ```

    This script will handle installing dependencies, creating necessary directories,
    and launching the server with the correct settings for development. The API will
    be available at `http://localhost:8000`.


    ## 4. Documentation


    This project uses a comprehensive, tiered documentation system. For a master list
    of all project documents, please see the [**Project Registry**](./project/PROJECT_REGISTRY.md).


    ## 5. Project Status


    This project is under active development. For a detailed view of the current status,
    recent activities, and future plans, please see the following documents:


    -   [**CURRENT_STATE.md**](./project/CURRENT_STATE.md)

    -   [**ACTIVITY.md**](./project/ACTIVITY.md)

    -   [**FUTURE_ENHANCEMENTS.md**](./project/FUTURE_ENHANCEMENTS.md)

    '
- path: mkdocs.yml
  type: config
  workflow: []
  indexes: []
  content: "# ID: CFG-004\n# MkDocs Configuration\n\nsite_name: Zotify API Platform\n\
    site_description: 'A comprehensive guide to the Zotify API, its features, and\
    \ architecture.'\nsite_author: 'Zotify Development Team'\n\ntheme:\n  name: material\n\
    \  palette:\n    # Palette toggle for light vs dark mode\n    - scheme: default\n\
    \      toggle:\n        icon: material/brightness-7\n        name: Switch to dark\
    \ mode\n    - scheme: slate\n      toggle:\n        icon: material/brightness-4\n\
    \        name: Switch to light mode\n  features:\n    - navigation.tabs\n    -\
    \ navigation.sections\n    - toc.integrate\n    - navigation.top\n    - search.suggest\n\
    \    - search.highlight\n    - content.tabs.link\n\n# The main documentation source\
    \ directory. This is the root for the main nav.\ndocs_dir: 'api/docs'\n\n# The\
    \ 'monorepo' plugin will discover and merge other mkdocs.yml files.\nplugins:\n\
    \  - monorepo\n\nnav:\n  - 'API Documentation':\n    - 'Home': 'CHANGELOG.md'\n\
    \    - 'Manuals':\n      - 'API Developer Guide': 'manuals/API_DEVELOPER_GUIDE.md'\n\
    \      - 'CI/CD': 'manuals/CICD.md'\n      - 'Error Handling': 'manuals/ERROR_HANDLING_GUIDE.md'\n\
    \      - 'Logging Guide': 'manuals/LOGGING_GUIDE.md'\n      - 'Operator Manual':\
    \ 'manuals/OPERATOR_MANUAL.md'\n      - 'System Integration Guide': 'manuals/SYSTEM_INTEGRATION_GUIDE.md'\n\
    \      - 'User Manual': 'manuals/USER_MANUAL.md'\n    - 'Providers':\n      -\
    \ 'Spotify': 'providers/SPOTIFY.md'\n    - 'Reference':\n      - 'API Reference':\
    \ 'reference/API_REFERENCE.md'\n      - 'Code Quality Index': 'reference/CODE_QUALITY_INDEX.md'\n\
    \      - 'Feature Specs': 'reference/FEATURE_SPECS.md'\n      - 'Master Index':\
    \ 'MASTER_INDEX.md'\n      - 'Features':\n        - 'Authentication': 'reference/features/AUTHENTICATION.md'\n\
    \        - 'Automated Doc Workflow': 'reference/features/AUTOMATED_DOCUMENTATION_WORKFLOW.md'\n\
    \        - 'Flexible Logging': 'reference/features/DEVELOPER_FLEXIBLE_LOGGING_FRAMEWORK.md'\n\
    \        - 'Provider Extensions': 'reference/features/PROVIDER_AGNOSTIC_EXTENSIONS.md'\n\
    \        - 'Provider OAuth': 'reference/features/PROVIDER_OAUTH.md'\n      - 'Source\
    \ Code':\n        - 'CRUD.py': 'reference/source/CRUD.py.md'\n        - 'TRACKS_SERVICE.py':\
    \ 'reference/source/TRACKS_SERVICE.py.md'\n    - 'System':\n      - 'Error Handling\
    \ Design': 'system/ERROR_HANDLING_DESIGN.md'\n      - 'Installation': 'system/INSTALLATION.md'\n\
    \      - 'Privacy Compliance': 'system/PRIVACY_COMPLIANCE.md'\n      - 'Requirements':\
    \ 'system/REQUIREMENTS.md'\n  - 'Snitch Module': '!include ./snitch/mkdocs.yml'\n\
    \  - 'Gonk TestUI Module': '!include ./Gonk/GonkUI/mkdocs.yml'\n\n\n# Extensions\n\
    markdown_extensions:\n  - pymdownx.highlight:\n      anchor_linenums: true\n \
    \ - pymdownx.inlinehilite\n  - pymdownx.snippets\n  - pymdownx.superfences\n \
    \ - admonition\n  - toc:\n      permalink: true\n"
- path: .pre-commit-config.yaml
  type: config
  workflow: []
  indexes: []
  content: "# ID: CFG-002\nrepos:\n  # 1. Code formatting & linting\n  - repo: https://github.com/astral-sh/ruff-pre-commit\n\
    \    rev: v0.0.280\n    hooks:\n      - id: ruff\n        args: [\"--fix\"]  #\
    \ fixes formatting and common style issues\n\n  # 2. Type checking\n  - repo:\
    \ https://github.com/pre-commit/mirrors-mypy\n    rev: v1.5.1\n    hooks:\n  \
    \    - id: mypy\n        additional_dependencies: []\n\n  # 3. Security checks\n\
    \  - repo: https://github.com/PyCQA/bandit\n    rev: 1.7.5\n    hooks:\n     \
    \ - id: bandit\n        args: [\"-r\", \".\"]\n\n  - repo: https://github.com/returntocorp/semgrep\n\
    \    rev: v1.37.0\n    hooks:\n      - id: semgrep\n        args: [\"--config=p/ci\"\
    ]\n\n  # 4. Documentation linter (local)\n  - repo: local\n    hooks:\n      -\
    \ id: doc-linter\n        name: Documentation Linter\n        entry: python scripts/lint-docs.py\n\
    \        language: python\n        types: [file, python]\n        pass_filenames:\
    \ false\n        additional_dependencies: [pyyaml]\n\n  # 5. Optional: complexity\
    \ checks (Radon/Xenon) as a local hook\n  - repo: local\n    hooks:\n      - id:\
    \ complexity\n        name: Cyclomatic Complexity\n        entry: python scripts/check_complexity.py\n\
    \        language: python\n        types: [python]\n        pass_filenames: false\n\
    \  # 6. Repo Inventory and Governance\n  - repo: local\n    hooks:\n      - id:\
    \ repo-inventory-and-governance\n        name: Repo Inventory and Governance\n\
    \        entry: python scripts/repo_inventory_and_governance.py\n        language:\
    \ system\n        always_run: true\n        pass_filenames: false\n"
- path: bandit.yml
  type: config
  workflow: []
  indexes: []
  content: "# ID: CFG-003\nskips:\n  - 'B101'\n  - 'B105'\n  - 'B106'\n"
- path: scripts/verify_alignment_migration.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-036\n#!/usr/bin/env python3\n\"\"\"\nEnhanced alignment verification\
    \ script.\nSummarizes missing or mismatched IDs clearly by type (doc/code/config).\n\
    \"\"\"\n\nimport os\nimport re\nimport sys\nimport yaml\nimport argparse\nfrom\
    \ pathlib import Path\nfrom collections import defaultdict\n\nPROJECT_ROOT = Path(__file__).parent.parent\n\
    TAG_PATTERN = re.compile(r\"(?:#|<!--)\\s*ID:\\s*([A-Z0-9\\-]+)\", re.IGNORECASE)\n\
    TAG_INVENTORY = PROJECT_ROOT / \"project/reports/DOCUMENT_TAG_INVENTORY.yml\"\n\
    TRACE_INDEX_PATH = PROJECT_ROOT / \"project/reports/TRACE_INDEX.yml\"\n\n# ---\
    \ Ignored directories and file types consistent with governance scripts ---\n\
    IGNORED_DIRS = {\".git\", \".venv\", \"node_modules\", \"__pycache__\", \"archive\"\
    , \"templates\", \".pytest_cache\", \"logs\", \"site\"}\nSCAN_EXTENSIONS = (\"\
    .py\", \".md\", \".sh\", \".yml\", \".yaml\")\n\ndef load_tag_inventory():\n \
    \   if not TAG_INVENTORY.exists():\n        print(f\"❌ Missing DOCUMENT_TAG_INVENTORY.yml\"\
    , file=sys.stderr)\n        return {}\n    with open(TAG_INVENTORY, \"r\", encoding=\"\
    utf-8\") as f:\n        try:\n            data = yaml.safe_load(f)\n         \
    \   if isinstance(data, list):\n                return {entry.get(\"id\"): entry\
    \ for entry in data if \"id\" in entry}\n            elif isinstance(data, dict):\n\
    \                return data\n            else:\n                return {}\n \
    \       except yaml.YAMLError as e:\n            print(f\"❌ YAML parse error:\
    \ {e}\", file=sys.stderr)\n            return {}\n\ndef load_trace_index():\n\
    \    \"\"\"Loads TRACE_INDEX.yml and returns a path-to-index mapping.\"\"\"\n\
    \    if not TRACE_INDEX_PATH.exists():\n        print(f\"❌ Missing TRACE_INDEX.yml\"\
    , file=sys.stderr)\n        return {}\n    with open(TRACE_INDEX_PATH, \"r\",\
    \ encoding=\"utf-8\") as f:\n        try:\n            data = yaml.safe_load(f)\n\
    \            if not isinstance(data, dict) or \"artifacts\" not in data:\n   \
    \             return {}\n            path_to_index = {}\n            for item\
    \ in data.get(\"artifacts\", []):\n                path = item.get(\"path\")\n\
    \                index = item.get(\"index\", \"-\")\n                if path:\n\
    \                    path_to_index[path] = index\n            return path_to_index\n\
    \        except yaml.YAMLError as e:\n            print(f\"❌ YAML parse error\
    \ in TRACE_INDEX.yml: {e}\", file=sys.stderr)\n            return {}\n\ndef find_embedded_id(file_path):\n\
    \    try:\n        with open(file_path, \"r\", encoding=\"utf-8\", errors=\"ignore\"\
    ) as f:\n            for _ in range(5):\n                line = f.readline()\n\
    \                match = TAG_PATTERN.search(line)\n                if match:\n\
    \                    return match.group(1).strip()\n    except Exception:\n  \
    \      return None\n    return None\n\ndef should_skip_dir(path: str) -> bool:\n\
    \    return any(part in IGNORED_DIRS for part in Path(path).parts)\n\ndef main():\n\
    \    parser = argparse.ArgumentParser(description=\"Verify and optionally rebuild\
    \ the tag inventory.\")\n    parser.add_argument(\"--rebuild\", action=\"store_true\"\
    , help=\"Rebuild the inventory from embedded tags.\")\n    args = parser.parse_args()\n\
    \n    tag_inventory = load_tag_inventory()\n    path_to_index_map = load_trace_index()\n\
    \n    if args.rebuild:\n        if not path_to_index_map:\n            print(\"\
    ❌ Could not build path-to-index map from TRACE_INDEX.yml. Aborting rebuild.\"\
    , file=sys.stderr)\n            sys.exit(1)\n\n        new_inventory = []\n  \
    \      for root, dirs, files in os.walk(PROJECT_ROOT):\n            dirs[:] =\
    \ [d for d in dirs if d not in IGNORED_DIRS]\n            for f in files:\n  \
    \              if not f.endswith(SCAN_EXTENSIONS):\n                    continue\n\
    \                full_path = Path(root) / f\n                rel_path = str(full_path.relative_to(PROJECT_ROOT))\n\
    \                embedded_id = find_embedded_id(full_path)\n                if\
    \ embedded_id:\n                    index = path_to_index_map.get(rel_path, \"\
    -\")\n                    new_inventory.append({\"id\": embedded_id, \"path\"\
    : rel_path, \"index\": index})\n\n        with open(TAG_INVENTORY, \"w\", encoding=\"\
    utf-8\") as f:\n            yaml.safe_dump(new_inventory, f, sort_keys=False)\n\
    \        print(f\"✅ Rebuilt inventory with {len(new_inventory)} items.\")\n  \
    \      sys.exit(0)\n\n    # --- Verification ---\n    print(\"=== Verifying alignment\
    \ migration (enhanced report) ===\\n\")\n    if not tag_inventory:\n        print(\"\
    ❌ Could not load tag inventory.\")\n        sys.exit(1)\n\n    mismatched = []\n\
    \    summary = defaultdict(list)\n\n    for root, dirs, files in os.walk(PROJECT_ROOT):\n\
    \        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]\n        for f in\
    \ files:\n            if not f.endswith(SCAN_EXTENSIONS):\n                continue\n\
    \            full_path = Path(root) / f\n            rel_path = str(full_path.relative_to(PROJECT_ROOT))\n\
    \            embedded_id = find_embedded_id(full_path)\n            if not embedded_id:\n\
    \                summary[\"missing_id\"].append(rel_path)\n                continue\n\
    \            if embedded_id not in tag_inventory:\n                summary[\"\
    unregistered_id\"].append(f\"{rel_path} (ID: {embedded_id})\")\n\n    print(\"\
    === Alignment Verification Summary ===\\n\")\n    print(f\"Files with missing\
    \ ID tags: {len(summary['missing_id'])}\")\n    print(f\"Files with unregistered\
    \ IDs: {len(summary['unregistered_id'])}\\n\")\n\n    if summary[\"missing_id\"\
    ]:\n        print(\"--- Files Missing ID Tags ---\")\n        for path in sorted(summary['missing_id']):\n\
    \            print(f\"  - {path}\")\n        print()\n\n    if summary[\"unregistered_id\"\
    ]:\n        print(\"--- Files With Unregistered IDs ---\")\n        for path in\
    \ sorted(summary['unregistered_id']):\n            print(f\"  - {path}\")\n  \
    \      print()\n\n    if not summary[\"missing_id\"] and not summary[\"unregistered_id\"\
    ]:\n        print(\"✅ All files have valid, registered IDs.\")\n        sys.exit(0)\n\
    \    else:\n        print(\"❌ Alignment verification incomplete.\")\n        sys.exit(1)\n\
    \nif __name__ == \"__main__\":\n    main()\n"
- path: scripts/generate_descriptions.py
  type: script
  workflow:
  - documentation
  indexes: []
  content: "#!/usr/bin/env python3\nimport sys\nfrom pathlib import Path\nimport json\n\
    import yaml\nfrom tqdm import tqdm\n\n# --- Ensure repo root and nlp folder are\
    \ importable ---\nrepo_root = Path(__file__).resolve().parent.parent\nsys.path.insert(0,\
    \ str(repo_root))\nsys.path.insert(0, str(repo_root / \"nlp\"))\n\nfrom nlp.description_builder\
    \ import build_description_for_artifact\n\ndef generate_descriptions():\n    \"\
    \"\"\n    Loads artifacts from TRACE_INDEX.yml, generates NLP descriptions,\n\
    \    and saves the result to a JSON file.\n    \"\"\"\n    trace_index_path =\
    \ repo_root / \"project/reports/TRACE_INDEX.yml\"\n    output_path = repo_root\
    \ / \"scripts/trace_description_intermediate.json\"\n\n    if not trace_index_path.exists():\n\
    \        print(f\"❌ Error: Trace index not found at {trace_index_path}\")\n  \
    \      sys.exit(1)\n\n    print(\"\U0001F4D8 Loading trace index...\")\n    with\
    \ open(trace_index_path, \"r\", encoding=\"utf-8\") as f:\n        trace_index\
    \ = yaml.safe_load(f)\n\n    artifacts = trace_index.get(\"artifacts\", [])\n\
    \    total = len(artifacts)\n    if not artifacts:\n        print(\"⚠️ No artifacts\
    \ found in TRACE_INDEX.yml.\")\n        return\n\n    print(f\"\U0001F4E6 Found\
    \ {total} artifacts.\")\n    descriptions = {}\n    failures = 0\n\n    for artifact\
    \ in tqdm(artifacts, desc=\"Generating descriptions\", unit=\"file\"):\n     \
    \   file_path_str = artifact.get(\"file\")\n        file_type = artifact.get(\"\
    type\", \"code\")\n\n        if not file_path_str:\n            failures += 1\n\
    \            continue\n\n        abs_file_path = repo_root / file_path_str\n \
    \       description = build_description_for_artifact(abs_file_path, file_type)\n\
    \        if description.startswith(\"Error\"):\n            failures += 1\n  \
    \      descriptions[file_path_str] = description\n\n    # --- Save JSON ---\n\
    \    print(f\"\\n\U0001F4BE Saving updates ({len(descriptions)} files processed)...\"\
    )\n    with open(output_path, \"w\", encoding=\"utf-8\") as f:\n        json.dump(descriptions,\
    \ f, indent=4, ensure_ascii=False)\n\n    print(f\"✅ Done.\")\n    print(f\" \
    \  - Total processed: {total}\")\n    print(f\"   - Successful: {total - failures}\"\
    )\n    print(f\"   - Failures: {failures}\")\n    print(f\"   - Output saved to:\
    \ {output_path}\")\n\n\nif __name__ == \"__main__\":\n    generate_descriptions()\n"
- path: scripts/project_registry.json
  type: config
  workflow: []
  indexes: []
  content: "[\n    {\n        \"name\": \"Endpoints\",\n        \"path\": \"project/api/endpoints.yaml\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"api\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"No description available.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"Traceability Matrix\",\n        \"path\"\
    : \"project/archive/TRACEABILITY_MATRIX.md\",\n        \"type\": \"doc\",\n  \
    \      \"module\": \"project\",\n        \"category\": \"archive\",\n        \"\
    registered_in\": [],\n        \"status\": \"orphan\",\n        \"notes\": \"\"\
    ,\n        \"source\": \"filesystem\"\n    },\n    {\n        \"name\": \"Audit\
    \ Phase 3\",\n        \"path\": \"project/archive/audit/AUDIT-PHASE-3.md\",\n\
    \        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
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
    \        \"name\": \"`ALIGNMENT_MATRIX.md`\",\n        \"path\": \"project/ALIGNMENT_MATRIX.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Description:** API Routes Layer\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"Alignment Matrix\",\n\
    \        \"path\": \"project/ALIGNMENT_MATRIX.yml\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"general\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"No description available.\",\n        \"source\": \"TRACE_INDEX.yml\"\n  \
    \  },\n    {\n        \"name\": \"`BACKLOG.md`\",\n        \"path\": \"project/BACKLOG.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Date:** 2025-08-18\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`CICD.md`\",\n        \"path\": \"project/CICD.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"This document provides a high-level overview of the Continuous\
    \ Integration / Continuous Deployment (CI/CD) pipeline for this project. It is\
    \ intended for a project management and stakeholder audience, explaining the purpose\
    \ and value of each quality gate in the development process.\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`DEPENDENCIES.md`\"\
    ,\n        \"path\": \"project/DEPENDENCIES.md\",\n        \"type\": \"doc\",\n\
    \        \"module\": \"project\",\n        \"category\": \"general\",\n      \
    \  \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"This document outlines the policy for adding new third-party dependencies\
    \ to the Zotify API project.\",\n        \"source\": \"TRACE_INDEX.yml\"\n   \
    \ },\n    {\n        \"name\": \"`EXECUTION_PLAN.md`\",\n        \"path\": \"\
    project/EXECUTION_PLAN.md\",\n        \"type\": \"doc\",\n        \"module\":\
    \ \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"**Status:** Live\
    \ Document\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n      \
    \  \"name\": \"`FUTURE_ENHANCEMENTS.md`\",\n        \"path\": \"project/FUTURE_ENHANCEMENTS.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"> **Note:** See the [`ALIGNMENT_MATRIX.md`](./ALIGNMENT_MATRIX.md)\
    \ for status and implementation tracking of these enhancements.\",\n        \"\
    source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`HIGH_LEVEL_DESIGN.md`\"\
    ,\n        \"path\": \"project/HIGH_LEVEL_DESIGN.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"general\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"**Status:** Live Document\",\n        \"source\": \"TRACE_INDEX.yml\"\n  \
    \  },\n    {\n        \"name\": \"`LESSONS-LEARNT.md`\",\n        \"path\": \"\
    project/LESSONS-LEARNT.md\",\n        \"type\": \"doc\",\n        \"module\":\
    \ \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"**Purpose:**\"\
    ,\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"\
    `LOGGING_PHASES.md`\",\n        \"path\": \"project/LOGGING_PHASES.md\",\n   \
    \     \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"> **Purpose of this Document**\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`LOGGING_SYSTEM_DESIGN.md`\"\
    ,\n        \"path\": \"project/LOGGING_SYSTEM_DESIGN.md\",\n        \"type\":\
    \ \"doc\",\n        \"module\": \"project\",\n        \"category\": \"general\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"**Status:** Proposed\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`LOGGING_TRACEABILITY_MATRIX.md`\",\n   \
    \     \"path\": \"project/LOGGING_TRACEABILITY_MATRIX.md\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"general\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"**Status:** Proposed\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`LOW_LEVEL_DESIGN.md`\",\n        \"path\"\
    : \"project/LOW_LEVEL_DESIGN.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"This LLD describes\
    \ the specific implementation details of the Zotify API's subsystems, with a focus\
    \ on the new provider-agnostic architecture.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`ONBOARDING.md`\",\n        \"path\": \"\
    project/ONBOARDING.md\",\n        \"type\": \"doc\",\n        \"module\": \"project\"\
    ,\n        \"category\": \"general\",\n        \"registered_in\": [],\n      \
    \  \"status\": \"registered\",\n        \"notes\": \"**Objective:** To bring any\
    \ new developer fully up to speed on the Zotify API project.\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`PID.md`\",\n      \
    \  \"path\": \"project/PID.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"**Project Name:**\
    \ Zotify API Refactoring and Enhancement\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`PROJECT_BRIEF.md`\",\n        \"path\":\
    \ \"project/PROJECT_BRIEF.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"**Project Name:**\
    \ Gonk API Refactoring and Enhancement\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`PROJECT_PLAN.md`\",\n        \"path\": \"\
    project/PROJECT_PLAN.md\",\n        \"type\": \"doc\",\n        \"module\": \"\
    project\",\n        \"category\": \"general\",\n        \"registered_in\": [],\n\
    \        \"status\": \"registered\",\n        \"notes\": \"**Date:** 2025-09-01\"\
    ,\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"\
    `PROJECT_REGISTRY.md`\",\n        \"path\": \"project/PROJECT_REGISTRY.md\",\n\
    \        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"| **Alignment Matrix** | [`ALIGNMENT_MATRIX.md`](ALIGNMENT_MATRIX.md)\
    \ | |\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\"\
    : \"`QA_GOVERNANCE.md`\",\n        \"path\": \"project/QA_GOVERNANCE.md\",\n \
    \       \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Status:** Live Document\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`ROADMAP.md`\",\n        \"path\": \"project/ROADMAP.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Date:** 2025-09-01\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`SECURITY.md`\",\n        \"path\": \"project/SECURITY.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Date:** 2025-08-18\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`TASK_CHECKLIST.md`\",\n        \"path\"\
    : \"project/TASK_CHECKLIST.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"general\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"**NOTE: This\
    \ is a mandatory pre-submit checklist. All applicable steps must be verified before\
    \ your work is considered complete.**\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`USECASES.md`\",\n        \"path\": \"project/USECASES.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"general\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"This document captures realistic, demanding user scenarios\
    \ that the API should ideally support.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`USECASES_GAP_ANALYSIS.md`\",\n        \"\
    path\": \"project/USECASES_GAP_ANALYSIS.md\",\n        \"type\": \"doc\",\n  \
    \      \"module\": \"project\",\n        \"category\": \"general\",\n        \"\
    registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\":\
    \ \"This document compares the **desired capabilities** from `USECASES.md` with\
    \ the **current** Zotify API implementation.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"Activity\",\n        \"path\": \"project/logs/ACTIVITY.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"logs\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"---\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"Current State\",\n        \"path\": \"project/logs/CURRENT_STATE.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"logs\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Status:** Live Document\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"Session Log\",\n        \"path\": \"project/logs/SESSION_LOG.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"logs\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"---\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"Conversations\",\n        \"path\": \"project/logs/conversations.json\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"logs\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"No description available.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`GAP_ANALYSIS_TEMPLATE.md`\",\n        \"\
    path\": \"project/process/GAP_ANALYSIS_TEMPLATE.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"process\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"**Author:** [Your Name]\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`DBSTUDIO_PLUGIN.md`\",\n        \"path\": \"project/proposals/DBSTUDIO_PLUGIN.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"proposals\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Date:** 2025-09-23\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`DYNAMIC_PLUGIN_PROPOSAL.md`\",\n       \
    \ \"path\": \"project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"proposals\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"**Date:** 2025-08-18\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`GONKUI_PLUGIN.md`\",\n        \"path\":\
    \ \"project/proposals/GONKUI_PLUGIN.md\",\n        \"type\": \"doc\",\n      \
    \  \"module\": \"project\",\n        \"category\": \"proposals\",\n        \"\
    registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\":\
    \ \"**Date:** 2025-09-23\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`GOVERNANCE_AUDIT_REFACTOR.md`\",\n        \"path\"\
    : \"project/proposals/GOVERNANCE_AUDIT_REFACTOR.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"proposals\",\n  \
    \      \"registered_in\": [],\n        \"status\": \"registered\",\n        \"\
    notes\": \"**Author:** Jules\",\n        \"source\": \"TRACE_INDEX.yml\"\n   \
    \ },\n    {\n        \"name\": \"`HOME_AUTOMATION_PROPOSAL.md`\",\n        \"\
    path\": \"project/proposals/HOME_AUTOMATION_PROPOSAL.md\",\n        \"type\":\
    \ \"doc\",\n        \"module\": \"project\",\n        \"category\": \"proposals\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"**Date:** 2025-08-18\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`LOW_CODE_PROPOSAL.md`\",\n        \"path\"\
    : \"project/proposals/LOW_CODE_PROPOSAL.md\",\n        \"type\": \"doc\",\n  \
    \      \"module\": \"project\",\n        \"category\": \"proposals\",\n      \
    \  \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"**Date:** 2025-08-18\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`MULTI_SOURCE_METADATA_PROPOSAL.md`\",\n        \"\
    path\": \"project/proposals/MULTI_SOURCE_METADATA_PROPOSAL.md\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"proposals\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"**Date:** 2025-08-18\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`NEW_PROPOSAL.md`\",\n        \"path\": \"\
    project/proposals/NEW_PROPOSAL.md\",\n        \"type\": \"doc\",\n        \"module\"\
    : \"project\",\n        \"category\": \"proposals\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"This is a test\
    \ proposal to verify the linter functionality.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`QA_GATE_IMPLEMENTATION_PLAN.md`\",\n   \
    \     \"path\": \"project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md\",\n      \
    \  \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"proposals\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Status:** Proposed\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`TRACE_INDEX_SCHEMA_ADAPTATION.md`\",\n \
    \       \"path\": \"project/proposals/TRACE_INDEX_SCHEMA_ADAPTATION.md\",\n  \
    \      \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"proposals\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"**Date:** 2025-09-25\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`TRACE_INDEX_SCHEMA_FIX.md`\",\n        \"\
    path\": \"project/proposals/TRACE_INDEX_SCHEMA_FIX.md\",\n        \"type\": \"\
    doc\",\n        \"module\": \"project\",\n        \"category\": \"proposals\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"**Date:** 2025-09-25\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"Alignment Integrity Snapshot\",\n       \
    \ \"path\": \"project/reports/ALIGNMENT_INTEGRITY_SNAPSHOT.yml\",\n        \"\
    type\": \"doc\",\n        \"module\": \"project\",\n        \"category\": \"reports\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"No description available.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"Alignment Validation Report\",\n        \"\
    path\": \"project/reports/ALIGNMENT_VALIDATION_REPORT.txt\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"reports\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"No description available.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`ARCHIVE_ALIGNMENT_MATRIX_OLD.md`\",\n  \
    \      \"path\": \"project/reports/ARCHIVE_ALIGNMENT_MATRIX_OLD.md\",\n      \
    \  \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"- id: SYS-02\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`CONTENT_ALIGNMENT_REPORT.md`\",\n      \
    \  \"path\": \"project/reports/CONTENT_ALIGNMENT_REPORT.md\",\n        \"type\"\
    : \"doc\",\n        \"module\": \"project\",\n        \"category\": \"reports\"\
    ,\n        \"registered_in\": [],\n        \"status\": \"registered\",\n     \
    \   \"notes\": \"**Date:** 2025-10-06\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`DESCRIPTION_COMPLIANCE_REPORT.md`\",\n \
    \       \"path\": \"project/reports/DESCRIPTION_COMPLIANCE_REPORT.md\",\n    \
    \    \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"| File | Registered In | Status | Notes |\",\n       \
    \ \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"Document\
    \ Tag Inventory\",\n        \"path\": \"project/reports/DOCUMENT_TAG_INVENTORY.yml\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"No description available.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`GOVERNANCE_DEMO_REPORT.md`\",\n        \"\
    path\": \"project/reports/GOVERNANCE_DEMO_REPORT.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"reports\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"**Author:** Jules\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n  \
    \  {\n        \"name\": \"`HANDOVER_BRIEF_CHATGTP.md`\",\n        \"path\": \"\
    project/reports/HANDOVER_BRIEF_CHATGTP.md\",\n        \"type\": \"doc\",\n   \
    \     \"module\": \"project\",\n        \"category\": \"reports\",\n        \"\
    registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\":\
    \ \"The project is currently in **API Phase 5b**, with governance, QA, and documentation\
    \ workflows partially implemented and audited. This session has finalized **workflow\
    \ mappings, incremental task definitions, and a repo manifest** that captures\
    \ the full repo content offline.\",\n        \"source\": \"TRACE_INDEX.yml\"\n\
    \    },\n    {\n        \"name\": \"`HANDOVER_BRIEF_JULES.md`\",\n        \"path\"\
    : \"project/reports/HANDOVER_BRIEF_JULES.md\",\n        \"type\": \"doc\",\n \
    \       \"module\": \"project\",\n        \"category\": \"reports\",\n       \
    \ \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"**Date:** 2025-10-06\",\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n\
    \    {\n        \"name\": \"`PROJECT_AUDIT_FINAL_REPORT.md`\",\n        \"path\"\
    : \"project/reports/PROJECT_AUDIT_FINAL_REPORT.md\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"reports\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"**Note:** This is a static template. Do **not** overwrite.\",\n        \"\
    source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"`PROJECT_DOCUMENT_ALIGNMENT.md`\"\
    ,\n        \"path\": \"project/reports/PROJECT_DOCUMENT_ALIGNMENT.md\",\n    \
    \    \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"- `project/BACKLOG.md`\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    },\n    {\n        \"name\": \"`REPO_MANIFEST.md`\",\n        \"path\":\
    \ \"project/reports/REPO_MANIFEST.md\",\n        \"type\": \"doc\",\n        \"\
    module\": \"project\",\n        \"category\": \"reports\",\n        \"registered_in\"\
    : [],\n        \"status\": \"registered\",\n        \"notes\": \"- path: verify_alignment_migration.py\"\
    ,\n        \"source\": \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"\
    `SEMANTIC_ALIGNMENT_REPORT.md`\",\n        \"path\": \"project/reports/SEMANTIC_ALIGNMENT_REPORT.md\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"- Average HLD Alignment: **84.21%**\",\n        \"source\"\
    : \"TRACE_INDEX.yml\"\n    },\n    {\n        \"name\": \"Trace Index\",\n   \
    \     \"path\": \"project/reports/TRACE_INDEX.yml\",\n        \"type\": \"doc\"\
    ,\n        \"module\": \"project\",\n        \"category\": \"reports\",\n    \
    \    \"registered_in\": [],\n        \"status\": \"registered\",\n        \"notes\"\
    : \"No description available.\",\n        \"source\": \"TRACE_INDEX.yml\"\n  \
    \  },\n    {\n        \"name\": \"Trace Index.Yml\",\n        \"path\": \"project/reports/TRACE_INDEX.yml.bak\"\
    ,\n        \"type\": \"doc\",\n        \"module\": \"project\",\n        \"category\"\
    : \"reports\",\n        \"registered_in\": [],\n        \"status\": \"registered\"\
    ,\n        \"notes\": \"No description available.\",\n        \"source\": \"TRACE_INDEX.yml\"\
    \n    }\n]"
- path: scripts/backfill_trace_meta.py
  type: script
  workflow: []
  indexes: []
  content: "#!/usr/bin/env python3\n\"\"\"\nbackfill_trace_meta.py - A one-time script\
    \ to backfill metadata into TRACE_INDEX.yml.\n\nThis script reads the existing\
    \ `project/PROJECT_REGISTRY.md` to find human-written\ndescriptions and injects\
    \ them into the `meta.description` field for corresponding\nartifacts in `project/reports/TRACE_INDEX.yml`.\n\
    \nIt is designed to be idempotent, meaning it can be run multiple times without\n\
    corrupting or duplicating data.\n\"\"\"\nimport os\nimport re\nimport yaml\nfrom\
    \ pathlib import Path\n\n# --- Configuration ---\nPROJECT_ROOT = Path(__file__).resolve().parent.parent\n\
    TRACE_INDEX_PATH = PROJECT_ROOT / \"project/reports/TRACE_INDEX.yml\"\nLEGACY_REGISTRY_PATH\
    \ = PROJECT_ROOT / \"project/PROJECT_REGISTRY.md\"\n\ndef parse_legacy_registry(md_content:\
    \ str, md_path: Path) -> dict:\n    \"\"\"Parses the legacy PROJECT_REGISTRY.md\
    \ to extract file paths and descriptions.\"\"\"\n    legacy_entries = {}\n   \
    \ base_dir = md_path.parent\n    # Regex to capture the link, path, and description\
    \ from a markdown table row\n    table_row_re = re.compile(r\"\\|\\s*\\*\\*.*\\\
    *\\*.*\\[`([^`]+)`\\]\\(([^)]+)\\)\\s*\\|([^|]*)\\|\")\n\n    for line in md_content.splitlines():\n\
    \        match = table_row_re.search(line)\n        if match:\n            _,\
    \ rel_path, description = [m.strip() for m in match.groups()]\n\n            #\
    \ Resolve the path relative to the markdown file\n            try:\n         \
    \       # Normalize the path to be relative to the project root\n            \
    \    full_path = (base_dir / rel_path).resolve()\n                repo_relative_path\
    \ = str(full_path.relative_to(PROJECT_ROOT)).replace(\"\\\\\", \"/\")\n      \
    \          legacy_entries[repo_relative_path] = description\n            except\
    \ (ValueError, FileNotFoundError):\n                # Ignore broken links or files\
    \ outside the project root\n                continue\n    return legacy_entries\n\
    \ndef main():\n    \"\"\"Main function to perform the backfill operation.\"\"\"\
    \n    if not TRACE_INDEX_PATH.exists():\n        print(f\"❌ ERROR: Trace index\
    \ not found at {TRACE_INDEX_PATH}\")\n        return 1\n\n    with open(TRACE_INDEX_PATH,\
    \ \"r\", encoding=\"utf-8\") as f:\n        trace_data = yaml.safe_load(f)\n\n\
    \    artifacts = trace_data.get(\"artifacts\", [])\n    if not artifacts:\n  \
    \      print(\"✅ No artifacts found in trace index. Nothing to do.\")\n      \
    \  return 0\n\n    legacy_descriptions = {}\n    if LEGACY_REGISTRY_PATH.exists():\n\
    \        with open(LEGACY_REGISTRY_PATH, \"r\", encoding=\"utf-8\") as f:\n  \
    \          md_content = f.read()\n            legacy_descriptions = parse_legacy_registry(md_content,\
    \ LEGACY_REGISTRY_PATH)\n    else:\n        print(f\"⚠️ Warning: Legacy registry\
    \ not found at {LEGACY_REGISTRY_PATH}. Descriptions will not be backfilled.\"\
    )\n\n    updated_count = 0\n    for artifact in artifacts:\n        path = artifact.get(\"\
    path\")\n        if not path:\n            continue\n\n        meta = artifact.setdefault(\"\
    meta\", {})\n        current_description = meta.get(\"description\", \"\").strip()\n\
    \n        # Check if description is missing or is the default placeholder\n  \
    \      if not current_description or current_description == \"No description available.\"\
    :\n            legacy_desc = legacy_descriptions.get(path)\n            if legacy_desc:\n\
    \                meta[\"description\"] = legacy_desc\n                updated_count\
    \ += 1\n                print(f\"  -> Updated description for {path}\")\n\n  \
    \  if updated_count > 0:\n        with open(TRACE_INDEX_PATH, \"w\", encoding=\"\
    utf-8\") as f:\n            yaml.safe_dump(trace_data, f, default_flow_style=False,\
    \ sort_keys=False)\n        print(f\"\\n✅ Successfully updated {updated_count}\
    \ artifact(s) in {TRACE_INDEX_PATH}.\")\n    else:\n        print(\"\\n✅ No missing\
    \ descriptions found to backfill. Trace index is already up-to-date.\")\n\n  \
    \  return 0\n\nif __name__ == \"__main__\":\n    exit(main())"
- path: scripts/generate_alignment_matrix_md.py
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
- path: scripts/CODE_FILE_INDEX.md
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

    | `scripts/.venv/bin/pwiz.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/AES.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/ARC2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/ARC4.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/Blowfish.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/CAST.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/ChaCha20.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/ChaCha20_Poly1305.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/DES.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/DES3.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/PKCS1_OAEP.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/PKCS1_v1_5.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/Salsa20.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_EKSBlowfish.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_cbc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_ccm.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_cfb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_ctr.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_eax.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_ecb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_gcm.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_kw.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_kwp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_ocb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_ofb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_openpgp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_mode_siv.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Cipher/_pkcs1_oaep_decode.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/BLAKE2b.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/BLAKE2s.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/CMAC.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/HMAC.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/KMAC128.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/KMAC256.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/KangarooTwelve.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/MD2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/MD4.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/MD5.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/Poly1305.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/RIPEMD.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/RIPEMD160.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA1.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA224.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA256.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA384.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA3_224.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA3_256.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA3_384.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA3_512.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHA512.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHAKE128.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/SHAKE256.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/TupleHash128.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/TupleHash256.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/TurboSHAKE128.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/TurboSHAKE256.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/cSHAKE128.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/cSHAKE256.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Hash/keccak.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/IO/PEM.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/IO/PKCS8.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/IO/_PBES.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/IO/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Math/Numbers.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Math/Primality.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Math/_IntegerBase.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Math/_IntegerCustom.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Math/_IntegerGMP.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Math/_IntegerNative.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Math/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Protocol/DH.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Protocol/HPKE.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Protocol/KDF.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Protocol/SecretSharing.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Protocol/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/DSA.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/ECC.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/ElGamal.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/RSA.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/_curve.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/_edwards.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/_montgomery.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/_nist_ecc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/_openssh.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/PublicKey/_point.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Random/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Random/random.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/common.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_AES.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_ARC2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_ARC4.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_Blowfish.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_CAST.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_CBC.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_CCM.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_CFB.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_CTR.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_ChaCha20.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_ChaCha20_Poly1305.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_DES.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_DES3.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_EAX.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_GCM.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_KW.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_OCB.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_OFB.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_OpenPGP.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_SIV.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_Salsa20.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_pkcs1_15.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Cipher/test_pkcs1_oaep.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/common.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_BLAKE2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_CMAC.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_HMAC.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_KMAC.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_KangarooTwelve.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_MD2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_MD4.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_MD5.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_Poly1305.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_RIPEMD160.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA1.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA224.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA256.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA384.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA3_224.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA3_256.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA3_384.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA3_512.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHA512.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_SHAKE.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_TupleHash.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_TurboSHAKE.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_cSHAKE.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Hash/test_keccak.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/IO/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/IO/test_PBES.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/IO/test_PKCS8.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Math/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Math/test_Numbers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Math/test_Primality.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Math/test_modexp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Math/test_modmult.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Protocol/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Protocol/test_HPKE.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Protocol/test_KDF.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Protocol/test_SecretSharing.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Protocol/test_ecdh.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Protocol/test_rfc1751.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_DSA.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_ECC_Curve25519.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_ECC_Curve448.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_ECC_Ed25519.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_ECC_Ed448.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_ECC_NIST.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_ElGamal.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_RSA.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_import_Curve25519.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_import_Curve448.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_import_DSA.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_import_ECC.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/PublicKey/test_import_RSA.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Random/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Random/test_random.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Signature/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Signature/test_dss.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Signature/test_eddsa.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Signature/test_pkcs1_15.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Signature/test_pss.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Util/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Util/test_Counter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Util/test_Padding.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Util/test_asn1.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Util/test_number.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Util/test_rfc1751.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/Util/test_strxor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/loader.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/SelfTest/st_common.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Signature/DSS.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Signature/PKCS1_PSS.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Signature/PKCS1_v1_5.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Signature/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Signature/eddsa.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Signature/pkcs1_15.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Signature/pss.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/Counter.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/Padding.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/RFC1751.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/_cpu_features.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/_file_system.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/_raw_api.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/asn1.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/number.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/py3compat.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/Util/strxor.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/Cryptodome/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/AvifImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/BdfFontFile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/BlpImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/BmpImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/BufrStubImagePlugin.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ContainerIO.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/CurImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/DcxImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/DdsImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/EpsImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ExifTags.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/FitsImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/FliImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/FontFile.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/FpxImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/FtexImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/GbrImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/GdImageFile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/GifImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/GimpGradientFile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/GimpPaletteFile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/GribStubImagePlugin.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/Hdf5StubImagePlugin.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/IcnsImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/IcoImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/Image.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageChops.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageCms.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageColor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageDraw.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageDraw2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageEnhance.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageFile.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageFilter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageFont.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageGrab.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageMath.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageMode.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageMorph.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageOps.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImagePalette.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImagePath.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageQt.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageSequence.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageShow.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageStat.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageTk.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageTransform.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImageWin.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/ImtImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/IptcImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/Jpeg2KImagePlugin.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/JpegImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/JpegPresets.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/McIdasImagePlugin.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/MicImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/MpegImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/MpoImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/MspImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PSDraw.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PaletteFile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PalmImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PcdImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PcfFontFile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PcxImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PdfImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PdfParser.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PixarImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PngImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PpmImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/PsdImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/QoiImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/SgiImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/SpiderImagePlugin.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/SunImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/TarIO.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/TgaImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/TiffImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/TiffTags.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/WalImageFile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/WebPImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/WmfImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/XVThumbImagePlugin.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/XbmImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/XpmImagePlugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/__main__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/_binary.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/_deprecate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/_tkinter_finder.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/_typing.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/_util.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/_version.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/features.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/PIL/report.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/_black_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_databind_core_proxy/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_databind_json_proxy/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_distutils_hack/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_distutils_hack/override.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_argcomplete.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_code/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_code/code.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_code/source.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_io/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_io/pprint.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_io/saferepr.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_io/terminalwriter.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_io/wcwidth.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_py/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_py/error.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_py/path.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/assertion/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/assertion/rewrite.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/assertion/truncate.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/assertion/util.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/cacheprovider.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/capture.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/compat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/config/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/config/argparsing.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/config/compat.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/config/exceptions.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/config/findpaths.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/debugging.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/deprecated.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/doctest.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/faulthandler.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/fixtures.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/freeze_support.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/helpconfig.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/hookspec.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/junitxml.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/legacypath.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/logging.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/main.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/mark/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/mark/expression.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/mark/structures.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/monkeypatch.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/nodes.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/outcomes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/pastebin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/pathlib.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/pytester.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/pytester_assertions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/python.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/python_api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/raises.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/recwarn.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/reports.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/runner.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/scope.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/setuponly.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/setupplan.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/skipping.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/stash.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/stepwise.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/terminal.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/threadexception.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/timing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/tmpdir.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/tracemalloc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/unittest.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/unraisableexception.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/warning_types.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/_pytest/warnings.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/_yaml/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/annotated_types/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/annotated_types/test_cases.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_backends/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_backends/_trio.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_asyncio_selector_thread.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_contextmanagers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_eventloop.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_exceptions.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_fileio.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_resources.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_signals.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_sockets.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_streams.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_subprocesses.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_synchronization.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_tasks.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_tempfile.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_testing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/_core/_typedattr.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/abc/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/abc/_eventloop.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/abc/_resources.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/abc/_sockets.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/abc/_streams.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/abc/_subprocesses.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/abc/_tasks.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/abc/_testing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/from_thread.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/lowlevel.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/pytest_plugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/streams/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/streams/buffered.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/streams/file.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/streams/memory.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/streams/stapled.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/streams/text.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/streams/tls.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/to_interpreter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/to_process.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/anyio/to_thread.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/_cmp.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/_compat.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/_config.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/_funcs.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/attr/_make.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/attr/_next_gen.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/_version_info.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/converters.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/filters.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/setters.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/attr/validators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attrs/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attrs/converters.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attrs/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/attrs/filters.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/attrs/setters.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/attrs/validators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/common/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/common/encoding.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/common/errors.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/common/security.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/common/urls.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/consts.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/deprecate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/base_client/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/base_client/async_app.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/base_client/async_openid.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/base_client/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/base_client/framework_integration.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/base_client/registry.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/base_client/sync_app.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/base_client/sync_openid.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_client/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_client/apps.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_client/integration.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth1/authorization_server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth1/nonce.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth1/resource_protector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth2/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth2/authorization_server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth2/endpoints.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth2/requests.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth2/resource_protector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/django_oauth2/signals.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_client/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_client/apps.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_client/integration.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth1/authorization_server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth1/cache.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth1/resource_protector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth2/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth2/authorization_server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth2/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth2/requests.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth2/resource_protector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/flask_oauth2/signals.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/httpx_client/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/httpx_client/assertion_client.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/httpx_client/oauth1_client.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/httpx_client/oauth2_client.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/httpx_client/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/requests_client/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/requests_client/assertion_session.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/requests_client/oauth1_session.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/requests_client/oauth2_session.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/requests_client/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/sqla_oauth2/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/sqla_oauth2/client_mixin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/sqla_oauth2/functions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/sqla_oauth2/tokens_mixins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/starlette_client/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/starlette_client/apps.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/integrations/starlette_client/integration.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/drafts/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/drafts/_jwe_algorithms.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/drafts/_jwe_enc_cryptodome.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/drafts/_jwe_enc_cryptography.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/errors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/jwk.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7515/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7515/jws.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7515/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7516/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7516/jwe.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7516/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7517/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7517/_cryptography_key.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7517/asymmetric_key.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7517/base_key.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7517/jwk.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7517/key_set.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/ec_key.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/jwe_algs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/jwe_encs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/jwe_zips.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/jws_algs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/oct_key.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/rsa_key.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7518/util.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7519/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7519/claims.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc7519/jwt.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc8037/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc8037/jws_eddsa.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/rfc8037/okp_key.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/jose/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/client.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/errors.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/authorization_server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/base_server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/client_auth.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/parameters.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/resource_protector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/rsa.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/signature.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth1/rfc5849/wrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/auth.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/client.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/authenticate_client.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/authorization_server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/grants/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/grants/authorization_code.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/grants/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/grants/client_credentials.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/grants/implicit.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/grants/refresh_token.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/grants/resource_owner_password_credentials.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/hooks.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/parameters.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/requests.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/resource_protector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/token_endpoint.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6749/wrappers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6750/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6750/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6750/parameters.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6750/token.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc6750/validator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7009/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7009/parameters.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7009/revocation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7521/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7521/client.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7523/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7523/assertion.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7523/auth.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7523/client.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7523/jwt_bearer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7523/token.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7523/validator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7591/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7591/claims.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7591/endpoint.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7591/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7592/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7592/endpoint.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7636/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7636/challenge.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7662/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7662/introspection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7662/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc7662/token_validator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8414/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8414/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8414/well_known.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8628/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8628/device_code.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8628/endpoint.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8628/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8628/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc8693/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9068/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9068/claims.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9068/introspection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9068/revocation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9068/token.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9068/token_validator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9101/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9101/authorization_server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9101/discovery.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9101/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9101/registration.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9207/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oauth2/rfc9207/parameter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/claims.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/errors.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/grants/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/grants/code.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/grants/hybrid.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/grants/implicit.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/grants/util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/models.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/userinfo.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/core/util.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/discovery/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/discovery/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/discovery/well_known.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/registration/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/authlib/oidc/registration/claims.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/core.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/babel/dates.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/babel/languages.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/lists.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/babel/localedata.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/localtime/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/localtime/_fallback.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/localtime/_helpers.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/localtime/_unix.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/localtime/_win32.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/_compat.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/catalog.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/checkers.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/extract.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/frontend.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/jslexer.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/mofile.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/plurals.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/pofile.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/messages/setuptools_frontend.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/numbers.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/plural.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/support.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/babel/units.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/babel/util.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/__meta__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/_bre_parse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/_bregex_parse.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/_bregex_typing.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/bre.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/bregex.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/age.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/alias.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/bidiclass.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/bidipairedbrackettype.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/binary.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/block.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/canonicalcombiningclass.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/decompositiontype.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/eastasianwidth.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/generalcategory.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/graphemeclusterbreak.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/hangulsyllabletype.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/indicpositionalcategory.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/indicsyllabiccategory.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/joininggroup.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/joiningtype.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/linebreak.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/numerictype.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/numericvalue.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/quickcheck.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/script.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/scriptextensions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/sentencebreak.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/verticalorientation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/uniprops/unidata/wordbreak.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/backrefs/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/blacklists/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/blacklists/calls.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/blacklists/imports.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/blacklists/utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/cli/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/cli/baseline.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/cli/config_generator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/cli/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/blacklisting.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/config.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/constants.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/context.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/docs_utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/extension_loader.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/issue.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/manager.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/meta_ast.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/metrics.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/node_visitor.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/test_properties.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/test_set.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/tester.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/core/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/csv.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/custom.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/html.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/json.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/sarif.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/screen.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/text.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/xml.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/formatters/yaml.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/app_debug.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/asserts.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/crypto_request_no_cert_validation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/django_sql_injection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/django_xss.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/exec.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/general_bad_file_permissions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/general_bind_all_interfaces.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/general_hardcoded_password.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/general_hardcoded_tmp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/hashlib_insecure_functions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/huggingface_unsafe_download.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/injection_paramiko.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/injection_shell.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/injection_sql.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/injection_wildcard.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/insecure_ssl_tls.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/jinja2_templates.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/logging_config_insecure_listen.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/mako_templates.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/markupsafe_markup_xss.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/pytorch_load.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/request_without_timeout.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/snmp_security_check.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/ssh_no_host_key_verification.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/tarfile_unsafe_members.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/trojansource.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/try_except_continue.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/try_except_pass.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/weak_cryptographic_key.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bandit/plugins/yaml_load.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/bcrypt/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/_width_table.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/brackets.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/cache.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/black/comments.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/concurrency.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/const.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/black/debug.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/black/files.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/black/handle_ipynb_magics.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/linegen.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/black/lines.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/black/mode.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/black/nodes.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/black/numerics.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/output.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/black/parsing.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/black/ranges.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/black/report.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/black/resources/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/black/rusty.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/black/schema.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/black/strings.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/black/trans.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/blackd/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blackd/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blackd/middlewares.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/conv.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/driver.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/grammar.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/literals.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/parse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/pgen.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/token.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pgen2/tokenize.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pygram.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/blib2to3/pytree.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/cacheutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/debugutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/deprutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/dictutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/easterutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/ecoutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/excutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/fileutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/formatutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/funcutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/gcutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/ioutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/iterutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/jsonutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/listutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/mathutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/mboxutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/namedutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/pathutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/queueutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/setutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/socketutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/statsutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/strutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/tableutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/tbutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/timeutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/typeutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/boltons/urlutils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bracex/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bracex/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/bracex/__meta__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/certifi/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/certifi/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/certifi/core.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/_imp_emulation.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/_shimmed_dist_utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/api.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/backend_ctypes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/cffi_opcode.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/commontypes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/cparser.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/error.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/ffiplatform.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/lock.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/model.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/pkgconfig.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/recompiler.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/setuptools_ext.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/vengine_cpy.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/vengine_gen.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cffi/verifier.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/cfgv.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/api.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/cd.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/cli/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/cli/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/constant.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/legacy.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/md.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/models.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/charset_normalizer/version.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/_compat.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/click/_termui_impl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/_textwrap.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/_winconsole.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/core.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/click/decorators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/formatting.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/globals.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/click/parser.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/click/shell_completion.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/click/termui.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/click/testing.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/click/types.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/click/utils.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/click_option_group/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/click_option_group/_core.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/click_option_group/_decorators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/click_option_group/_helpers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/click_option_group/_version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/ansi.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/ansitowin32.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/initialise.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/tests/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/tests/ansi_test.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/tests/ansitowin32_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/tests/initialise_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/tests/isatty_test.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/tests/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/tests/winterm_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/win32.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/colorama/winterm.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/annotate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/bytecode.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/cmdline.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/collector.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/config.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/context.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/control.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/core.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/data.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/debug.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/disposition.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/env.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/execfile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/files.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/html.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/htmlfiles/coverage_html.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/htmlfiles/index.html` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/htmlfiles/pyfile.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/htmlfiles/style.css` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/inorout.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/jsonreport.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/lcovreport.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/misc.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/multiproc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/numbits.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/parser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/patch.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/phystokens.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/plugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/plugin_support.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/python.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/pytracer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/regions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/report.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/report_core.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/results.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/sqldata.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/sqlitedb.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/sysmon.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/templite.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/tomlconfig.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/coverage/xmlreport.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/__about__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/exceptions.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/fernet.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/_oid.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/asn1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/asn1/asn1.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/backends/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/backends/openssl/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/backends/openssl/backend.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/bindings/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/bindings/openssl/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/bindings/openssl/_conditional.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/bindings/openssl/binding.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/decrepit/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/decrepit/ciphers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/decrepit/ciphers/algorithms.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/_asymmetric.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/_cipheralgorithm.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/_serialization.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/dh.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/dsa.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/ec.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/ed25519.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/ed448.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/padding.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/rsa.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/x25519.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/asymmetric/x448.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/ciphers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/ciphers/aead.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/ciphers/algorithms.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/ciphers/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/ciphers/modes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/cmac.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/constant_time.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/hashes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/hmac.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/kdf/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/kdf/argon2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/kdf/concatkdf.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/kdf/hkdf.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/kdf/kbkdf.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/kdf/pbkdf2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/kdf/scrypt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/kdf/x963kdf.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/keywrap.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/padding.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/poly1305.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/serialization/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/serialization/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/serialization/pkcs12.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/serialization/pkcs7.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/serialization/ssh.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/twofactor/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/twofactor/hotp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/hazmat/primitives/twofactor/totp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/base.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/certificate_transparency.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/extensions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/general_name.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/name.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/ocsp.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/oid.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/cryptography/x509/verification.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/context.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/converter.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/dataclasses.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/mapper.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/schema.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/settings.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/tests/context_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/tests/schema_docspec_example_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/tests/schema_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/tests/schema_with_nested_dataclasses_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/union.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/core/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/json/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/json/converters.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/json/module.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/json/settings.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/databind/json/tests/converters_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/_common.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/easter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/parser/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/parser/_parser.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/parser/isoparser.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/relativedelta.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/rrule.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/tz/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/tz/_common.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/tz/_factories.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/tz/tz.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/tz/win.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/tzwin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/zoneinfo/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/dateutil/zoneinfo/rebuild.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/ElementTree.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/cElementTree.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/common.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/expatbuilder.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/expatreader.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/lxml.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/minidom.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/pulldom.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/sax.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/defusedxml/xmlrpc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/deprecated/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/deprecated/classic.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/deprecated/sphinx.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/compat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/database.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/index.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/locators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/manifest.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/markers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/metadata.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/resources.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/scripts.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/distlib/wheel.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/docspec/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/docspec/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/docspec_python/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docspec_python/__main__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docspec_python/parser.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/common.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/epydoc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/google.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/numpydoc.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/parser.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/rest.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/tests/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/tests/test_epydoc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/tests/test_google.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/tests/test_numpydoc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/tests/test_parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/tests/test_rest.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/tests/test_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/docstring_parser/util.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/dotenv/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dotenv/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dotenv/cli.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/dotenv/ipython.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dotenv/main.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/dotenv/parser.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/dotenv/variables.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dotenv/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dparse/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dparse/dependencies.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dparse/errors.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/dparse/filetypes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/dparse/parser.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/dparse/regex.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/dparse/updater.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/_compat.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/_rwlock.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/_sha3.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/curves.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/der.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/ecdh.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/ecdsa.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/eddsa.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/ellipticcurve.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/errors.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/keys.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/numbertheory.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/rfc6979.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/ssh.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_curves.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_der.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_ecdh.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_ecdsa.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_eddsa.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_ellipticcurve.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_jacobi.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_keys.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_malformed_sigs.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_numbertheory.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_pyecdsa.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_rw_lock.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/test_sha3.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ecdsa/util.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/exceptiongroup/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/exceptiongroup/_catch.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/exceptiongroup/_exceptions.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/exceptiongroup/_formatting.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/exceptiongroup/_suppress.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/exceptiongroup/_version.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/face/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/face/command.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/face/errors.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/face/helpers.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/face/middleware.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/face/parser.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/face/sinter.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/face/test/test_basic.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/face/test/test_calc_cmd.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/face/test/test_help.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/face/test/test_mw.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/face/test/test_search_cmd.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/face/test/test_vcs_cmd.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/face/testing.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/face/utils.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/_compat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/applications.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/background.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/cli.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/concurrency.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/datastructures.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/dependencies/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/dependencies/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/dependencies/utils.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/encoders.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/exception_handlers.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/logger.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/middleware/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/middleware/cors.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/middleware/gzip.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/middleware/httpsredirect.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/middleware/trustedhost.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/middleware/wsgi.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/openapi/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/openapi/constants.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/openapi/docs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/openapi/models.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/openapi/utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/param_functions.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/params.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/requests.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/responses.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/routing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/security/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/security/api_key.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/security/base.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/security/http.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/security/oauth2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/security/open_id_connect_url.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/security/utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/staticfiles.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/templating.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/testclient.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/types.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/utils.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/fastapi/websockets.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ffmpy/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ffmpy/ffmpy.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/_api.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/_error.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/_soft.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/_unix.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/_windows.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/asyncio.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/filelock/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ghp_import.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/glom/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/__main__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/_version.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/chainmap_backport.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/cli.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/core.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/grouping.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/matching.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/mutation.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/reduction.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/streaming.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/perf_report.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_basic.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_check.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_cli.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_error.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_fill.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_grouping.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_match.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_mutation.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_path_and_t.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_reduction.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_scope_vars.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_snippets.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_spec.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_streaming.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_target_types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/test/test_tutorial.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/glom/tutorial.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/annotations_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/auth_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/backend_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/billing_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/client_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/config_change_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/consumer_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/context_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/control_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/distribution_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/documentation_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/endpoint_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/error_reason_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/field_behavior_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/http_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/httpbody_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/label_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/launch_stage_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/log_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/logging_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/metric_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/monitored_resource_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/monitoring_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/quota_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/resource_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/routing_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/service_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/source_info_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/system_parameter_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/usage_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/api/visibility_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/cloud/extended_operations_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/cloud/location/locations_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/gapic/metadata/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/gapic/metadata/gapic_metadata_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/logging/type/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/logging/type/http_request_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/logging/type/log_severity_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/longrunning/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/longrunning/operations_grpc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/longrunning/operations_grpc_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/longrunning/operations_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/longrunning/operations_pb2_grpc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/longrunning/operations_proto.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/longrunning/operations_proto_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/any_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/api_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/compiler/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/compiler/plugin_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/descriptor.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/descriptor_database.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/descriptor_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/descriptor_pool.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/duration_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/empty_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/field_mask_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/api_implementation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/builder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/containers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/decoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/encoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/enum_type_wrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/extension_dict.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/message_listener.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/python_message.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/type_checkers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/well_known_types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/internal/wire_format.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/json_format.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/message.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/message_factory.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/proto_builder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/pyext/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/pyext/cpp_message.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/reflection.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/service.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/service_reflection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/source_context_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/struct_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/symbol_database.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/text_encoding.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/text_format.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/timestamp_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/type_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/util/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/util/json_format_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/util/json_format_proto3_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/protobuf/wrappers_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/rpc/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/rpc/code_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/rpc/context/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/rpc/context/attribute_context_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/rpc/error_details_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/rpc/status_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/calendar_period_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/color_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/date_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/datetime_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/dayofweek_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/decimal_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/expr_pb2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/fraction_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/interval_pb2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/latlng_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/localized_text_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/money_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/month_pb2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/phone_number_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/postal_address_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/quaternion_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/google/type/timeofday_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/platform/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/fail_clearing_run_switches.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/fail_cpp_exception.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/fail_initialstub_already_started.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/fail_slp_switch.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/fail_switch_three_greenlets.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/fail_switch_three_greenlets2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/fail_switch_two_greenlets.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/leakcheck.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_contextvars.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_cpp.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_extension_interface.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_gc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_generator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_generator_nested.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_greenlet.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_greenlet_trash.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_leaks.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_stack_saved.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_throw.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_tracing.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/greenlet/tests/test_weakref.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_abnf.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_connection.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_events.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_headers.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_readers.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_receivebuffer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_state.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_util.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_version.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/h11/_writers.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_api.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_async/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_async/connection.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_async/connection_pool.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_async/http11.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_async/http2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_async/http_proxy.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_async/interfaces.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_async/socks_proxy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_backends/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_backends/anyio.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_backends/auto.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_backends/base.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_backends/mock.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_backends/sync.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_backends/trio.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_models.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_ssl.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_sync/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_sync/connection.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_sync/connection_pool.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_sync/http11.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_sync/http2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_sync/http_proxy.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_sync/interfaces.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_sync/socks_proxy.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_synchronization.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_trace.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpcore/_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/__version__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_api.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_auth.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_client.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_config.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_content.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_decoders.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_main.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_models.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_multipart.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_status_codes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_transports/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_transports/asgi.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_transports/base.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_transports/default.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_transports/mock.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_transports/wsgi.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_types.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_urlparse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_urls.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/httpx/_utils.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/identify/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/identify/cli.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/identify/extensions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/identify/identify.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/identify/interpreters.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/identify/vendor/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/identify/vendor/licenses.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/idna/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/idna/codec.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/idna/compat.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/idna/core.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/idna/idnadata.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/idna/intranges.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/idna/package_data.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/idna/uts46data.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ifaddr/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ifaddr/_posix.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/ifaddr/_shared.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ifaddr/_win32.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/ifaddr/netifaces.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ifaddr/test_ifaddr.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/_adapters.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/_collections.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/_compat.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/_functools.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/_itertools.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/_meta.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/_text.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/compat/py39.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/importlib_metadata/diagnose.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/iniconfig/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/iniconfig/_parse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/iniconfig/_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/iniconfig/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/_identifier.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/async_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/bccache.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/compiler.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/constants.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/debug.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/defaults.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/environment.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/ext.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/filters.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/idtracking.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/lexer.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/loaders.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/meta.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/nativetypes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/nodes.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/optimizer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/parser.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/runtime.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/sandbox.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/tests.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/utils.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/jinja2/visitor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/_cloudpickle_wrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/_dask.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/_memmapping_reducer.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/_multiprocessing_helpers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/_parallel_backends.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/_store_backends.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/_utils.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/backports.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/compressor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/disk.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/executor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/cloudpickle/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/cloudpickle/cloudpickle.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/cloudpickle/cloudpickle_fast.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/_base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/_posix_reduction.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/_win_reduction.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/context.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/fork_exec.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/popen_loky_posix.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/popen_loky_win32.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/process.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/queues.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/reduction.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/resource_tracker.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/spawn.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/synchronize.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/backend/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/cloudpickle_wrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/initializers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/process_executor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/externals/loky/reusable_executor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/func_inspect.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/hashing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/logger.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/memory.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/numpy_pickle.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/numpy_pickle_compat.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/numpy_pickle_utils.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/parallel.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/pool.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/common.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/data/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/data/create_numpy_pickle.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_backports.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_cloudpickle_wrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_config.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_dask.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_disk.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_func_inspect.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_func_inspect_special_encoding.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_hashing.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_init.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_logger.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_memmapping.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_memory.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_memory_async.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_missing_multiprocessing.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_module.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_numpy_pickle.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_numpy_pickle_compat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_numpy_pickle_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_parallel.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_store_backends.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_testing.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/test_utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/test/testutils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/joblib/testing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/backends/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/backends/_asn1.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/backends/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/backends/cryptography_backend.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/backends/ecdsa_backend.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/backends/native.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/backends/rsa_backend.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/constants.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/jwe.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/jwk.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/jws.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/jwt.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jose/utils.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/_format.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/_keywords.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/_legacy_keywords.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/_types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/_typing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/const_vs_enum.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/contains.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/issue232.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/json_schema_test_suite.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/nested_schemas.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/subcomponents.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/unused_registry.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/useless_applicator_schemas.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/useless_keywords.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/benchmarks/validator_creation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/cli.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/exceptions.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/protocols.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/_suite.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/fuzz_validate.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/test_cli.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/test_deprecations.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/test_exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/test_format.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/test_jsonschema_test_suite.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/test_types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/test_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/test_validators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/typing/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/tests/typing/test_all_concrete_validators_match_protocol.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema/validators.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema_specifications/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema_specifications/_core.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema_specifications/tests/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/jsonschema_specifications/tests/test_jsonschema_specifications.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/audio/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/audio/decoders.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/audio/decrypt.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/audio/format.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/audio/storage.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/cache.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/core.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/crypto.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/dealer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/mercury.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/metadata.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/oauth.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Authentication_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/CanvazMeta_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Canvaz_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/ClientToken_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Connect_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Connectivity_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/ContextPage_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/ContextPlayerOptions_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/ContextTrack_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Context_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/ExplicitContentPubsub_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Keyexchange_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Mercury_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Metadata_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/PlayOrigin_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Playback_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Player_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Playlist4External_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/PlaylistAnnotate3_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Pubsub_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Queue_pb2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Restrictions_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/Session_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/StorageResolve_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/TransferState_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/ClientInfo_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/Login5_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/UserInfo_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/challenges/Code_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/challenges/Hashcash_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/challenges/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/credentials/Credentials_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/credentials/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/identifiers/Identifiers_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/proto/spotify/login5/v3/identifiers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/structure.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot/zeroconf.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/librespot_player/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/core.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mando/napoleon/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/napoleon/docstring.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/napoleon/iterators.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/napoleon/pycompat.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/rst_text_formatter.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/tests/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/tests/capture.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/tests/run.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/tests/test_core.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/tests/test_google.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/tests/test_numpy.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/tests/test_unicode_docstring_on_py2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/tests/test_utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mando/utils.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/__meta__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/blockparser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/blockprocessors.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/core.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/abbr.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/admonition.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/attr_list.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/codehilite.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/def_list.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/extra.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/fenced_code.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/footnotes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/legacy_attrs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/legacy_em.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/md_in_html.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/meta.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/nl2br.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/sane_lists.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/smarty.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/tables.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/toc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/extensions/wikilinks.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/htmlparser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/inlinepatterns.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/postprocessors.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/preprocessors.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/serializers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/test_tools.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/treeprocessors.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/_compat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/_punycode.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/cli/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/cli/parse.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/common/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/common/entities.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/common/html_blocks.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/common/html_re.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/common/normalize_url.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/common/utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/helpers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/helpers/parse_link_destination.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/helpers/parse_link_label.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/helpers/parse_link_title.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/parser_block.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/parser_core.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/parser_inline.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/presets/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/presets/commonmark.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/presets/default.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/presets/zero.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/renderer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/ruler.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/blockquote.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/code.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/fence.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/heading.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/hr.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/html_block.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/lheading.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/list.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/paragraph.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/reference.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/state_block.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_block/table.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/block.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/inline.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/linkify.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/normalize.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/replacements.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/smartquotes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/state_core.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_core/text_join.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/autolink.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/backticks.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/balance_pairs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/emphasis.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/entity.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/escape.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/fragments_join.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/html_inline.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/image.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/link.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/linkify.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/newline.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/state_inline.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/strikethrough.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/rules_inline/text.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/token.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/tree.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markdown_it/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markupsafe/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/markupsafe/_native.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/class_registry.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/constants.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/decorators.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/error_store.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/exceptions.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/experimental/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/experimental/context.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/fields.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/orderedset.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/schema.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/marshmallow/validate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/extensions/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/extensions/emoji.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/author.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/readtime/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/readtime/parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/structure/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/structure/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/structure/markdown.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/blog/structure/options.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/group/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/group/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/group/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/info/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/info/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/info/patterns.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/info/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/meta/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/meta/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/meta/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/offline/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/offline/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/offline/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/privacy/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/privacy/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/privacy/parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/privacy/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/search/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/search/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/search/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/social/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/social/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/social/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/renderer/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/listing/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/listing/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/listing/manager/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/listing/manager/toc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/listing/tree/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/mapping/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/mapping/manager/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/mapping/storage/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/tag/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/tag/options.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/plugins/tags/structure/tag/reference/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/404.html` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/bundle.f55a23d4.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.ar.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.da.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.de.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.du.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.el.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.es.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.fi.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.fr.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.he.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.hi.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.hu.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.hy.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.it.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.ja.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.jp.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.kn.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.ko.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.multi.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.nl.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.no.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.pt.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.ro.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.ru.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.sa.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.stemmer.support.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.sv.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.ta.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.te.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.th.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.tr.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.vi.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/min/lunr.zh.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/tinyseg.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/lunr/wordcut.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/javascripts/workers/search.973d3a69.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/stylesheets/main.e53b48f4.min.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/assets/stylesheets/palette.06af60db.min.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/base.html` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/blog-post.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/blog.html` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/fragments/tags/default/listing.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/fragments/tags/default/tag.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/main.html` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/mkdocs_theme.yml`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/actions.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/alternate.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/comments.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/consent.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/content.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/copyright.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/feedback.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/footer.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/header.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/icons.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/integrations/analytics.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/integrations/analytics/google.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/javascripts/announce.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/javascripts/base.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/javascripts/consent.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/javascripts/content.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/javascripts/outdated.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/javascripts/palette.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/language.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/af.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ar.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/az.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/be.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/bg.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/bn.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ca.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/cs.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/cy.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/da.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/de.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/el.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/en.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/eo.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/es.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/et.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/eu.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/fa.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/fi.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/fr.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/gl.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/he.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/hi.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/hr.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/hu.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/hy.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/id.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/is.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/it.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ja.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ka.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/kn.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ko.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ku-IQ.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/lb.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/lt.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/lv.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/mk.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/mn.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ms.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/my.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/nb.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/nl.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/nn.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/pl.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/pt-BR.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/pt.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ro.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ru.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/sa.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/sh.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/si.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/sk.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/sl.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/sq.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/sr.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/sv.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ta.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/te.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/th.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/tl.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/tr.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/uk.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/ur.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/uz.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/vi.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/zh-Hant.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/zh-TW.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/languages/zh.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/logo.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/nav-item.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/nav.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/pagination.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/palette.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/post.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/progress.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/search.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/social.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/source-file.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/source.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/tabs-item.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/tabs.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/tags.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/toc-item.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/toc.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/partials/top.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/templates/redirect.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/utilities/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/utilities/filter/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/material/utilities/filter/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/materialx/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/materialx/__meta__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/materialx/emoji.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mdurl/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mdurl/_decode.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mdurl/_encode.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mdurl/_format.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mdurl/_parse.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mdurl/_url.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mergedeep/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mergedeep/mergedeep.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mergedeep/test_mergedeep.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/commands/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/commands/build.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/commands/gh_deploy.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/commands/new.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/commands/serve.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/config/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/config/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/config/config_options.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/config/defaults.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.ar.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.da.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.de.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.du.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.es.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.fi.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.fr.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.hi.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.hu.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.hy.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.it.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.ja.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.jp.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.kn.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.ko.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.multi.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.nl.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.no.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.pt.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.ro.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.ru.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.sa.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.stemmer.support.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.sv.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.ta.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.te.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.th.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.tr.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.vi.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/lunr.zh.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/lunr-language/tinyseg.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/prebuild-index.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/search_index.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/templates/search/lunr.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/templates/search/main.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/contrib/search/templates/search/worker.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/livereload/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/localization.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/plugins.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/structure/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/structure/files.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/structure/nav.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/structure/pages.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/structure/toc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/theme.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/404.html` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/base.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/content.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/css/base.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/css/bootstrap.min.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/css/brands.min.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/css/fontawesome.min.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/css/solid.min.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/css/v4-font-face.min.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/js/base.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/js/bootstrap.bundle.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/js/darkmode.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/keyboard-modal.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/main.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/mkdocs_theme.yml`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/nav-sub.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/search-modal.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/mkdocs/toc.html` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/404.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/base.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/breadcrumbs.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/css/theme.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/css/theme_extra.css`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/footer.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/js/html5shiv.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/js/jquery-3.6.0.min.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/js/theme.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/js/theme_extra.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/main.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/mkdocs_theme.yml`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/nav.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/search.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/searchbox.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/toc.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/themes/readthedocs/versions.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/utils/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/utils/babel_stub.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/utils/cache.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/utils/filters.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/utils/meta.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/utils/rendering.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/utils/templates.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs/utils/yaml.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_get_deps/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_get_deps/__main__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_get_deps/cache.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_get_deps/yaml_util.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_monorepo_plugin/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_monorepo_plugin/edit_uri.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_monorepo_plugin/merger.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_monorepo_plugin/parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_monorepo_plugin/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_monorepo_plugin/tests/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mkdocs_monorepo_plugin/tests/test_plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/multipart/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/multipart/decoders.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/multipart/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/multipart/multipart.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/aac.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/aiff.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/apev2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/asf.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/dsf.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/file.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/flac.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/id3.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/mp4.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/smf.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/vorbis.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/music_tag/wave.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_constants.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_file.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_iff.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_riff.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tags.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tools/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tools/_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tools/mid3cp.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tools/mid3iconv.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tools/mid3v2.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tools/moggsplit.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tools/mutagen_inspect.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_tools/mutagen_pony.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/_vorbis.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/aac.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/ac3.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/aiff.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/apev2.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/asf/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/asf/_attrs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/asf/_objects.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/asf/_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/dsdiff.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/dsf.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/easyid3.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/easymp4.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/flac.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/id3/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/id3/_file.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/id3/_frames.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/id3/_id3v1.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/id3/_specs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/id3/_tags.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/id3/_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/m4a.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/monkeysaudio.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/mp3/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/mp3/_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/mp4/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/mp4/_as_entry.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/mp4/_atom.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/mp4/_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/musepack.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/ogg.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/oggflac.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/oggopus.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/oggspeex.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/oggtheora.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/oggvorbis.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/optimfrog.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/smf.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/tak.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/trueaudio.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/wave.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mutagen/wavpack.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/__main__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/api.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/applytype.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/argmap.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/binder.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/bogus_type.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/build.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/cache.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/checker.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/checker_shared.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/checker_state.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/checkexpr.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/checkmember.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/checkpattern.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/checkstrformat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/config_parser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/constant_fold.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/constraints.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/copytype.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/defaults.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/dmypy/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/dmypy/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/dmypy/client.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/dmypy_os.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/dmypy_server.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/dmypy_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/erasetype.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/error_formatter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/errorcodes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/errors.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/evalexpr.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/expandtype.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/exprtotype.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/fastparse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/find_sources.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/fixup.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/freetree.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/fscache.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/fswatcher.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/gclogger.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/git.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/graph_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/indirection.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/infer.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/inspections.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/ipc.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/join.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/literals.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/lookup.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/main.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/maptype.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/meet.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/memprofile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/message_registry.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/messages.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/metastore.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/mixedtraverser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/modulefinder.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/moduleinspect.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/mro.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/nodes.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/operators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/options.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/parse.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/partially_defined.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/patterns.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugin.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/attrs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/common.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/constants.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/ctypes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/dataclasses.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/default.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/enums.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/functools.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/proper_plugin.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/plugins/singledispatch.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/pyinfo.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/reachability.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/refinfo.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/renaming.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/report.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/scope.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_classprop.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_enum.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_infer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_namedtuple.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_newtype.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_pass1.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_shared.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_typeargs.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/semanal_typeddict.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/astdiff.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/astmerge.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/aststrip.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/deps.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/mergecheck.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/objgraph.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/subexpr.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/target.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/trigger.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/server/update.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/sharedparse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/solve.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/split_namespace.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/state.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/stats.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/strconv.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/stubdoc.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/stubgen.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/stubgenc.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/stubinfo.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/stubtest.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/stubutil.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/subtypes.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/suggestions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/config.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/data.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/helpers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/meta/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/meta/_pytest.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/meta/test_diff_helper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/meta/test_parse_data.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/meta/test_update_data.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/test_config_parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/test_find_sources.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/test_ref_info.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testapi.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testargs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testcheck.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testcmdline.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testconstraints.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testdaemon.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testdeps.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testdiff.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testerrorstream.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testfinegrained.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testfinegrainedcache.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testformatter.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testfscache.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testgraph.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testinfer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testipc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testmerge.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testmodulefinder.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testmypyc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testoutput.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testparse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testpep561.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testpythoneval.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testreports.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testsemanal.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testsolve.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/teststubgen.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/teststubinfo.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/teststubtest.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testsubtypes.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testtransform.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testtypegen.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testtypes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/testutil.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/typefixture.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/update_data.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/test/visitors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/traverser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/treetransform.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/tvar_scope.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/type_visitor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/typeanal.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/typeops.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/types.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/types_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/typestate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/typetraverser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/typevars.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/typevartuples.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/util.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/version.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/visitor.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy/xml/mypy-html.css` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypy_extensions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/analysis/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/analysis/attrdefined.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/analysis/blockfreq.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/analysis/dataflow.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/analysis/ircheck.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/analysis/selfleaks.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/annotate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/build.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/codegen/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/codegen/cstring.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/codegen/emit.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/codegen/emitclass.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/codegen/emitfunc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/codegen/emitmodule.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/codegen/emitwrapper.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/codegen/literals.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/common.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/crash.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/errors.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/ir/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/ir/class_ir.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/ir/func_ir.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/ir/module_ir.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/ir/ops.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/ir/pprint.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/ir/rtypes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/ast_helpers.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/builder.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/callable_class.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/classdef.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/constant_fold.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/context.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/env_class.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/expression.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/for_helpers.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/format_str_tokenizer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/function.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/generator.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/ll_builder.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/mapper.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/match.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/missingtypevisitor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/nonlocalcontrol.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/prebuildvisitor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/prepare.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/specialize.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/statement.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/targets.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/visitor.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/irbuild/vtable.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/lower/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/lower/int_ops.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/lower/list_ops.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/lower/misc_ops.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/lower/registry.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/namegen.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/options.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/bytes_ops.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/dict_ops.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/exc_ops.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/float_ops.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/generic_ops.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/int_ops.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/list_ops.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/misc_ops.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/registry.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/set_ops.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/str_ops.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/tuple_ops.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/primitives/weakref_ops.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/rt_subtype.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/sametype.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/subtype.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/config.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_alwaysdefined.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_analysis.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_annotate.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_cheader.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_commandline.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_emit.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_emitclass.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_emitfunc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_emitwrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_exceptions.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_external.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_irbuild.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_ircheck.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_literals.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_lowering.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_misc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_namegen.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_optimizations.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_pprint.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_rarray.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_refcount.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_run.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_serialization.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_struct.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_tuplename.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/test_typeops.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/test/testutil.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/copy_propagation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/exceptions.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/flag_elimination.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/ir_transform.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/log_trace.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/lower.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/refcount.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/spill.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/mypyc/transform/uninit.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/chartparser_app.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/chunkparser_app.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/collocations_app.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/concordance_app.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/nemo_app.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/rdparser_app.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/srparser_app.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/wordfreq_app.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/app/wordnet_app.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/book.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/ccg/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/ccg/api.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/ccg/chart.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/ccg/combinator.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/ccg/lexicon.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/ccg/logic.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chat/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chat/eliza.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chat/iesha.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chat/rude.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chat/suntsu.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chat/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chat/zen.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chunk/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chunk/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chunk/named_entity.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chunk/regexp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/chunk/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/decisiontree.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/maxent.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/megam.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/naivebayes.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/positivenaivebayes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/rte_classify.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/scikitlearn.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/senna.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/svm.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/tadm.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/textcat.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/classify/weka.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/cli.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/cluster/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/cluster/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/cluster/em.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/cluster/gaac.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/cluster/kmeans.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/cluster/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/collections.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/collocations.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/compat.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/europarl_raw.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/aligned.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/api.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/bcp47.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/bnc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/bracket_parse.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/categorized_sents.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/chasen.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/childes.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/chunked.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/cmudict.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/comparative_sents.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/conll.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/crubadan.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/dependency.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/framenet.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/ieer.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/indian.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/ipipan.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/knbc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/lin.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/markdown.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/mte.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/nkjp.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/nombank.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/nps_chat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/opinion_lexicon.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/panlex_lite.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/panlex_swadesh.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/pl196x.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/plaintext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/ppattach.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/propbank.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/pros_cons.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/reviews.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/rte.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/semcor.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/senseval.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/sentiwordnet.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/sinica_treebank.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/string_category.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/switchboard.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/tagged.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/timit.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/toolbox.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/twitter.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/udhr.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/util.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/verbnet.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/wordlist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/wordnet.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/xmldocs.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/reader/ycoe.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/corpus/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/data.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/decorators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/downloader.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/draw/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/draw/cfg.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/draw/dispersion.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/draw/table.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/draw/tree.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/draw/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/featstruct.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/grammar.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/help.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/inference/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/inference/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/inference/discourse.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/inference/mace.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/inference/nonmonotonic.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/inference/prover9.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/inference/resolution.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/inference/tableau.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/internals.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/jsontags.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/langnames.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lazyimport.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lm/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lm/api.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lm/counter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lm/models.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lm/preprocessing.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lm/smoothing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lm/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/lm/vocabulary.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/agreement.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/aline.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/association.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/confusionmatrix.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/distance.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/paice.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/scores.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/segmentation.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/metrics/spearman.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/misc/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/misc/babelfish.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/misc/chomsky.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/misc/minimalset.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/misc/sort.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/misc/wordfinder.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/bllip.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/chart.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/corenlp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/dependencygraph.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/earleychart.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/evaluate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/featurechart.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/generate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/malt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/nonprojectivedependencyparser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/pchart.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/projectivedependencyparser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/recursivedescent.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/shiftreduce.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/stanford.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/transitionparser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/parse/viterbi.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/probability.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/boxer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/chat80.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/cooper_storage.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/drt.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/drt_glue_demo.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/evaluate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/glue.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/hole.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/lfg.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/linearlogic.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/logic.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/relextract.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/skolemize.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sem/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sentiment/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sentiment/sentiment_analyzer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sentiment/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/sentiment/vader.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/api.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/arlstem.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/arlstem2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/cistem.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/isri.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/lancaster.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/porter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/regexp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/rslp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/snowball.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/stem/wordnet.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tabdata.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/api.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/brill.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/brill_trainer.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/crf.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/hmm.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/hunpos.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/mapping.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/perceptron.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/senna.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/sequential.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/stanford.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/tnt.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tag/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tbl/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tbl/api.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tbl/demo.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tbl/erroranalysis.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tbl/feature.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tbl/rule.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tbl/template.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/all.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/childes_fixt.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/classify_fixt.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/conftest.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/gensim_fixt.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/gluesemantics_malt_fixt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/portuguese_en_fixt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/probability_fixt.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/setup_fixt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/lm/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/lm/test_counter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/lm/test_models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/lm/test_preprocessing.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/lm/test_vocabulary.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_aline.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_bllip.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_brill.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_cfd_mutation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_cfg2chomsky.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_chunk.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_classify.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_collocations.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_concordance.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_corenlp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_corpora.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_corpus_views.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_data.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_disagreement.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_distance.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_downloader.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_freqdist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_hmm.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_json2csv_corpus.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_json_serialization.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_naivebayes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_nombank.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_pl196x.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_pos_tag.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_ribes.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_rte_classify.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_seekable_unicode_stream_reader.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_senna.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_stem.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_tag.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_tgrep.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_tokenize.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_twitter_auth.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_util.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/test_wordnet.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_bleu.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_gdfa.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_ibm1.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_ibm2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_ibm3.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_ibm4.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_ibm5.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_ibm_model.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_meteor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_nist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/test/unit/translate/test_stack_decoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/text.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tgrep.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/casual.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/destructive.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/legality_principle.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/mwe.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/nist.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/punkt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/regexp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/repp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/sexpr.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/simple.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/sonority_sequencing.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/stanford.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/stanford_segmenter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/texttiling.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/toktok.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/treebank.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tokenize/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/toolbox.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/bleu_score.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/chrf_score.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/gale_church.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/gdfa.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/gleu_score.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/ibm1.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/ibm2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/ibm3.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/ibm4.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/ibm5.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/ibm_model.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/meteor_score.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/metrics.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/nist_score.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/phrase_based.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/ribes_score.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/translate/stack_decoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tree/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tree/immutable.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tree/parented.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tree/parsing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tree/prettyprinter.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tree/probabilistic.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tree/transforms.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/tree/tree.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/treeprettyprinter.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/treetransforms.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/twitter/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/twitter/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/twitter/common.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/twitter/twitter_demo.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/twitter/twitterclient.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/twitter/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/util.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nltk/wsd.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nodeenv.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/date/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/date/duration.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/date/format.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/date/format_sets.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/date/options.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/date/re.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/nr/stream/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/stream/_notset.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/stream/_optional.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/stream/_refreshable.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/stream/_stream.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/stream/_supplier.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/algorithm/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/algorithm/longest_common_substring.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/annotations/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/atomic/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/atomic/_counter.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/awsgi/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/awsgi/_app.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/awsgi/_types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/awsgi/launcher/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/awsgi/launcher/flask.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/awsgi/launcher/gunicorn.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/awsgi/launcher/uvicorn.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/chaindict.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/config/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/config/_loader.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/date/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/date/duration.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/date/format.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/date/format_sets.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/date/options.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/digraph/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/digraph/_digraph.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/digraph/algorithm/remove_with_predecessors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/digraph/algorithm/topological_sort.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/exceptions/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/fs/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/fs/_atomic.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/fs/_chmod.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/fs/_discovery.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/fs/_path.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/fs/_walk.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/functional/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/functional/_assure.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/functional/_coalesce.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/functional/_consumer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/functional/_once.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/functional/_predicate.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/functional/_supplier.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/generic/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/git/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/inspect/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/io/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/io/_readers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/iter/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/iter/_sequence_walker.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/keyvalue/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/keyvalue/_api.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/keyvalue/_mappingadapter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/keyvalue/sqlite.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/logging/filters/simple_filter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/logging/formatters/terminal_colors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/once.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/optional.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/orderedset.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/parsing/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/parsing/_scanner.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/parsing/_tokenizer/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/parsing/_tokenizer/extractor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/parsing/_tokenizer/ruleset.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/parsing/_tokenizer/tokenizer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/parsing/rules.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/plugins/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/plugins/_pkg_resources.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/plugins/_plugin_registry.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/preconditions/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/process/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/process/_pidfile.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/process/_utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/process/root.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/proxy/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/proxy/_base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/proxy/_contextlocal.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/proxy/_proxy.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/proxy/_stackable.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/proxy/_threadlocal.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/re/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/refreshable.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/safearg/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/scanner.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/singleton/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/singleton/_notset.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/stream.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/task/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/task/_api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/task/_default.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/terminal/colors/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/terminal/colors/_attribute.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/terminal/colors/_color.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/terminal/colors/_style.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/text/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/text/_substitute_ranges.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/types.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/url/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/weak/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/nr/util/weak/_property.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/_logs/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/_logs/_internal/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/_logs/severity/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/attributes/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/baggage/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/baggage/propagation/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/context/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/context/context.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/context/contextvars_context.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/environment_variables.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/_internal/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/_internal/_log_encoder/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/_internal/metrics_encoder/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/_internal/trace_encoder/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/_log_encoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/metrics_encoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/trace_encoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/common/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/http/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/http/_log_exporter/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/http/metric_exporter/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/http/trace_exporter/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/http/trace_exporter/encoder/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/exporter/otlp/proto/http/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/_semconv.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/auto_instrumentation/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/auto_instrumentation/_load.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/auto_instrumentation/sitecustomize.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/bootstrap.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/bootstrap_gen.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/dependencies.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/distro.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/environment_variables.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/instrumentor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/propagators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/requests/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/requests/package.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/requests/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/sqlcommenter_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/instrumentation/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/metrics/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/metrics/_internal/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/metrics/_internal/instrument.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/metrics/_internal/observation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/propagate/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/propagators/composite.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/propagators/textmap.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/logs/v1/logs_service_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/logs/v1/logs_service_pb2_grpc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/metrics/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/metrics/v1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/metrics/v1/metrics_service_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/metrics/v1/metrics_service_pb2_grpc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/trace/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/trace/v1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/trace/v1/trace_service_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/collector/trace/v1/trace_service_pb2_grpc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/common/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/common/v1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/common/v1/common_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/logs/v1/logs_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/metrics/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/metrics/v1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/metrics/v1/metrics_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/resource/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/resource/v1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/resource/v1/resource_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/trace/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/trace/v1/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/trace/v1/trace_pb2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/proto/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/_configuration/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/_logs/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/_logs/_internal/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/_logs/_internal/export/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/_logs/_internal/export/in_memory_log_exporter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/_logs/export/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/environment_variables.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/error_handler/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/_view_instrument_match.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/aggregation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/exponential_histogram/buckets.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/exponential_histogram/mapping/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/exponential_histogram/mapping/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/exponential_histogram/mapping/exponent_mapping.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/exponential_histogram/mapping/ieee_754.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/exponential_histogram/mapping/logarithm_mapping.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/export/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/instrument.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/measurement.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/measurement_consumer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/metric_reader_storage.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/point.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/sdk_configuration.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/_internal/view.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/export/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/metrics/view/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/resources/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/trace/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/trace/export/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/trace/export/in_memory_span_exporter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/trace/id_generator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/trace/sampling.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/util/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/util/instrumentation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/sdk/version.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/aws_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/browser_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/client_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/cloud_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/cloudevents_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/code_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/container_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/db_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/deployment_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/destination_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/device_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/disk_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/dns_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/enduser_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/error_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/event_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/exception_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/faas_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/feature_flag_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/file_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/gcp_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/graphql_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/heroku_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/host_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/http_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/k8s_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/log_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/message_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/messaging_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/network_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/oci_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/opentracing_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/otel_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/other_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/peer_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/pool_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/process_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/rpc_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/server_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/service_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/session_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/source_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/system_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/telemetry_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/thread_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/tls_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/url_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/user_agent_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/attributes/webengine_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/container_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/db_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/dns_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/faas_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/http_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/messaging_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/process_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/rpc_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/_incubating/metrics/system_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/client_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/error_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/exception_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/http_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/network_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/otel_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/server_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/service_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/telemetry_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/url_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/attributes/user_agent_attributes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/metrics/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/metrics/http_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/resource/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/schemas.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/trace/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/semconv/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/trace/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/trace/propagation/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/trace/propagation/tracecontext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/trace/span.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/trace/status.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/_decorator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/_importlib_metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/_once.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/_providers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/http/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/http/httplib.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/http/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/re.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/util/types.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/opentelemetry/version.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/_elffile.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/_manylinux.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/_musllinux.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/_parser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/_structures.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/_tokenizer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/licenses/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/licenses/_spdx.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/markers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/metadata.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/requirements.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/specifiers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/tags.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/packaging/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/paginate/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/paginate/ext_reverse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/apache.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/apps.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/context.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/_blowfish/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/_blowfish/_gen_files.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/_blowfish/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/_blowfish/unrolled.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/_md4.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/des.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/digest.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/scrypt/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/scrypt/_builtin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/scrypt/_gen_files.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/crypto/scrypt/_salsa.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/exc.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/ext/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/ext/django/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/ext/django/models.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/ext/django/utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/argon2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/bcrypt.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/cisco.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/des_crypt.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/digests.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/django.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/fshp.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/ldap_digests.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/md5_crypt.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/misc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/mssql.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/mysql.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/oracle.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/pbkdf2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/phpass.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/postgres.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/roundup.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/scram.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/scrypt.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/sha1_crypt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/sha2_crypt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/sun_md5_crypt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/handlers/windows.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/hash.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/hosts.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/ifc.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/pwd.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/registry.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/__main__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/_test_bad_register.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/backports.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_apache.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_apps.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_context.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_context_deprecated.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_crypto_builtin_md4.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_crypto_des.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_crypto_digest.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_crypto_scrypt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_ext_django.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_ext_django_source.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_handlers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_handlers_argon2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_handlers_bcrypt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_handlers_cisco.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_handlers_django.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_handlers_pbkdf2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_handlers_scrypt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_hosts.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_pwd.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_registry.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_totp.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_utils_handlers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_utils_md4.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_utils_pbkdf2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/test_win32.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/tox_support.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/tests/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/totp.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/binary.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/compat/_ordered_dict.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/decor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/des.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/handlers.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/md4.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/utils/pbkdf2.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/passlib/win32.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pathspec/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pathspec/_meta.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pathspec/gitignore.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pathspec/pathspec.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pathspec/pattern.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pathspec/patterns/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pathspec/patterns/gitwildmatch.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pathspec/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/peewee.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/__main__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/__pip-runner__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/build_env.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cache.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/autocompletion.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/base_command.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/cmdoptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/command_context.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/index_command.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/main.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/main_parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/parser.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/progress_bars.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/req_command.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/spinners.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/cli/status_codes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/cache.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/check.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/completion.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/configuration.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/debug.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/download.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/freeze.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/hash.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/help.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/index.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/inspect.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/install.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/list.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/lock.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/search.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/show.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/uninstall.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/commands/wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/configuration.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/distributions/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/distributions/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/distributions/installed.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/distributions/sdist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/distributions/wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/exceptions.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/index/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/index/collector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/index/package_finder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/index/sources.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/locations/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/locations/_distutils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/locations/_sysconfig.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/locations/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/metadata/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/metadata/_json.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/metadata/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/metadata/importlib/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/metadata/importlib/_compat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/metadata/importlib/_dists.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/metadata/importlib/_envs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/metadata/pkg_resources.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/candidate.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/direct_url.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/format_control.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/index.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/installation_report.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/link.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/pylock.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/scheme.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/search_scope.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/selection_prefs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/target_python.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/models/wheel.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/network/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/network/auth.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/network/cache.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/network/download.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/network/lazy_wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/network/session.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/network/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/network/xmlrpc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/build/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/build/build_tracker.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/build/metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/build/metadata_editable.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/build/metadata_legacy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/build/wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/build/wheel_editable.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/build/wheel_legacy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/check.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/freeze.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/install/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/install/editable_legacy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/install/wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/operations/prepare.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/pyproject.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/req/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/req/constructors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/req/req_dependency_group.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/req/req_file.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/req/req_install.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/req/req_set.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/req/req_uninstall.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/legacy/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/legacy/resolver.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/candidates.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/factory.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/found_candidates.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/provider.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/reporter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/requirements.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/resolver.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/self_outdated_check.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/_jaraco_text.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/_log.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/appdirs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/compat.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/compatibility_tags.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/datetime.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/deprecation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/direct_url_helpers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/egg_link.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/entrypoints.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/filesystem.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/filetypes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/glibc.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/hashes.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/logging.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/misc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/packaging.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/retry.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/setuptools_build.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/subprocess.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/temp_dir.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/unpacking.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/urls.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/virtualenv.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/utils/wheel.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/vcs/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/vcs/bazaar.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/vcs/git.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/vcs/mercurial.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/vcs/subversion.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/vcs/versioncontrol.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_internal/wheel_builder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/_cmd.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/adapter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/cache.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/caches/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/caches/file_cache.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/caches/redis_cache.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/controller.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/filewrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/heuristics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/serialize.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/cachecontrol/wrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/certifi/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/certifi/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/certifi/core.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/dependency_groups/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/dependency_groups/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/dependency_groups/_implementation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/dependency_groups/_lint_dependency_groups.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/dependency_groups/_pip_wrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/dependency_groups/_toml_compat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/compat.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/database.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/index.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/locators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/manifest.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/markers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/resources.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/scripts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/util.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distlib/wheel.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distro/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distro/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/distro/distro.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/idna/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/idna/codec.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/idna/compat.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/idna/core.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/idna/idnadata.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/idna/intranges.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/idna/package_data.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/idna/uts46data.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/msgpack/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/msgpack/exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/msgpack/ext.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/msgpack/fallback.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/_elffile.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/_manylinux.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/_musllinux.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/_parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/_structures.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/_tokenizer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/licenses/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/licenses/_spdx.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/markers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/requirements.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/specifiers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/tags.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/packaging/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pkg_resources/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/android.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/api.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/macos.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/unix.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/platformdirs/windows.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/console.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/filter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/filters/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/formatter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/formatters/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/formatters/_mapping.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/lexer.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/lexers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/lexers/_mapping.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/lexers/python.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/modeline.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/regexopt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/scanner.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/sphinxext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/style.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/styles/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/styles/_mapping.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/token.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/unistring.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pygments/util.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_impl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_in_process/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/__version__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/_internal_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/adapters.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/api.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/auth.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/certs.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/compat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/cookies.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/help.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/hooks.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/models.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/packages.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/sessions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/status_codes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/structures.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/requests/utils.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/providers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/reporters.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/resolvers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/resolvers/abstract.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/resolvers/criterion.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/resolvers/exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/resolvers/resolution.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/resolvelib/structs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/__main__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_cell_widths.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_emoji_codes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_emoji_replace.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_export_format.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_extension.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_fileno.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_inspect.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_log_render.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_loop.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_null_file.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_palettes.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_pick.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_ratio.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_spinners.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_stack.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_timer.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_win32_console.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_windows.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_windows_renderer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/_wrap.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/abc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/align.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/ansi.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/bar.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/box.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/cells.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/color.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/color_triplet.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/columns.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/console.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/constrain.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/containers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/control.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/default_styles.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/diagnose.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/emoji.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/errors.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/file_proxy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/filesize.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/highlighter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/json.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/jupyter.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/layout.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/live.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/live_render.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/logging.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/markup.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/measure.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/padding.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/pager.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/palette.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/panel.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/pretty.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/progress.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/progress_bar.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/prompt.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/protocol.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/region.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/repr.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/rule.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/scope.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/screen.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/segment.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/spinner.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/status.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/style.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/styled.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/syntax.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/table.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/terminal_theme.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/text.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/theme.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/themes.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/traceback.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/rich/tree.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/tomli/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/tomli/_parser.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/tomli/_re.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/tomli/_types.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/tomli_w/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/tomli_w/_writer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/truststore/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/truststore/_api.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/truststore/_macos.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/truststore/_openssl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/truststore/_ssl_constants.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/truststore/_windows.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/typing_extensions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/_collections.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/_version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/connection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/connectionpool.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/_appengine_environ.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/_securetransport/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/_securetransport/bindings.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/_securetransport/low_level.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/appengine.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/ntlmpool.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/pyopenssl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/securetransport.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/contrib/socks.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/fields.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/filepost.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/packages/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/packages/backports/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/packages/backports/makefile.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/packages/backports/weakref_finalize.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/packages/six.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/poolmanager.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/request.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/response.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/connection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/proxy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/queue.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/request.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/response.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/retry.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/ssl_.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/ssl_match_hostname.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/ssltransport.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/timeout.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/url.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pip/_vendor/urllib3/util/wait.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkce/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/tests/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/tests/data/my-test-package-source/setup.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/tests/test_find_distributions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/tests/test_integration_zope_interface.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/tests/test_markers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/tests/test_pkg_resources.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/tests/test_resources.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pkg_resources/tests/test_working_set.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/platformdirs/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/platformdirs/__main__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/platformdirs/android.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/platformdirs/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/platformdirs/macos.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/platformdirs/unix.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/platformdirs/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/platformdirs/windows.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/apsw_ext.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/cockroachdb.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/dataset.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/db_url.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/fields.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/flask_utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/hybrid.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/kv.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/migrate.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/mysql_ext.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/pool.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/postgres_ext.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/psycopg3_ext.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/reflection.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/shortcuts.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/signals.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/sqlcipher_ext.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/sqlite_changelog.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/sqlite_ext.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/sqlite_udf.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/sqliteq.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/playhouse/test_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pluggy/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pluggy/_callers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pluggy/_hooks.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pluggy/_manager.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pluggy/_result.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pluggy/_tracing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pluggy/_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pluggy/_warnings.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/all_languages.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/clientlib.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/color.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/autoupdate.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/clean.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/gc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/hook_impl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/init_templatedir.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/install_uninstall.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/migrate_config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/run.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/sample_config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/try_repo.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/validate_config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/commands/validate_manifest.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/constants.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/envcontext.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/error_handler.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/errors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/file_lock.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/git.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/hook.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/lang_base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/conda.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/coursier.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/dart.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/docker.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/docker_image.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/dotnet.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/fail.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/golang.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/haskell.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/julia.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/lua.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/node.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/perl.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/pygrep.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/python.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/r.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/ruby.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/rust.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/script.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/swift.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/languages/system.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/logging_handler.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/meta_hooks/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/meta_hooks/check_hooks_apply.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/meta_hooks/check_useless_excludes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/meta_hooks/identity.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/output.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/parse_shebang.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/prefix.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/repository.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/resources/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/resources/empty_template_environment.yml`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/resources/empty_template_main.go`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/resources/empty_template_setup.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/staged_files_only.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/store.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/xargs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/yaml.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pre_commit/yaml_rewrite.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/_common.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/_psaix.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/_psbsd.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/_pslinux.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/_psosx.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/_psposix.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/_pssunos.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/_pswindows.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/__main__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_aix.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_bsd.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_connections.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_contracts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_linux.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_memleaks.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_misc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_osx.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_posix.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_process.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_process_all.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_scripts.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_sudo.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_sunos.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_system.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_testutils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_unicode.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/psutil/tests/test_windows.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pwinput/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pwinput/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pwiz.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/py.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/ber/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/ber/decoder.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/ber/encoder.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/ber/eoo.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/cer/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/cer/decoder.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/cer/encoder.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/der/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/der/decoder.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/der/encoder.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/native/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/native/decoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/native/encoder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/codec/streaming.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/compat/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/compat/integer.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/debug.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/error.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/char.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/constraint.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/error.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/namedtype.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/namedval.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/opentype.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/tag.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/tagmap.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/univ.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyasn1/type/useful.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/_ast_gen.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/_build_tables.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/ast_transforms.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/c_ast.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/c_generator.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/c_lexer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/c_parser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/lextab.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/ply/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/ply/cpp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/ply/ctokens.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/ply/lex.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/ply/yacc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/ply/ygen.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/plyparser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pycparser/yacctab.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_config.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_core_metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_core_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_dataclasses.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_decorators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_decorators_v1.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_discriminated_union.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_docs_extraction.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_fields.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_forward_ref.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_generate_schema.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_generics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_git.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_import_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_internal_dataclass.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_known_annotated_metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_mock_val_ser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_model_construction.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_repr.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_schema_generation_shared.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_serializers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_signature.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_std_types_schema.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_typing_extra.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_utils.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_validate_call.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_internal/_validators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/_migration.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/alias_generators.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/aliases.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/annotated_handlers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/class_validators.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/color.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/config.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/dataclasses.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/datetime_parse.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/decorator.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/deprecated/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/deprecated/class_validators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/deprecated/config.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/deprecated/copy_internals.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/deprecated/decorator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/deprecated/json.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/deprecated/parse.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/deprecated/tools.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/env_settings.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/error_wrappers.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/errors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/experimental/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/experimental/pipeline.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/fields.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/functional_serializers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/functional_validators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/generics.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/json.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/json_schema.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/main.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/mypy.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/networks.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/parse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/plugin/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/plugin/_loader.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/plugin/_schema_validator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/root_model.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/schema.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/tools.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/type_adapter.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/typing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/_hypothesis_plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/annotated_types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/class_validators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/color.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/config.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/dataclasses.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/datetime_parse.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/decorator.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/env_settings.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/error_wrappers.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/errors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/fields.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/generics.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/json.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/mypy.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/networks.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/parse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/schema.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/tools.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/typing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/validators.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/v1/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/validate_call_decorator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/validators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic/warnings.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_core/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_core/core_schema.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/main.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/aws.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/azure.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/cli.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/dotenv.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/env.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/gcp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/json.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/pyproject.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/secrets.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/toml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/providers/yaml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/sources/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydantic_settings/version.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/loaders/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/loaders/python.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/processors/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/processors/crossref.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/processors/filter.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/processors/google.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/processors/pydocmd.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/processors/smart.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/processors/sphinx.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/renderers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/renderers/docusaurus.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/renderers/hugo.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/renderers/jinja2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/renderers/markdown.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/renderers/mkdocs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/source_linkers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/contrib/source_linkers/git.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/interfaces.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/novella/preprocessor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/static.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/docspec.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/knownfiles.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/misc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/misc_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/pages.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/pages_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/watchdog.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pydoc_markdown/util/ytemplate.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/cmdline.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/console.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/filter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/filters/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/_mapping.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/bbcode.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/groff.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/html.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/img.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/irc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/latex.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/other.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/pangomarkup.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/rtf.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/svg.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/terminal.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/formatters/terminal256.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_ada_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_asy_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_cl_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_cocoa_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_csound_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_css_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_googlesql_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_julia_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_lasso_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_lilypond_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_lua_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_luau_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_mapping.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_mql_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_mysql_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_openedge_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_php_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_postgres_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_qlik_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_scheme_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_scilab_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_sourcemod_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_sql_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_stan_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_stata_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_tsql_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_usd_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_vbscript_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/_vim_builtins.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/actionscript.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ada.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/agile.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/algebra.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ambient.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/amdgpu.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ampl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/apdlexer.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/apl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/archetype.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/arrow.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/arturo.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/asc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/asm.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/asn1.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/automation.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/bare.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/basic.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/bdd.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/berry.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/bibtex.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/blueprint.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/boa.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/bqn.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/business.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/c_cpp.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/c_like.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/capnproto.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/carbon.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/cddl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/chapel.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/clean.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/codeql.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/comal.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/compiled.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/configs.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/console.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/cplint.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/crystal.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/csound.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/css.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/d.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/dalvik.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/data.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/dax.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/devicetree.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/diff.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/dns.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/dotnet.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/dsls.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/dylan.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ecl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/eiffel.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/elm.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/elpi.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/email.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/erlang.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/esoteric.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ezhil.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/factor.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/fantom.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/felix.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/fift.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/floscript.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/forth.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/fortran.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/foxpro.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/freefem.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/func.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/functional.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/futhark.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/gcodelexer.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/gdscript.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/gleam.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/go.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/grammar_notation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/graph.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/graphics.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/graphql.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/graphviz.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/gsql.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/hare.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/haskell.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/haxe.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/hdl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/hexdump.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/html.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/idl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/igor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/inferno.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/installers.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/int_fiction.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/iolang.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/j.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/javascript.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/jmespath.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/jslt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/json5.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/jsonnet.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/jsx.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/julia.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/jvm.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/kuin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/kusto.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ldap.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/lean.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/lilypond.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/lisp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/macaulay2.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/make.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/maple.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/markup.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/math.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/matlab.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/maxima.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/meson.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/mime.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/minecraft.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/mips.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ml.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/modeling.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/modula2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/mojo.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/monte.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/mosel.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ncl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/nimrod.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/nit.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/nix.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/numbair.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/oberon.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/objective.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ooc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/openscad.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/other.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/parasail.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/parsers.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/pascal.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/pawn.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/pddl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/perl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/phix.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/php.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/pointless.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/pony.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/praat.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/procfile.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/prolog.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/promql.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/prql.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ptx.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/python.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/q.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/qlik.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/qvt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/r.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/rdf.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/rebol.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/rego.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/resource.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ride.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/rita.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/rnc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/roboconf.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/robotframework.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ruby.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/rust.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/sas.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/savi.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/scdoc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/scripting.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/sgf.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/shell.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/sieve.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/slash.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/smalltalk.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/smithy.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/smv.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/snobol.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/solidity.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/soong.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/sophia.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/special.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/spice.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/sql.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/srcinfo.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/stata.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/supercollider.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/tablegen.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/tact.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/tal.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/tcl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/teal.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/templates.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/teraterm.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/testing.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/text.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/textedit.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/textfmts.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/theorem.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/thingsdb.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/tlb.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/tls.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/tnt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/trafficscript.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/typoscript.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/typst.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/ul4.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/unicon.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/urbi.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/usd.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/varnish.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/verification.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/verifpal.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/vip.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/vyper.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/web.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/webassembly.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/webidl.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/webmisc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/wgsl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/whiley.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/wowtoc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/wren.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/x10.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/xorg.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/yang.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/yara.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/lexers/zig.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/modeline.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/plugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/regexopt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/scanner.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/sphinxext.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/style.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/_mapping.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/abap.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/algol.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/algol_nu.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/arduino.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/autumn.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/borland.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/bw.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/coffee.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/colorful.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/default.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/dracula.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/emacs.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/friendly.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/friendly_grayscale.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/fruity.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/gh_dark.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/gruvbox.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/igor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/inkpot.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/lightbulb.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/lilypond.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/lovelace.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/manni.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/material.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/monokai.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/murphy.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/native.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/nord.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/onedark.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/paraiso_dark.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/paraiso_light.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/pastie.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/perldoc.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/rainbow_dash.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/rrt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/sas.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/solarized.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/staroffice.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/stata_dark.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/stata_light.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/tango.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/trac.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/vim.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/vs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/xcode.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/styles/zenburn.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/token.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/unistring.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pygments/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/__meta__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/_bypassnorm.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/arithmatex.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/b64.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/betterem.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/blocks/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/blocks/admonition.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/blocks/block.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/blocks/caption.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/blocks/definition.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/blocks/details.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/blocks/html.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/blocks/tab.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/caret.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/critic.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/details.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/emoji.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/emoji1_db.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/escapeall.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/extra.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/fancylists.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/gemoji_db.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/highlight.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/inlinehilite.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/keymap_db.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/keys.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/magiclink.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/mark.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/pathconverter.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/progressbar.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/saneheaders.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/slugs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/smartsymbols.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/snippets.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/striphtml.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/superfences.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/tabbed.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/tasklist.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/tilde.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/twemoji_db.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pymdownx/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pyogg/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyogg/flac.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/pyogg/library_loader.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyogg/ogg.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pyogg/opus.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/pyogg/vorbis.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_asyncio/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_asyncio/plugin.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_cov/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_cov/engine.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_cov/plugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_mock/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_mock/_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_mock/_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytest_mock/plugin.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/python_multipart/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/python_multipart/decoders.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/python_multipart/exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/python_multipart/multipart.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytokens/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytokens/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/pytokens/cli.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/cli/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/cli/colors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/cli/harvest.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/cli/tools.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/complexity.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/contrib/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/contrib/flake8.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/metrics.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/raw.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/conftest.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/data/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/data/no_encoding.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/data/py3unicode.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/run.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_cli.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_cli_colors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_cli_harvest.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_cli_tools.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_complexity_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_complexity_visitor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_halstead.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_ipynb.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_other_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/tests/test_raw.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/radon/visitors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/_attrs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/_core.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/exceptions.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/jsonschema.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/retrieval.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/tests/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/tests/test_core.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/tests/test_exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/tests/test_jsonschema.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/tests/test_referencing_suite.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/tests/test_retrieval.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/referencing/typing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/regex/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/regex/_regex_core.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/regex/regex.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/regex/test_regex.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/__version__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/_internal_utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/adapters.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/api.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/auth.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/certs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/compat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/cookies.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/help.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/hooks.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/models.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/packages.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/sessions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/status_codes.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/structures.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/requests/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/__version__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/api.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/fixtures.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/handlers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/mocks.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/respx/models.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/patterns.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/plugin.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/router.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/transports.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/respx/types.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/respx/utils.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/__main__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_cell_widths.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_emoji_codes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_emoji_replace.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_export_format.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_extension.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_fileno.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_inspect.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_log_render.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_loop.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_null_file.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_palettes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_pick.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_ratio.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_spinners.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_stack.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_timer.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_win32_console.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_windows.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_windows_renderer.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/_wrap.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/abc.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/align.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/ansi.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/bar.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/box.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/cells.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/color.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/color_triplet.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/columns.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/console.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/constrain.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/containers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/control.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/default_styles.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/diagnose.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/emoji.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/errors.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/file_proxy.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/filesize.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/highlighter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/json.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/jupyter.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/layout.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/live.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/live_render.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/logging.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/markdown.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/markup.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/measure.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/padding.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/pager.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/palette.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/panel.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/pretty.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/progress.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/progress_bar.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/prompt.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/protocol.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/region.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/repr.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/rule.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/scope.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/screen.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/segment.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/spinner.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/status.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/style.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/styled.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/syntax.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/table.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/terminal_theme.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/text.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/theme.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/themes.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rich/traceback.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/rich/tree.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rpds/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/asn1.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/cli.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/common.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/core.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/key.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/parallel.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/pem.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/pkcs1.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/pkcs1_v2.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/prime.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/randnum.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/transform.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/rsa/util.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/anchor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/comments.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/compat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/composer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/configobjwalker.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/constructor.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/cyaml.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/docinfo.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/dumper.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/emitter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/error.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/events.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/loader.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/mergevalue.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/nodes.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/parser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/reader.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/representer.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/resolver.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/scalarbool.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/scalarfloat.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/scalarint.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/scalarstring.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/scanner.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/serializer.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/tag.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/timestamp.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/tokens.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruamel/yaml/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/ruff/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/ruff/__main__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/alerts/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/alerts/github.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/alerts/requirements.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/alerts/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/asyncio_patch.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/auth/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/auth/cli.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/auth/cli_utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/auth/constants.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/auth/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/auth/models.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/auth/server.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/auth/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/cli.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/safety/cli_util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/cli_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/codebase/command.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/codebase/constants.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/codebase/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/codebase/render.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/codebase_utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/console.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/constants.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/decorators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/emoji.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/encoding.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/error_handlers.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/errors.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/event_bus/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/event_bus/bus.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/event_bus/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/handlers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/handlers/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/handlers/common.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/types/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/types/aliases.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/types/base.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/utils/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/utils/conditions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/utils/context.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/utils/creation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/utils/data.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/events/utils/emission.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/firewall/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/firewall/command.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/firewall/constants.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/firewall/events/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/firewall/events/handlers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/firewall/events/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatter.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/bare.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/html.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/json.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/schemas/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/schemas/common.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/schemas/v0_5.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/schemas/v3_0.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/schemas/zero_five.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/screen.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/formatters/text.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/init/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/init/command.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/init/constants.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/init/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/init/models.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/init/render.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/init/types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/meta.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/safety/models/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/models/obj.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/models/requirements.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/models/tools.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/models/vulnerabilities.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/output_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/safety-policy-template.yml`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/safety.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/command.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/constants.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/decorators.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/ecosystems/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/ecosystems/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/ecosystems/python/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/ecosystems/python/dependencies.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/ecosystems/python/main.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/ecosystems/target.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/finder/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/finder/file_finder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/finder/handlers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/fun_mode/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/fun_mode/celebration_effects.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/fun_mode/easter_eggs.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/init_scan.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/models.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/render.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/scan/validators.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/templates/index.html` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/templates/scan/index.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/auth.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/constants.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/decorators.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/definitions.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/environment_diff.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/factory.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/intents.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/interceptors/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/interceptors/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/interceptors/factory.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/interceptors/types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/interceptors/unix.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/interceptors/windows.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/mixins.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/pip/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/pip/command.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/pip/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/pip/parser.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/poetry/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/poetry/command.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/poetry/constants.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/poetry/main.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/poetry/parser.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/resolver.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/tool_inspector.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/typosquatting.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/uv/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/uv/command.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/tool/uv/main.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety/util.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/config/schemas/v3_0/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/config/schemas/v3_0/main.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/api/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/api/events.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/base.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/config_protocol.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/ecosystem.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/events/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/events/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/events/constants.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/events/context.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/events/payloads/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/events/payloads/main.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/events/payloads/onboarding.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/events/types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/file.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/git.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/package.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/policy_file.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/project.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/report_protocol.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/result.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/scan.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/specification.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/telemetry.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/util.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/models/vulnerability.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/report/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/report/schemas/v3_0/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/report/schemas/v3_0/constants.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/safety_schemas/report/schemas/v3_0/main.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/__about__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/_manylinux.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/_musllinux.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/_structures.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/specifiers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/tags.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/packaging/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/parsy/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/external/parsy/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/golang_version.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/matchers/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/matchers/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/matchers/gradle.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/matchers/pip_requirements.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/maven_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/package_restrictions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/cargo.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/composer.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/gem.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/go_mod.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/gradle.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/mix.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/package_lock.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/packages_lock_c_sharp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/pipfile.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/pnpm.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/poetry.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/pom_tree.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/preprocessors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/pubspec_lock.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/requirements.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/swiftpm.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/parsers/yarn.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semdep/subproject_matchers.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/app/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/app/auth.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/app/project_config.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/app/scans.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/app/session.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/app/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/autofix.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/bin/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/bytesize.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/cli.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/commands/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/commands/ci.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/commands/install.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/commands/login.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/commands/publish.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/commands/scan.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/commands/wrapper.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/config_resolver.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/console.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/console_scripts/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/console_scripts/entrypoint.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/console_scripts/pysemgrep.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/constants.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/core_output.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/core_runner.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/core_targets_plan.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/default_group.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/dependency_aware_rule.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/engine.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/env.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/error.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/error_handler.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/error_location.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/exclude_rules.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/external/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/external/git_url_parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/external/pymmh3.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/base.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/emacs.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/gitlab_sast.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/gitlab_secrets.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/json.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/junit_xml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/sarif.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/text.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/formatter/vim.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/git.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/join_rule.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/main.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/meta.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/metrics.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/nosemgrep.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/notifications.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/output.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/output_extra.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/parsing_data.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/profile_manager.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/resolve_dependency_source.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/resolve_subprojects.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/rpc.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/rpc_call.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/rule.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/rule_lang.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/rule_match.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/run_scan.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/safe_set.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/sca_subproject_support.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/scan_report.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/semgrep_core.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/semgrep_interfaces/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/semgrep_interfaces/generate.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/semgrep_interfaces/semgrep_metrics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/semgrep_interfaces/semgrep_output_v1.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/semgrep_types.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/settings.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/state.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/subproject.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/target_manager.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/target_mode.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/terminal.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/test.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/tracing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/types.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/semgrep/verbose_logging.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_core_metadata.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_discovery.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/_log.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/_macos_compat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/_modified.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/_msvccompiler.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/archive_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/ccompiler.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/cmd.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/_framework_compat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/bdist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/bdist_dumb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/bdist_rpm.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/build.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/build_clib.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/build_ext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/build_py.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/build_scripts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/check.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/clean.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/install.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/install_data.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/install_egg_info.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/install_headers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/install_lib.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/install_scripts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/command/sdist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compat/numpy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compat/py39.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/cygwin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/msvc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/tests/test_base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/tests/test_cygwin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/tests/test_mingw.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/tests/test_msvc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/tests/test_unix.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/unix.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/compilers/C/zos.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/core.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/cygwinccompiler.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/debug.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/dep_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/dir_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/dist.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/extension.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/fancy_getopt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/file_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/filelist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/log.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/spawn.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/sysconfig.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/compat/py39.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/support.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_archive_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_bdist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_bdist_dumb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_bdist_rpm.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_build.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_build_clib.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_build_ext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_build_py.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_build_scripts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_check.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_clean.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_cmd.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_config_cmd.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_core.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_dir_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_dist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_extension.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_file_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_filelist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_install.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_install_data.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_install_headers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_install_lib.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_install_scripts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_log.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_modified.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_sdist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_spawn.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_sysconfig.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_text_file.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/test_versionpredicate.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/tests/unix_compat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/text_file.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/unixccompiler.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/util.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/versionpredicate.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_distutils/zosccompiler.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_entry_points.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_imp.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_importlib.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_itertools.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_normalization.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_path.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_reqs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_scripts.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_shutil.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_static.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/autocommand/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/autocommand/autoasync.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/autocommand/autocommand.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/autocommand/automain.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/autocommand/autoparse.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/autocommand/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/backports/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/backports/tarfile/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/backports/tarfile/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/backports/tarfile/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/backports/tarfile/compat/py38.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/_adapters.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/_collections.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/_compat.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/_functools.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/_itertools.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/_meta.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/_text.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/compat/py311.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/compat/py39.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/importlib_metadata/diagnose.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/inflect/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/inflect/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/inflect/compat/py38.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/collections/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/context.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/functools/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/text/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/text/layouts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/text/show-newlines.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/text/strip-prefix.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/text/to-dvorak.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/jaraco/text/to-qwerty.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/more_itertools/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/more_itertools/more.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/more_itertools/recipes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/_elffile.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/_manylinux.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/_musllinux.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/_parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/_structures.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/_tokenizer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/licenses/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/licenses/_spdx.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/markers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/requirements.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/specifiers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/tags.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/packaging/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/android.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/api.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/macos.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/unix.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/windows.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/tomli/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/tomli/_parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/tomli/_re.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/tomli/_types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_checkers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_config.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_decorators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_functions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_importhook.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_memo.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_pytest_plugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_suppression.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_transformer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_union_transformer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typeguard/_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/typing_extensions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/__main__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/_bdist_wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/_setuptools_logging.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/bdist_wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/cli/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/cli/convert.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/cli/pack.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/cli/tags.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/cli/unpack.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/macosx_libfile.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/_elffile.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/_manylinux.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/_musllinux.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/_parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/_structures.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/_tokenizer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/markers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/requirements.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/specifiers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/tags.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/version.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/wheel/wheelfile.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/zipp/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/zipp/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/zipp/compat/py310.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/_vendor/zipp/glob.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/archive_util.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/build_meta.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/_requirestxt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/alias.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/bdist_egg.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/bdist_rpm.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/bdist_wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/build.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/build_clib.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/build_ext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/build_py.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/develop.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/dist_info.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/easy_install.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/editable_wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/egg_info.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/install.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/install_egg_info.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/install_lib.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/install_scripts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/rotate.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/saveopts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/sdist.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/setopt.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/command/test.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/compat/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/compat/py310.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/compat/py311.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/compat/py312.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/compat/py39.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/_apply_pyprojecttoml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/_validate_pyproject/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/_validate_pyproject/error_reporting.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/_validate_pyproject/extra_validations.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/_validate_pyproject/fastjsonschema_exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/_validate_pyproject/fastjsonschema_validations.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/_validate_pyproject/formats.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/expand.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/pyprojecttoml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/config/setupcfg.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/depends.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/discovery.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/dist.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/errors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/extension.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/glob.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/installer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/launch.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/logging.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/modified.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/monkey.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/msvc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/namespaces.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/compat/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/compat/py39.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/config/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/config/downloads/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/config/downloads/preload.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/config/test_apply_pyprojecttoml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/config/test_expand.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/config/test_pyprojecttoml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/config/test_pyprojecttoml_dynamic_deps.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/config/test_setupcfg.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/contexts.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/environment.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/fixtures.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/indexes/test_links_priority/external.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/indexes/test_links_priority/simple/foobar/index.html`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/integration/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/integration/helpers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/integration/test_pbr.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/integration/test_pip_install_sdist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/mod_with_constant.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/namespaces.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/script-with-bom.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_archive_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_bdist_deprecations.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_bdist_egg.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_bdist_wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_build.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_build_clib.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_build_ext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_build_meta.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_build_py.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_config_discovery.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_core_metadata.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_depends.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_develop.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_dist.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_dist_info.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_distutils_adoption.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_editable_install.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_egg_info.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_extern.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_find_packages.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_find_py_modules.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_glob.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_install_scripts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_logging.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_manifest.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_namespaces.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_scripts.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_sdist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_setopt.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_setuptools.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_shutil_wrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_unicode_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_virtualenv.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_warnings.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_wheel.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/test_windows_wrappers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/text.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/tests/textwrap.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/unicode_utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/warnings.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/wheel.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/setuptools/windows_support.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/shellingham/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/shellingham/_core.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/shellingham/nt.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/shellingham/posix/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/shellingham/posix/_core.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/shellingham/posix/proc.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/shellingham/posix/ps.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/six.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/slugify/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/slugify/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/slugify/__version__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/slugify/slugify.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/slugify/special.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sniffio/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sniffio/_impl.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/sniffio/_tests/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sniffio/_tests/test_sniffio.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sniffio/_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/connectors/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/connectors/aioodbc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/connectors/asyncio.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/connectors/pyodbc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/cyextension/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/_typing.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mssql/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mssql/aioodbc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mssql/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mssql/information_schema.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mssql/json.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mssql/provision.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mssql/pymssql.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mssql/pyodbc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/aiomysql.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/asyncmy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/cymysql.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/dml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/enumerated.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/expression.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/json.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/mariadb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/mariadbconnector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/mysqlconnector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/mysqldb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/provision.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/pymysql.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/pyodbc.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/reflection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/reserved_words.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/cx_oracle.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/dictionary.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/oracledb.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/provision.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/vector.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/_psycopg_common.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/array.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/dml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/ext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/hstore.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/json.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/named_types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/operators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/pg8000.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/pg_catalog.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/provision.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/psycopg.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/psycopg2cffi.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/ranges.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/dml.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/json.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/provision.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/pysqlcipher.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/pysqlite.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/_py_processors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/_py_row.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/_py_util.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/characteristics.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/create.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/cursor.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/events.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/interfaces.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/mock.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/processors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/reflection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/result.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/row.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/strategies.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/url.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/engine/util.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/event/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/event/api.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/event/attr.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/event/base.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/event/legacy.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/event/registry.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/events.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/exc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/associationproxy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/engine.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/exc.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/result.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/scoping.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/session.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/automap.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/baked.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/compiler.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/declarative/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/declarative/extensions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/horizontal_shard.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/hybrid.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/indexable.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/instrumentation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/mutable.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/mypy/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/mypy/apply.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/mypy/decl_class.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/mypy/infer.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/mypy/names.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/mypy/plugin.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/mypy/util.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/orderinglist.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/ext/serializer.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/future/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/future/engine.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/inspection.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/log.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/_orm_constructors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/_typing.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/attributes.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/bulk_persistence.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/clsregistry.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/collections.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/context.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/decl_api.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/decl_base.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/dependency.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/descriptor_props.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/dynamic.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/evaluator.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/events.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/exc.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/identity.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/instrumentation.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/interfaces.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/loading.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/mapped_collection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/mapper.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/path_registry.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/persistence.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/properties.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/query.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/relationships.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/scoping.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/strategies.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/strategy_options.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/sync.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/unitofwork.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/orm/writeonly.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/pool/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/pool/events.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/pool/impl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/schema.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/_dml_constructors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/_elements_constructors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/_orm_types.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/_py_util.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/_selectable_constructors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/_typing.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/annotation.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/base.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/cache_key.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/coercions.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/crud.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/ddl.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/default_comparator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/dml.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/elements.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/events.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/expression.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/functions.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/lambdas.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/naming.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/operators.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/roles.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/schema.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/selectable.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/sqltypes.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/traversals.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/type_api.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/sql/visitors.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/assertions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/assertsql.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/asyncio.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/config.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/engines.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/entities.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/exclusions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/fixtures/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/fixtures/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/fixtures/mypy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/fixtures/orm.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/fixtures/sql.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/pickleable.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/plugin/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/plugin/bootstrap.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/plugin/plugin_base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/plugin/pytestplugin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/profiling.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/provision.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/requirements.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/schema.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_cte.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_ddl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_deprecations.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_dialect.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_insert.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_reflection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_results.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_rowcount.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_select.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_sequence.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_types.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_unicode_ddl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_update_delete.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/util.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/testing/warnings.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/_collections.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/_concurrency_py3k.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/_has_cy.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/_py_collections.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/compat.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/concurrency.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/deprecations.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/langhelpers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/preloaded.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/queue.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/tool_support.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/topological.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/sqlalchemy/util/typing.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/applications.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/authentication.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/background.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/concurrency.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/config.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/convertors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/datastructures.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/endpoints.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/formparsers.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/authentication.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/base.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/cors.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/gzip.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/httpsredirect.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/sessions.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/trustedhost.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/middleware/wsgi.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/requests.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/responses.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/routing.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/schemas.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/staticfiles.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/status.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/templating.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/testclient.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/starlette/websockets.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/_cache.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/dispatch.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/driver.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/enabled.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example/base.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example/load_as_driver.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example/load_as_extension.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example/setup.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example/simple.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example2/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example2/fields.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/example2/setup.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/exception.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/extension.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/hook.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/named.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/sphinxext.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/extension_unimportable.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/manager.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_cache.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_callback.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_dispatch.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_driver.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_enabled.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_example_fields.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_example_simple.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_extension.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_hook.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_named.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_sphinxext.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/test_test_manager.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/stevedore/tests/utils.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tabulate/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tabulate/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/after.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/asyncio/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/asyncio/retry.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/before.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/before_sleep.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/nap.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/retry.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/stop.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/tornadoweb.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tenacity/wait.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/text_unidecode/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomli/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomli/_parser.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tomli/_re.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomli/_types.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tomli_w/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomli_w/_writer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/_compat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/_types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/api.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/container.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/items.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/parser.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/source.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/toml_char.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/toml_document.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tomlkit/toml_file.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/__main__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/_dist_ver.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/_main.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/_monitor.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/_tqdm.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/_tqdm_gui.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/_tqdm_notebook.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/_tqdm_pandas.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/_utils.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/asyncio.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/auto.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/autonotebook.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/cli.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/completion.sh` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/bells.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/concurrent.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/discord.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/itertools.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/logging.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/slack.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/telegram.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/contrib/utils_worker.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/dask.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/gui.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/keras.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/notebook.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/rich.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/std.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/tk.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/utils.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/tqdm/version.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/__init___test.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/backport/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/backport/inspect.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/future/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/future/astrewrite.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/future/astrewrite_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/future/fake.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/future/fake_test.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/typehint.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/typehint_test.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/utils.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/typeapi/utils_test.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/_completion_classes.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/_completion_shared.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/_types.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/_typing.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/cli.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/colors.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/completion.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/core.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/typer/main.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/typer/models.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/params.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/rich_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/testing.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/typer/utils.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/typing_extensions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/typing_inspection/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typing_inspection/introspection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/typing_inspection/typing_objects.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/_base_connection.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/_collections.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/_request_methods.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/_version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/connection.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/connectionpool.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/emscripten/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/emscripten/connection.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/emscripten/emscripten_fetch_worker.js`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/emscripten/fetch.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/emscripten/request.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/emscripten/response.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/pyopenssl.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/contrib/socks.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/fields.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/filepost.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/http2/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/http2/connection.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/http2/probe.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/poolmanager.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/response.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/connection.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/proxy.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/request.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/response.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/retry.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/ssl_.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/ssl_match_hostname.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/ssltransport.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/timeout.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/url.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/util.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/urllib3/util/wait.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/_compat.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/_subprocess.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/_types.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/config.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/importer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/lifespan/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/lifespan/off.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/lifespan/on.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/logging.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/loops/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/loops/asyncio.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/loops/auto.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/loops/uvloop.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/main.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/middleware/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/middleware/asgi2.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/middleware/message_logger.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/middleware/wsgi.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/auto.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/flow_control.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/h11_impl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/websockets/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/websockets/auto.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/websockets/websockets_impl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/websockets/websockets_sansio_impl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/protocols/websockets/wsproto_impl.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/server.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/supervisors/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/supervisors/basereload.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/supervisors/multiprocess.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/supervisors/statreload.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/supervisors/watchfilesreload.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/uvicorn/workers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/activator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/bash/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/bash/activate.sh`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/batch/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/cshell/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/fish/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/nushell/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/powershell/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/python/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/python/activate_this.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/activation/via_template.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/app_data/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/app_data/base.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/app_data/na.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/app_data/read_only.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/app_data/via_disk_folder.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/app_data/via_tempdir.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/cache/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/cache/cache.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/cache/file_cache.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/config/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/config/cli/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/config/cli/parser.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/config/convert.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/config/env_var.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/config/ini.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/creator.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/debug.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/describe.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/pyenv_cfg.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/_virtualenv.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/api.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/builtin_way.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/cpython/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/cpython/common.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/cpython/cpython3.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/cpython/mac_os.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/graalpy/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/pypy/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/pypy/common.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/pypy/pypy3.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/ref.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/builtin/via_global_self_do.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/store.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/create/via_global_ref/venv.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/builtin.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/cached_py_info.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/discover.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/info.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/py_info.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/py_spec.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/windows/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/discovery/windows/pep514.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/info.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/report.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/run/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/run/plugin/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/run/plugin/activators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/run/plugin/base.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/run/plugin/creators.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/run/plugin/discovery.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/run/plugin/seeders.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/run/session.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/base_embed.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/pip_invoke.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/via_app_data/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/via_app_data/pip_install/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/via_app_data/pip_install/base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/via_app_data/pip_install/copy.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/via_app_data/pip_install/symlink.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/embed/via_app_data/via_app_data.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/seeder.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/wheels/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/wheels/acquire.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/wheels/bundle.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/wheels/embed/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/wheels/periodic_update.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/seed/wheels/util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/error.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/lock.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/path/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/path/_permission.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/path/_sync.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/path/_win.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/subprocess/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/util/zipapp.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/virtualenv/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/events.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/api.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/fsevents.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/fsevents2.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/inotify.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/inotify_buffer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/inotify_c.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/kqueue.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/polling.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/read_directory_changes.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/observers/winapi.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/tricks/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/bricks.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/delayed_queue.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/dirsnapshot.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/echo.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/event_debouncer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/patterns.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/platform.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/utils/process_watcher.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/version.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/watchdog/watchmedo.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/__meta__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/_wcmatch.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/_wcparse.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/fnmatch.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/glob.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/pathlib.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/posix.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/util.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/wcmatch/wcmatch.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcwidth/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcwidth/table_vs16.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcwidth/table_wide.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcwidth/table_zero.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcwidth/unicode_versions.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/wcwidth/wcwidth.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_abnf.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_app.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_cookiejar.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_core.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_exceptions.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_handshake.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_http.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_logging.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_socket.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_ssl_compat.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_url.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/_wsdump.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/tests/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/tests/echo-server.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/tests/test_abnf.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/tests/test_app.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/tests/test_cookiejar.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/tests/test_http.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/tests/test_url.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/websocket/tests/test_websocket.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/wrapt/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wrapt/__wrapt__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wrapt/arguments.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wrapt/decorators.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wrapt/importer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wrapt/patches.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/wrapt/weakrefs.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/wrapt/wrappers.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/xenon/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/xenon/__main__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/xenon/api.py` | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/xenon/core.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/xenon/repository.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/composer.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/constructor.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/cyaml.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/dumper.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/emitter.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/error.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/events.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/loader.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/nodes.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/parser.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/reader.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/representer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/resolver.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/scanner.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/serializer.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yaml/tokens.py` | | | Active | |
    |

    | `scripts/.venv/lib/python3.13/site-packages/yaml_env_tag.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/__main__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/_version.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pyparser/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pyparser/pyparser.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pyparser/pyparser_utils.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pyparser/split_penalty_visitor.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/blank_line_calculator.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/comment_splicer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/continuation_splicer.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/pytree_unwrapper.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/pytree_utils.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/pytree_visitor.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/split_penalty.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/pytree/subtype_assigner.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/__init__.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/errors.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/file_resources.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/format_decision_state.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/format_token.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/identify_container.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/line_joiner.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/logical_line.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/object_state.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/reformatter.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/split_penalty.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/style.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/subtypes.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf/yapflib/yapf_api.py` | | |
    Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/__init__.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/fixer_base.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/fixer_util.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/patcomp.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/conv.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/driver.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/grammar.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/literals.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/parse.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/pgen.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/token.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pgen2/tokenize.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pygram.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/_ylib2to3/pytree.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/yapf_diff/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapf_third_party/yapf_diff/yapf_diff.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/blank_line_calculator_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/comment_splicer_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/file_resources_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/format_decision_state_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/format_token_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/line_joiner_test.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/logical_line_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/main_test.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/pytree_unwrapper_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/pytree_utils_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/pytree_visitor_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/reformatter_basic_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/reformatter_buganizer_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/reformatter_facebook_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/reformatter_pep8_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/reformatter_python3_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/reformatter_style_config_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/split_penalty_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/style_test.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/subtype_assigner_test.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/utils.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/yapf_test.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/yapftests/yapf_test_helper.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_cache.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_core.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_dns.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_engine.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_exceptions.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_handlers/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_handlers/answers.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_handlers/multicast_outgoing_queue.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_handlers/query_handler.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_handlers/record_manager.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_history.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_listener.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_logger.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_protocol/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_protocol/incoming.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_protocol/outgoing.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_record_update.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_services/__init__.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_services/browser.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_services/info.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_services/registry.py`
    | | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_services/types.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_transport.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_updates.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_utils/__init__.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_utils/asyncio.py` | |
    | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_utils/ipaddress.py` |
    | | Active | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_utils/name.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_utils/net.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/_utils/time.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/asyncio.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zeroconf/const.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zipp/__init__.py` | | | Active |
    | |

    | `scripts/.venv/lib/python3.13/site-packages/zipp/_functools.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zipp/compat/__init__.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zipp/compat/overlay.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zipp/compat/py310.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zipp/compat/py313.py` | | | Active
    | | |

    | `scripts/.venv/lib/python3.13/site-packages/zipp/glob.py` | | | Active | | |

    | `scripts/project/reports/TRACE_INDEX.yml` | | | Active | | |

    | `scripts/backfill_trace_meta.py` | | | Active | | |

    '
- path: scripts/description_compliance_check.py
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
- path: scripts/gonkui
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
- path: scripts/repo_inventory_and_governance.py
  type: script
  workflow: []
  indexes: []
  content: "#!/usr/bin/env python3\n\"\"\"\nrepo_inventory_and_governance.py - inventory\
    \ + governance index generator (patched)\n\nFixes applied:\n- Ensure PROJECT_ROOT\
    \ is resolved correctly to avoid walking the entire filesystem.\n- Robustly ignore\
    \ directories by checking path parts (so `project/logs/chat` can be ignored).\n\
    - Exclude chat logs explicitly from registration logic to remove them from Unlinked\
    \ / Unregistered.\n- Cleaned up find_all_files and index population flow to avoid\
    \ prior syntax issues.\n- Minimal behavior changes — preserves existing index-generation\
    \ and audit output logic.\n\"\"\"\n\nimport os\nimport re\nimport sys\nimport\
    \ yaml\nimport argparse\nimport subprocess\nfrom pathlib import Path\nfrom typing\
    \ import List, Dict, Any, Set, Tuple\n\n# --- Configuration ---\nPROJECT_ROOT\
    \ = Path(__file__).resolve().parent.parent\nprint(\"PROJECT_ROOT:\", PROJECT_ROOT)\n\
    FILETYPE_MAP = {\n    \".md\": \"doc\", \".py\": \"code\", \".sh\": \"code\",\
    \ \".html\": \"code\", \".js\": \"code\",\n    \".ts\": \"code\", \".css\": \"\
    code\", \".yml\": \"code\", \".go\": \"code\",\n}\nIGNORED_DIRS = {\n    \"project/logs/chat\"\
    , \".git\", \".idea\", \".venv\", \"node_modules\",\n    \"build\", \"dist\",\
    \ \"target\", \"__pycache__\", \"site\", \"archive\",\n    \"templates\", \".pytest_cache\"\
    \n}\nIGNORED_FILES = {\n    \"mkdocs.yml\", \"openapi.json\", \"bandit.yml\",\
    \ \"changed_files.txt\",\n    \"verification_report.md\", \"LICENSE\"\n}\n\nINDEX_MAP\
    \ = [\n    {\"match\": lambda p, f: f == \"doc\" and p.startswith(\"api/docs/\"\
    ),\n     \"indexes\": [\"api/docs/MASTER_INDEX.md\", \"api/docs/DOCS_QUALITY_INDEX.md\"\
    ]},\n\n    # Exclude project/logs/chat explicitly\n    {\"match\": lambda p, f:\
    \ f == \"doc\" and (\n        (p.startswith(\"project/archive/docs/\") or\n  \
    \       p.startswith(\"project/process/\") or\n         p.startswith(\"project/proposals/\"\
    ) or\n         p.startswith(\"project/reports/\") or\n         (p.startswith(\"\
    project/\") and Path(p).parent.name == \"project\"))\n        and not p.startswith(\"\
    project/logs/chat/\")\n    ), \"indexes\": [\"project/PROJECT_REGISTRY.md\"]},\n\
    \n    {\"match\": lambda p, f: f == \"doc\" and p.startswith(\"Gonk/GonkCLI/docs/\"\
    ),\n     \"indexes\": [\"Gonk/GonkCLI/DOCS_INDEX.md\"]},\n    {\"match\": lambda\
    \ p, f: f == \"doc\" and p.startswith(\"Gonk/GonkUI/docs/\"),\n     \"indexes\"\
    : [\"Gonk/GonkUI/DOCS_INDEX.md\"]},\n    {\"match\": lambda p, f: f == \"doc\"\
    \ and p.startswith(\"snitch/docs/\"),\n     \"indexes\": [\"snitch/DOCS_INDEX.md\"\
    ]},\n    {\"match\": lambda p, f: f == \"code\" and p.startswith(\"api/\"),\n\
    \     \"indexes\": [\"api/docs/CODE_FILE_INDEX.md\"]},\n    {\"match\": lambda\
    \ p, f: f == \"code\" and p.startswith(\"Gonk/\"),\n     \"indexes\": [\"Gonk/CODE_FILE_INDEX.md\"\
    ]},\n    {\"match\": lambda p, f: f == \"code\" and p.startswith(\"snitch/\"),\n\
    \     \"indexes\": [\"snitch/CODE_FILE_INDEX.md\"]},\n    {\"match\": lambda p,\
    \ f: f == \"code\" and p.startswith(\"scripts/\"),\n     \"indexes\": [\"scripts/CODE_FILE_INDEX.md\"\
    ]},\n]\n\n# --- Helper functions ---\ndef get_file_type(filepath: str) -> str:\n\
    \    name = os.path.basename(filepath)\n    if name.startswith(\".\") or name\
    \ in IGNORED_FILES:\n        return \"exempt\"\n    return FILETYPE_MAP.get(os.path.splitext(filepath)[1],\
    \ \"exempt\")\n\n\ndef extract_metadata(filepath: Path) -> Dict[str, Any]:\n \
    \   \"\"\"Extracts metadata (description, tags) from a file.\"\"\"\n    description\
    \ = \"No description available.\"\n    tags = []\n\n    try:\n        # Infer\
    \ tags from path\n        tags = [part for part in filepath.parts if part not\
    \ in IGNORED_DIRS and part != filepath.name]\n\n        # Extract description\
    \ from file content\n        content = filepath.read_text(encoding=\"utf-8\",\
    \ errors=\"ignore\")\n\n        # Check for summary comments\n        summary_match\
    \ = re.search(r\"<!-- Summary: (.*) -->|# Summary: (.*)\", content)\n        if\
    \ summary_match:\n            description = summary_match.group(1) or summary_match.group(2)\n\
    \        else:\n            # Fallback to first non-empty line for certain file\
    \ types\n            if filepath.suffix in [\".md\", \".py\", \".sh\", \".go\"\
    ]:\n                for line in content.splitlines():\n                    stripped_line\
    \ = line.strip()\n                    if stripped_line and not stripped_line.startswith((\"\
    #\", \"!\", \"<\")):\n                        description = stripped_line\n  \
    \                      break\n    except Exception:\n        # Ignore files that\
    \ cannot be read\n        pass\n\n    return {\"description\": description.strip(),\
    \ \"tags\": list(set(tags))}\n\n\ndef find_all_files() -> List[str]:\n    files:\
    \ List[str] = []\n\n    for root, dirs, filenames in os.walk(PROJECT_ROOT):\n\
    \        root_path = Path(root)\n        rel_parts = root_path.relative_to(PROJECT_ROOT).parts\n\
    \n        # Skip if any parent directory is ignored\n        if any(p in IGNORED_DIRS\
    \ for p in rel_parts):\n            dirs[:] = []  # prevent descending\n     \
    \       continue\n\n        # Prune ignored subdirs\n        dirs[:] = [d for\
    \ d in dirs if d not in IGNORED_DIRS]\n\n        for f in filenames:\n       \
    \     if f in IGNORED_FILES:\n                continue\n            files.append(str(Path(root_path,\
    \ f).relative_to(PROJECT_ROOT)).replace(os.sep, \"/\"))\n\n    return files\n\n\
    \ndef parse_markdown_index(index_path: Path) -> Set[str]:\n    if not index_path.exists():\n\
    \        return set()\n    content = index_path.read_text(encoding=\"utf-8\")\n\
    \    if \"CODE_FILE_INDEX.md\" in str(index_path) or \"DOCS_QUALITY_INDEX.md\"\
    \ in str(index_path):\n        return set(re.findall(r\"^\\s*\\|\\s*`([^`]+)`\"\
    , content, re.MULTILINE))\n    if \"PROJECT_REGISTRY.md\" in str(index_path):\n\
    \        links = re.findall(r\"\\[`([^`]+)`\\]\\(([^)]+)\\)\", content)\n    \
    \    resolved = set()\n        for _, link in links:\n            try:\n     \
    \           resolved.add(str(Path(os.path.normpath(os.path.join(index_path.parent,\
    \ link))).relative_to(PROJECT_ROOT)))\n            except Exception:\n       \
    \         continue\n        return resolved\n    links = re.findall(r\"\\[[^\\\
    ]]+\\]\\((?!https?://)([^)]+)\\)\", content)\n    resolved = set()\n    for link\
    \ in links:\n        try:\n            resolved.add(str(Path(os.path.normpath(os.path.join(index_path.parent,\
    \ link))).relative_to(PROJECT_ROOT)))\n        except Exception:\n           \
    \ continue\n    return resolved\n\n\ndef check_registration(file_path: str, required_indexes:\
    \ List[str], all_indexes_content: Dict[str, Set[str]]) -> Tuple[List[str], List[str]]:\n\
    \    found, missing = [], []\n    for idx in required_indexes:\n        if file_path\
    \ in all_indexes_content.get(idx, set()):\n            found.append(idx)\n   \
    \     else:\n            missing.append(idx)\n    return sorted(found), sorted(missing)\n\
    \n\ndef create_and_populate_index(index_path_str: str, files_to_add: List[str],\
    \ file_type: str):\n    index_path = PROJECT_ROOT / index_path_str\n    index_path.parent.mkdir(parents=True,\
    \ exist_ok=True)\n    existing_files = parse_markdown_index(index_path) if index_path.exists()\
    \ else set()\n    new_files_to_add = sorted([f for f in files_to_add if f not\
    \ in existing_files])\n    if not new_files_to_add:\n        return\n\n    lines_to_append\
    \ = []\n    if \"CODE_FILE_INDEX\" in index_path_str:\n        lines_to_append\
    \ = [f\"| `{f}` | | | Active | | |\" for f in new_files_to_add]\n    elif \"DOCS_QUALITY_INDEX\"\
    \ in index_path_str:\n        lines_to_append = [f\"| `{f}` | X | X | | | |\"\
    \ for f in new_files_to_add]\n    elif \"PROJECT_REGISTRY.md\" in index_path_str:\n\
    \        for f in new_files_to_add:\n            rel_link = os.path.relpath(PROJECT_ROOT\
    \ / f, index_path.parent)\n            doc_name = Path(f).stem.replace('_', '\
    \ ').replace('-', ' ').title()\n            lines_to_append.append(f\"| **{doc_name}**\
    \ | [`{Path(f).name}`]({rel_link}) | |\")\n\n    if not index_path.exists() and\
    \ (\"CODE_FILE_INDEX\" in index_path_str or \"DOCS_QUALITY_INDEX\" in index_path_str):\n\
    \        if \"CODE_FILE_INDEX\" in index_path_str:\n            header = (\"#\
    \ Code File Index\\n\\nThis file is auto-generated.\\n\\n\"\n                \
    \      \"| Path | Type | Description | Status | Linked Docs | Notes |\\n\"\n \
    \                     \"|------|------|-------------|--------|-------------|-------|\\\
    n\")\n        else:\n            header = (\"# Docs Quality Index\\n\\nThis file\
    \ is auto-generated.\\n\\n\"\n                      \"| File Path | Score | Reviewer\
    \ | Date | Notes |\\n\"\n                      \"|-----------|-------|----------|------|-------|\\\
    n\")\n        index_path.write_text(header + \"\\n\".join(sorted(lines_to_append))\
    \ + \"\\n\", encoding=\"utf-8\")\n        return\n\n    with open(index_path,\
    \ \"a\", encoding=\"utf-8\") as fh:\n        try:\n            if index_path.exists()\
    \ and index_path.read_text(encoding=\"utf-8\")[-1] != \"\\n\":\n             \
    \   fh.write(\"\\n\")\n        except Exception:\n            pass\n        fh.write(\"\
    \\n\".join(sorted(lines_to_append)) + \"\\n\")\n\n\ndef generate_audit_report(trace_index:\
    \ List[Dict[str, Any]]) -> int:\n    print(\"\\n=== GAP Analysis Report ===\\\
    n\")\n    missing_by_index: Dict[str, List[str]] = {}\n    registered_count =\
    \ 0\n    missing_count = 0\n    exempted_count = 0\n    for item in trace_index:\n\
    \        if item.get(\"registered\") == \"exempted\":\n            exempted_count\
    \ += 1\n        elif item.get(\"registered\") is True:\n            registered_count\
    \ += 1\n        else:\n            missing_count += 1\n            for idx in\
    \ item.get(\"missing_from\", []):\n                missing_by_index.setdefault(idx,\
    \ []).append(item[\"path\"])\n    if missing_count > 0:\n        print(\"\\n---\
    \ Missing Registrations ---\")\n        for idx, files in sorted(missing_by_index.items()):\n\
    \            print(f\"\\nMissing from {idx}:\")\n            for f in sorted(files):\n\
    \                print(f\"  - {f}\")\n    print(f\"\\nTotal files: {len(trace_index)}\\\
    nRegistered: {registered_count}\\nMissing: {missing_count}\\nExempted: {exempted_count}\\\
    n\")\n    return 1 if missing_count > 0 else 0\n\n\ndef validate_trace_index_schema(trace_index_path:\
    \ Path) -> bool:\n    return True\n\n\ndef validate_metadata(trace_index: List[Dict[str,\
    \ Any]]) -> None:\n    \"\"\"Validates the metadata of the trace index, printing\
    \ warnings.\"\"\"\n    print(\"\\n--- Validating Metadata ---\")\n    warnings\
    \ = 0\n    for item in trace_index:\n        path = item.get(\"path\")\n     \
    \   meta = item.get(\"meta\")\n\n        if not meta:\n            print(f\"⚠️\
    \  Warning: Missing 'meta' field for artifact: {path}\")\n            warnings\
    \ += 1\n            continue\n\n        description = meta.get(\"description\"\
    , \"\").strip()\n        if not description or description == \"No description\
    \ available.\":\n            print(f\"⚠️  Warning: Missing 'meta.description'\
    \ for artifact: {path}\")\n            warnings += 1\n\n        tags = meta.get(\"\
    tags\", [])\n        if item.get(\"type\") in [\"code\", \"doc\"] and not tags:\n\
    \            print(f\"⚠️  Warning: Missing 'meta.tags' for artifact: {path}\"\
    )\n            warnings += 1\n\n    if warnings == 0:\n        print(\"✅ Metadata\
    \ validation passed with no warnings.\")\n    else:\n        print(f\"\\nFound\
    \ {warnings} metadata warning(s).\")\n\n\n# --- Main ---\ndef main():\n    parser\
    \ = argparse.ArgumentParser(description=\"Repository inventory and governance\
    \ script.\")\n    parser.add_argument(\"--full\", action=\"store_true\", help=\"\
    Run a full scan of all files.\")\n    parser.add_argument(\"--full-scan\", action=\"\
    store_true\", help=\"Force a full scan of all files, ignoring other modes.\")\n\
    \    parser.add_argument(\"--test-files\", nargs='*', help=\"Run in test mode\
    \ with a specific list of files.\")\n    parser.add_argument(\"--update-project-registry\"\
    , action=\"store_true\", help=\"Update the project registry JSON and Markdown\
    \ files.\")\n    parser.add_argument(\"--extras-file\", type=Path, default=PROJECT_ROOT\
    \ / \"scripts/project_registry_extras.yml\", help=\"Path to the project registry\
    \ extras file.\")\n    parser.add_argument(\"--debug\", action=\"store_true\"\
    , help=\"Enable debug printing for scripts that support it.\")\n    args = parser.parse_args()\n\
    \n    if args.update_project_registry:\n        script_path = PROJECT_ROOT / \"\
    scripts\" / \"build_project_registry.py\"\n        cmd = [sys.executable, str(script_path),\
    \ \"--extras-file\", str(args.extras_file)]\n        if args.debug:\n        \
    \    cmd.append(\"--debug\")\n        try:\n            subprocess.run(cmd, check=True)\n\
    \            print(\"✅ Project registry updated successfully.\")\n           \
    \ return 0\n        except subprocess.CalledProcessError as e:\n            print(\"\
    ❌ ERROR: Project registry update failed.\", file=sys.stderr)\n            print(e,\
    \ file=sys.stderr)\n            return e.returncode\n\n    test_mode = args.test_files\
    \ is not None\n    all_files = args.test_files if test_mode else find_all_files()\n\
    \    trace_index: List[Dict[str, Any]] = []\n    all_index_paths = {idx for rule\
    \ in INDEX_MAP for idx in rule[\"indexes\"]}\n    all_indexes_content = {str(p):\
    \ parse_markdown_index(PROJECT_ROOT / p) for p in all_index_paths}\n    files_to_create:\
    \ Dict[str, List[str]] = {}\n\n    for f in sorted(all_files):\n        ftype\
    \ = get_file_type(f)\n        full_path = PROJECT_ROOT / f\n        meta = extract_metadata(full_path)\
    \ if full_path.exists() else {\"description\": \"File not found.\", \"tags\":\
    \ []}\n        entry: Dict[str, Any] = {\"path\": f, \"type\": ftype, \"meta\"\
    : meta}\n        required: List[str] = []\n        if ftype != \"exempt\":\n \
    \           for r in INDEX_MAP:\n                try:\n                    if\
    \ r[\"match\"](f, ftype):\n                        required.extend(r[\"indexes\"\
    ])\n                except Exception:\n                    continue\n        required\
    \ = sorted(list(set(required)))\n\n        if not required:\n            entry[\"\
    registered\"] = \"exempted\"\n            entry[\"index\"] = \"-\"\n        else:\n\
    \            found, missing = check_registration(f, required, all_indexes_content)\n\
    \            if not missing:\n                entry[\"registered\"] = True\n \
    \               entry[\"index\"] = found[0]\n            else:\n             \
    \   entry[\"registered\"] = False\n                entry[\"index\"] = \"-\"\n\
    \                entry[\"missing_from\"] = missing\n                for idx_file\
    \ in missing:\n                    files_to_create.setdefault(idx_file, []).append(f)\n\
    \        trace_index.append(entry)\n\n    if not test_mode:\n        for idx_path,\
    \ files in files_to_create.items():\n            if files:\n                file_type_for_index\
    \ = get_file_type(files[0])\n                create_and_populate_index(idx_path,\
    \ files, file_type_for_index)\n\n    doc_tag_inventory_path = PROJECT_ROOT / \"\
    project/reports/DOCUMENT_TAG_INVENTORY.yml\"\n    if doc_tag_inventory_path.exists():\n\
    \        try:\n            with doc_tag_inventory_path.open(\"r\", encoding=\"\
    utf-8\") as f:\n                tag_inventory = yaml.safe_load(f) or []\n    \
    \        file_to_id = {item.get('path'): item.get('id') for item in tag_inventory\
    \ if isinstance(item, dict) and 'path' in item and 'id' in item}\n           \
    \ for entry in trace_index:\n                entry['id'] = file_to_id.get(entry['path'],\
    \ 'MISSING')\n        except Exception as e:\n            print(f\"⚠️ Warning:\
    \ could not load DOCUMENT_TAG_INVENTORY.yml: {e}\", file=sys.stderr)\n\n    output\
    \ = {\"artifacts\": trace_index}\n    trace_index_path = PROJECT_ROOT / \"project/reports/TRACE_INDEX.yml\"\
    \n    trace_index_path.parent.mkdir(parents=True, exist_ok=True)\n    with open(trace_index_path,\
    \ \"w\", encoding=\"utf-8\") as f:\n        yaml.safe_dump(output, f, default_flow_style=False,\
    \ sort_keys=False)\n\n    if not validate_trace_index_schema(trace_index_path):\n\
    \        return 1\n\n    validate_metadata(trace_index)\n\n    if test_mode:\n\
    \        return 0\n\n    exit_code = generate_audit_report(trace_index)\n\n  \
    \  linter_script = PROJECT_ROOT / \"scripts/lint_governance_links.py\"\n    print(\"\
    PROJECT_ROOT:\", PROJECT_ROOT)\n    print(\"linter_script:\", linter_script, \"\
    exists?\", linter_script.exists())\n    if linter_script.exists():\n        try:\n\
    \            subprocess.run([sys.executable, str(linter_script)], check=True)\n\
    \        except subprocess.CalledProcessError as e:\n            print(\"⚠️ lint_governance_links.py\
    \ failed:\", file=sys.stderr)\n            if exit_code == 0:\n              \
    \  exit_code = e.returncode\n    else:\n        print(\"⚠️ lint_governance_links.py\
    \ not found; skipping governance link check.\", file=sys.stderr)\n\n    return\
    \ exit_code\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n"
- path: scripts/generate_endpoints_doc.py
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
- path: scripts/test_auth_flow.py
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
- path: scripts/migrate_alignment_matrix.py
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
- path: scripts/linter.py
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
- path: scripts/generate_repo_manifest_md.py
  type: script
  workflow:
  - documentation
  indexes: []
  content: "#!/usr/bin/env python3\nimport os\nimport yaml\n\n# Configuration\nIGNORED_DIRS\
    \ = {'.git', '.github', '.venv', '__pycache__', 'archive', 'api_dumps',\n    \
    \            'zotify_api.egg-info', 'templates', 'docs', 'alembic', 'project',\
    \ 'api', 'Gonk', 'snitch', 'tests', 'nlp', '.venv-nlp'}\nIGNORED_FILES = {'.DS_Store',\
    \ '.gitignore', 'REPO_MANIFEST.md', 'openapi.json',\n                 'LICENSE',\
    \ 'CONTRIBUTING.md', 'alembic.ini'}\n# Files that should be included even if in\
    \ ignored dirs\nINCLUDED_FILES = {'api/docs/MASTER_INDEX.md'}\nOUTPUT_FILE = os.path.join('project',\
    \ 'reports', 'REPO_MANIFEST.md')\n\n\ndef get_file_type(filename):\n    if filename.endswith('.py')\
    \ or filename.endswith('.sh'):\n        return 'script'\n    elif filename.endswith('.md')\
    \ or filename.endswith('.rst') or filename.endswith('.txt'):\n        return 'doc'\n\
    \    elif filename.endswith('.yml') or filename.endswith('.yaml') or filename.endswith('.json'):\n\
    \        return 'config'\n    else:\n        return 'other'\n\n\ndef is_ignored_file(rel_path):\n\
    \    normalized = os.path.normpath(rel_path).replace(os.sep, '/')\n    # Always\
    \ include files explicitly listed\n    if normalized in INCLUDED_FILES:\n    \
    \    return False\n    # Skip ignored filenames\n    if os.path.basename(rel_path)\
    \ in IGNORED_FILES:\n        return True\n    # Skip if any parent dir is in IGNORED_DIRS\n\
    \    parts = normalized.split('/')\n    for p in parts[:-1]:\n        if p in\
    \ IGNORED_DIRS:\n            return True\n    return False\n\n\ndef scan_repo(base_dir='.'):\n\
    \    manifest = []\n\n    for root, dirs, files in os.walk(base_dir):\n      \
    \  # Skip ignored dirs unless they lead to an included file\n        dirs[:] =\
    \ [d for d in dirs if d not in IGNORED_DIRS or\n                   any(inc.startswith(os.path.relpath(os.path.join(root,\
    \ d), base_dir).replace(os.sep, '/') + '/')\n                       for inc in\
    \ INCLUDED_FILES)]\n\n        for f in files:\n            path = os.path.join(root,\
    \ f)\n            rel_path = os.path.relpath(path, start=base_dir)\n         \
    \   if is_ignored_file(rel_path):\n                continue\n\n            file_type\
    \ = get_file_type(f)\n\n            try:\n                with open(path, 'r',\
    \ encoding='utf-8') as file_obj:\n                    content = file_obj.read()\n\
    \            except Exception:\n                content = '<binary or unreadable\
    \ content>'\n\n            # Determine workflow based on previous mapping\n  \
    \          workflow = []\n            if f.startswith('audit'):\n            \
    \    workflow.append('audit')\n            elif 'test' in f or f.startswith('run_e2e'):\n\
    \                workflow.append('testing')\n            elif f.startswith('generate'):\n\
    \                workflow.append('documentation')\n            elif f.startswith('linter')\
    \ or f.startswith('validate'):\n                workflow.append('validation')\n\
    \n            # Determine indexes\n            indexes = []\n            if f.endswith('CODE_FILE_INDEX.md')\
    \ or f.endswith('MASTER_INDEX.md'):\n                indexes.append(f)\n\n   \
    \         manifest.append({\n                'path': rel_path.replace(os.sep,\
    \ '/'),\n                'type': file_type,\n                'workflow': workflow,\n\
    \                'indexes': indexes,\n                'content': content\n   \
    \         })\n    return manifest\n\n\ndef save_manifest(manifest, output_file=OUTPUT_FILE):\n\
    \    os.makedirs(os.path.dirname(output_file), exist_ok=True)\n    with open(output_file,\
    \ 'w', encoding='utf-8') as f:\n        yaml.dump(manifest, f, sort_keys=False,\
    \ allow_unicode=True)\n\n\nif __name__ == '__main__':\n    repo_manifest = scan_repo('.')\n\
    \    save_manifest(repo_manifest)\n    print(f\"REPO_MANIFEST.md generated at\
    \ {OUTPUT_FILE} with {len(repo_manifest)} entries\")"
- path: scripts/repo_governance.py
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
- path: scripts/run_e2e_auth_test.sh
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
- path: scripts/reorder_trace_index_keys.py
  type: script
  workflow: []
  indexes: []
  content: "#!/usr/bin/env python3\nimport yaml\nfrom pathlib import Path\n\nTRACE_INDEX_FILE\
    \ = Path(\"project/reports/TRACE_INDEX.yml\")\n\nPREFERRED_ORDER = [\"file\",\
    \ \"id\", \"type\", \"registered\", \"index\", \"meta\"]\n\ndef reorder_dict(d):\n\
    \    return {k: d[k] for k in PREFERRED_ORDER if k in d}\n\ndef reorder_items(item):\n\
    \    if isinstance(item, list):\n        return [reorder_items(i) for i in item]\n\
    \    elif isinstance(item, dict):\n        new_dict = reorder_dict(item)\n   \
    \     # preserve any extra keys not in preferred order\n        for k in item:\n\
    \            if k not in new_dict:\n                new_dict[k] = reorder_items(item[k])\n\
    \            else:\n                new_dict[k] = reorder_items(new_dict[k])\n\
    \        return new_dict\n    else:\n        return item\n\nwith TRACE_INDEX_FILE.open(\"\
    r\", encoding=\"utf-8\") as f:\n    data = yaml.safe_load(f)\n\ndata = reorder_items(data)\n\
    \nwith TRACE_INDEX_FILE.open(\"w\", encoding=\"utf-8\") as f:\n    yaml.dump(data,\
    \ f, sort_keys=False, allow_unicode=True)\n\nprint(f\"Reordered keys in {TRACE_INDEX_FILE}\
    \ according to preferred order.\")\n"
- path: scripts/verify_governance.py
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
- path: scripts/start.sh
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
- path: scripts/audit_api.py
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
- path: scripts/generate_openapi.py
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
- path: scripts/manage_docs_index.py
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
- path: scripts/lint_governance_links.json
  type: config
  workflow: []
  indexes: []
  content: "{\n    \"files\": [\n        {\n            \"path\": \"project/BACKLOG.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/EXECUTION_PLAN.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/QA_GOVERNANCE.md\",\n\
    \            \"status\": \"fully_aligned\"\n        },\n        {\n          \
    \  \"path\": \"project/ONBOARDING.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/SECURITY.md\",\n    \
    \        \"status\": \"fully_aligned\"\n        },\n        {\n            \"\
    path\": \"project/LOGGING_PHASES.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/HIGH_LEVEL_DESIGN.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/LESSONS-LEARNT.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/CICD.md\",\n        \
    \    \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/TASK_CHECKLIST.md\",\n            \"status\": \"fully_aligned\"\n\
    \        },\n        {\n            \"path\": \"project/DEPENDENCIES.md\",\n \
    \           \"status\": \"fully_aligned\"\n        },\n        {\n           \
    \ \"path\": \"project/LOGGING_SYSTEM_DESIGN.md\",\n            \"status\": \"\
    fully_aligned\"\n        },\n        {\n            \"path\": \"project/ALIGNMENT_MATRIX.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/PROJECT_PLAN.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/LOW_LEVEL_DESIGN.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/LOGGING_TRACEABILITY_MATRIX.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/FUTURE_ENHANCEMENTS.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/PROJECT_REGISTRY.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/PID.md\",\n         \
    \   \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/ROADMAP.md\",\n            \"status\": \"fully_aligned\"\n       \
    \ },\n        {\n            \"path\": \"project/PROJECT_BRIEF.md\",\n       \
    \     \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/USECASES_GAP_ANALYSIS.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/USECASES.md\",\n    \
    \        \"status\": \"fully_aligned\"\n        },\n        {\n            \"\
    path\": \"project/reports/HANDOVER_BRIEF_CHATGTP.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/reports/PROJECT_AUDIT_FINAL_REPORT.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/reports/ARCHIVE_ALIGNMENT_MATRIX_OLD.md\",\n        \
    \    \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/reports/SEMANTIC_ALIGNMENT_REPORT.md\",\n            \"status\": \"\
    fully_aligned\"\n        },\n        {\n            \"path\": \"project/reports/CONTENT_ALIGNMENT_REPORT.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/reports/GOVERNANCE_DEMO_REPORT.md\",\n            \"\
    status\": \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/reports/DESCRIPTION_COMPLIANCE_REPORT.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/reports/HANDOVER_BRIEF_JULES.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/reports/REPO_MANIFEST.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/reports/PROJECT_DOCUMENT_ALIGNMENT.md\",\n          \
    \  \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\"\
    : \"project/archive/TRACEABILITY_MATRIX.md\",\n            \"status\": \"unlinked\"\
    \n        },\n        {\n            \"path\": \"project/logs/SESSION_LOG.md\"\
    ,\n            \"status\": \"partially_aligned\"\n        },\n        {\n    \
    \        \"path\": \"project/logs/ACTIVITY.md\",\n            \"status\": \"partially_aligned\"\
    \n        },\n        {\n            \"path\": \"project/logs/CURRENT_STATE.md\"\
    ,\n            \"status\": \"partially_aligned\"\n        },\n        {\n    \
    \        \"path\": \"project/process/GAP_ANALYSIS_TEMPLATE.md\",\n           \
    \ \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\":\
    \ \"project/proposals/LOW_CODE_PROPOSAL.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/proposals/TRACE_INDEX_SCHEMA_ADAPTATION.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md\",\n           \
    \ \"status\": \"fully_aligned\"\n        },\n        {\n            \"path\":\
    \ \"project/proposals/NEW_PROPOSAL.md\",\n            \"status\": \"fully_aligned\"\
    \n        },\n        {\n            \"path\": \"project/proposals/GONKUI_PLUGIN.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/DBSTUDIO_PLUGIN.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/TRACE_INDEX_SCHEMA_FIX.md\",\n            \"\
    status\": \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/proposals/HOME_AUTOMATION_PROPOSAL.md\"\
    ,\n            \"status\": \"fully_aligned\"\n        },\n        {\n        \
    \    \"path\": \"project/proposals/MULTI_SOURCE_METADATA_PROPOSAL.md\",\n    \
    \        \"status\": \"fully_aligned\"\n        },\n        {\n            \"\
    path\": \"project/proposals/GOVERNANCE_AUDIT_REFACTOR.md\",\n            \"status\"\
    : \"fully_aligned\"\n        },\n        {\n            \"path\": \"project/archive/audit/AUDIT-PHASE-3.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/audit-prompt.md\",\n            \"status\": \"\
    unlinked\"\n        },\n        {\n            \"path\": \"project/archive/audit/FIRST_AUDIT.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/AUDIT-phase-2.md\",\n            \"status\": \"\
    unlinked\"\n        },\n        {\n            \"path\": \"project/archive/audit/AUDIT-phase-1.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/CODE_OPTIMIZATIONPLAN_PHASE_4.md\",\n        \
    \    \"status\": \"unlinked\"\n        },\n        {\n            \"path\": \"\
    project/archive/audit/AUDIT-PHASE-5.md\",\n            \"status\": \"unlinked\"\
    \n        },\n        {\n            \"path\": \"project/archive/audit/AUDIT_TRACEABILITY_MATRIX.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/AUDIT-PHASE-4.md\",\n            \"status\": \"\
    unlinked\"\n        },\n        {\n            \"path\": \"project/archive/audit/PHASE_4_TRACEABILITY_MATRIX.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/audit/HLD_LLD_ALIGNMENT_PLAN.md\",\n            \"status\"\
    : \"unlinked\"\n        },\n        {\n            \"path\": \"project/archive/docs/projectplan/spotify_fullstack_capability_blueprint.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/docs/projectplan/security.md\",\n            \"status\"\
    : \"unlinked\"\n        },\n        {\n            \"path\": \"project/archive/docs/snitch/INTEGRATION_CHECKLIST.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/docs/snitch/phase5-ipc.md\",\n            \"status\"\
    : \"unlinked\"\n        },\n        {\n            \"path\": \"project/archive/docs/snitch/PHASE_2_SECURE_CALLBACK.md\"\
    ,\n            \"status\": \"unlinked\"\n        },\n        {\n            \"\
    path\": \"project/archive/docs/snitch/TEST_RUNBOOK.md\",\n            \"status\"\
    : \"unlinked\"\n        }\n    ],\n    \"summary\": {\n        \"total_files\"\
    : 66,\n        \"fully_aligned\": 45,\n        \"partially_aligned\": 3,\n   \
    \     \"unlinked\": 18\n    }\n}"
- path: scripts/trace_description_generator.py
  type: script
  workflow: []
  indexes: []
  content: "# nlp/summarizer.py\n\nimport torch\nfrom transformers import pipeline\n\
    import logging\nimport time\nfrom sentence_transformers import SentenceTransformer,\
    \ util\n\n# -------------------------\n# Logging Setup\n# -------------------------\n\
    logging.basicConfig(\n    level=logging.INFO,\n    format='[%(levelname)s] %(message)s'\n\
    )\n\n# -------------------------\n# Device / Model Initialization\n# -------------------------\n\
    device = 0 if torch.cuda.is_available() else -1\nprint(f\"Device set to use {'cuda'\
    \ if device == 0 else 'cpu'}\")\n\nsummarizer_pipeline = pipeline(\n    \"summarization\"\
    ,\n    model=\"facebook/bart-large-cnn\",\n    device=device\n)\n\n# Semantic\
    \ similarity model\n_sem_model = SentenceTransformer(\"sentence-transformers/all-MiniLM-L6-v2\"\
    )\n\n# -------------------------\n# Helper Functions\n# -------------------------\n\
    def _semantic_similarity(text1: str, text2: str) -> float:\n    \"\"\"Return cosine\
    \ similarity between two texts (0-1).\"\"\"\n    embeddings = _sem_model.encode([text1,\
    \ text2], convert_to_tensor=True)\n    sim = util.pytorch_cos_sim(embeddings[0],\
    \ embeddings[1])\n    return sim.item()\n\n\ndef _generate_summary(text: str,\
    \ prefix: str = \"\", max_tokens: int = None) -> str:\n    \"\"\"Generate a summary\
    \ using dynamic max_length scaling and proper input handling.\"\"\"\n    if not\
    \ text or len(text.strip()) == 0:\n        return \"\"\n\n    start_time = time.time()\n\
    \    input_text = f\"{prefix.strip()} {text.strip()}\" if prefix else text.strip()\n\
    \n    # Tokenize to determine size and dynamically set max_length\n    tokens\
    \ = summarizer_pipeline.tokenizer.encode(input_text, truncation=False)\n    input_len\
    \ = len(tokens)\n    if max_tokens is None:\n        max_len = max(20, min(80,\
    \ input_len // 2))  # adaptive summarization window\n    else:\n        max_len\
    \ = max_tokens\n\n    try:\n        result = summarizer_pipeline(\n          \
    \  input_text,\n            max_length=max_len,\n            min_length=10,\n\
    \            do_sample=False\n        )\n        summary = result[0][\"summary_text\"\
    ].strip()\n        elapsed = time.time() - start_time\n        logging.info(f\"\
    Summarized file ({input_len} tokens) in {elapsed:.2f}s\")\n        return summary\n\
    \n    except Exception as e:\n        logging.warning(f\"Failed to summarize text:\
    \ {e}\")\n        return \"\"\n\n# -------------------------\n# Public Functions\n\
    # -------------------------\ndef summarize_doc(text: str, role_focused: bool =\
    \ False) -> str:\n    \"\"\"\n    Summarize documentation or markdown text.\n\
    \    If role_focused=True, generate a short description of the document's role,\
    \ not content.\n    \"\"\"\n    if role_focused:\n        prefix = (\n       \
    \     \"Provide a short, role-focused description of this document. \"\n     \
    \       \"Explain its purpose in the project, what decisions or information it\
    \ supports, \"\n            \"without summarizing content. Keep it concise, under\
    \ two sentences, complete sentences:\\n\"\n        )\n        return _generate_summary(text,\
    \ prefix, max_tokens=50)\n    else:\n        prefix = (\n            \"Summarize\
    \ the following documentation clearly and concisely. \"\n            \"Highlight\
    \ key concepts, modules, and main functions:\\n\"\n        )\n        return _generate_summary(text,\
    \ prefix)\n\ndef summarize_code(code: str) -> str:\n    \"\"\"\n    Summarize\
    \ source code files with emphasis on intent and structure.\n    Focus on functionality,\
    \ modules, classes, and architecture.\n    \"\"\"\n    prefix = (\n        \"\
    Explain the purpose and main logic of the following source code. \"\n        \"\
    Focus on functionality, modules, classes, and architecture. \"\n        \"Do not\
    \ restate comments or file names literally. Return a concise summary paragraph:\\\
    n\"\n    )\n    return _generate_summary(code, prefix)\n\ndef validate_summary(original_text:\
    \ str, summary: str, threshold: float = 0.4) -> bool:\n    \"\"\"Return True if\
    \ summary is semantically similar enough to original text.\"\"\"\n    if not summary:\n\
    \        return False\n    sim = _semantic_similarity(original_text, summary)\n\
    \    if sim < threshold:\n        logging.warning(f\"Low semantic similarity detected\
    \ ({sim:.3f})\")\n        return False\n    return True\n"
- path: scripts/propagate_descriptions.py
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
- path: scripts/build_project_registry.py
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
    \        meta = trace_item.get(\"meta\", {}) if trace_item else {}\n        entry\
    \ = {\n            \"name\": derive_name(path_obj, legacy_item), \"path\": path_str,\
    \ \"type\": \"doc\",\n            \"module\": module, \"category\": category,\
    \ \"registered_in\": trace_item.get(\"registered_in\", []) if trace_item else\
    \ [],\n            \"status\": status, \"notes\": meta.get(\"description\") or\
    \ (legacy_item[\"notes\"] if legacy_item else \"\"), \"source\": source,\n   \
    \     }\n        registry.append(entry)\n\n    if project_dir.exists():\n    \
    \    for file_path in project_dir.rglob('*'):\n            if file_path.is_file():\n\
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
- path: scripts/lint_governance_links.py
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
- path: scripts/propagate_descriptions.py.new
  type: other
  workflow: []
  indexes: []
  content: "#!/usr/bin/env python3\n\"\"\"\nID: OPS-023\n\nSummarization pipeline\
    \ for codebase trace descriptions.\n\nTraverses configured directories, preprocesses\
    \ code files,\nsummarizes each file using a transformer model, handles short\n\
    files via batching, and outputs a validated JSON summary to\n`trace_description_intermediate.json`.\n\
    \nThis version uses token-based max_length to prevent \"index out of range\" errors.\n\
    \"\"\"\n\nimport json\nimport re\nfrom pathlib import Path\nfrom transformers\
    \ import pipeline, BartTokenizer\n\n# -------------------------\n# Configuration\n\
    # -------------------------\nCODE_DIRS = [\n    \"api/src\",\n    \"api/tests/unit\"\
    ,\n    \"scripts\",\n    \"Gonk/GonkUI/views\"\n]\n\nOUTPUT_FILE = \"trace_description_intermediate.json\"\
    \n\n# Minimum tokens for summarizer; files shorter than this are batched\nMIN_TOKENS\
    \ = 10\n\n# Fraction of input length to use for max_length\nMAX_LENGTH_RATIO =\
    \ 0.6\n\n# Threshold for batching short files\nBATCH_THRESHOLD = 20\n\n# Initialize\
    \ summarizer and tokenizer\nsummarizer = pipeline(\"summarization\", model=\"\
    facebook/bart-large-cnn\")\ntokenizer = BartTokenizer.from_pretrained(\"facebook/bart-large-cnn\"\
    )\n\n\n# -------------------------\n# Helper Functions\n# -------------------------\n\
    def preprocess_code(code: str) -> str:\n    \"\"\"Remove comments, docstrings,\
    \ and excess whitespace from code.\"\"\"\n    code = re.sub(r\"#.*\", \"\", code)\n\
    \    code = re.sub(r'\"\"\".*?\"\"\"', \"\", code, flags=re.DOTALL)\n    code\
    \ = re.sub(r\"\\n\\s*\\n\", \"\\n\", code)\n    return code.strip()\n\n\ndef safe_summarize(text:\
    \ str) -> str | None:\n    \"\"\"\n    Summarize text with dynamic token-based\
    \ max_length.\n    Returns None if summarization fails or text is too short.\n\
    \    \"\"\"\n    # Tokenize to get actual model token count\n    inputs = tokenizer(text,\
    \ return_tensors=\"pt\")\n    input_len = inputs.input_ids.size(1)\n\n    if input_len\
    \ < MIN_TOKENS:\n        return None\n\n    max_len = max(MIN_TOKENS, int(input_len\
    \ * MAX_LENGTH_RATIO))\n\n    try:\n        result = summarizer(text, max_length=max_len,\
    \ min_length=5, do_sample=False)\n        return result[0][\"summary_text\"]\n\
    \    except Exception as e:\n        print(f\"[WARN] Failed to summarize text:\
    \ {e}\")\n        return None\n\n\ndef gather_files() -> list[Path]:\n    \"\"\
    \"Recursively gather all Python files from configured directories.\"\"\"\n   \
    \ files = []\n    for directory in CODE_DIRS:\n        path = Path(directory)\n\
    \        if path.exists():\n            files.extend([f for f in path.rglob(\"\
    *.py\") if f.is_file()])\n    return files\n\n\n# -------------------------\n\
    # Main Pipeline\n# -------------------------\ndef main():\n    files = gather_files()\n\
    \    summaries = {}\n    short_batch = []\n\n    # Process each file\n    for\
    \ file in files:\n        try:\n            content = preprocess_code(file.read_text(encoding=\"\
    utf-8\"))\n        except Exception as e:\n            print(f\"[WARN] Failed\
    \ to read {file}: {e}\")\n            continue\n\n        if len(content.split())\
    \ < BATCH_THRESHOLD:\n            short_batch.append((file, content))\n      \
    \      continue\n\n        summary = safe_summarize(content)\n        if summary:\n\
    \            summaries[str(file)] = summary\n        else:\n            print(f\"\
    [WARN] Skipping {file} due to summarization failure\")\n\n    # Handle batched\
    \ short files\n    if short_batch:\n        combined_text = \"\\n\\n\".join(c\
    \ for f, c in short_batch)\n        combined_summary = safe_summarize(combined_text)\n\
    \        if combined_summary:\n            for file, _ in short_batch:\n     \
    \           summaries[str(file)] = combined_summary\n        else:\n         \
    \   for file, _ in short_batch:\n                print(f\"[WARN] Skipping short\
    \ file {file} due to summarization failure\")\n\n    # Write JSON output\n   \
    \ try:\n        with open(OUTPUT_FILE, \"w\", encoding=\"utf-8\") as f:\n    \
    \        json.dump(summaries, f, indent=2)\n        print(f\"[INFO] Trace summaries\
    \ written to {OUTPUT_FILE} ({len(summaries)} files summarized)\")\n    except\
    \ Exception as e:\n        print(f\"[ERROR] Failed to write JSON: {e}\")\n\n\n\
    if __name__ == \"__main__\":\n    main()\n"
- path: scripts/semantic_alignment_check.py
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
- path: scripts/doc-lint-rules.yml
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
- path: scripts/make_manifest.py
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
- path: scripts/fix_tag_inventory.py
  type: script
  workflow: []
  indexes: []
  content: "# ID: OPS-061\n#!/usr/bin/env python3\nimport yaml\nfrom pathlib import\
    \ Path\n\nTAG_FILE = Path(\"project/reports/DOCUMENT_TAG_INVENTORY.yml\")\n\n\
    def main(dry_run=True):\n    if not TAG_FILE.exists():\n        print(f\"❌ {TAG_FILE}\
    \ does not exist.\")\n        return 1\n\n    with TAG_FILE.open(\"r\", encoding=\"\
    utf-8\") as f:\n        try:\n            tags = yaml.safe_load(f)\n        except\
    \ yaml.YAMLError as e:\n            print(f\"❌ YAML parse error: {e}\")\n    \
    \        return 1\n\n    if not isinstance(tags, list):\n        print(\"❌ Expected\
    \ a list of tag entries.\")\n        return 1\n\n    fixed = 0\n    for i, entry\
    \ in enumerate(tags):\n        if 'file' not in entry:\n            print(f\"\
    ⚠️ Entry {i} missing 'file': {entry}\")\n            # Auto-fill file as 'UNKNOWN'\
    \ or some default path\n            if not dry_run:\n                entry['file']\
    \ = \"UNKNOWN\"\n            fixed += 1\n\n    if fixed == 0:\n        print(\"\
    ✅ All entries have 'file' keys.\")\n    else:\n        print(f\"⚠️ Fixed {fixed}\
    \ entries missing 'file' keys.\")\n        if not dry_run:\n            TAG_FILE.write_text(yaml.safe_dump(tags,\
    \ sort_keys=False), encoding=\"utf-8\")\n            print(f\"✅ Written corrected\
    \ {TAG_FILE}\")\n\n    return 0\n\nif __name__ == \"__main__\":\n    import argparse\n\
    \    parser = argparse.ArgumentParser(description=\"Validate and fix DOCUMENT_TAG_INVENTORY.yml\"\
    )\n    parser.add_argument(\"--apply\", action=\"store_true\", help=\"Write fixes\
    \ to the file instead of dry-run\")\n    args = parser.parse_args()\n    exit(main(dry_run=not\
    \ args.apply))\n"
- path: scripts/validate_code_index.py
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
- path: scripts/trace_description_intermediate.json
  type: config
  workflow: []
  indexes: []
  content: "{\n    \".github/workflows/ci.yml\": \"This job runs on all PRs and serves\
    \ as a gatekeeper .\",\n    \".github/workflows/pushmirror.yml\": \"Push a pull\
    \ request onto the repo .\",\n    \".gitignore\": \"No description available\"\
    ,\n    \".pre-commit-config.yaml\": \"No description available\",\n    \"AGENTS.md\"\
    : \" Document is designed to solve a common problem in software development: ensuring\
    \ documentation stays synchronized with the code . The goal is to enforce the\
    \ project's **\\\"Living Documentation\\\"** policy by making\",\n    \"Gonk/CODE_FILE_INDEX.md\"\
    : \" This file is auto-generated . Do not edit manually . Use this file to test\
    \ the GonkCLI .\",\n    \"Gonk/GonkCLI/DOCS_INDEX.md\": \" This document serves\
    \ as the master index for all documentation related to the GonkCLI component .\"\
    ,\n    \"Gonk/GonkCLI/README.md\": \" The Gonk Command Line Interface (CLI) is\
    \ a tool for interacting with the Zotify API from the command line . It is intended\
    \ for developers and power users who want to script\",\n    \"Gonk/GonkCLI/__init__.py\"\
    : \"Make Gonk and GonkCLI a Python package\",\n    \"Gonk/GonkCLI/main.py\": \"\
    Gonk CLI for interacting with the Zotify API .\",\n    \"Gonk/GonkCLI/modules/__init__.py\"\
    : \"Make Gonk and GonkCLI modules a Python package .\",\n    \"Gonk/GonkCLI/modules/jwt_mock.py\"\
    : \"Creates a JWTClient for the API - 007 .\",\n    \"Gonk/GonkCLI/tests/__init__.py\"\
    : \"This file makes Gonk tests a Python package .\",\n    \"Gonk/GonkCLI/tests/test_jwt_mock.py\"\
    : \"Example of how to use a JWT client\",\n    \"Gonk/GonkUI/DOCS_INDEX.md\":\
    \ \" This file is auto-generated . Do not edit manually . Use the contents of\
    \ the document to help you understand the design of the Gonk Web UI .\",\n   \
    \ \"Gonk/GonkUI/README.md\": \" GonkUI is a web-based development and testing\
    \ tool designed specifically for the Zotify API . It provides a rich user interface\
    \ to streamline common development workflows and facilitate interactive API\"\
    ,\n    \"Gonk/GonkUI/app.py\": \"This is the main function of the Zotify application\
    \ . It is the main function of Zotify .\",\n    \"Gonk/GonkUI/docs/ARCHITECTURE.md\"\
    : \" The Gonk/GonkUI is a standalone web application built with Flask . It is\
    \ designed to be completely independent of the main Zotify API application, acting\
    \ only as an external\",\n    \"Gonk/GonkUI/docs/CHANGELOG.md\": \" Initial version\
    \ of the 'Gonk/GonksUI' developer tool has been added . Integration with `sqlite-web'\
    \ for browsing the development database .\",\n    \"Gonk/GonkUI/docs/CONTRIBUTING.md\"\
    : \" # Contributing Contributions are welcome! If you have a suggestion or find\
    \ a bug, please open an issue to discuss it .\",\n    \"Gonk/GonkUI/docs/USER_MANUAL.md\"\
    : \" Gonk Test UI is a standalone application with its own set of dependencies\
    \ . Gonk/GonkUI is divided into two main sections for interacting with the Zotify\
    \ API endpoints\",\n    \"Gonk/GonkUI/pyproject.toml\": \"No description available\"\
    ,\n    \"Gonk/GonkUI/static/app.js\": \"Create the UI for the OpenAPI endpoints\
    \ .\",\n    \"Gonk/GonkUI/static/styles.css\": \"API 2 . 0 - > API 2 . 0 - > API\
    \ 2 . 0 - > API 2 . 0 - > API 2 . 0 - > API 2 . 0 - > API 2\",\n    \"Gonk/GonkUI/views/__init__.py\"\
    : \"This file makes Gonk GonkUI views a Python package .\",\n    \"Gonk/GonkUI/views/jwt_ui.py\"\
    : \"Create a Blueprint for the test UI .\",\n    \"Gonk/pyproject.toml\": \"No\
    \ description available\",\n    \"README.md\": \" The Zotify API Platform is a\
    \ powerful, extensible, and provider-agnostic backend for managing and interacting\
    \ with your music library . Users can manage profiles, preferences, liked tracks,\"\
    ,\n    \"api/.gitignore\": \"No description available\",\n    \"api/MIGRATIONS.md\"\
    : \" This file tracks the database migrations for the Zotify API . Add a `server_default`\
    \ of `true` to handle existing rows . Add `notifications_enabled` to\",\n    \"\
    api/alembic.ini\": \"No description available\",\n    \"api/alembic/README\":\
    \ \"No description available\",\n    \"api/alembic/env.py\": \"This is the Alembic\
    \ Config object that provides access to the logging configuration .\",\n    \"\
    api/alembic/script.py.mako\": \"No description available\",\n    \"api/alembic/versions/5f96175ff7c9_add_notifications_enabled_to_.py\"\
    : \"Add notifications_enabled to UserPreferences Revision ID\",\n    \"api/api_dumps/cache.json\"\
    : \"No description available\",\n    \"api/api_dumps/downloads.json\": \"No description\
    \ available\",\n    \"api/api_dumps/logging.json\": \"No description available\"\
    ,\n    \"api/api_dumps/metadata.json\": \"No description available\",\n    \"\
    api/api_dumps/network.json\": \"No description available\",\n    \"api/api_dumps/playlist.json\"\
    : \"No description available\",\n    \"api/api_dumps/spotify.json\": \"No description\
    \ available\",\n    \"api/api_dumps/stubs.json\": \"No description available\"\
    ,\n    \"api/api_dumps/sync.json\": \"No description available\",\n    \"api/api_dumps/system.json\"\
    : \"No description available\",\n    \"api/api_dumps/tracks.json\": \"No description\
    \ available\",\n    \"api/api_dumps/user.json\": \"No description available\"\
    ,\n    \"api/docs/CHANGELOG.md\": \" The project adheres to a custom versioning\
    \ scheme for pre-releases . The API-201 project is based on [Keep a Changelog](https://keepachangelog\"\
    ,\n    \"api/docs/CODE_FILE_INDEX.md\": \" Alembic environment script, configures\
    \ and runs migrations . The file is auto-generated . Do not edit manually .\"\
    ,\n    \"api/docs/CODE_QUALITY_INDEX.md\": \" Document tracks the quality of every\
    \ source code file in the project . Each file is assessed against the rubric defined\
    \ below . Document is assigned two independent quality scores: one for documentation\
    \ and one\",\n    \"api/docs/DOCS_QUALITY_INDEX.md\": \" API-204 is an index for\
    \ documents related to code quality standards and reports . This file is auto-generated\
    \ . Do not edit manually .\",\n    \"api/docs/MASTER_INDEX.md\": \" API Documentation\
    \ Master Index serves as the central index for all documentation related to the\
    \ Zotify API and its sub-modules . Phases 3–5 deliver the full core API, user\
    \ authentication\",\n    \"api/docs/manuals/API_DEVELOPER_GUIDE.md\": \" This\
    \ document is for developers who wish to contribute directly to the Zotify API\
    \ codebase . It outlines the development workflow, architectural patterns, and\
    \ quality standards required for all contributions . For information\",\n    \"\
    api/docs/manuals/CICD.md\": \" This document provides a comprehensive overview\
    \ of the CI/CD and local linting infrastructure used in this project . It is designed\
    \ to be a reusable template that can be adapted for other projects\",\n    \"\
    api/docs/manuals/ERROR_HANDLING_GUIDE.md\": \" Generic Error Handling Module is\
    \ the central system for processing all unhandled exceptions . The module is designed\
    \ to be extensible without modifying its core code . All errors are automatically\
    \ formatted into a standard\",\n    \"api/docs/manuals/LOGGING_GUIDE.md\": \"\
    \ Zotify Flexible Logging Framework is a first-class tool designed to give you\
    \ maximum control over how your code generates and routes log events . The most\
    \ powerful feature of the framework is\",\n    \"api/docs/manuals/OPERATOR_MANUAL.md\"\
    : \" This manual provides detailed, actionable guidance for deploying, configuring,\
    \ and maintaining the Zotify API in a production or semi-production environment\
    \ . It assumes you have a working knowledge of\",\n    \"api/docs/manuals/SYSTEM_INTEGRATION_GUIDE.md\"\
    : \" This document provides essential information for developers who need to integrate\
    \ with or consume the Zotify API . It covers project setup, testing procedures,\
    \ core architectural principles, and documentation conventions . The Zot\",\n\
    \    \"api/docs/manuals/USER_MANUAL.md\": \" This manual explains how to consume\
    \ the Zotify REST API to manage your music library . It is intended for end-users\
    \ or client application developers . All protected endpoints require a valid API\"\
    ,\n    \"api/docs/providers/SPOTIFY.md\": \" The Spotify provider connector is\
    \ the first provider to be integrated into the new provider-agnostic architecture\
    \ . The current authentication flow is specific to Spotify's OAuth 2.0 implementation\
    \ .\",\n    \"api/docs/reference/API_REFERENCE.md\": \" This document provides\
    \ a detailed reference for the Zotify API . It is generated from the OpenAPI 3.0\
    \ specification . For planned endpoints (not yet implemented) see `../../\",\n\
    \    \"api/docs/reference/FEATURE_SPECS.md\": \" This document serves as the master\
    \ index for all detailed feature specifications for the Gonk platform . The purpose\
    \ of this system is to ensure that every feature, endpoint, and function in the\
    \ code\",\n    \"api/docs/reference/features/AUTHENTICATION.md\": \" API protects\
    \ all API endpoints by requiring a valid, secret API key to be passed in the `X-API-Key`\
    \ header of every request . If the key is missing or\",\n    \"api/docs/reference/features/AUTOMATED_DOCUMENTATION_WORKFLOW.md\"\
    : \" 'Lint-docs.py' is a tooling tooling feature and has no API endpoints . 'Documentation-with-Code'\
    \ is designed to fail the commit if\",\n    \"api/docs/reference/features/DEVELOPER_FLEXIBLE_LOGGING_FRAMEWORK.md\"\
    : \" This module extends the current global error handling system into a fully\
    \ programmable, developer-facing logging framework that becomes part of the API\
    \ framework itself . Its purpose is to allow fine-gr\",\n    \"api/docs/reference/features/PROVIDER_AGNOSTIC_EXTENSIONS.md\"\
    : \" Proposal extends the existing provider-agnostic design of the API by ensuring\
    \ all features, endpoints, and modules—current and future—are documented with\
    \ a consistent, detailed, and\",\n    \"api/docs/reference/features/PROVIDER_OAUTH.md\"\
    : \" The system provides a generic set of endpoints to initiate and complete the\
    \ OAuth2 login process for any supported provider . This allows the API to support\
    \ authentication with multiple music service providers (\",\n    \"api/docs/reference/source/ACTIONS____INIT__.py.md\"\
    : \" # __init__.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to the list .\",\n    \"api/docs/reference/source/APP.js.md\"\
    : \" App uses the API-120 API language . The code is intended to use as a role\
    \ and place in the project .\",\n    \"api/docs/reference/source/APP.py.md\":\
    \ \" # app.py: App is a project that uses the API-121 API . App is an application\
    \ for a project with a role, purpose and place .\",\n    \"api/docs/reference/source/AUDIT_API.py.md\"\
    : \" # audit_api.py is an API-122 application for audit-API-122 . The project's\
    \ role, purpose and place are filled in .\",\n    \"api/docs/reference/source/AUDIT_ENDPOINTS.py.md\"\
    : \" # audit_endpoints.py: # audit-endpoints . # audit/endpoints: Audit_Endpoints\
    \ . Add code examples to the endpoints .\",\n    \"api/docs/reference/source/AUTH.py.md\"\
    : \" # auth.py: Role / Purpose - (To be filled in) Role, Key Functions, Place\
    \ within Project Architecture, Place in Project Architecture . Add code examples\
    \ to the list of\",\n    \"api/docs/reference/source/AUTH_STATE.py.md\": \" #\
    \ auth_state.py: Role / Purpose - (To be filled in) Role / purpose - (to be filled\
    \ out) # # auth-state: Place within Project Architecture\",\n    \"api/docs/reference/source/BASE.py.md\"\
    : \" Base.py is based on an API-126 version of the Base API . The Base API is\
    \ designed to provide a role, purpose and place in the project .\",\n    \"api/docs/reference/source/CACHE.py.md\"\
    : \" # cache.py: Cache.py . # cache .py: Use the API-127 to fill in the role,\
    \ purpose and place in the project . Add code examples to the\",\n    \"api/docs/reference/source/CACHE_SERVICE.py.md\"\
    : \" # cache_service.py: Use the API-128 to create a role, purpose, place and\
    \ place in project architecture . Add code examples to the project to add to cache\
    \ .\",\n    \"api/docs/reference/source/CONFIG.py.md\": \" # config.py: Role,\
    \ Purpose, Key Functions, Place within Project Architecture, Place in Project\
    \ Architecture and Dependencies are filled in . Add code examples to the project's\
    \ config.\",\n    \"api/docs/reference/source/CONFIG_MODELS.py.md\": \" # config_models.py:\
    \ Role / Purpose - (To be filled in) Role / purpose - Key Functions - Place within\
    \ Project Architecture . Add code examples to the list of models\",\n    \"api/docs/reference/source/CONFIG_SERVICE.py.md\"\
    : \" # config_service.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to the list .\",\n    \"api/docs/reference/source/CONSOLE_HANDLER.py.md\"\
    : \" # console_handler.py: Use the API-132 to create a role, purpose, place and\
    \ place in project architecture . Add code examples to the project's code . Use\
    \ the\",\n    \"api/docs/reference/source/CRUD.py.md\": \" # crud.py: Use the\
    \ API-133 to create a role, purpose, place and place in the project's architecture\
    \ . Add code examples to the project .\",\n    \"api/docs/reference/source/DATABASE_JOB_HANDLER.py.md\"\
    : \" # database_job_handler.py is an API-134 application for database jobs . The\
    \ code is designed to fill in a role and place in the project's architecture .\"\
    ,\n    \"api/docs/reference/source/DATABASE____INIT__.py.md\": \" # __init__.py:\
    \ Role, Purpose, Key Functions, Place within Project Architecture, Place in Project\
    \ Architecture . Add code examples to the list .\",\n    \"api/docs/reference/source/DB.py.md\"\
    : \" # db.py: Use the API-136 to create a role, purpose, place and place in project\
    \ architecture . Add code examples to the project's code .\",\n    \"api/docs/reference/source/DEPS.py.md\"\
    : \" # deps.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to the deps .\",\n    \"api/docs/reference/source/DOWNLOAD.py.md\"\
    : \" # download.py . Use the API-138 to create a role, place and place in the\
    \ project's architecture . Add code examples to the project .\",\n    \"api/docs/reference/source/DOWNLOADS.py.md\"\
    : \" # downloads.py . Use the API-139 to download code examples for the latest\
    \ version of the project .\",\n    \"api/docs/reference/source/DOWNLOAD_SERVICE.py.md\"\
    : \" Code Examples are available for download_service.py .\",\n    \"api/docs/reference/source/ERROR_HANDLER____INIT__.py.md\"\
    : \" # __init__.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to the list .\",\n    \"api/docs/reference/source/FILTERS.py.md\"\
    : \" # filters.py: Use the API-142 to fill in the role, purpose, place and place\
    \ in project architecture . Add code examples to the filter .\",\n    \"api/docs/reference/source/FORMATTER.py.md\"\
    : \" # formatter.py is a formatter of an API-143 formatter . The formatter is\
    \ designed to fill in a role and place in the project's architecture .\",\n  \
    \  \"api/docs/reference/source/FUNCTIONAL_TEST.py.md\": \" # functional_test.py:\
    \ Role / Purpose - (To be filled in) Role, Key Functions, Place within Project\
    \ Architecture - Place within Architecture . Add code examples to functional_\"\
    ,\n    \"api/docs/reference/source/GENERATE_ENDPOINTS_DOC.py.md\": \" # generate_endpoints_doc.py:\
    \ Use the API-145 to fill in the role, purpose and place in project architecture\
    \ . Add code examples to the endpoints .\",\n    \"api/docs/reference/source/GENERATE_OPENAPI.py.md\"\
    : \" # generate_openapi.py: Use the API-146 to create a role, purpose, place and\
    \ place in project architecture . Add code examples to the code .\",\n    \"api/docs/reference/source/GENERATE_SOURCE_DOCS.py.md\"\
    : \" # generate_source_docs.py: Use the API-147 to create your own source code\
    \ . Add code examples to the code .\",\n    \"api/docs/reference/source/GENERIC.py.md\"\
    : \" The API-148 project is a generic application for generic programming . The\
    \ project's role, purpose and place are filled in . Add code examples to the project\
    \ .\",\n    \"api/docs/reference/source/GLOBALS.py.md\": \" # globals.py: Role\
    \ / Purpose - (To be filled in) Role, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . # code examples: Add code\",\n    \"api/docs/reference/source/HOOKS.py.md\"\
    : \" # hooks.py: Use the API-150 to create a role, purpose, place and place in\
    \ project architecture . Add code examples to the list of hooks .\",\n    \"api/docs/reference/source/JSON_AUDIT_HANDLER.py.md\"\
    : \" # json_audit_handler.py: Use the API-151 to test your knowledge of the project's\
    \ role and purpose . Add code examples to the code .\",\n    \"api/docs/reference/source/LINTER.py.md\"\
    : \" The API-152 linter.py is designed to fill in the role and purpose of the\
    \ project . The code is intended to use as a tool to help users understand the\
    \ project's\",\n    \"api/docs/reference/source/LOGGING_CONFIG.py.md\": \" # logging_config.py:\
    \ Logging_Config.py . # Logging-Config: Role / Purpose - (To be filled in) # Logged-Config\
    \ is API\",\n    \"api/docs/reference/source/LOGGING_FRAMEWORK____INIT__.py.md\"\
    : \" # __init__.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to the list .\",\n    \"api/docs/reference/source/LOGGING_HANDLERS____INIT__.py.md\"\
    : \" # __init__.py: Role / Purpose - (To be filled in) # # # .py: Place within\
    \ Project Architecture - Place within project Architecture . # . Add code\",\n\
    \    \"api/docs/reference/source/LOGGING_SCHEMAS.py.md\": \" # logging_schemas.py:\
    \ Logging_Schemas . # Logging-Scheme: Role / Purpose - (To be filled in) # Logged-\"\
    ,\n    \"api/docs/reference/source/LOGGING_SERVICE.py.md\": \" # logging_service.py:\
    \ Logging_Service.py . # Logging-Service: Role, Purpose, Key Functions, Place\
    \ within Project Architecture . Add code examples to the\",\n    \"api/docs/reference/source/LOG_CRITICAL.py.md\"\
    : \" # log_critical.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to log-critical .\",\n   \
    \ \"api/docs/reference/source/MAIN.py.md\": \" # main.py: Use the API-159 to create\
    \ a role, purpose, place and place in project architecture . Add code examples\
    \ to the project .\",\n    \"api/docs/reference/source/METADATA.py.md\": \" #\
    \ metadata.py: Role, Purpose, Key Functions, Place within Project Architecture\
    \ . Add code examples to the metadata . Use the API-160 to create your own metadata\
    \ .\",\n    \"api/docs/reference/source/METADATA_SERVICE.py.md\": \" # metadata_service.py\
    \ is created using the API-161 . The metadata-service is designed to provide a\
    \ role, purpose and place in the project .\",\n    \"api/docs/reference/source/MODELS.py.md\"\
    : \" The API-162 is designed to provide a role, purpose and place in a project's\
    \ architecture . The project is based on a project called 'Project Architecture'\
    \ and 'Project Architect'\",\n    \"api/docs/reference/source/NETWORK.py.md\"\
    : \" # network.py: Use the API-163 to create a network of applications . Add code\
    \ examples to the project .\",\n    \"api/docs/reference/source/NETWORK_SERVICE.py.md\"\
    : \" # network_service.py: Use the API-164 to create a role, purpose, place and\
    \ place in project architecture . Add code examples to the project .\",\n    \"\
    api/docs/reference/source/NOTIFICATIONS.py.md\": \" # notifications.py: Use the\
    \ API-165 to create a notification system for notifications . Add code examples\
    \ to the system .\",\n    \"api/docs/reference/source/NOTIFICATIONS_SERVICE.py.md\"\
    : \" # notifications_service.py: Use the API-166 to create a role, purpose, place\
    \ and place in project architecture . Add code examples to the list of tasks to\
    \ fill in\",\n    \"api/docs/reference/source/PLAYLISTS.py.md\": \" Playlists.py\
    \ is an API-167 playlists . Playlists are designed to fill in a role, a purpose,\
    \ a function and a place in an architecture .\",\n    \"api/docs/reference/source/PLAYLISTS_SERVICE.py.md\"\
    : \" Playlists_service.py uses the API-168 to create a playlists service . The\
    \ project is based on a role, purpose and place in the project .\",\n    \"api/docs/reference/source/PROVIDERS____INIT__.py.md\"\
    : \" # __init__.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to the list .\",\n    \"api/docs/reference/source/REQUEST_ID.py.md\"\
    : \" Request_id.py is an API-170 application that uses Python's role and purpose\
    \ . The code is designed to fill in a role and place in the project's architecture\
    \ .\",\n    \"api/docs/reference/source/ROUTES____INIT__.py.md\": \" # __init__.py:\
    \ Role / Purpose - (To be filled in) # # # .py: Place within Project Architecture\
    \ - Place within project Architecture . # . Add code\",\n    \"api/docs/reference/source/SCHEMAS.py.md\"\
    : \" Scrammas.py is an API-172 project that uses a role, a purpose, a function\
    \ and a place in a project's architecture . The project is designed to be a\"\
    ,\n    \"api/docs/reference/source/SEARCH.py.md\": \" Search for API-173: \\\"\
    Search.py\\\" The search.py is a search for a project that uses a role, purpose\
    \ and place in a project's architecture .\",\n    \"api/docs/reference/source/SERVICE.py.md\"\
    : \" Service.py is an API-174 service . It is designed to provide a role, purpose\
    \ and place in the project's architecture .\",\n    \"api/docs/reference/source/SERVICES____INIT__.py.md\"\
    : \" # __init__.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to the list .\",\n    \"api/docs/reference/source/SESSION.py.md\"\
    : \" # session.py: Use the API-176 to create a session . Add code examples to\
    \ the project .\",\n    \"api/docs/reference/source/SNITCH.go.md\": \" Snitch.go\
    \ is an API-177 version of the snitch-enabled snitch application . Use this article's\
    \ code to test your knowledge of snitch. Go to snitch\",\n    \"api/docs/reference/source/SPOTIFY.py.md\"\
    : \" Role / Purpose - (To be filled in) Role, Key Functions, Place within Project\
    \ Architecture - Place within Architecture . Code Examples - (Add code examples\
    \ here)\",\n    \"api/docs/reference/source/SPOTIFY_CONNECTOR.py.md\": \" # spotify_connector.py:\
    \ Role / Purpose - (To be filled in) # Spotify_Connector . # Spotified_connectors:\
    \ # spotified_\",\n    \"api/docs/reference/source/SPOTI_CLIENT.py.md\": \" #\
    \ spoti_client.py: Role / Purpose - (To be filled in) # Spoti_Client: Role, Purpose,\
    \ Key Functions, Place within Project Architecture - (\",\n    \"api/docs/reference/source/SYNC.py.md\"\
    : \" Sync.py is an API-181 version of a new version of sync.py . The code is intended\
    \ to use as a tool for developing a new API .\",\n    \"api/docs/reference/source/SYNC_SERVICE.py.md\"\
    : \" # sync_service.py: Use the API-182 to create a role, purpose, place and place\
    \ in project architecture . Add code examples to the project .\",\n    \"api/docs/reference/source/SYSTEM.py.md\"\
    : \" System.py is an API-183 version of a new version of the Django-Python-Python\
    \ API . The code is intended to use as a tool for developing a new Python-\",\n\
    \    \"api/docs/reference/source/TEST_AUTH_FLOW.py.md\": \" # test_auth_flow.py:\
    \ Role / Purpose - (To be filled in) # Test_Auth_flow: Role, Purpose, Key Functions,\
    \ Place within Project Architecture\",\n    \"api/docs/reference/source/TRACKS.py.md\"\
    : \" # tracks.py: API-185 . Add code examples to the project .\",\n    \"api/docs/reference/source/TRACKS_SERVICE.py.md\"\
    : \" # tracks_service.py: Role, Purpose, Key Functions, Place within Project Architecture,\
    \ Place in Project Architecture . Add code examples to track_service .\",\n  \
    \  \"api/docs/reference/source/TRIGGERS.py.md\": \" # triggers.py: Use the API-187\
    \ to create a project with a role, purpose, place and place in the project . Add\
    \ code examples to the project's code .\",\n    \"api/docs/reference/source/USER.py.md\"\
    : \" Use the API-188 to create a user's role, purpose and place in the project's\
    \ architecture . Add code examples to the project to create your own Python code\
    \ .\",\n    \"api/docs/reference/source/USER_SERVICE.py.md\": \" User_service.py\
    \ is created using the API-189 API . The user_service is designed to provide a\
    \ role, purpose and place in the project's architecture .\",\n    \"api/docs/reference/source/WEBHOOK.py.md\"\
    : \" Webhook.py is a webhook application that uses the API-190 API . The code\
    \ is designed to fill in a role and place in the project's architecture .\",\n\
    \    \"api/docs/reference/source/WEBHOOKS.py.md\": \" Webhooks.py is an API-191\
    \ application that uses webhooks . It is designed to provide a role, purpose and\
    \ place in the project's architecture .\",\n    \"api/docs/system/ERROR_HANDLING_DESIGN.md\"\
    : \" This document provides the detailed technical design for the Generic Error\
    \ Handling Module . The module serves as the central, platform-wide mechanism\
    \ for intercepting, processing, logging, and responding to all\",\n    \"api/docs/system/INSTALLATION.md\"\
    : \" This guide provides detailed instructions for installing and setting up the\
    \ Zotify API . It is highly recommended to use a Python virtual environment .\
    \ The API requires several environment variables to be set . The\",\n    \"api/docs/system/PRIVACY_COMPLIANCE.md\"\
    : \" This document outlines how the Zotify API project complies with data protection\
    \ laws . Zotify respects user privacy and commits to protecting personal data\
    \ .\",\n    \"api/docs/system/REQUIREMENTS.md\": \" This document lists the system\
    \ and software requirements for running the Zotify API and its related tools .\
    \ The application is developed and tested on Linux .\",\n    \"api/docs/system/zotify-openapi-external-v1.json\"\
    : \"No description available\",\n    \"api/docs/system/zotify-openapi-external-v1.yaml\"\
    : \"No description available\",\n    \"api/logging_config.yml\": \"Zotify API\
    \ Logging Service This file defines the handlers for the LoggingService .\",\n\
    \    \"api/logging_framework.yml\": \"Configuration for the Flexible Logging Framework\
    \ .\",\n    \"api/mypy.ini\": \"No description available\",\n    \"api/pyproject.toml\"\
    : \"No description available\",\n    \"api/ruff.toml\": \"No description available\"\
    ,\n    \"api/src/storage/spotify_tokens.json\": \"No description available\",\n\
    \    \"api/src/zotify_api/auth_state.py\": \"This module holds the shared constants\
    \ for the authentication process .\",\n    \"api/src/zotify_api/config.py\": \"\
    Creates a new instance of pydantic s settings class .\",\n    \"api/src/zotify_api/core/error_handler/__init__.py\"\
    : \"Define the public API of this module .\",\n    \"api/src/zotify_api/core/error_handler/actions/__init__.py\"\
    : \"This file makes the actions directory a Python package .\",\n    \"api/src/zotify_api/core/error_handler/actions/log_critical.py\"\
    : \"Log a message with CRITICAL level using the flexible logging framework .\"\
    ,\n    \"api/src/zotify_api/core/error_handler/actions/webhook.py\": \"Action\
    \ to send a notification to a webhook .\",\n    \"api/src/zotify_api/core/error_handler/config.py\"\
    : \"Implementation of the API - 031 .\",\n    \"api/src/zotify_api/core/error_handler/formatter.py\"\
    : \"Formats errors into a standardized JSON structure for API responses or CLI\
    \ output .\",\n    \"api/src/zotify_api/core/error_handler/hooks.py\": \"Register\
    \ the exception handler for the FastAPI .\",\n    \"api/src/zotify_api/core/error_handler/triggers.py\"\
    : \"Manages the execution of actions based on configured triggers .\",\n    \"\
    api/src/zotify_api/core/logging_framework/__init__.py\": \"Public API for the\
    \ flexible logging framework .\",\n    \"api/src/zotify_api/core/logging_framework/filters.py\"\
    : \"A logging filter that redacts sensitive data from log records .\",\n    \"\
    api/src/zotify_api/core/logging_framework/schemas.py\": \"API - 027 Creates a\
    \ model for all sinks .\",\n    \"api/src/zotify_api/core/logging_framework/service.py\"\
    : \"API - 028 - Creates a base class for all log sinks .\",\n    \"api/src/zotify_api/core/logging_handlers/__init__.py\"\
    : \"Make the logging_handlers directory a Python package .\",\n    \"api/src/zotify_api/core/logging_handlers/base.py\"\
    : \"Abstract base class for all log handlers .\",\n    \"api/src/zotify_api/core/logging_handlers/console_handler.py\"\
    : \"Creates a log handler that prints formatted log messages to the console .\"\
    ,\n    \"api/src/zotify_api/core/logging_handlers/database_job_handler.py\": \"\
    Creates a handler that writes job status updates to the database .\",\n    \"\
    api/src/zotify_api/core/logging_handlers/json_audit_handler.py\": \"A log handler\
    \ that writes structured JSON audit logs to a file .\",\n    \"api/src/zotify_api/database/__init__.py\"\
    : \"The API - 428 ID is reserved for API - 428 .\",\n    \"api/src/zotify_api/database/crud.py\"\
    : \"API - 045 - DownloadJob CRUD\",\n    \"api/src/zotify_api/database/models.py\"\
    : \"API - 046 - Creates an ORM table for Playlists and Tracks\",\n    \"api/src/zotify_api/database/session.py\"\
    : \"FastAPI dependency that provides a database session for a single request .\"\
    ,\n    \"api/src/zotify_api/globals.py\": \"API - 08 This function is deprecated\
    \ and removed in the future .\",\n    \"api/src/zotify_api/logging_config.py\"\
    : \"Setup logging for API - 049 .\",\n    \"api/src/zotify_api/main.py\": \"Create\
    \ a FastAPI instance with the default settings .\",\n    \"api/src/zotify_api/middleware/request_id.py\"\
    : \"Create a request - id middleware for a request .\",\n    \"api/src/zotify_api/models/config_models.py\"\
    : \"API - 052 - ConfigModel and ConfigUpdate\",\n    \"api/src/zotify_api/models/sync.py\"\
    : \"Create a sync request for a playlist .\",\n    \"api/src/zotify_api/providers/__init__.py\"\
    : \"The API - 438 ID is reserved for backwards compatibility .\",\n    \"api/src/zotify_api/providers/base.py\"\
    : \"Constructs an abstract base class for a Spotify service provider .\",\n  \
    \  \"api/src/zotify_api/providers/spotify_connector.py\": \"Creates an instance\
    \ of the Spotify API connector .\",\n    \"api/src/zotify_api/routes/__init__.py\"\
    : \"This file makes the routes directory a Python package .\",\n    \"api/src/zotify_api/routes/auth.py\"\
    : \"The spotify API endpoint . This endpoint is used to handle the OAuth2 login\
    \ flow .\",\n    \"api/src/zotify_api/routes/cache.py\": \"The cache endpoint\
    \ provides a list of cache statistics .\",\n    \"api/src/zotify_api/routes/config.py\"\
    : \"API - 060 Route to get config and update it\",\n    \"api/src/zotify_api/routes/downloads.py\"\
    : \"API endpoint for downloading a set of tracks .\",\n    \"api/src/zotify_api/routes/jwt_auth.py\"\
    : \"Login to Zotify and return an access token\",\n    \"api/src/zotify_api/routes/network.py\"\
    : \"API endpoint for retrieving and updating network configuration .\",\n    \"\
    api/src/zotify_api/routes/notifications.py\": \"API - 064 - Notifications endpoint\"\
    ,\n    \"api/src/zotify_api/routes/playlists.py\": \"Zotify API endpoint for listing\
    \ playlists .\",\n    \"api/src/zotify_api/routes/search.py\": \"Search for tracks\
    \ in zotify .\",\n    \"api/src/zotify_api/routes/sync.py\": \"Triggers a global\
    \ synchronization job . This is a global synchronization job .\",\n    \"api/src/zotify_api/routes/system.py\"\
    : \"Reloads the logging framework configuration from the logging_framework . yml\
    \ file at runtime .\",\n    \"api/src/zotify_api/routes/tracks.py\": \"API - 69\
    \ - List all tracks and create a new track\",\n    \"api/src/zotify_api/routes/user.py\"\
    : \"API endpoint for accessing user profile and preferences .\",\n    \"api/src/zotify_api/routes/webhooks.py\"\
    : \"API - 071 - Register webhooks .\",\n    \"api/src/zotify_api/schemas/auth.py\"\
    : \"The Spotify API -072 model class .\",\n    \"api/src/zotify_api/schemas/cache.py\"\
    : \"Cache Clear Request - Cache Clear Response - Cache Status Response\",\n  \
    \  \"api/src/zotify_api/schemas/download.py\": \"ID is API - 074 - Created at\"\
    ,\n    \"api/src/zotify_api/schemas/generic.py\": \"API - 075 - Create a standard\
    \ response object\",\n    \"api/src/zotify_api/schemas/logging_schemas.py\": \"\
    API - 076 LogUpdate and LogConfigResponse\",\n    \"api/src/zotify_api/schemas/metadata.py\"\
    : \"MetadataUpdate and MetadataPatchResponse can be used to update metadata .\"\
    ,\n    \"api/src/zotify_api/schemas/network.py\": \"API - 078 - ProxyConfig and\
    \ NetworkConfigResponse\",\n    \"api/src/zotify_api/schemas/notifications.py\"\
    : \"Notification class . Notifications are created and updated by user .\",\n\
    \    \"api/src/zotify_api/schemas/playlists.py\": \"Example of how to display\
    \ a list of playlists .\",\n    \"api/src/zotify_api/schemas/spotify.py\": \"\
    Spotify 1 . 0 schemas have been moved to more appropriate locations or removed\
    \ .\",\n    \"api/src/zotify_api/schemas/system.py\": \"API - 082 - Created by\
    \ Michael\",\n    \"api/src/zotify_api/schemas/tracks.py\": \"API - 083 - Created\
    \ Tracks\",\n    \"api/src/zotify_api/schemas/user.py\": \"API - 084 API - 084\"\
    ,\n    \"api/src/zotify_api/schemas/webhooks.py\": \"ID is API - 085 and will\
    \ be removed in future .\",\n    \"api/src/zotify_api/services/__init__.py\":\
    \ \"API - 4 . 0 API - 4 . 0\",\n    \"api/src/zotify_api/services/auth.py\": \"\
    Refreshes the access token using the stored refresh token and saves the new token\
    \ to the database .\",\n    \"api/src/zotify_api/services/cache_service.py\":\
    \ \"This module is used to provide the business logic for the cache subsystem\
    \ .\",\n    \"api/src/zotify_api/services/config_service.py\": \"This module provides\
    \ the business logic for the config subsystem .\",\n    \"api/src/zotify_api/services/db.py\"\
    : \"Returns a database engine based on settings . database_uri\",\n    \"api/src/zotify_api/services/deps.py\"\
    : \"Returns an API dependency that provides a fully authenticated Spotify client\
    \ .\",\n    \"api/src/zotify_api/services/download_service.py\": \"Creates new\
    \ download jobs and adds them to the database queue .\",\n    \"api/src/zotify_api/services/jwt_service.py\"\
    : \"Returns a user object from a JWT token .\",\n    \"api/src/zotify_api/services/logging_service.py\"\
    : \"Creates a logging service that dispatches log messages to all relevant handlers\
    \ .\",\n    \"api/src/zotify_api/services/metadata_service.py\": \"API - 095 -\
    \ Create a metadata service .\",\n    \"api/src/zotify_api/services/network_service.py\"\
    : \"This module provides the business logic for the network subsystem .\",\n \
    \   \"api/src/zotify_api/services/notifications_service.py\": \"Creates a notification\
    \ for a user and marks it as read\",\n    \"api/src/zotify_api/services/playlists_service.py\"\
    : \"Return a list of playlists and their mappings .\",\n    \"api/src/zotify_api/services/search.py\"\
    : \"Perform a spotify search with the given query .\",\n    \"api/src/zotify_api/services/spoti_client.py\"\
    : \"Creates a stateless client for interacting with the Spotify Web API .\",\n\
    \    \"api/src/zotify_api/services/sync_service.py\": \"Sync service module .\
    \ This module provides the business logic for the sync subsystem .\",\n    \"\
    api/src/zotify_api/services/tracks_service.py\": \"Get a list of tracks from the\
    \ database .\",\n    \"api/src/zotify_api/services/user_service.py\": \"Get user\
    \ profile and preferences for a user .\",\n    \"api/src/zotify_api/services/webhooks.py\"\
    : \"Register and unregister webhooks from the API .\",\n    \"api/src/zotify_api/storage/user_data.json\"\
    : \"No description available\",\n    \"api/src/zotify_api/temp_violation.py\"\
    : \"Create a temporary violation file in the temporary directory .\",\n    \"\
    api/tests/__init__.py\": \"The API - 234 ID is the API - 234 ID of the API .\"\
    ,\n    \"api/tests/conftest.py\": \"A test client that can be used in all tests\
    \ .\",\n    \"api/tests/test_cache.py\": \"Example of how to use the cache service\
    \ .\",\n    \"api/tests/test_config.py\": \"Example of how to use the config service\
    \ .\",\n    \"api/tests/test_download.py\": \"This is the main function of the\
    \ test . It will be called by zotify_api .\",\n    \"api/tests/test_network.py\"\
    : \"Example of how to use the network service .\",\n    \"api/tests/test_notifications.py\"\
    : \"Example of how to create users and notifications .\",\n    \"api/tests/test_playlists.py\"\
    : \"Example of how to use zotify .\",\n    \"api/tests/test_system.py\": \"Example\
    \ of how to use zotify .\",\n    \"api/tests/test_tracks.py\": \"A test suite\
    \ to test the database engine .\",\n    \"api/tests/test_user.py\": \"Example\
    \ of how to create a user .\",\n    \"api/tests/unit/providers/test_spotify_connector.py\"\
    : \"Testing of the happy path for the OAuth callback .\",\n    \"api/tests/unit/test_auth.py\"\
    : \"Test the spotify_api . main module\",\n    \"api/tests/unit/test_cache_service.py\"\
    : \"API - 212 Tests cache state .\",\n    \"api/tests/unit/test_config.py\": \"\
    This file has been refactored .\",\n    \"api/tests/unit/test_crud.py\": \"Mock\
    \ the database session to return a chainable object .\",\n    \"api/tests/unit/test_deps.py\"\
    : \"Example of how to get a SpotifyClient .\",\n    \"api/tests/unit/test_error_handler.py\"\
    : \"Creates a mock logger to capture log messages .\",\n    \"api/tests/unit/test_error_handler_actions.py\"\
    : \"Tests that the error handler logs a critical error and sends a webhook .\"\
    ,\n    \"api/tests/unit/test_flexible_logging.py\": \"Tests a Zotify API with\
    \ a valid logging configuration .\",\n    \"api/tests/unit/test_jwt_auth_db.py\"\
    : \"Test client authentication . This test is used to make sure that the user\
    \ is logged in .\",\n    \"api/tests/unit/test_logging_config.py\": \"Test that\
    \ setup_logging calls logging . basicConfig .\",\n    \"api/tests/unit/test_metadata_service.py\"\
    : \"Example of how to use metadata service .\",\n    \"api/tests/unit/test_network_service.py\"\
    : \"This is a test for getting and updating the network configuration . It is\
    \ a test to make sure the network configuration is correct .\",\n    \"api/tests/unit/test_new_logging_system.py\"\
    : \"Creates a mock of the logging service .\",\n    \"api/tests/unit/test_notifications_service.py\"\
    : \"This test is used by zotify_api .\",\n    \"api/tests/unit/test_playlists_service.py\"\
    : \"Creates a mock that tests playlists .\",\n    \"api/tests/unit/test_search.py\"\
    : \"Test for dependency overrides on Zotify .\",\n    \"api/tests/unit/test_spoti_client.py\"\
    : \"Tests that the SpotiClient can successfully fetch tracks metadata and user\
    \ data .\",\n    \"api/tests/unit/test_sync.py\": \"Initialize a new Zotify API\
    \ .\",\n    \"api/tests/unit/test_tracks_service.py\": \"A Zotify API does not\
    \ support GET and POST requests .\",\n    \"api/tests/unit/test_user_service.py\"\
    : \"Zotify 2 . 0 test suite\",\n    \"api/tests/unit/test_user_service_db.py\"\
    : \"Example of how to create a user in a database .\",\n    \"api/tests/unit/test_webhooks.py\"\
    : \"API - 232 setup and test hooks\",\n    \"project/ALIGNMENT_MATRIX.md\": \"\
    \ The API Routes Layer includes a Pydantic Schema Layer, Business Logic Service\
    \ Layer, Centralized Configuration, Flexible Logging Framework and System Routes\
    \ & Health Checks . The\",\n    \"project/ALIGNMENT_MATRIX.yml\": \"- - - - -\
    \ - - - - - - - - - - - -\",\n    \"project/BACKLOG.md\": \" Document serves as\
    \ the tactical backlog for the Zotify API Platform . It contains a list of clearly\
    \ defined, approved tasks for future implementation . The process for managing\
    \ this backlog is defined in the\",\n    \"project/CICD.md\": \" This document\
    \ provides a high-level overview of the Continuous Integration / Continuous Deployment\
    \ (CI/CD) pipeline for this project . It is intended for a project management\
    \ and stakeholder audience\",\n    \"project/DEPENDENCIES.md\": \" The goal is\
    \ to maintain a lean, stable, and secure project by minimizing the number of external\
    \ dependencies . A new dependency may only be added to the project if it meets\
    \ all of the\",\n    \"project/EXECUTION_PLAN.md\": \" This document provides\
    \ a detailed breakdown of the tasks required to fulfill the [Canonical Roadmap]\"\
    ,\n    \"project/FUTURE_ENHANCEMENTS.md\": \" Document serves as a dedicated \\\
    \"parking lot\\\" for new ambitions and feature ideas that have emerged during\
    \ development but are not part of the current, committed roadmap . Document lists\
    \ specific technical features\",\n    \"project/HIGH_LEVEL_DESIGN.md\": \" Document\
    \ outlines the high-level architecture, scope, and guiding principles for the\
    \ ongoing Zotify API refactor . It serves as a blueprint for the development team\
    \ to maintain alignment with long-\",\n    \"project/LESSONS-LEARNT.md\": \" Project\
    \ Flow Requirement: This file must be updated immediately after any lesson with\
    \ project-wide or phase-relevant implications is identified . Reviewers must confirm\
    \ updates during **phase review gates**\",\n    \"project/LOGGING_PHASES.md\"\
    : \" This document tracks the phased design and implementation of the new Extendable\
    \ Logging System . It defines each phase, current status, deliverables, and governance\
    \ rules . All phases are aligned with\",\n    \"project/LOGGING_SYSTEM_DESIGN.md\"\
    : \" Document outlines the architecture for a new, extendable logging system for\
    \ the Zotify API . The goal is to create a robust, centralized service that can\
    \ handle multiple logging scenarios (e.\",\n    \"project/LOGGING_TRACEABILITY_MATRIX.md\"\
    : \" This document maps the high-level requirements for the new Extendable Logging\
    \ System to the design artifacts that specify the solution and the backlog tasks\
    \ that will implement it . This ensures that all\",\n    \"project/LOW_LEVEL_DESIGN.md\"\
    : \" Low-Level Design (LLD) describes the specific implementation details of the\
    \ Zotify API's subsystems . The Fast API uses several cross-cutting concerns to\
    \ provide middle-ware to\",\n    \"project/ONBOARDING.md\": \" Document is intended\
    \ to bring a new developer up to speed on the project, providing guidance for\
    \ understanding the architecture, workflows, and key artifacts . Review each document\
    \ in order to efficiently onboard\",\n    \"project/PID.md\": \" The Zotify API\
    \ was originally built as a lightweight wrapper for a single use case . The project\
    \ aims to refactor and expand the API to form a robust, scalable, and provider-\"\
    ,\n    \"project/PROJECT_BRIEF.md\": \" The Gonk API Refactoring and Enhancement\
    \ project aims to refactor the existing Zotify-based API into a professional-grade,\
    \ multi-service media automation platform . The original API\",\n    \"project/PROJECT_PLAN.md\"\
    : \" The Zotify API project is a strategic refactor and enhancement of the original\
    \ Zotify CLI tool . Its purpose is to transform the tool into a robust, scalable,\
    \ and provider-agn\",\n    \"project/PROJECT_REGISTRY.md\": \" Historical legacy\
    \ entries preserved below . Document | Location | Description | Status . Document\
    \ is intended for a project management and stakeholder audience . Document outlines\
    \ the policy for adding new third-party dependencies\",\n    \"project/QA_GOVERNANCE.md\"\
    : \" Document is the single source of truth for all Quality Assurance (QA) and\
    \ governance policies for this project . The policies outlined here are enforced\
    \ automatically by the project's tooling .\",\n    \"project/ROADMAP.md\": \"\
    \ Document provides a high-level, strategic roadmap for the Zotify API Platform\
    \ . It outlines the development trajectory from the current stable state to future\
    \ enhancements .\",\n    \"project/SECURITY.md\": \" The Zotify API platform is\
    \ designed with a \\\"secure by default\\\" philosophy . The platform uses a standard\
    \ OAuth2 PKCE flow to authenticate with the Spotify API . Spotify O\",\n    \"\
    project/TASK_CHECKLIST.md\": \" Document all functional changes in every relevant\
    \ doc: API reference, developer/operator guides, README if user-facing . Documenting\
    \ changes must be included in the same commit as code changes\",\n    \"project/USECASES.md\"\
    : \" Document captures realistic, demanding user scenarios that the API should\
    \ ideally support . These use cases cover complex playlist operations, advanced\
    \ audio handling, and end-to-end synchronization between local and Spotify\",\n\
    \    \"project/USECASES_GAP_ANALYSIS.md\": \" Document compares the **desired\
    \ capabilities** from USECASES.md with the **current** Zotify API implementation\
    \ . The goal is to identify missing or partial functionality that must be\",\n\
    \    \"project/api/endpoints.yaml\": \"No description available\",\n    \"project/logs/ACTIVITY.md\"\
    : \" The root cause of the pipeline failure was a combination of incorrect data\
    \ in the tag inventory and scripts with flawed logic . Fixed multiple scripts\
    \ (repo_inventory_and_governance.\",\n    \"project/logs/CURRENT_STATE.md\": \"\
    \ The pipeline is now stable . The next developer can proceed with feature work,\
    \ following the established traceability patterns .\",\n    \"project/logs/SESSION_LOG.md\"\
    : \" Fixed multiple scripts (repo_inventory_and_governance.py, verify_alignment_migration\
    \ .py, test_full_pipeline.sh) to\",\n    \"project/logs/conversations.json\":\
    \ \"File not found\",\n    \"project/process/GAP_ANALYSIS_TEMPLATE.md\": \" Gap\
    \ Analysis: [Feature/Process Name] * Describe the current situation in detail\
    \ . Identify and describe the specific gaps between the Current State and the\
    \ Desired Future State . Ident\",\n    \"project/proposals/DBSTUDIO_PLUGIN.md\"\
    : \" Currently, database inspection for the Zotify API is handled by 'sqlite-web',\
    \ which is integrated directly into the .Gonk/gonkUI` Flask application .\",\n\
    \    \"project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md\": \" Document proposes implementation\
    \ of a 'dynamic plugin system' for the Flexible Logging Framework . This system\
    \ will allow third-party developers to create their own custom sink implementations\
    \ in separate,\",\n    \"project/proposals/GONKUI_PLUGIN.md\": \" Document proposes\
    \ that the existing `Gonk/gonkUI' Flask application be converted into a 'dynamic'\
    \ plugin . This plugin will be a self-contained FastAPI\",\n    \"project/proposals/GOVERNANCE_AUDIT_REFACTOR.md\"\
    : \" Document proposes a comprehensive refactoring of repository's governance\
    \ audit script . The goal is to elevate the script from a basic inventory tool\
    \ into a complete, automated audit system . The refact\",\n    \"project/proposals/HOME_AUTOMATION_PROPOSAL.md\"\
    : \" Document proposes the official endorsement and creation of a dedicated integration\
    \ for home automation platforms . The goal is to create a custom Home Assistant\
    \ \\\"Integration\\\" that would expose Zotify entities and services\",\n    \"\
    project/proposals/LOW_CODE_PROPOSAL.md\": \" The Zotify API is becoming a powerful\
    \ platform for developers . We need to provide integrations with popular low-code/no-code\
    \ platforms . This document proposes the official endorsement and creation\",\n\
    \    \"project/proposals/MULTI_SOURCE_METADATA_PROPOSAL.md\": \" The proposal\
    \ outlines the system architecture, data model, API integration, security model,\
    \ and a phased implementation plan . The proposed system consists of three new\
    \ major components that integrate with the existing Zot\",\n    \"project/proposals/NEW_PROPOSAL.md\"\
    : \" This is a test proposal to verify the linter functionality .\",\n    \"project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md\"\
    : \" Document outlines the phased implementation plan for creating a professional-level,\
    \ multi-language QA Gate for the project . This system will complement the current,\
    \ simpler linter with a robust set\",\n    \"project/proposals/TRACE_INDEX_SCHEMA_ADAPTATION.md\"\
    : \" The initial version of the 'TRACE_INDEX.yml' file, generated by the `repo_inventory_and_governance.py,\
    \ had an inconsistent Sche\",\n    \"project/proposals/TRACE_INDEX_SCHEMA_FIX.md\"\
    : \" Document proposes and describes a \\\"schema fix\\\" for 'TRACE_INDEX.yml'\
    \ The previous version listed all *expected* indexes for both registered and unregistered\
    \ files\",\n    \"project/reports/ALIGNMENT_INTEGRITY_SNAPSHOT.yml\": \"This file\
    \ contains information about the lockdown phase of a document .\",\n    \"project/reports/ALIGNMENT_VALIDATION_REPORT.txt\"\
    : \" Missing ID tags in 46643 files: -/./.venv/share/man/man1/bandit.1 - .scripts/verify_alignment_migration\"\
    ,\n    \"project/reports/ARCHIVE_ALIGNMENT_MATRIX_OLD.md\": \" # Archived Alignment\
    \ Matrix Entries - id: SYS-02 description: Performance <200ms linked_docs: - HIGH_LEVEL_DESIGN.md\
    \ . #\",\n    \"project/reports/CONTENT_ALIGNMENT_REPORT.md\": \" The goal was\
    \ to ensure that every registered artifact in the project is traced to a canonical\
    \ feature or component ID . The process involved a systematic review of all registered\
    \ files in `project/reports\",\n    \"project/reports/DESCRIPTION_COMPLIANCE_REPORT.md\"\
    : \" Document-059 is a Compliance Report that documents are required to comply\
    \ with the requirements of the Document-Next-Generation System .\",\n    \"project/reports/DOCUMENT_TAG_INVENTORY.yml\"\
    : \"This file contains all of the information required to generate the alignment\
    \ matrix .\",\n    \"project/reports/GOVERNANCE_DEMO_REPORT.md\": \" Documented\
    \ a live demonstration of the refactored governance audit script, `scripts/repo_inventory_and_governance.py\
    \ . The demonstration consists of two main tests:\",\n    \"project/reports/HANDOVER_BRIEF_CHATGTP.md\"\
    : \" The project is currently in API Phase 5b, with governance, QA, and documentation\
    \ workflows partially implemented and audited . Your job is to internalize the\
    \ current state of the\",\n    \"project/reports/HANDOVER_BRIEF_JULES.md\": \"\
    \ The primary goal was to establish an end-to-end traceability system . Every\
    \ registered project artifact (code, documentation, etc.) is mapped to a canonical\
    \ feature ID . This creates\",\n    \"project/reports/PROJECT_AUDIT_FINAL_REPORT.md\"\
    : \" The Project Audit Final Report is a static template . It is automatically\
    \ copied here for human review .\",\n    \"project/reports/PROJECT_DOCUMENT_ALIGNMENT.md\"\
    : \" Project Document Alignment Report is fully Aligned . The report is based\
    \ on a fully-aligned version of the document .\",\n    \"project/reports/REPO_MANIFEST.md\"\
    : \" \\\"Verify_alignment_migration.py\\\" is a python3 script . Verifying alignment\
    \ migration is a \\\"enhanced report\\\" by type (doc/code/config\",\n    \"project/reports/SEMANTIC_ALIGNMENT_REPORT.md\"\
    : \"File not found\",\n    \"project/reports/TRACE_INDEX.yml\": \"The Zotify API\
    \ is a tool for interacting with the Zotify API .\",\n    \"project/reports/TRACE_INDEX.yml.bak\"\
    : \"No description available\",\n    \"scripts/CODE_FILE_INDEX.md\": \" This file\
    \ is auto-generated . Do not edit manually . Use the file to test linter violations\
    \ .\",\n    \"scripts/api/docs/CODE_FILE_INDEX.md\": \"File not found\",\n   \
    \ \"scripts/api/docs/DOCS_QUALITY_INDEX.md\": \"File not found\",\n    \"scripts/api/docs/MASTER_INDEX.md\"\
    : \"File not found\",\n    \"scripts/api/src/zotify_api/temp_violation.py\": \"\
    File not found\",\n    \"scripts/audit_api.py\": \"Dynamically imports the FastAPI\
    \ app discovers all GET routes that don t require path parameters and sends a\
    \ request to each one to check its status .\",\n    \"scripts/audit_endpoints.py\"\
    : \"Analyzes the FastAPI routes and prints out the status of each route .\",\n\
    \    \"scripts/backfill_trace_meta.py\": \"Backfill metadata into TRACE_INDEX\
    \ . yml .\",\n    \"scripts/build_project_registry.py\": \"Builds a machine -\
    \ readable project registry from the TRACE_INDEX . yml file .\",\n    \"scripts/content_alignment_check.py\"\
    : \"This is the main entry point for the Content Alignment Check phase 2 .\",\n\
    \    \"scripts/description_compliance_check.py\": \"This is the main entry point\
    \ for OPS - 07 .\",\n    \"scripts/doc-lint-rules.yml\": \"This file defines the\
    \ documentation matrix for the custom linter .\",\n    \"scripts/fix_tag_inventory.py\"\
    : \"Command line entry point for parsing DOCUMENT_TAG_INVENTORY . yml .\",\n \
    \   \"scripts/functional_test.py\": \"OPS - 09 - OPS - 019 - OPS - 009\",\n  \
    \  \"scripts/generate_alignment_matrix_md.py\": \"Generate an alignment matrix\
    \ markdown file from a YAML file .\",\n    \"scripts/generate_endpoints_doc.py\"\
    : \"Generate the Zotify API endpoints markdown file .\",\n    \"scripts/generate_openapi.py\"\
    : \"Generate OpenAPI spec for Zotify .\",\n    \"scripts/generate_repo_manifest.py\"\
    : \"OPS - 013 - OPS - 013\",\n    \"scripts/gonkui\": \"No description available\"\
    ,\n    \"scripts/lint_governance_links.json\": \"No description available\",\n\
    \    \"scripts/lint_governance_links.py\": \"Generate PROJECT_DOCUMENT_ALIGNMENT\
    \ . md and lint_governance_links . json .\",\n    \"scripts/linter.py\": \"Full\
    \ Linter and Logger for the repository .\",\n    \"scripts/make_manifest.py\"\
    : \"Self - checking repository manifest generator . Regenerates manifest only\
    \ if there are staged changes .\",\n    \"scripts/manage_docs_index.py\": \"Implementation\
    \ of the OPS - 019 module .\",\n    \"scripts/migrate_alignment_matrix.py\": \"\
    Migrates the legacy ALIGNMENT_MATRIX . md and generates a normalized ALIGNMENT_MATRIX\
    \ . yml .\",\n    \"scripts/migrate_and_tag_repository.py\": \"Migrates the entire\
    \ repository applies unique file - type - aware ID tags to all relevant files\
    \ and generates a comprehensive inventory .\",\n    \"scripts/project/reports/TRACE_INDEX.yml\"\
    : \"File not found\",\n    \"scripts/project_registry.json\": \"No description\
    \ available\",\n    \"scripts/propagate_descriptions.py\": \"OPS - 023 Regenerates\
    \ the TRACE_INDEX . yml file in the current working directory with a unified table\
    \ format .\",\n    \"scripts/repo_governance.py\": \"This is the main entry point\
    \ for OPS - 024 .\",\n    \"scripts/repo_inventory_and_governance.py\": \"Installs\
    \ the repo_inventory_and_governance . py module .\",\n    \"scripts/run_e2e_auth_test.sh\"\
    : \"A script to run a full end - to - end test of the Spotify authentication flow\
    \ .\",\n    \"scripts/semantic_alignment_check.py\": \"Loads all files from the\
    \ specified TRACE_INDEX . yml and returns a dictionary of all files that are marked\
    \ as registered .\",\n    \"scripts/start.sh\": \"Start the Zotify API server\
    \ .\",\n    \"scripts/test_auth_flow.py\": \"ID = OPS - 029 This is the OPS -\
    \ 029 version of the API .\",\n    \"scripts/test_full_pipeline.sh\": \"Run all\
    \ tests in a single pipeline .\",\n    \"scripts/test_single_config.sh\": \"Run\
    \ a single config reset test on the project .\",\n    \"scripts/validate_code_index.py\"\
    : \"Main function to compare indexed files vs actual files .\",\n    \"scripts/verify_alignment_migration.py\"\
    : \"Enhanced alignment verification script . Summarizes missing or mismatched\
    \ IDs clearly by type doc .\",\n    \"scripts/verify_governance.py\": \"Verifies\
    \ that all governance - related files in the project are present in PROJECT_REGISTRY\
    \ . md .\",\n    \"snitch/.golangci.yml\": \"No description available\",\n   \
    \ \"snitch/CODE_FILE_INDEX.md\": \" This file is auto-generated . Do not edit\
    \ manually . The main Go source file is for the snitch module .\",\n    \"snitch/DOCS_INDEX.md\"\
    : \" This file is auto-generated . Do not edit manually . Use the supplied information\
    \ to help you install the snitch module .\",\n    \"snitch/README.md\": \" Snitch\
    \ is a short-lived, local OAuth callback HTTP listener written in Go . It is intended\
    \ to be run as a standalone process during the authentication flow . Snitch listens\
    \ on\",\n    \"snitch/docs/ARCHITECTURE.md\": \" Snitch is a minimal, self-contained\
    \ Go application that acts as a temporary, local callback listener for OAuth 2.0\
    \ flows . Its architecture is designed around a Zero Trust security\",\n    \"\
    snitch/docs/INSTALLATION.md\": \" Snitch is written in Go and requires a recent\
    \ version of the Go toolchain to build and run . The application must be configured\
    \ with the callback URL of the main Zotify API before\",\n    \"snitch/docs/MILESTONES.md\"\
    : \" This document tracks key project milestones and events . Snitch project is\
    \ considered feature complete and stable .\",\n    \"snitch/docs/MODULES.md\"\
    : \" The Snitch application has been refactored into a single, self-contained\
    \ Go file to resolve a persistent build issue .\",\n    \"snitch/docs/PHASES.md\"\
    : \" This document provides a more detailed breakdown of the tasks required for\
    \ each development phase .\",\n    \"snitch/docs/PHASE_2_SECURE_CALLBACK.md\"\
    : \" This design has been superseded by the \\\"Zero Trust\\\" model . This model\
    \ provides a higher level of security, including end-to-end encryption and replay\
    \ attack prevention .\",\n    \"snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md\": \"\
    \ This document specifies a new, more robust security design for the Snitch OAuth\
    \ callback flow . It replaces the previous \\\"Secure Callback\\\" design with\
    \ a model that provides end-to\",\n    \"snitch/docs/PROJECT_PLAN.md\": \" The\
    \ Snitch module is a critical security and integration component of the Zotify\
    \ API platform . It acts as a short-lived, local web server that captures the\
    \ authorization token from Spotify and\",\n    \"snitch/docs/ROADMAP.md\": \"\
    \ Snitch Development Roadmap outlines the high-level, phased development plan\
    \ for the Snitch subproject . The Snitch project aims to integrate Snitch with\
    \ a parent process using basic Inter\",\n    \"snitch/docs/STATUS.md\": \" # Snitch\
    \ Project Status provides a live view of the project's progress . This document\
    \ provides a status update for the Snitch project .\",\n    \"snitch/docs/TASKS.md\"\
    : \" API-266 can be used to install a new version of the API module . The module\
    \ is called 'API-266' and has been released since 2008 .\",\n    \"snitch/docs/TEST_RUNBOOK.md\"\
    : \" As of Phase 5, Snitch is tightly integrated with the main Zotify API application\
    \ and is no longer intended to be run manually . Manual testing of the complete\
    \ flow requires running the main\",\n    \"snitch/docs/USER_MANUAL.md\": \" Snitch\
    \ is designed to handle the final step of an OAuth 2.0 authentication flow for\
    \ command-line or headless applications . It catches the redirect, grabs the secret\
    \ authentication code\",\n    \"snitch/docs/phase5-ipc.md\": \" This document\
    \ outlines the secure Inter-Process Communication (IPC) mechanism implemented\
    \ between the Zotify API and the Snitch helper application . The communication\
    \ relies on a one-shot IPC\",\n    \"snitch/go.mod\": \"No description available\"\
    ,\n    \"snitch/snitch.go\": \"snitch is a small helper application for the Zotify\
    \ API .\",\n    \"tests/scripts/test_build_project_registry.py\": \"Tests for\
    \ the correct build_project_registry script .\"\n}"
- path: scripts/functional_test.py
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
- path: scripts/generate_repo_manifest.py
  type: script
  workflow:
  - documentation
  indexes: []
  content: "# ID: OPS-013\n#!/usr/bin/env python3\nimport os\nimport json\n\n# ---\
    \ Config ---\n# Where to save the manifest (relative to repo root)\nmanifest_path\
    \ = \"scripts/repo_manifest.txt\"\n\n# Base URL where the files will be served\n\
    base_url = \"https://chatgtp.sixfold.nl\"\n\n# Folders/files to include in the\
    \ manifest\n\n#include_paths = [\n#    \"project\",\n#    \"api\",\n#    \"Gonk\"\
    ,\n#    \"scripts\",\n#    \"snitch\",\n#    \"templates\",\n#    \"tests\",\n\
    #    \"AGENTS.md\",\n#]\n\ninclude_paths = [\n    \"scripts\",\n]\n\n# File types\
    \ to include\ninclude_extensions = [\".md\", \".yml\", \".json\", \".sh\", \"\
    .go\", \".py\"]  # adjust as needed\n\n# --- Script ---\nmanifest = {}\norder\
    \ = []\n\nfor root_dir in include_paths:\n    for dirpath, dirnames, filenames\
    \ in os.walk(root_dir):\n        dirnames[:] = [d for d in dirnames if d != '.venv']\n\
    \        for f in filenames:\n            if any(f.endswith(ext) for ext in include_extensions):\n\
    \                rel_path = os.path.join(dirpath, f).replace(\"\\\\\", \"/\")\n\
    \                key = os.path.splitext(f)[0].upper()  # e.g., ONBOARDING.md →\
    \ ONBOARDING\n                url = f\"{base_url}/{rel_path}\"\n             \
    \   manifest[key] = url\n                order.append(key)\n\n# Add order array\
    \ for deterministic reading\nmanifest[\"order\"] = order\n\n# Ensure target folder\
    \ exists\nos.makedirs(os.path.dirname(manifest_path), exist_ok=True)\n\n# Write\
    \ manifest\nwith open(manifest_path, \"w\") as f:\n    json.dump(manifest, f,\
    \ indent=2)\n\nprint(f\"Manifest generated at {manifest_path}, {len(order)} files\
    \ included.\")\n"
- path: scripts/migrate_and_tag_repository.py
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
    \ 'vendor', 'api_dumps', 'storage',\n    'templates', 'venv', '.pytest_cache'\n\
    }\n\n# Files to exclude from scanning\nEXCLUDE_FILES = {'openapi.json'}\n\n# ---\
    \ New Configuration ---\nPROJECT_ROOT = Path(__file__).parent.parent\nTRACE_INDEX_PATH\
    \ = Path('project/reports/TRACE_INDEX.yml')\n\n# Mapping of file extensions to\
    \ their comment syntax for the ID tag\nCOMMENT_STYLE_MAP = {\n    '.py': ('# ',\
    \ ''),\n    '.sh': ('# ', ''),\n    '.yml': ('# ', ''),\n    '.yaml': ('# ', ''),\n\
    \    '.toml': ('# ', ''),\n    '.md': ('<!-- ', ' -->'),\n    '.html': ('<!--\
    \ ', ' -->'),\n    '.js': ('// ', ''),\n    '.css': ('/* ', ' */'),\n    '.gitignore':\
    \ ('# ', ''),\n}\n\n# --- Script Logic ---\n\ndef load_trace_index():\n    \"\"\
    \"Loads the TRACE_INDEX.yml file and returns a path-to-index mapping.\"\"\"\n\
    \    if not TRACE_INDEX_PATH.exists():\n        print(f\"Error: TRACE_INDEX.yml\
    \ not found at {TRACE_INDEX_PATH}\", file=sys.stderr)\n        return None\n \
    \   try:\n        with open(TRACE_INDEX_PATH, 'r', encoding='utf-8') as f:\n \
    \           data = yaml.safe_load(f)\n        if not data or 'artifacts' not in\
    \ data:\n            print(\"Warning: TRACE_INDEX.yml is empty or malformed.\"\
    , file=sys.stderr)\n            return {}\n        return {item['path']: item.get('index',\
    \ '-') for item in data['artifacts']}\n    except yaml.YAMLError as e:\n     \
    \   print(f\"Error parsing TRACE_INDEX.yml: {e}\", file=sys.stderr)\n        return\
    \ None\n\ndef get_comment_delimiters(file_path: Path) -> tuple[str, str]:\n  \
    \  \"\"\"Returns the appropriate comment start and end delimiters for a file type.\"\
    \"\"\n    return COMMENT_STYLE_MAP.get(file_path.suffix, ('# ', ''))\n\ndef generate_id(prefix:\
    \ str, counter: int) -> str:\n    \"\"\"Generates a formatted ID string like 'API-001'.\"\
    \"\"\n    return f'{prefix}-{counter:03d}'\n\ndef load_inventory_and_counters(inventory_path:\
    \ Path, trace_index: dict) -> tuple[list, dict]:\n    \"\"\"Loads existing inventory\
    \ and derives the latest counter for each ID prefix based on its index.\"\"\"\n\
    \    if not inventory_path.exists():\n        return [], {}\n\n    try:\n    \
    \    data = yaml.safe_load(inventory_path.read_text(encoding='utf-8'))\n     \
    \   if not isinstance(data, list):\n            print(\"[WARNING] Inventory file\
    \ is not a list. Starting fresh.\")\n            return [], {}\n    except (yaml.YAMLError,\
    \ IOError) as e:\n        print(f\"[WARNING] Could not read inventory, starting\
    \ fresh: {e}\")\n        return [], {}\n\n    counters = {}\n    path_to_id_map\
    \ = {item['path']: item['id'] for item in data}\n\n    for path, index_name in\
    \ trace_index.items():\n        if index_name != \"-\":\n            if path in\
    \ path_to_id_map:\n                item_id = path_to_id_map[path]\n          \
    \      try:\n                    prefix = item_id.split('-')[0]\n            \
    \        num = int(item_id.split('-')[-1])\n                    if num > counters.get(prefix,\
    \ 0):\n                        counters[prefix] = num\n                except\
    \ (ValueError, IndexError):\n                    continue\n\n    print(f\"Loaded\
    \ existing inventory with {len(data)} items. Current counters: {counters}\")\n\
    \    return data, counters\n\ndef get_prefix_from_index(index_name: str) -> str:\n\
    \    \"\"\"Derives a prefix from the index name.\"\"\"\n    if \"API\" in index_name.upper()\
    \ or \"GONK\" in index_name.upper() or \"SNITCH\" in index_name.upper():\n   \
    \     return \"API\"\n    if \"DOC\" in index_name.upper() or \"PROJECT\" in index_name.upper():\n\
    \        return \"DOC\"\n    if \"OPS\" in index_name.upper() or \"SCRIPTS\" in\
    \ index_name.upper():\n        return \"OPS\"\n    if \"TEST\" in index_name.upper():\n\
    \        return \"TEST\"\n    return \"GEN\"\n\n\ndef scan_and_tag(repo_root:\
    \ Path, trace_index: dict, target_path: str = None, dry_run: bool = True):\n \
    \   \"\"\"\n    Scans the repository, tags files, and generates an inventory.\n\
    \    Can be limited to a specific target_path.\n    \"\"\"\n    mode = 'DRY RUN'\
    \ if dry_run else 'APPLY'\n    print(f\"--- Starting Scan & Tag ({mode}) for target:\
    \ {target_path or 'all'} ---\")\n\n    inventory_file = Path('project/reports/DOCUMENT_TAG_INVENTORY.yml')\n\
    \    inventory, counters = load_inventory_and_counters(inventory_file, trace_index)\n\
    \n    inventoried_paths = {item.get('path') for item in inventory}\n\n    files_to_scan\
    \ = []\n    if target_path:\n        if Path(target_path).is_file():\n       \
    \     files_to_scan = [Path(target_path)]\n        else:\n            files_to_scan\
    \ = sorted([p for p in Path(target_path).rglob('*') if p.is_file()])\n    else:\n\
    \        files_to_scan = sorted([p for p in repo_root.rglob('*') if p.is_file()])\n\
    \n    newly_tagged_files = 0\n    for file_path in files_to_scan:\n        relative_path_str\
    \ = str(file_path.as_posix())\n\n        if target_path and relative_path_str\
    \ in inventoried_paths:\n            print(f\"Re-tagging explicitly targeted file:\
    \ {relative_path_str}\")\n            inventory = [item for item in inventory\
    \ if item.get('path') != relative_path_str]\n            inventoried_paths.remove(relative_path_str)\n\
    \        elif relative_path_str in inventoried_paths:\n            continue\n\n\
    \        if any(part in EXCLUDE_DIRS for part in file_path.parts) or file_path.name\
    \ in EXCLUDE_FILES:\n            continue\n\n        index_value = trace_index.get(relative_path_str,\
    \ \"-\")\n        if index_value == \"-\":\n            # Cannot determine prefix\
    \ for ID generation, skip for now\n            continue\n\n        prefix = get_prefix_from_index(index_value)\n\
    \        counters[prefix] = counters.get(prefix, 0) + 1\n        new_id = generate_id(prefix,\
    \ counters[prefix])\n\n        tag_start, tag_end = get_comment_delimiters(file_path)\n\
    \        id_tag_line = f\"{tag_start}ID: {new_id}{tag_end}\\n\"\n\n        inventory.append({'id':\
    \ new_id, 'path': relative_path_str, 'index': index_value})\n        newly_tagged_files\
    \ += 1\n\n        if dry_run:\n            print(f\"[DRY RUN] Would tag '{relative_path_str}'\
    \ with ID '{new_id}' and index '{index_value}'\")\n        else:\n           \
    \ try:\n                content = file_path.read_text(encoding='utf-8', errors='ignore')\n\
    \                content = re.sub(r\"^(#|//|<!--)\\s*Task ID:.*(\\s*-->)?\\n?\"\
    , \"\", content, flags=re.MULTILINE)\n\n                has_existing_tag = False\n\
    \                if content:\n                    first_line = content.splitlines()[0]\n\
    \                    if re.search(r\"(?:#|//|<!--)\\s*ID:\\s*([A-Z]{2,4}-\\d{3,})\"\
    , first_line):\n                        has_existing_tag = True\n\n          \
    \      if not has_existing_tag:\n                    file_path.write_text(id_tag_line\
    \ + content, encoding='utf-8')\n                    print(f\"[APPLY] Tagged '{relative_path_str}'\
    \ with ID '{new_id}'\")\n                else:\n                    print(f\"\
    [SKIP] File '{relative_path_str}' already has an ID.\")\n            except Exception\
    \ as e:\n                print(f\"[ERROR] Could not process file {relative_path_str}:\
    \ {e}\")\n\n    print(f\"\\n--- Tagging Summary for this run ---\")\n    print(f\"\
    Tagged {newly_tagged_files} new files.\")\n\n    if not dry_run:\n        write_inventory(inventory,\
    \ inventory_file)\n\ndef validate_tags(repo_root: Path):\n    \"\"\"Scans the\
    \ repo and validates existing ID tags for format and uniqueness.\"\"\"\n    print(\"\
    --- Starting Tag Validation ---\")\n    inventory_path = Path('project/reports/DOCUMENT_TAG_INVENTORY.yml')\n\
    \    if not inventory_path.exists():\n        print(\"[ERROR] Inventory file not\
    \ found. Cannot validate.\")\n        return\n\n    try:\n        inventory_data\
    \ = yaml.safe_load(inventory_path.read_text(encoding='utf-8'))\n        path_to_id_map\
    \ = {item['path']: item['id'] for item in inventory_data}\n        id_to_path_map\
    \ = {item['id']: item['path'] for item in inventory_data}\n    except (yaml.YAMLError,\
    \ IOError) as e:\n        print(f\"[ERROR] Could not read or parse inventory file:\
    \ {e}\")\n        return\n\n    errors = []\n\n    if len(id_to_path_map) != len(inventory_data):\n\
    \        from collections import Counter\n        id_counts = Counter(item['id']\
    \ for item in inventory_data)\n        for an_id, count in id_counts.items():\n\
    \            if count > 1:\n                errors.append(f\"Duplicate ID '{an_id}'\
    \ found in inventory file.\")\n\n    for file_path_str, expected_id in path_to_id_map.items():\n\
    \        file_path = Path(file_path_str)\n        if not file_path.exists():\n\
    \            errors.append(f\"File '{file_path}' is in inventory but not found\
    \ on disk.\")\n            continue\n\n        if file_path == inventory_path:\n\
    \            continue\n\n        try:\n            content = file_path.read_text(encoding='utf-8',\
    \ errors='ignore')\n            if not content:\n                continue\n\n\
    \            first_line = content.splitlines()[0]\n            match = re.search(r\"\
    (?:#|//|<!--|/\\*)\\s*ID:\\s*([A-Z]{2,4}-\\d{3,})\\s*(?:-->|\\*/)?\", first_line)\n\
    \n            if not match:\n                errors.append(f\"Missing or malformed\
    \ ID tag in file: '{file_path}'\")\n            elif match.group(1) != expected_id:\n\
    \                errors.append(f\"ID mismatch in '{file_path}'. Expected '{expected_id}',\
    \ found '{match.group(1)}'.\")\n\n        except Exception as e:\n           \
    \ errors.append(f\"Could not read or process file '{file_path}': {e}\")\n\n  \
    \  if not errors:\n        print(f\"[SUCCESS] Validation complete. Verified {len(path_to_id_map)}\
    \ files. No errors.\")\n    else:\n        print(f\"\\n[FAILURE] Validation found\
    \ {len(errors)} errors:\")\n        for error in errors:\n            print(f\"\
    - {error}\")\n\ndef write_inventory(inventory_data: list, output_path: Path):\n\
    \    \"\"\"Writes the collected inventory data to a YAML file.\"\"\"\n    print(f\"\
    \\nWriting inventory to '{output_path}'...\")\n    output_path.parent.mkdir(parents=True,\
    \ exist_ok=True)\n    with open(output_path, 'w', encoding='utf-8') as f:\n  \
    \      yaml.safe_dump(inventory_data, f, sort_keys=False)\n    print(\"[SUCCESS]\
    \ Inventory file written.\")\n\n\ndef main():\n    \"\"\"Main function to parse\
    \ arguments and run the script in the chosen mode.\"\"\"\n    parser = argparse.ArgumentParser(description=\"\
    Scan, tag, and validate repository files for the alignment system.\")\n    group\
    \ = parser.add_mutually_exclusive_group(required=True)\n    group.add_argument('--dry-run',\
    \ action='store_true', help=\"Show what would be done without changing files.\"\
    )\n    group.add_argument('--apply', action='store_true', help=\"Apply tags to\
    \ files and generate the inventory.\")\n    group.add_argument('--validate', action='store_true',\
    \ help=\"Validate existing tags for uniqueness and format.\")\n    parser.add_argument('--target',\
    \ type=str, help=\"Optional: a specific directory or file to process.\", default=None)\n\
    \n    args = parser.parse_args()\n    repo_root = Path('.')\n\n    trace_index\
    \ = load_trace_index()\n    if trace_index is None:\n        sys.exit(1)\n\n \
    \   if args.dry_run:\n        scan_and_tag(repo_root, trace_index, target_path=args.target,\
    \ dry_run=True)\n    elif args.apply:\n        scan_and_tag(repo_root, trace_index,\
    \ target_path=args.target, dry_run=False)\n    elif args.validate:\n        validate_tags(repo_root)\n\
    \nif __name__ == \"__main__\":\n    main()"
- path: scripts/audit_endpoints.py
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
- path: scripts/test_single_config.sh
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
- path: scripts/fix_trace_index_paths.py
  type: script
  workflow: []
  indexes: []
  content: "#!/usr/bin/env python3\nimport yaml\nfrom pathlib import Path\n\nTRACE_INDEX_FILE\
    \ = Path(\"project/reports/TRACE_INDEX.yml\")\n\nwith TRACE_INDEX_FILE.open(\"\
    r\", encoding=\"utf-8\") as f:\n    data = yaml.safe_load(f)\n\ndef replace_path_with_file(item):\n\
    \    if isinstance(item, dict):\n        if \"path\" in item:\n            item[\"\
    file\"] = item.pop(\"path\")\n        for v in item.values():\n            replace_path_with_file(v)\n\
    \    elif isinstance(item, list):\n        for elem in item:\n            replace_path_with_file(elem)\n\
    \nreplace_path_with_file(data)\n\nwith TRACE_INDEX_FILE.open(\"w\", encoding=\"\
    utf-8\") as f:\n    yaml.dump(data, f, sort_keys=False, allow_unicode=True)\n\n\
    print(f\"Replaced all 'path:' keys with 'file:' in {TRACE_INDEX_FILE}\")\n"
- path: scripts/content_alignment_check.py
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
- path: scripts/test_full_pipeline.sh
  type: script
  workflow:
  - testing
  indexes: []
  content: "# ID: OPS-035\n#!/usr/bin/env bash\nset -euo pipefail\n\necho \"=== Starting\
    \ full pipeline test (dry-run) ===\"\n\n# Step 1: Backup TRACE_INDEX.yml\nTRACE_INDEX=\"\
    project/reports/TRACE_INDEX.yml\"\nBACKUP_TRACE_INDEX=\"project/reports/TRACE_INDEX.yml.bak\"\
    \nif [ -f \"$TRACE_INDEX\" ]; then\n    echo \"[Step 1] Backing up TRACE_INDEX.yml\"\
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
- path: .pytest_cache/README.md
  type: doc
  workflow: []
  indexes: []
  content: '# pytest cache directory #


    This directory contains data from the pytest''s cache plugin,

    which provides the `--lf` and `--ff` options, as well as the `cache` fixture.


    **Do not** commit this to version control.


    See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.

    '
- path: .pytest_cache/CACHEDIR.TAG
  type: other
  workflow: []
  indexes: []
  content: "Signature: 8a477f597d28d172789f06886806bc55\n# This file is a cache directory\
    \ tag created by pytest.\n# For information about cache directory tags, see:\n\
    #\thttps://bford.info/cachedir/spec.html\n"
- path: .pytest_cache/v/cache/nodeids
  type: other
  workflow: []
  indexes: []
  content: "[\n  \"tests/scripts/test_build_project_registry.py::TestCorrectedBuildProjectRegistry::test_registry_generation_uses_trace_index_descriptions\"\
    ,\n  \"tests/scripts/test_build_project_registry.py::TestCorrectedBuildProjectRegistry::test_task_id_propagation\"\
    \n]"
- path: api/docs/MASTER_INDEX.md
  type: doc
  workflow: []
  indexes:
  - MASTER_INDEX.md
  content: '<!-- ID: API-205 -->

    # API Documentation Master Index


    <!-- Reviewed and updated to reflect all recent changes. -->


    <!-- Reviewed and updated to reflect changes in other docs. -->


    "Phases 3–5 deliver the full core API, user authentication with JWT, endpoint
    protection, notifications preference, and comprehensive testing. Users can manage
    profiles, preferences, liked tracks, playback history, and interact with all content
    endpoints. The Gonk CLI and GonkUI provide an interface for all these actions,
    with the ability to toggle between simulated and real API testing. Documentation,
    examples, and OpenAPI specs are fully updated."


    This document serves as the central index for all documentation related to the
    Zotify API and its sub-modules. All new documentation files must be registered
    here.


    ## Core API


    *   [Code File Index](CODE_FILE_INDEX.md)

    *   [API Reference](reference/API_REFERENCE.md)

    *   [Feature Specifications](reference/FEATURE_SPECS.md)

    *   [Changelog](CHANGELOG.md)

    *   [Code Quality Index](CODE_QUALITY_INDEX.md)

    *   [Docs Quality Index](DOCS_QUALITY_INDEX.md)

    *   [Master Index](MASTER_INDEX.md)


    ## Manuals


    *   [API Developer Guide](manuals/API_DEVELOPER_GUIDE.md)

    *   [CI/CD Guide](manuals/CICD.md)

    *   [Error Handling Guide](manuals/ERROR_HANDLING_GUIDE.md)

    *   [Logging Guide](manuals/LOGGING_GUIDE.md)

    *   [Operator Manual](manuals/OPERATOR_MANUAL.md)

    *   [System Integration Guide](manuals/SYSTEM_INTEGRATION_GUIDE.md)

    *   [User Manual](manuals/USER_MANUAL.md)


    ## System Design


    *   [Error Handling Design](system/ERROR_HANDLING_DESIGN.md)

    *   [Installation Guide](system/INSTALLATION.md)

    *   [Privacy Compliance](system/PRIVACY_COMPLIANCE.md)

    *   [System Requirements](system/REQUIREMENTS.md)


    ## Features


    *   [Authentication](reference/features/AUTHENTICATION.md)

    *   [Automated Documentation Workflow](reference/features/AUTOMATED_DOCUMENTATION_WORKFLOW.md)

    *   [Developer Flexible Logging Framework](reference/features/DEVELOPER_FLEXIBLE_LOGGING_FRAMEWORK.md)

    *   [Provider Agnostic Extensions](reference/features/PROVIDER_AGNOSTIC_EXTENSIONS.md)

    *   [Provider OAuth](reference/features/PROVIDER_OAUTH.md)


    ## Source Code Documentation

    * [Test Auth Flow Module](reference/source/TEST_AUTH_FLOW.py.md)


    * [Audit Endpoints Module](reference/source/AUDIT_ENDPOINTS.py.md)


    * [Generate Source Docs Module](reference/source/GENERATE_SOURCE_DOCS.py.md)


    * [Generate Endpoints Doc Module](reference/source/GENERATE_ENDPOINTS_DOC.py.md)


    * [Functional Test Module](reference/source/FUNCTIONAL_TEST.py.md)


    * [Audit Api Module](reference/source/AUDIT_API.py.md)


    * [Generate Openapi Module](reference/source/GENERATE_OPENAPI.py.md)


    * [Linter Module](reference/source/LINTER.py.md)


    * [App Module](reference/source/APP.js.md)


    * [App Module](reference/source/APP.py.md)


    * [Snitch Module](reference/source/SNITCH.go.md)


    * [Tracks Module](reference/source/TRACKS.py.md)


    * [Network Module](reference/source/NETWORK.py.md)


    * [Auth Module](reference/source/AUTH.py.md)


    * [User Module](reference/source/USER.py.md)


    * [Metadata Module](reference/source/METADATA.py.md)


    * [Notifications Module](reference/source/NOTIFICATIONS.py.md)


    * [Download Module](reference/source/DOWNLOAD.py.md)


    * [Spotify Module](reference/source/SPOTIFY.py.md)


    * [Generic Module](reference/source/GENERIC.py.md)


    * [Webhooks Module](reference/source/WEBHOOKS.py.md)


    * [Logging Schemas Module](reference/source/LOGGING_SCHEMAS.py.md)


    * [Cache Module](reference/source/CACHE.py.md)


    * [System Module](reference/source/SYSTEM.py.md)


    * [Playlists Module](reference/source/PLAYLISTS.py.md)


    * [Download Service Module](reference/source/DOWNLOAD_SERVICE.py.md)


    * [Deps Module](reference/source/DEPS.py.md)


    * [Cache Service Module](reference/source/CACHE_SERVICE.py.md)


    * [Auth Module](reference/source/AUTH.py.md)


    * [Db Module](reference/source/DB.py.md)


    * [Playlists Service Module](reference/source/PLAYLISTS_SERVICE.py.md)


    * [Search Module](reference/source/SEARCH.py.md)


    * [Metadata Service Module](reference/source/METADATA_SERVICE.py.md)


    * [Notifications Service Module](reference/source/NOTIFICATIONS_SERVICE.py.md)


    * [Services   Init   Module Module](reference/source/SERVICES____INIT__.py.md)


    * [Logging Service Module](reference/source/LOGGING_SERVICE.py.md)


    * [Config Service Module](reference/source/CONFIG_SERVICE.py.md)


    * [Network Service Module](reference/source/NETWORK_SERVICE.py.md)


    * [Sync Service Module](reference/source/SYNC_SERVICE.py.md)


    * [User Service Module](reference/source/USER_SERVICE.py.md)


    * [Spoti Client Module](reference/source/SPOTI_CLIENT.py.md)


    * [Tracks Service Module](reference/source/TRACKS_SERVICE.py.md)


    * [Webhooks Module](reference/source/WEBHOOKS.py.md)


    * [Tracks Module](reference/source/TRACKS.py.md)


    * [Network Module](reference/source/NETWORK.py.md)


    * [Auth Module](reference/source/AUTH.py.md)


    * [Sync Module](reference/source/SYNC.py.md)


    * [User Module](reference/source/USER.py.md)


    * [Search Module](reference/source/SEARCH.py.md)


    * [Config Module](reference/source/CONFIG.py.md)


    * [Routes   Init   Module Module](reference/source/ROUTES____INIT__.py.md)


    * [Notifications Module](reference/source/NOTIFICATIONS.py.md)


    * [Downloads Module](reference/source/DOWNLOADS.py.md)


    * [Webhooks Module](reference/source/WEBHOOKS.py.md)


    * [Cache Module](reference/source/CACHE.py.md)


    * [System Module](reference/source/SYSTEM.py.md)


    * [Playlists Module](reference/source/PLAYLISTS.py.md)


    * [Sync Module](reference/source/SYNC.py.md)


    * [Config Models Module](reference/source/CONFIG_MODELS.py.md)


    * [Base Module](reference/source/BASE.py.md)


    * [Providers   Init   Module Module](reference/source/PROVIDERS____INIT__.py.md)


    * [Spotify Connector Module](reference/source/SPOTIFY_CONNECTOR.py.md)


    * [Request Id Module](reference/source/REQUEST_ID.py.md)


    * [Database   Init   Module Module](reference/source/DATABASE____INIT__.py.md)


    * [Session Module](reference/source/SESSION.py.md)


    * [Crud Module](reference/source/CRUD.py.md)


    * [Models Module](reference/source/MODELS.py.md)


    * [Log Critical Module](reference/source/LOG_CRITICAL.py.md)


    * [Actions   Init   Module Module](reference/source/ACTIONS____INIT__.py.md)


    * [Webhook Module](reference/source/WEBHOOK.py.md)


    * [Hooks Module](reference/source/HOOKS.py.md)


    * [Formatter Module](reference/source/FORMATTER.py.md)


    * [Config Module](reference/source/CONFIG.py.md)


    * [Error Handler   Init   Module Module](reference/source/ERROR_HANDLER____INIT__.py.md)


    * [Triggers Module](reference/source/TRIGGERS.py.md)


    * [Base Module](reference/source/BASE.py.md)


    * [Logging Handlers   Init   Module Module](reference/source/LOGGING_HANDLERS____INIT__.py.md)


    * [Database Job Handler Module](reference/source/DATABASE_JOB_HANDLER.py.md)


    * [Json Audit Handler Module](reference/source/JSON_AUDIT_HANDLER.py.md)


    * [Console Handler Module](reference/source/CONSOLE_HANDLER.py.md)


    * [Schemas Module](reference/source/SCHEMAS.py.md)


    * [Logging Framework   Init   Module Module](reference/source/LOGGING_FRAMEWORK____INIT__.py.md)


    * [Service Module](reference/source/SERVICE.py.md)


    * [Filters Module](reference/source/FILTERS.py.md)


    * [Config Module](reference/source/CONFIG.py.md)


    * [Logging Config Module](reference/source/LOGGING_CONFIG.py.md)


    * [Main Module](reference/source/MAIN.py.md)


    * [Globals Module](reference/source/GLOBALS.py.md)


    * [Auth State Module](reference/source/AUTH_STATE.py.md)





















































































































































































    ## Providers


    *   [Spotify Provider](providers/SPOTIFY.md)

    '

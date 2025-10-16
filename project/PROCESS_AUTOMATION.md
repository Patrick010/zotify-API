# PROCESS_AUTOMATION.md — Updated for Trace NLP Integration and Semantic Governance (Phase 5c)

## 1. Overview

This document describes the automation processes that maintain **structural consistency**, **metadata accuracy**, and **traceability** across the repository.  
The goal is to ensure that **every artifact** — code, documentation, configuration, or test — is **discoverable, documented, and linked** to the correct indices automatically.

Automation ensures that the registry and trace systems evolve alongside the codebase without manual intervention.  
Each automated script is self-contained, validated, and interconnected through a shared data flow.

**Phase 5c updates:**  
- Integration of semantic enrichment via NLP modules.  
- Automated generation of contextual summaries for trace artifacts.  
- Alignment of NLP outputs with `ALIGNMENT_MATRIX.yml` and `DOCUMENT_TAG_INVENTORY.yml`.

---

## 2. Core Automation Scripts

Each automation module has a distinct purpose, a defined input/output relationship, and clear execution rules.  
These scripts collectively form the repository’s **documentation and governance backbone**.

---

### 2.1 `repo_inventory_and_governance.py`

**Purpose:**  
Scans the repository and generates the canonical trace index (`TRACE_INDEX.yml`).

**Functionality:**  
- Walks the entire project directory tree and records all relevant artifacts (code, docs, configs, tests, etc.).  
- Populates metadata fields: `type`, `registered`, and `meta` (including a generated `description` and `tags`).  
- Integrates with the **description generator** and NLP modules to produce meaningful, context-aware summaries for each file.  
- Ensures consistent ordering and formatting across all YAML entries.  

**Inputs:**  
- Repository filesystem.

**Outputs:**  
- `project/reports/TRACE_INDEX.yml` — the authoritative, machine-readable trace map of all repository artifacts.

**Execution Rules:**  
- Run in dry-run mode before committing changes.  
- Never manually edit `TRACE_INDEX.yml`; always regenerate through this script.  
- Automatically detects and adds newly created files.  

---

### 2.2 `build_project_registry.py`

**Purpose:**  
Converts the trace index into a human-readable registry (`PROJECT_REGISTRY.md`) for maintainers and auditors.

**Functionality:**  
- Translates structured metadata from `TRACE_INDEX.yml` into descriptive Markdown.  
- Maintains a consistent layout with hyperlinks, descriptions, and categories.  
- Aggregates related entries into grouped sections (by type or subsystem).  
- Updates descriptive summaries using the NLP description generator to ensure parity between index and registry.  

**Inputs:**  
- `project/reports/TRACE_INDEX.yml`

**Outputs:**  
- `project/PROJECT_REGISTRY.md`

**Execution Rules:**  
- Must run only after a successful `repo_inventory_and_governance.py` execution.  
- Regenerates all description text unless marked as `locked`.  
- Keeps the registry and index synchronized at all times.  

---

### 2.3 `repo_lint.py` / `lint_governance_links.py`

**Purpose:**  
Validates that all references, indices, and trace links remain accurate and up to date.

**Functionality:**  
- Cross-checks file references between the registry, alignment matrix, and trace index.  
- Verifies that all `meta.description` and `meta.tags` fields meet quality requirements.  
- Detects missing references, orphaned files, or structural drift.  
- Produces JSON and Markdown reports for auditing.  

**Inputs:**  
- `TRACE_INDEX.yml`  
- `PROJECT_REGISTRY.md`  
- All relevant code and documentation indices.

**Outputs:**  
- `project/reports/LINT_REPORT.json`  
- `project/reports/LINT_SUMMARY.md`

**Execution Rules:**  
- Part of the continuous validation pipeline.  
- Execution succeeds only if no inconsistencies or missing descriptions are detected.

---

## 3. Automation Modules

### Description & Semantic Enrichment Module (`trace_description_generator.py`)

**Purpose:**  
Automatically generates **context-aware semantic descriptions** for repository artifacts in `TRACE_INDEX.yml`.

**Trigger:**  
Invoked as part of the `repo_inventory_and_governance.py` workflow whenever `TRACE_INDEX.yml` is rebuilt.

**Logic Summary:**
1. For each file in `TRACE_INDEX.yml`, check for an existing description.
2. If present → retain it.
3. If absent → search related index files for existing descriptions:
   - `scripts/project_registry.json`
   - `api/docs/CODE_FILE_INDEX.md`
   - `api/docs/DOCS_QUALITY_INDEX.md`
   - `api/docs/CODE_QUALITY_INDEX.md`
   - `snitch/CODE_FILE_INDEX.md`
   - `snitch/DOCS_INDEX.md`
   - `Gonk/CODE_FILE_INDEX.md`
   - `Gonk/GonkUI/DOCS_INDEX.md`
4. If still absent → generate using **heuristic + NLP modules**:
   - **Python scripts (.py):** summarize input/output and functionality.  
   - **Markdown (.md):** summarize purpose or information conveyed.  
   - **Config files (.yml/.json):** summarize repository or CI/CD role.  
5. Store output in `trace_description_intermediate.json` before integration into governance matrix.

**Meaningful Description Criteria:**  
- Must capture **purpose and role**.  
- Concise (<120 characters), capitalized, ending with a period.  
- Avoid line-level details or literal code snippets.

**Update Policy:**  
- Re-evaluated automatically whenever `TRACE_INDEX.yml` is rebuilt.  
- Ensures new or updated artifacts always have meaningful semantic summaries.

---

### NLP Submodules

| Module | Purpose |
|--------|---------|
| `nlp/summarizer.py` | Produces file-level summaries using transformer models. |
| `nlp/description_builder.py` | Constructs structured semantic descriptions. |
| `nlp/tagger.py` | Assigns document IDs, prefixes, and semantic tags for alignment. |

**Runtime Environment:**  
- Python venv `.venv-nlp` with SpaCy and transformer models.  
- Future plan: caching models to reduce memory/swap usage in LXC environments.

---

## 4. Data Flow Overview

| Stage | Input | Process | Output | Notes |
|-------|--------|----------|---------|--------|
| 1 | Filesystem | `repo_inventory_and_governance.py` | `TRACE_INDEX.yml` | Canonical trace data, metadata, preliminary description |
| 2 | `TRACE_INDEX.yml` | `trace_description_generator.py` | `trace_description_intermediate.json` | Semantic summaries for all artifacts |
| 3 | `TRACE_INDEX.yml` + JSON | `build_project_registry.py` | `PROJECT_REGISTRY.md` | Human-readable registry with enriched descriptions |
| 4 | Both indices + matrix | `repo_lint.py` | `LINT_REPORT.json` / `LINT_SUMMARY.md` | Validation, audit trail, and QA |

This forms a **continuous documentation and governance pipeline**.

---

## 5. Automation Lifecycle

### Trigger Conditions
- **On-demand:** Manual execution for validation or regeneration.  
- **CI/CD Integration:** Recommended as pipeline stages:
  1. Inventory update  
  2. Semantic enrichment  
  3. Registry build  
  4. Lint validation  

### Expected Checkpoints
- `TRACE_INDEX.yml` contains all artifacts with valid descriptions.  
- `PROJECT_REGISTRY.md` mirrors the trace index and includes semantic summaries.  
- Lint reports must pass before any merge or release.

---

## 6. Maintenance & Extension

### Adding New Modules
1. Place script under appropriate subsystem (`scripts/`, `api/`, `snitch/`, `Gonk/`).  
2. Ensure automatic registration in the next trace inventory.  
3. Add purpose and category tags in the `meta` section.

### Adding New Tags or Categories
- Update taxonomy configuration in `repo_inventory_and_governance.py`.  
- Rebuild trace to propagate changes.

### Testing Changes
- Dry-run mode simulates updates without committing files.  
- Validate new automation logic with `repo_lint.py`.

---

### Final Notes

The system now incorporates **semantic enrichment** and **trace-based governance**.  
By embedding NLP description generation and validation into the automation cycle, repository documentation remains high-quality, discoverable, and aligned with governance matrices.  
The automation framework is fully extensible for future modules, new artifact types, and updated alignment rules.

# Alignment & Governance Audit Report

**Date:** 2025-10-21

---

## 1. Alignment Summary


| Metric                          | Count |
| ------------------------------- | ----- |
| Total Artifacts in Trace Index  | 374 |
| Total Artifacts in Tag Inventory| 341 |
| **Orphans** (in Trace, not Inv) | 43 |
| **Missing** (in Inv, not Trace) | 10 |
| Duplicate IDs in Inventory      | 0 |
| Mismatched IDs (Embedded vs Inv)| 0 |


### Details: Orphans (In Trace Index but not Tag Inventory)
- `.github/workflows/ci.yml`
- `.github/workflows/pushmirror.yml`
- `Gonk/GonkUI/static/app.js`
- `Gonk/GonkUI/static/styles.css`
- `nlp/__init__.py`
- `nlp/description_builder.py`
- `nlp/nlp_config.py`
- `nlp/nlp_engine.py`
- `nlp/summarizer.py`
- `nlp/summarizer_self_test.py`
- `nlp/tagger.py`
- `project/PROCESS_AUTOMATION.md`
- `project/REPOSITORY_TASK_DOCUMENT_MANAGEMENT_PLAN.md`
- `project/logs/ACTIVITY.md`
- `project/logs/CURRENT_STATE.md`
- `project/logs/SESSION_LOG.md`
- `project/logs/chat/File_linting_review.md`
- `project/logs/chat/File_linting_review_manifest.md`
- `project/logs/chat/Manifest_review_and_mapping.md`
- `project/logs/chat/Manifest_review_and_mapping_001.md`
- `project/logs/chat/Manifest_review_and_mapping_002.md`
- `project/logs/chat/Manifest_review_and_mapping_manifest.md`
- `project/logs/chat/Repo_Task_Doc_Mgmt_Step_2.md`
- `project/logs/chat/Repo_Task_Doc_Mgmt_Step_2_001.md`
- `project/logs/chat/Repo_Task_Doc_Mgmt_Step_2_002.md`
- `project/logs/chat/Repo_Task_Doc_Mgmt_Step_2_manifest.md`
- `project/logs/chat/chats.py`
- `project/logs/chat/combined_chats_manifest.md`
- `project/logs/handover/End of session HANDOVER_BRIEF_CHATGTP.md`
- `project/logs/handover/HANDOVER_BRIEF_CHATGTP_File_linting_review.md`
- `project/logs/handover/HANDOVER_BRIEF_CHATGTP_Trace_NLP_Integration_Phase_5c_Semantic_Governance_Alignment.md`
- `project/logs/handover/HANDOVER_BRIEF_CHATGTP_template.md`
- `project/reports/DOCUMENT_TAG_INVENTORY.yml`
- `project/reports/PROJECT_DOCUMENT_ALIGNMENT.md`
- `project/reports/TRACE_INDEX.yml`
- `scripts/backfill_trace_meta.py`
- `scripts/fix_trace_index_paths.py`
- `scripts/generate_descriptions.py`
- `scripts/generate_repo_manifest_md.py`
- `scripts/post_install.sh`
- `scripts/reorder_trace_index_keys.py`
- `scripts/trace_description_generator.py`
- `snitch/snitch.go`

### Details: Missing (In Tag Inventory but not Trace Index)
- `mkdocs.yml`
- `.pre-commit-config.yaml`
- `bandit.yml`
- `scripts/api/src/zotify_api/temp_violation.py`
- `snitch/mkdocs.yml`
- `snitch/.golangci.yml`
- `project/reports/SEMANTIC_ALIGNMENT_REPORT.md`
- `project/api/endpoints.yaml`
- `Gonk/GonkUI/mkdocs.yml`
- `api/docs/system/zotify-openapi-external-v1.yaml`

### Details: Duplicate IDs
- ``

---

## 2. Semantic Description Quality

Found 13 files with low-quality descriptions.

| File Path | Severity | Description Preview |
| --- | --- | --- |
| `Gonk/CODE_FILE_INDEX.md` | **NON-SEMANTIC** | `This file is auto-generated . Do not edit manually . Use this file to test the GonkCLI .` |
| `Gonk/GonkUI/DOCS_INDEX.md` | **NON-SEMANTIC** | `This file is auto-generated . Do not edit manually . Use the contents of the document to help you un` |
| `api/docs/CODE_FILE_INDEX.md` | **NON-SEMANTIC** | `Alembic environment script, configures and runs migrations . The file is auto-generated . Do not edi` |
| `api/docs/DOCS_QUALITY_INDEX.md` | **NON-SEMANTIC** | `API-204 is an index for documents related to code quality standards and reports . This file is auto-` |
| `project/logs/chat/File_linting_review.md` | **NON-SEMANTIC** | `No description available.` |
| `project/logs/chat/Manifest_review_and_mapping.md` | **NON-SEMANTIC** | `No description available.` |
| `project/logs/chat/Manifest_review_and_mapping_001.md` | **NON-SEMANTIC** | `No description available.` |
| `project/logs/chat/Manifest_review_and_mapping_002.md` | **NON-SEMANTIC** | `No description available.` |
| `project/logs/chat/Repo_Task_Doc_Mgmt_Step_2.md` | **NON-SEMANTIC** | `No description available.` |
| `scripts/CODE_FILE_INDEX.md` | **NON-SEMANTIC** | `This file is auto-generated . Do not edit manually . Use the file to test linter violations .` |
| `snitch/CODE_FILE_INDEX.md` | **NON-SEMANTIC** | `This file is auto-generated . Do not edit manually . The main Go source file is for the snitch modul` |
| `snitch/DOCS_INDEX.md` | **NON-SEMANTIC** | `This file is auto-generated . Do not edit manually . Use the supplied information to help you instal` |
| `api/src/zotify_api/schemas/user.py` | **WEAK** | `API - 084 API - 084` |


---

## 3. Tag & ID Consistency

- ID format error in `Gonk/CODE_FILE_INDEX.md`: Expected prefix `GONK-`, found `API-001`.
- Missing embedded ID in `project/PROJECT_REGISTRY.md`.
- Missing embedded ID in `project/PROCESS_AUTOMATION.md`.
- Missing embedded ID in `project/REPOSITORY_TASK_DOCUMENT_MANAGEMENT_PLAN.md`.
- ID format error in `scripts/CODE_FILE_INDEX.md`: Expected prefix `SCR-`, found `OPS-001`.
- ID format error in `snitch/DOCS_INDEX.md`: Expected prefix `SNITCH-`, found `API-254`.
- ID format error in `snitch/CODE_FILE_INDEX.md`: Expected prefix `SNITCH-`, found `API-253`.
- ID format error in `snitch/README.md`: Expected prefix `SNITCH-`, found `API-255`.
- Missing embedded ID in `templates/ONBOARDING.md`.
- Missing embedded ID in `templates/API-DEVELOPER-GUIDE.md`.
- Missing embedded ID in `templates/SECURITY.md`.
- Missing embedded ID in `templates/HANDOVER_BRIEF.md`.
- Missing embedded ID in `templates/LESSONS-LEARNT.md`.
- Missing embedded ID in `templates/PROJECT_REGISTRY.md`.
- Missing embedded ID in `templates/CICD-DEV.md`.
- Missing embedded ID in `templates/LOGGING_SYSTEM_DESIGN.md`.
- Missing embedded ID in `templates/FUTURE_ENHANCEMENTS.md`.
- Missing embedded ID in `templates/PID.md`.
- Missing embedded ID in `templates/TRACEABILITY_MATRIX.md`.
- Missing embedded ID in `templates/TASK_CHECKLIST.md`.
- Missing embedded ID in `templates/USECASES.md`.
- Missing embedded ID in `templates/PROJECT_BRIEF.md`.
- Missing embedded ID in `templates/BACKLOG.md`.
- Missing embedded ID in `templates/LOW_LEVEL_DESIGN.md`.
- Missing embedded ID in `templates/USECASES_GAP_ANALYSIS.md`.
- Missing embedded ID in `templates/LOGGING_PHASES.md`.
- Missing embedded ID in `templates/INITIATION.md`.
- Missing embedded ID in `templates/EXECUTION_PLAN.md`.
- Missing embedded ID in `templates/CICD-PROJ.md`.
- Missing embedded ID in `templates/HIGH_LEVEL_DESIGN.md`.
- Missing embedded ID in `templates/ROADMAP.md`.
- Missing embedded ID in `templates/ENDPOINTS.md`.
- Missing embedded ID in `templates/LOGGING_TRACEABILITY_MATRIX.md`.
- Missing embedded ID in `templates/SYSTEM-INTEGRATION-GUIDE.md`.
- Missing embedded ID in `templates/AGENTS.md`.
- ID format error in `Gonk/GonkUI/DOCS_INDEX.md`: Expected prefix `GONK-`, found `API-010`.
- ID format error in `Gonk/GonkUI/README.md`: Expected prefix `GONK-`, found `API-011`.
- ID format error in `Gonk/GonkCLI/DOCS_INDEX.md`: Expected prefix `GONK-`, found `API-002`.
- ID format error in `Gonk/GonkCLI/README.md`: Expected prefix `GONK-`, found `API-003`.
- ID format error in `Gonk/GonkUI/docs/CHANGELOG.md`: Expected prefix `GONK-`, found `API-014`.
- ID format error in `Gonk/GonkUI/docs/CONTRIBUTING.md`: Expected prefix `GONK-`, found `API-015`.
- ID format error in `Gonk/GonkUI/docs/ARCHITECTURE.md`: Expected prefix `GONK-`, found `API-013`.
- ID format error in `Gonk/GonkUI/docs/USER_MANUAL.md`: Expected prefix `GONK-`, found `API-017`.
- Missing embedded ID in `project/reports/PROJECT_DOCUMENT_ALIGNMENT.md`.
- Missing embedded ID in `project/reports/ALIGNMENT_AUDIT_2025-10-21.md`.
- ID format error in `snitch/docs/INSTALLATION.md`: Expected prefix `SNITCH-`, found `API-257`.
- ID format error in `snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md`: Expected prefix `SNITCH-`, found `API-262`.
- ID format error in `snitch/docs/MILESTONES.md`: Expected prefix `SNITCH-`, found `API-258`.
- ID format error in `snitch/docs/PHASE_2_SECURE_CALLBACK.md`: Expected prefix `SNITCH-`, found `API-261`.
- ID format error in `snitch/docs/ARCHITECTURE.md`: Expected prefix `SNITCH-`, found `API-256`.
- ID format error in `snitch/docs/STATUS.md`: Expected prefix `SNITCH-`, found `API-265`.
- ID format error in `snitch/docs/phase5-ipc.md`: Expected prefix `SNITCH-`, found `API-269`.
- ID format error in `snitch/docs/TEST_RUNBOOK.md`: Expected prefix `SNITCH-`, found `API-267`.
- ID format error in `snitch/docs/TASKS.md`: Expected prefix `SNITCH-`, found `API-266`.
- ID format error in `snitch/docs/PROJECT_PLAN.md`: Expected prefix `SNITCH-`, found `API-263`.
- ID format error in `snitch/docs/PHASES.md`: Expected prefix `SNITCH-`, found `API-260`.
- ID format error in `snitch/docs/MODULES.md`: Expected prefix `SNITCH-`, found `API-259`.
- ID format error in `snitch/docs/ROADMAP.md`: Expected prefix `SNITCH-`, found `API-264`.
- ID format error in `snitch/docs/USER_MANUAL.md`: Expected prefix `SNITCH-`, found `API-268`.
- Missing embedded ID in `templates/proposals/HOME_AUTOMATION_PROPOSAL.md`.
- Missing embedded ID in `templates/proposals/LOW_CODE_PROPOSAL.md`.
- Missing embedded ID in `templates/proposals/DYNAMIC_PLUGIN_PROPOSAL.md`.
- Missing embedded ID in `templates/proposals/MULTI_SOURCE_METADATA_PROPOSAL.md`.
- Missing embedded ID in `templates/audit/PHASE_1_TRACEABILITY_MATRIX.md`.
- Missing embedded ID in `templates/audit/HLD_LLD_ALIGNMENT_PLAN.md`.
- Missing embedded ID in `templates/audit/AUDIT_TRACEABILITY_MATRIX.md`.
- Missing embedded ID in `templates/audit/FIRST_AUDIT.md`.
- Missing embedded ID in `templates/audit/AUDIT-PHASE-1.md`.
- Missing embedded ID in `templates/audit/audit-prompt.md`.
- ID format error in `tests/scripts/test_linter.py`: Expected prefix `TEST-`, found `DOC-123`.

---

## 4. Governance Violations

This section audits project markdown files for their registration and linkage status.

### Fully Aligned
- `project/ALIGNMENT_MATRIX.md`

### Partially Aligned (Registered but not in an index)
None

### Unlinked (Present in Index but Marked `registered: false`)
- `project/ONBOARDING.md`
- `project/SECURITY.md`
- `project/LESSONS-LEARNT.md`
- `project/PROJECT_REGISTRY.md`
- `project/QA_GOVERNANCE.md`
- `project/LOGGING_SYSTEM_DESIGN.md`
- `project/PROCESS_AUTOMATION.md`
- `project/REPOSITORY_TASK_DOCUMENT_MANAGEMENT_PLAN.md`
- `project/FUTURE_ENHANCEMENTS.md`
- `project/PID.md`
- `project/TASK_CHECKLIST.md`
- `project/USECASES.md`
- `project/DEPENDENCIES.md`
- `project/PROJECT_BRIEF.md`
- `project/BACKLOG.md`
- `project/LOW_LEVEL_DESIGN.md`
- `project/PROJECT_PLAN.md`
- `project/USECASES_GAP_ANALYSIS.md`
- `project/LOGGING_PHASES.md`
- `project/EXECUTION_PLAN.md`
- `project/CICD.md`
- `project/HIGH_LEVEL_DESIGN.md`
- `project/ROADMAP.md`
- `project/LOGGING_TRACEABILITY_MATRIX.md`
- `project/process/GAP_ANALYSIS_TEMPLATE.md`
- `project/proposals/HOME_AUTOMATION_PROPOSAL.md`
- `project/proposals/LOW_CODE_PROPOSAL.md`
- `project/proposals/NEW_PROPOSAL.md`
- `project/proposals/DYNAMIC_PLUGIN_PROPOSAL.md`
- `project/proposals/GONKUI_PLUGIN.md`
- `project/proposals/TRACE_INDEX_SCHEMA_FIX.md`
- `project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md`
- `project/proposals/GOVERNANCE_AUDIT_REFACTOR.md`
- `project/proposals/DBSTUDIO_PLUGIN.md`
- `project/proposals/TRACE_INDEX_SCHEMA_ADAPTATION.md`
- `project/proposals/MULTI_SOURCE_METADATA_PROPOSAL.md`
- `project/reports/PROJECT_AUDIT_FINAL_REPORT.md`
- `project/reports/REPO_MANIFEST.md`
- `project/reports/HANDOVER_BRIEF_CHATGTP.md`
- `project/reports/CONTENT_ALIGNMENT_REPORT.md`
- `project/reports/GOVERNANCE_DEMO_REPORT.md`
- `project/reports/PROJECT_DOCUMENT_ALIGNMENT.md`
- `project/reports/DESCRIPTION_COMPLIANCE_REPORT.md`
- `project/reports/HANDOVER_BRIEF_JULES.md`
- `project/reports/ARCHIVE_ALIGNMENT_MATRIX_OLD.md`

### Unlinked (Not Found in Index)
- `project/reports/ALIGNMENT_AUDIT_2025-10-21.md`

---

## 5. Recommendations


- Run `scripts/repo_inventory_and_governance.py --full-scan` to resolve discrepancies between the file system and `TRACE_INDEX.yml`.
- Review files with low-quality descriptions to improve project clarity.
- Correct files with ID format errors or missing embedded IDs.
- For `Partially Aligned` files, ensure they are correctly added to a documentation index file.
- For files `Marked 'registered: false'`, decide if they should be officially governed and update their `registered` status in `TRACE_INDEX.yml` accordingly.


---
✅ Audit completed – no changes applied.
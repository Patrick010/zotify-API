<!-- ID: DOC-057 -->
# Proposal: Schema Fix for TRACE_INDEX.yml

**Date:** 2025-09-25
**Author:** Jules
**Status:** Proposed & Implemented

## 1. Problem Statement

The `TRACE_INDEX.yml` schema, while recently adapted for uniformity, could be more precise in its representation of registration status. The previous version listed all *expected* indexes for both registered and unregistered files, which could be ambiguous. A clearer distinction is needed between where a file *is* registered versus where it *should be* registered.

## 2. Proposed Solution

This document proposes and describes a "schema fix" for `TRACE_INDEX.yml` to make its reporting more precise and less ambiguous.

### 2.1. How It Works

The `repo_inventory_and_governance.py` script has been updated to enforce the following new schema rules:

1.  **`registered: true`:**
    *   The `index` field **must** list all index files where the artifact was actually found.
    *   The `missing_from` field is not present.

2.  **`registered: false`:**
    *   The `index` field is always `null` (represented as `-` in YAML), as the artifact is not considered registered anywhere.
    *   The `missing_from` field **must** list all expected index files where the artifact was not found.

3.  **`registered: exempted`:**
    *   The `index` field is always `null` (`-`), as there are no assigned indexes.

### Example of the New Schema:

```yaml
# Exempted file
- path: .gitignore
  type: exempt
  registered: exempted
  index: -

# Properly registered doc file
- path: api/docs/usage.md
  type: doc
  registered: true
  index:
    - api/docs/MASTER_INDEX.md
    - api/docs/DOCS_QUALITY_INDEX.md

# File with missing registrations
- path: api/src/zotify_api/main.py
  type: code
  registered: false
  index: -
  missing_from:
    - api/docs/CODE_FILE_INDEX.md
```

## 3. Benefits

-   **Reduced Ambiguity:** The schema now makes a clear distinction between found registrations and missing registrations.
-   **Improved Precision:** The `index` field accurately reflects the ground truth of where a file is currently registered.
-   **Enhanced Clarity:** It is now easier to see at a glance which files are fully registered, partially registered, or not registered at all.

## 4. High-Level Implementation Plan

The following changes were made to `scripts/repo_inventory_and_governance.py`:

1.  **Modified `check_registration`:** The function was updated to return two lists: `found_in` and `missing_from`.
2.  **Updated Main Loop:** The main loop was updated to populate the `index` and `missing_from` fields according to the new, stricter rules.
3.  **Added YAML Custom Representer:** A custom YAML representer was added to ensure that `None` values in Python are serialized to a dash (`-`) in the final YAML output, as per the specification.

## 5. Security Considerations

This change is a schema adaptation for a generated data file and has no direct security implications.

## 6. Architectural Impact

This change further refines the data integrity of the project's "Living Documentation" framework, making its primary data artifact, `TRACE_INDEX.yml`, a more precise and reliable source of truth.
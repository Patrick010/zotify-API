# Proposal: Refactor and Strengthen Governance Audit System

**Author:** Jules
**Date:** 2025-09-27
**Status:** Proposed

## 1. Abstract

This document proposes a significant refactoring of the repository's primary governance script, `scripts/repo_inventory_and_governance.py`. The goal is to elevate the script into a comprehensive, audit-ready tool that fully aligns with the project's "Living Documentation" policy. The changes will consolidate code indexing, introduce more precise file-type mapping, implement stub/placeholder detection, and generate a formal, detailed audit report.

## 2. Problem Statement

The current governance script is functional but has several limitations:
*   **Fragmented Indexing:** It relies on multiple, component-specific code indexes, making it difficult to get a holistic view of all code-related artifacts.
*   **Incomplete Reporting:** The script outputs its findings to the console, but does not produce a persistent, shareable audit report.
*   **Limited Detection:** It cannot identify placeholder files or wrongly categorized artifacts, allowing low-quality or misclassified files to go unnoticed.
*   **Outdated Rules:** The file classification rules do not accurately reflect the current project standards.

## 3. Proposed Solution

This refactor will address these issues by implementing the following enhancements:

1.  **Consolidate Code Indexing:** All code, script, and configuration files (`.py`, `.go`, `.sh`, `.yml`, `.json`, etc.) will be tracked in a single, canonical index: `api/docs/CODE_FILE_INDEX.md`. This simplifies the architecture and provides a single source of truth.
2.  **Update File Mappings:** The `FILETYPE_MAP` will be updated to the new standard, introducing more granular types like `script` and `config`.
3.  **Implement Stub Detection:** A new function will be added to identify and flag placeholder or stub files based on a clear set of criteria (file size, keywords, empty content).
4.  **Generate Enhanced Audit Report:** The script will produce a comprehensive, human-readable report in Markdown format, saved to `project/reports/GOVERNANCE_AUDIT_REPORT.md`. This report will detail the status of every file, including whether it is correctly indexed, miscategorized, or a stub.
5.  **Strengthen Verification:** The overall system will be more robust, providing a reliable mechanism for enforcing documentation and code quality standards across the repository.

## 4. Scope

This proposal covers the following:
*   Modifications to `scripts/repo_inventory_and_governance.py`.
*   Creation of a new, persistent audit report at `project/reports/GOVERNANCE_AUDIT_REPORT.md`.
*   Documentation of the new functionality via a demo report.

This proposal does **not** cover:
*   Fixing all the violations that the new script will uncover.
*   Changes to the `scripts/linter.py` integration, other than ensuring it continues to function correctly.

## 5. Justification

This refactor is a critical step in maturing the project's automated governance capabilities. It will provide the team with a powerful tool to maintain high standards for documentation and code quality, ensuring the "Living Documentation" model remains effective and sustainable. By creating a persistent, detailed audit trail, we enhance transparency and accountability.
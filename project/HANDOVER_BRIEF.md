# Handover Brief

**Project:** Zotify API Refactoring 
**Author:** Jules 
**Date:** 2025-09-03

## 1. Context
This document outlines the context and next steps for a major project enhancement: the implementation of a new, professional-level QA Gate.

The project currently uses a simple, ad-hoc linter (`scripts/linter.py`) that enforces documentation-related rules. While effective for its narrow purpose, it does not perform any deep code quality analysis (e.g., complexity checks, mutation testing) and lacks comprehensive checks for documentation content and alignment.

A new, detailed specification has been provided to complement this system with a much more robust, multi-language QA Gate that is run at the end of project phases.

## 2. Objective
The overall objective is to implement the full QA Gate as defined in the user's specification. This will provide a professional, reliable, and transparent quality enforcement system for the entire repository.

## 3. Current Status & Plan
Given the large scope of the new QA Gate, the decision was made to implement it in a structured, phased approach. I have created a comprehensive, multi-phase plan that breaks down the work into manageable chunks.

This plan is located at: **`project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md`**.

I have also created a high-priority task in the `project/BACKLOG.md` to kick off this work.

Phase 1 is completed and successfully established the foundational layer for code quality checks. The key deliverables from this phase include:

    scripts/qa_gate.py: The main entrypoint script for the QA Gate has been created.
    Code Quality Tooling: Checks for ruff (linting), pytest (testing and coverage), radon (complexity), and mutmut (mutation testing) have been integrated into the gate.
    Initial Documentation: The QA_GATE.md manual has been created to document the purpose and usage of the new system.
    Placeholder Scripts: Placeholders for future checks have been established.

The system is now ready for the next stage of development, which focuses on documentation.

## 4. Your Task: Begin Phase 2 - Documentation Quality Foundation

As per the master plan outlined in project/proposals/QA_GATE_IMPLEMENTATION_PLAN.md, the next logical step is to implement Phase 2. This phase is critical for enforcing the "Living Documentation" policy by creating a robust link between our source code and its documentation.

**Objective:**  
Implement a professional-level, system-wide documentation quality check as part of the QA Gate, ensuring that all source files have high-quality corresponding `.md` documentation and that quality indexes are maintained consistently.

**Important:**  
This QA Gate **does not replace the existing pre-commit linter**. The standard linter continues to run on every commit for immediate syntax and style feedback. The QA Gate is intended to run **at the end of a phase** (the "Code QA" task in the Execution Plan) or manually, for comprehensive verification of code and documentation quality.

---

## 1. Implement `check_docs_alignment.py`

**Purpose:**  
Scan all source files across the project (including `api/src/`, `snitch/`, `gonk-testUI/`, `scripts/`, and future modules) and ensure each has a corresponding, well-structured documentation file.

**Tasks:**

1. **Scan Source Files**
   - Include `.py`, `.go`, `.js`, `.ts`, `.sh`, `.html`.
   - Determine the expected `.md` file path using the deterministic naming convention:
     ```
     source_to_doc_filename(path) -> DOCS_ROOT / <UPPERCASE_PATH_WITH_DOUBLE_UNDERSCORES>.ext.md
     Example: snitch/core/main.py -> SNITCH__CORE__MAIN.py.md
     ```

2. **Check Documentation Existence**
   - Verify that a documentation file exists for each source file.
   - If missing, report as a failure in the QA Gate.

3. **Verify Content Quality**
   - Parse the `.md` file to ensure it contains required sections:
     - **Role & Purpose**
     - **Usage Examples**
     - **Public API Description**
     - Reference to all public functions/classes in the source file.
   - Enforce that all public functions/classes have non-empty docstrings.

4. **Migrate Existing Documentation (Optional)**
   - Identify existing `.md` files that do not follow the deterministic naming.
   - Move/rename them to the correct names.
   - Log any missing docs that need authoring.

---

## 2. Implement `check_quality_indexes.py`

**Purpose:**  
Maintain consistency of quality indexes and enforce reporting.

**Tasks:**

1. **Parse `CODE_QUALITY_INDEX.md`**
   - Ensure all source files are listed.
   - Verify ratings:
     - Readability (A–F)
     - Complexity (A–F)
     - Test Coverage (A–F)
     - Docs Completeness (A–F)
   - New files → start with `X` (unknown).
   - Fail if entry is missing or inconsistent with actual metrics.

2. **Parse `DOCS_QUALITY_INDEX.md`**
   - Ensure all `.md` documentation files are listed.
   - Verify ratings:
     - Clarity (A–F)
     - Completeness (A–F)
     - Accuracy (A–F)
   - New docs → start with `X` (unknown).
   - Fail if entry is missing or stale.

3. **Ensure Index Synchronization**
   - Confirm that all source files have corresponding documentation entries.
   - Confirm that all docs correspond to existing source files.

---

## 3. Integrate into `qa_gate.py`

**Tasks:**

- Update `run_docs_quality()` to call:
  ```python
  check_docs_alignment()
  check_quality_indexes()

    Run intelligently:

        Only trigger doc checks if relevant files (source code or documentation) have been modified.

        Ensure full validation on main branch merges or manual --all runs.

4. Deterministic Doc Filename Logic

def source_to_doc_filename(source_path: str) -> str:
    """
    Converts a source file path to the deterministic doc filename.
    Example:
        snitch/core/main.py -> SNITCH__CORE__MAIN.py.md
    """
    relative_path = source_path.replace(os.sep, "__").upper()
    return f"{relative_path}.md"

    Ensures one-to-one mapping between source files and docs.

    Avoids collisions.

    Allows the QA Gate to validate consistently across the project.

5. Documentation Updates

Update QA_GATE.md to include:

    Purpose and scope of Phase 2 documentation checks.

    Deterministic filename convention.

    Required sections for each .md file.

    How to resolve QA Gate errors for missing or low-quality documentation.

    Reference the new DOCS_QUALITY_INDEX.md rubric table.

Update MASTER_INDEX.md to register all existing and newly migrated .md files.
6. Execution Notes

    Run via QA Gate:

    python scripts/qa_gate.py --all

    CI/CD:

        Trigger doc checks only when doc or source files change.

        Full run on main branch merges.

Outcome

    All source files across the system have high-quality, structured documentation.

    Quality indexes (CODE_QUALITY_INDEX.md and DOCS_QUALITY_INDEX.md) remain consistent and complete.

    Ensures professional-level documentation across code and future modules.

    Maintains separation of concerns: QA Gate is a phase-end / manual check, while the pre-commit linter continues to enforce immediate syntax and style standards.


This plan fully integrates the **Phase 2 objectives**, **deterministic doc filenames**, **high-quality doc content checks**, and **index maintenance** in a system-wide, scalable approach. It avoids creating redundant enforcement scripts and ensures documentation quality will be verifiable in the QA Gate.

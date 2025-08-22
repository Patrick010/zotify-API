# HLD/LLD Alignment Plan

**Status:** Live Document

This document outlines the plan to align the High-Level Design (HLD) and Low-Level Design (LLD) with the current implementation of the Zotify project.

---

## Phase 1: Initial Audit & Reality Check (Done)

**Objective:** To establish a definitive baseline of the project's current state.
**Status:** ✅ Done

**Activities:**
- A comprehensive audit was performed, comparing the codebase against all available documentation.
- The `AUDIT_TRACEABILITY_MATRIX.md` was created to serve as the single source of truth for tracking alignment.

---

## Phase 2: Documentation Overhaul (Done)

**Objective:** To create a "single source of truth" by consolidating, archiving, and updating all project documentation.
**Status:** ✅ Done

**Activities:**
- All project documents were reviewed. Obsolete files were archived.
- Key documents like `HLD.md`, `LLD.md`, and `PID.md` were updated.
- The `PROJECT_REGISTRY.md` was created to track all official project documents.

---

## Phase 3: Implementation & Alignment (Done)

**Objective:** To implement missing features and align existing code with the design documents, based on the findings of the traceability matrix.
**Status:** ✅ Done

**Activities:**
- All features marked as `Exists? = N` in the `AUDIT_TRACEABILITY_MATRIX.md` were reviewed.
- Features that were in scope were implemented.
- Features that were out of scope were formally deferred and tracked in `FUTURE_ENHANCEMENTS.md`.
- All related documentation was updated to reflect the final state.

---

## Phase 4: Enforce & Automate (Ongoing)

**Objective:** To introduce and enforce a suite of quality gates and automation to prevent future design drift and maintain a high-quality codebase.
**Status:** 🏃 Ongoing

### Phase 4a: Technical Debt Remediation
**Objective:** Before implementing new quality gates, the existing codebase must be brought to a clean baseline by running and remediating findings from a suite of static analysis tools.
**Status:** 🏃 Ongoing

**Tasks:**
- [x] **`ruff` Linter Remediation:**
    - Run `ruff` linter and remediate all findings.
    - *Note: This task is complete. All 395 linting errors were fixed, and the test suite was stabilized.*
- [ ] **`mypy` Static Type Checking:**
    - Resolve any blockers (e.g., conflicting module names).
    - Run `mypy` and remediate all findings.
- [ ] **`bandit` Security Scan:**
    - Run `bandit` and remediate all critical/high-severity findings.
- [ ] **`safety` Dependency Scan:**
    - Run `safety` to check for insecure dependencies and remediate all findings.
- [ ] **`golangci-lint` for `snitch`:**
    - Run `golangci-lint` on the `snitch` microservice and remediate all findings.

### Phase 4b: CI/CD Hardening
**Objective:** To integrate the new quality gates into the CI/CD pipeline.
**Status:** 📝 To Do

**Tasks:**
- [ ] Add a `lint` job to the CI workflow (`ruff`, `golangci-lint`).
- [ ] Add a `type-check` job to the CI workflow (`mypy`).
- [ ] Add a `security-scan` job to the CI workflow (`bandit`, `safety`).
- [ ] Gate pull requests on the successful completion of all new jobs.

### Phase 4c: Custom Architectural & Documentation Linting
**Objective:** To automatically enforce the project's "living documentation" philosophy.
**Status:** 📝 To Do

**Tasks:**
- [ ] Develop a custom linting script to verify documentation changes alongside code changes.

### Phase 4d: Deep Code Review Process & Local Enforcement
**Objective:** To formalize the human review process and provide immediate local feedback.
**Status:** 📝 To Do

**Tasks:**
- [ ] Update `TASK_CHECKLIST.md` with a formal code review checklist.
- [ ] Implement `pre-commit` hooks for local, instant feedback.

---

## Phase 5: Ongoing Maintenance

**Objective:** To ensure the established quality gates and processes are maintained over the long term.
**Status:** 📝 To Do

**Tasks:**
- [ ] Use audit findings as triggers for spot updates in design docs.
- [ ] Keep the alignment matrix updated as a living artifact.
- [ ] Continue incremental updates as new features or refactors happen.

# Loose Ends Backlog

This document tracks design and documentation tasks that were discussed but never fully integrated into the repository.
Each item should be reviewed, documented, and closed out systematically.

---

## Done
1. **Code & Documentation Quality Ratings**
   - Status: **Done**
   - Integrated into repo docs (A/B/C rubric with objective + human criteria).
   - No further action needed.

2. **Snitch Integration (Base)**
   - Status: **Done (basic version exists)**

---

## Open Items

### 2. Gap Analysis Framework (Template + Skeleton)
- **Problem**: We drafted a combined skeleton+template form for gap analysis, so devs can be tasked with "Run a gap analysis and solve it. Use this form."
- **Status**: **Done**.
- **Action**: The template has been created at `project/process/GAP_ANALYSIS_TEMPLATE.md`. No further action needed.

---

### 3. Snitch OAuth Helper (Security Improvements)
- **Problem**: Current Snitch is basic. Browser ↔ helper comms are vulnerable to replay/sniffing attacks.
- **Action**: Update `snitch/PROJECT_PLAN.md` including:
  - **Goals**: Secure OAuth callback transport (ephemeral, authenticated, replay-resistant).
  - **Milestones**:
    1. Define secure comms mechanism (e.g. HMAC token exchange or mutual auth).
    2. Implement replay protection + TLS support.
    3. Add automated integration test with Zotify-API.
    4. Document usage in `snitch/README.md`.
  - **Roadmap**: Link into `roadmap.md` Phase 7 or next open milestone.

---

### 4. Roadmap File (Outdated)
- **Problem**: `roadmap.md` exists but content is outdated vs. actual phase progress.
- **Action**:
  - Compare `roadmap.md` with Next Steps/Phase Sequencing doc.
  - Rewrite `roadmap.md` to reflect current state (Phase 3 wrap-up, Phase 4 approval, Phase 6–7 work planned).
  - Add pointers to loose ends tracked here.

---

### 5. Privacy Compliance Documentation
- **Problem**: `PRIVACY_COMPLIANCE.md` exists but is sparse. Endpoints like `/privacy/data` were added, but not fully documented.
- **Action**:
  - Flesh out compliance doc: list implemented endpoints, describe data handling flow, add operator instructions.
  - Ensure `API Reference.md` reflects compliance endpoints.
  - Cross-link from `SECURITY_GUIDE.md` and `OPERATOR_GUIDE.md`.

---

## Meta
- This file (`LOOSE_ENDS_BACKLOG.md`) is temporary.
- Once each item is resolved, it should be removed and archived in `project/archive/` and marked fully **Done**.

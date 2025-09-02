# Alignment Matrix (Living Document)

**Purpose:**
This matrix maintains a live mapping between high-level design (HLD), low-level design (LLD), implementation, and reference documentation.
It must be updated with every feature, refactor, or documentation change.

---

## 1. Core Modules

| Module / Feature     | HLD Reference | LLD Reference | Code Path(s) | Documentation |
|----------------------|---------------|---------------|--------------|---------------|
| Track Service        | HIGH_LEVEL_DESIGN.md#track-service | LOW_LEVEL_DESIGN.md#track-service | api/src/zotify_api/services/tracks_service.py | api/docs/reference/API_REFERENCE.md#track-endpoints |
| Playlist Service     | …             | …             | api/src/zotify_api/services/playlists_service.py | … |
| Auth & OAuth Flow    | …             | …             | api/src/zotify_api/auth/ | project/SECURITY.md, HIGH_LEVEL_DESIGN.md#auth |
| Database Models      | …             | LOW_LEVEL_DESIGN.md#database | api/src/zotify_api/database/models.py | … |

---

## 2. Supporting Components

| Component            | HLD Reference | LLD Reference | Code Path(s) | Documentation |
|----------------------|---------------|---------------|--------------|---------------|
| Snitch Module        | HIGH_LEVEL_DESIGN.md#snitch | LOW_LEVEL_DESIGN.md#snitch | snitch/ | api/docs/modules/snitch.md |
| Gonk Test UI         | HIGH_LEVEL_DESIGN.md#gonk-testui | LOW_LEVEL_DESIGN.md#gonk-testui | gonk-testUI/ | api/docs/modules/gonk-testUI.md |
| Logging & Agents     | …             | …             | scripts/log-work.py | AGENTS.md |

---

## 3. Infrastructure & Tooling

| Area                 | HLD Reference | LLD Reference | Code Path(s) | Documentation |
|----------------------|---------------|---------------|--------------|---------------|
| CI/CD Pipeline       | HIGH_LEVEL_DESIGN.md#cicd | LOW_LEVEL_DESIGN.md#cicd | .github/workflows/ | project/CICD.md, api/docs/manuals/CICD.md |
| Linter & QA          | HIGH_LEVEL_DESIGN.md#qa | LOW_LEVEL_DESIGN.md#qa | scripts/lint-docs.py, doc-lint-rules.yml | project/DEVELOPER_GUIDE.md |

---

**Maintenance Rule:**
Whenever code under `api/src/zotify_api/`, `snitch/`, `gonk-testUI/`, or `scripts/` changes, this matrix must be updated to reflect the change. The linter enforces this as of Phase 5.

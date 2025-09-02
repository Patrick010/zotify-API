# Alignment Matrix (Living Document)

**Purpose:**
This matrix maintains a live mapping between high-level design (HLD), low-level design (LLD), implementation, and reference documentation.
It must be updated with every feature, refactor, or documentation change.

---

## 1. Core Modules

| Module / Feature     | HLD Reference | LLD Reference | Code Path(s) | Documentation |
|----------------------|---------------|---------------|--------------|---------------|
| Track Service        | [HLD §3](HIGH_LEVEL_DESIGN.md#3-architecture-overview) | [LLD §Tracks](LOW_LEVEL_DESIGN.md#tracks) | `api/src/zotify_api/services/tracks_service.py` | `api/docs/reference/API_REFERENCE.md#tracks` |
| Playlist Service     | [HLD §3](HIGH_LEVEL_DESIGN.md#3-architecture-overview) | [LLD §Playlists](LOW_LEVEL_DESIGN.md#playlists) | `api/src/zotify_api/services/playlists_service.py` | `api/docs/reference/API_REFERENCE.md#playlists` |
| Auth & OAuth Flow    | [HLD §3](HIGH_LEVEL_DESIGN.md#3-architecture-overview) | [LLD §Auth](LOW_LEVEL_DESIGN.md#auth) | `api/src/zotify_api/routes/auth.py`, `api/src/zotify_api/services/auth.py` | `project/SECURITY.md`, `HIGH_LEVEL_DESIGN.md#7-security-model` |
| Database Models      | [HLD §3](HIGH_LEVEL_DESIGN.md#3-architecture-overview) | [LLD §Database](LOW_LEVEL_DESIGN.md#unified-database-architecture) | `api/src/zotify_api/database/models.py` | `project/LOW_LEVEL_DESIGN.md#unified-database-architecture` |

---

## 2. Supporting Components

| Component            | HLD Reference | LLD Reference | Code Path(s) | Documentation |
|----------------------|---------------|---------------|--------------|---------------|
| Snitch Module        | [HLD §3.1](HIGH_LEVEL_DESIGN.md#31-supporting-modules) | [LLD §Snitch](LOW_LEVEL_DESIGN.md#snitch) | `snitch/` | `snitch/docs/` |
| Gonk Test UI         | [HLD §3.1](HIGH_LEVEL_DESIGN.md#31-supporting-modules) | [LLD §Gonk-TestUI](LOW_LEVEL_DESIGN.md#gonk-testui) | `gonk-testUI/` | `gonk-testUI/docs/` |
| Logging & Agents     | [HLD §3.3](HIGH_LEVEL_DESIGN.md#33-flexible-logging-framework) | [LLD §Agents](LOW_LEVEL_DESIGN.md#agents) | `scripts/log-work.py` | `AGENTS.md` |

---

## 3. Infrastructure & Tooling

| Area                 | HLD Reference | LLD Reference | Code Path(s) | Documentation |
|----------------------|---------------|---------------|--------------|---------------|
| CI/CD Pipeline       | [HLD §6](HIGH_LEVEL_DESIGN.md#6-deployment-model) | [LLD §CI/CD](LOW_LEVEL_DESIGN.md#cicd) | `.github/workflows/` | `project/CICD.md`, `api/docs/manuals/CICD.md` |
| Linter & QA          | [HLD §5](HIGH_LEVEL_DESIGN.md#5-documentation-governance) | [LLD §QA](LOW_LEVEL_DESIGN.md#qa) | `scripts/lint-docs.py`, `scripts/doc-lint-rules.yml` | `api/docs/manuals/API_DEVELOPER_GUIDE.md` |

---

**Maintenance Rule:**
Whenever code under `api/src/zotify_api/`, `snitch/`, `gonk-testUI/`, or `scripts/` changes, this matrix must be updated to reflect the change. The linter enforces this as of Phase 5.

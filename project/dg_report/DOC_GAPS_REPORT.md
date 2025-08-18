# Documentation Gaps & Inconsistencies Report

_Generated on 2025-08-17T15:55:53.735654Z_

## Summary Metrics

- **Total Files**: 97
- **By Category**: {'project': 48, 'snitch': 21, 'api-docs': 17, 'gonk': 11}
- **Has Endpoints Md**: False
- **Unique Endpoints Detected**: 350
- **Unique Paths Detected**: 334
- **Missing Required Files**: ['docs/reference/ENDPOINTS.md', 'project/audit/TRA
CEABILITY_MATRIX.md', 'project/COMPLETE_DOCS_FOR_ANALYSIS.json']
- **Missing References Count**: 183
- **Snitch Mentions**: 41
- **Gonk Mentions**: 24
- **Logging Mentions**: 30

## Top Missing References

| Referenced File | # Sources Referencing | Example Sources |
|---|---:|---|
| `docs/projectplan/task_checklist.md` | 8 | TASK_CHECKLIST.md, AUDIT-phase-1.md
, FIRST_AUDIT.md, 20250808-oauth-unification-completion-report.md, 20250809-api-
endpoints-completion-report.md |
| `docs/projectplan/security.md` | 7 | TASK_CHECKLIST.md, AUDIT-PHASE-3.md, AUDI
T-phase-1.md, 20250808-comprehensive-auth-and-docs-update-report.md, 20250809-ph
ase5-final-cleanup-report.md |
| `docs/roadmap.md` | 7 | TASK_CHECKLIST.md, AUDIT-phase-1.md, FIRST_AUDIT.md, 2
0250809-phase5-endpoint-refactor-report.md, 20250809-phase5-final-cleanup-report
.md |
| `docs/projectplan/next_steps_and_phases.md` | 6 | AUDIT-phase-1.md, FIRST_AUDI
T.md, 20250808-oauth-unification-completion-report.md, 20250809-phase5-final-cle
anup-report.md, 20250809-phase5-playlist-implementation-report.md |
| `api/docs/MANUAL.md` | 6 | AUDIT-phase-1.md, 20250807-doc-clarification-comple
tion-report.md, 20250808-comprehensive-auth-and-docs-update-report.md, 20250808-
oauth-unification-completion-report.md, 20250809-phase5-playlist-implementation-
report.md |
| `task_checklist.md` | 6 | LOW_LEVEL_DESIGN.md, LOW_LEVEL_DESIGN_previous.md, R
OADMAP.md, 20250808-oauth-unification-completion-report.md, 20250809-phase5-fina
l-cleanup-report.md |
| `docs/projectplan/spotify_fullstack_capability_blueprint.md` | 6 | AUDIT-phase
-1.md, FIRST_AUDIT.md, 20250807-spotify-blueprint-completion-report.md, 20250809
-phase5-final-cleanup-report.md, 20250809-phase5-playlist-implementation-report.
md |
| `docs/projectplan/spotify_capability_audit.md` | 6 | TASK_CHECKLIST.md, AUDIT-
phase-1.md, FIRST_AUDIT.md, 20250809-phase5-final-cleanup-report.md, 20250809-ph
ase5-playlist-implementation-report.md |
| `docs/projectplan/privacy_compliance.md` | 6 | TASK_CHECKLIST.md, AUDIT-phase-
1.md, FIRST_AUDIT.md, 20250809-phase5-final-cleanup-report.md, 20250809-phase5-p
laylist-implementation-report.md |
| `docs/projectplan/spotify_gap_alignment_report.md` | 5 | AUDIT-phase-1.md, FIR
ST_AUDIT.md, 20250809-phase5-final-cleanup-report.md, 20250809-phase5-playlist-i
mplementation-report.md, 20250809-phase5-search-cleanup-report.md |
| `docs/developer_guide.md` | 5 | AUDIT-phase-1.md, FIRST_AUDIT.md, 20250809-pha
se5-final-cleanup-report.md, 20250809-phase5-playlist-implementation-report.md,
20250809-phase5-search-cleanup-report.md |
| `docs/projectplan/HLD_Zotify_API.md` | 5 | AUDIT-phase-1.md, FIRST_AUDIT.md, 2
0250809-phase5-final-cleanup-report.md, 20250809-phase5-playlist-implementation-
report.md, 20250809-phase5-search-cleanup-report.md |
| `docs/projectplan/LLD_18step_plan_Zotify_API.md` | 5 | AUDIT-phase-1.md, FIRST
_AUDIT.md, 20250809-phase5-final-cleanup-report.md, 20250809-phase5-playlist-imp
lementation-report.md, 20250809-phase5-search-cleanup-report.md |
| `docs/projectplan/admin_api_key_mitigation.md` | 5 | TASK_CHECKLIST.md, AUDIT-
phase-1.md, 20250809-phase5-final-cleanup-report.md, 20250809-phase5-playlist-im
plementation-report.md, 20250809-phase5-search-cleanup-report.md |
| `docs/zotify-api-manual.md` | 4 | AUDIT-phase-1.md, 20250809-phase5-final-clea
nup-report.md, 20250809-phase5-playlist-implementation-report.md, 20250809-phase
5-search-cleanup-report.md |
| `github/ISSUE_TEMPLATE/bug-report.md` | 4 | AUDIT-phase-1.md, 20250809-phase5-
final-cleanup-report.md, 20250809-phase5-playlist-implementation-report.md, 2025
0809-phase5-search-cleanup-report.md |
| `docs/INTEGRATION_CHECKLIST.md` | 4 | AUDIT-phase-1.md, 20250809-phase5-final-
cleanup-report.md, 20250809-phase5-playlist-implementation-report.md, 20250809-p
hase5-search-cleanup-report.md |
| `docs/projectplan/roadmap.md` | 4 | AUDIT-phase-1.md, 20250809-phase5-final-cl
eanup-report.md, 20250809-phase5-playlist-implementation-report.md, 20250809-pha
se5-search-cleanup-report.md |
| `docs/operator_guide.md` | 4 | AUDIT-phase-1.md, 20250809-phase5-final-cleanup
-report.md, 20250809-phase5-playlist-implementation-report.md, 20250809-phase5-s
earch-cleanup-report.md |
| `docs/projectplan/admin_api_key_security_risk.md` | 4 | AUDIT-phase-1.md, 2025
0809-phase5-final-cleanup-report.md, 20250809-phase5-playlist-implementation-rep
ort.md, 20250809-phase5-search-cleanup-report.md |
| `github/ISSUE_TEMPLATE/feature-request.md` | 4 | AUDIT-phase-1.md, 20250809-ph
ase5-final-cleanup-report.md, 20250809-phase5-playlist-implementation-report.md,
 20250809-phase5-search-cleanup-report.md |
| `docs/projectplan/doc_maintenance.md` | 4 | AUDIT-phase-1.md, 20250809-phase5-
final-cleanup-report.md, 20250809-phase5-playlist-implementation-report.md, 2025
0809-phase5-search-cleanup-report.md |
| `LOGGING_GUIDE.md` | 3 | LOGGING_TRACEABILITY_MATRIX.md, PID.md, PID_previous.
md |
| `spotify_fullstack_capability_blueprint.md` | 3 | ROADMAP.md, 20250807-doc-cla
rification-completion-report.md, 20250807-spotify-blueprint-completion-report.md
 |
| `api/docs/manuals/LOGGING_GUIDE.md` | 3 | ACTIVITY.md, BACKLOG.md, LOGGING_TRA
CEABILITY_MATRIX.md |
| `api/docs/DATABASE.md` | 3 | AUDIT-phase-1.md, 20250809-phase5-playlist-implem
entation-report.md, 20250809-phase5-search-cleanup-report.md |
| `developer_guide.md` | 3 | TASK_CHECKLIST.md, FIRST_AUDIT.md, 20250809-api-end
points-completion-report.md |
| `security.md` | 3 | PRIVACY_COMPLIANCE.md, AUDIT-PHASE-3.md, AUDIT_TRACEABILIT
Y_MATRIX.md |
| `HLD.md` | 2 | ERROR_HANDLING_DESIGN.md, AUDIT-PHASE-4.md |
| `archive/docs/projectplan/security.md` | 2 | PROJECT_REGISTRY.md, SECURITY.md
|

## Recommendations


1. **Create missing anchor documents** (e.g., `docs/reference/ENDPOINTS.md`) and
 reconcile all references.
2. **Clarify doc locations**: enforce `docs/` for product manuals & references;
`project/` for project governance, plans, and audits.
3. **Add CI link-checker** for Markdown to prevent broken or stale references.
4. **Publish `ENDPOINTS.md` from OpenAPI** during CI, then cross-link from PID,
ROADMAP, and FEATURE_SPECS.
5. **Differentiate matrices**: Ensure `project/audit/AUDIT_TRACEABILITY_MATRIX.m
d` vs `project/audit/TRACEABILITY_MATRIX.md` are distinct, up-to-date, and cross
-referenced.
6. **Adopt 'docs-first' PR template**: Require changes to reference docs and fea
ture specs for any functional change.

# Traceability Matrix – Zotify API

> **Note:** For a high-level summary of feature coverage and gaps, see the [`USECASES_GAP_ANALYSIS.md`](./USECASES_GAP_ANALYSIS.md) document.

## Legend
- ✅ Implemented
- 🟡 Partial
- ❌ Missing
- 🔍 Needs Verification

| Requirement ID | Description | Source Doc | Implementation Status | Code Reference | Test Coverage | Linked Enhancement | Notes |
|----------------|-------------|------------|-----------------------|----------------|---------------|--------------------|-------|
| UC-01 | Merge and sync local `.m3u` playlists with Spotify playlists | USECASES.md | ❌ Missing | N/A | N/A | FE-02 | Dependent on Spotify playlist write support |
| UC-02 | Remote playlist rebuild based on metadata filters | USECASES.md | ❌ Missing | N/A | N/A | FE-05 | — |
| UC-03 | Upload local tracks to Spotify library | USECASES.md | ❌ Missing | N/A | N/A | | |
| UC-04 | Smart auto-download and sync for playlists | USECASES.md | 🟡 Partial | `services/download_service.py` | 🔍 Needs Verification | FE-03, FE-04 | Lacks automation and file management |
| UC-05 | Collaborative playlist version history | USECASES.md | ❌ Missing | N/A | N/A | | |
| UC-06 | Bulk playlist re-tagging for events | USECASES.md | ❌ Missing | N/A | N/A | | |
| UC-07 | Multi-format/quality audio library | USECASES.md | 🟡 Partial | `services/download_service.py` | 🔍 Needs Verification | | Lacks multi-format and quality control |
| UC-08 | Fine-grained conversion settings | USECASES.md | ❌ Missing | N/A | N/A | | |
| UC-09 | Flexible codec support | USECASES.md | ❌ Missing | N/A | N/A | | |
| UC-10 | Automated downmixing for devices | USECASES.md | ❌ Missing | N/A | N/A | | |
| UC-11 | Size-constrained batch conversion | USECASES.md | ❌ Missing | N/A | N/A | | |
| UC-12 | Quality upgrade watchdog | USECASES.md | ❌ Missing | N/A | N/A | | |
| **Future Enhancements** | | | | | | | |
| FE-01 | Advanced Admin Endpoint Security | FUTURE_ENHANCEMENTS.md | ❌ Missing | N/A | N/A | | e.g., JWT, rate limiting |
| FE-02 | Persistent & Distributed Job Queue | FUTURE_ENHANCEMENTS.md | 🟡 Partial | `services/download_service.py` | 🔍 Needs Verification | | Currently in-memory DB queue |
| FE-03 | Full Spotify OAuth2 Integration & Library Sync | FUTURE_ENHANCEMENTS.md | 🟡 Partial | `providers/spotify_connector.py` | 🔍 Needs Verification | | Lacks write-sync and full library management |
| FE-04 | Enhanced Download & Job Management | FUTURE_ENHANCEMENTS.md | ❌ Missing | N/A | N/A | | e.g., progress reporting, notifications |
| FE-05 | API Governance | FUTURE_ENHANCEMENTS.md | ❌ Missing | N/A | N/A | | e.g., rate limiting, quotas |
| FE-06 | Observability | FUTURE_ENHANCEMENTS.md | 🟡 Partial | `middleware/request_id.py` | 🔍 Needs Verification | | Lacks detailed audit trails. See FE-07a. |
| FE-07 | Standardized Error Handling | FUTURE_ENHANCEMENTS.md | ✅ Implemented | `core/error_handler/` | ✅ Implemented | | Centralized error handling module is complete and integrated. |
| FE-07a | Flexible Logging Framework (MVP) | FUTURE_ENHANCEMENTS.md | ✅ Implemented | `core/logging_framework/` | ✅ Implemented | FE-06 | Core framework is complete, including configurable sinks (file, console, webhook), tag-based routing, and automatic redaction of sensitive data in production. |
| DOC-01 | Comprehensive Logging Guide | PID.md | ✅ Implemented | `docs/manuals/LOGGING_GUIDE.md` | N/A | FE-07a | A detailed developer guide for the new logging framework has been created as per the project's documentation-first principles. |
| FE-08 | Comprehensive Health Checks | FUTURE_ENHANCEMENTS.md | 🟡 Partial | `routes/system.py` | 🔍 Needs Verification | | Only basic uptime/env endpoints exist |
| FE-09 | Unified Configuration Management | FUTURE_ENHANCEMENTS.md | 🟡 Partial | `services/config_service.py` | 🔍 Needs Verification | | Dual system exists, not unified |
| FE-10 | Dynamic Logging Plugin System | DYNAMIC_PLUGIN_PROPOSAL.md | ❌ Missing | N/A | N/A | FE-07a | A proposal for a dynamic plugin system to allow custom logging sinks. |
| FE-11 | Low-Code Platform Integration | LOW_CODE_PROPOSAL.md | ❌ Missing | N/A | N/A | | A proposal for integrating with platforms like Node-RED. |
| FE-12 | Home Automation Integration | HOME_AUTOMATION_PROPOSAL.md | ❌ Missing | N/A | N/A | | A proposal for integrating with platforms like Home Assistant. |
| **System Requirements (NFRs)** | | | | | | | |
| SYS-01 | Test Coverage >90% | HIGH_LEVEL_DESIGN.md | ❌ Missing | N/A | `pytest --cov` | | CI gating not implemented |
| SYS-02 | Performance <200ms | HIGH_LEVEL_DESIGN.md | 🔍 Needs Verification | N/A | N/A | | No performance benchmarks exist |
| SYS-03 | Security (Admin Auth) | HIGH_LEVEL_DESIGN.md | ✅ Implemented | `services/auth.py` | 🔍 Needs Verification | FE-01 | Basic API key auth is implemented |
| SYS-04 | Extensibility | HIGH_LEVEL_DESIGN.md | ✅ Implemented | `providers/base.py` | N/A | | Provider model allows for extension |
| SYS-05 | CORS Policy for Web UI | HIGH_LEVEL_DESIGN.md | ✅ Implemented | `zotify_api/main.py` | N/A | | Permissive CORS policy to allow browser-based clients. |
| SYS-06 | Snitch Secure Callback | `snitch/docs/PHASE_2_ZERO_TRUST_DESIGN.md` | 🟡 Partial | `snitch/snitch.go` | ✅ Implemented | | Zero Trust model with end-to-end payload encryption and nonce-based replay protection. |

---

## Logging System Traceability

| Requirement | Source Doc | Phase(s) | Status |
|-------------|------------|----------|--------|
| Central LoggingService with async pipeline | LOGGING_SYSTEM_DESIGN.md | Phase 1 | ✅ Implemented |
| Developer API with per-module log control | LOGGING_SYSTEM_DESIGN.md | Phase 2 | ✅ Implemented |
| Multi-sink destinations (file, syslog, db, Kafka, RabbitMQ) | LOGGING_SYSTEM_DESIGN.md | Phase 3 | 🟡 Partial |
| Runtime triggers with hot reload | LOGGING_SYSTEM_DESIGN.md | Phase 4 | 🟡 Partial |
| Observability integration (OTel, Prometheus, JSON logs) | LOGGING_SYSTEM_DESIGN.md | Phase 5 | TODO |
| Security & Compliance audit stream | LOGGING_SYSTEM_DESIGN.md | Phase 6 | TODO |
| Extensibility framework for custom adapters | LOGGING_SYSTEM_DESIGN.md | Phase 7 | TODO |
| Full observability suite (dashboard, anomaly detection) | LOGGING_SYSTEM_DESIGN.md | Phase 8 | TODO |

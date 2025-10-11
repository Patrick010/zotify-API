<!-- ID: API-263 -->
# Snitch Module Project Plan

**Date:** 2025-09-01
**Author:** Jules

**Reference Links:**
- **Main Project Plan:** `../../api/PROJECT_PLAN.md`
- **PID:** `../../project/PID.md`
- **Roadmap:** `../../project/ROADMAP.md`
- **Snitch Architecture:** `./ARCHITECTURE.md`

---

## 1. Purpose & Scope

### Purpose
The Snitch module is a critical security and integration component of the Zotify API platform. Its primary purpose is to provide a secure, reliable, and user-friendly mechanism for handling the browser-based OAuth 2.0 callback during CLI-driven authentication flows. It acts as a short-lived, local web server that captures the authorization token from Spotify and securely forwards it to the main Zotify API backend.

### Scope
- **In Scope:**
    - Listening on a local port for the OAuth redirect.
    - Validating the `state` parameter to prevent CSRF attacks.
    - Securely transmitting the captured authorization `code` to the Zotify API.
    - Providing clear, user-facing status messages in the browser.
    - Graceful startup, shutdown, and timeout handling.
- **Out of Scope:**
    - Storing any long-term credentials or tokens.
    - Handling any part of the OAuth flow beyond the `redirect_uri` callback.
    - Any direct interaction with the Spotify API.

---

## 2. Milestones & Phases

The development of the Snitch module follows the high-level phases of the main Zotify API project.

### Phase 1: Initial Implementation & Refactoring (✅ Done)
- **Milestone:** Basic functionality achieved.
- **Tasks:**
    - Initial `stdout`-based proof of concept.
    - Addition of `state` validation for CSRF protection.
    - Refactoring into a standard Go project structure.
    - Transition to a secure `POST`-based handoff to the main API.
- **Link to PID:** This work was part of the "Core Platform Stability & Security" phase of the main project.

### Phase 2: Hardening & Integration (Next Up)
- **Milestone:** Achieve production-ready security and reliability for the OAuth callback transport.
- **Goals:** The primary goal is to secure the communication channel between the user's browser, the Snitch helper, and the Zotify API backend, making it ephemeral, authenticated, and replay-resistant.
- **Security Milestones:**
    - **Define Secure Comms Mechanism:** Formalize the design for a secure token exchange mechanism (e.g., using HMAC-signed tokens or mutual TLS) to authenticate the API call from Snitch.
    - **Implement Replay Protection:** Add a nonce or timestamp to all Snitch-to-API communications to prevent replay attacks.
    - **Implement TLS Support:** Add TLS support to the Snitch listener to encrypt the browser-to-Snitch leg of the communication.
    - **End-to-End Encryption:** Implement the Zero Trust model described in `PHASE_2_ZERO_TRUST_DESIGN.md`, where the payload from Snitch to the API is encrypted.
    - **Dynamic Port Allocation:** Use a randomized, ephemeral port for the listener to prevent port squatting, communicating the port number back to the parent Zotify API process.
- **Testing Milestones:**
    - **Automated Integration Test:** Add a CI step that performs a full, automated, end-to-end authentication flow test involving the Zotify API and the compiled Snitch binary.
    - **Unit Test Coverage:** Achieve >90% unit test coverage for the Go codebase.
    - **Security Verification:** Perform a manual security audit of the entire IPC mechanism.
- **Documentation Milestones:**
    - **Document Usage:** Update `snitch/README.md` with clear instructions on the new, secure setup.

---

## 3. Roadmap Integration

The Snitch module is a "Supporting Module" as defined in the `project/PID.md`. Its development is intrinsically linked to the Core API's authentication and security features.

| Snitch Milestone | Zotify API PID/Roadmap Phase | Dependencies |
|---|---|---|
| Hardening & Integration | Platform Extensibility | A stable Core API authentication endpoint. |
| Maintenance & Updates | Future Vision | Dependent on future changes to the API's authentication model (e.g., transition to JWT). |

---

## 4. Tasks & Deliverables

### Development Tasks
| Task ID | Description | Owner | Status |
|---|---|---|---|
| `SNITCH-FEAT-01` | Design and implement a secure comms mechanism (e.g., HMAC or mTLS). | TBD | `Planned` |
| `SNITCH-FEAT-02` | Add replay protection (nonce/timestamp) to the Snitch-API payload. | TBD | `Planned` |
| `SNITCH-FEAT-03` | Implement TLS support in the Snitch web server. | TBD | `Planned` |
| `SNITCH-FEAT-04` | Implement dynamic port allocation for the listener. | TBD | `Planned` |
| `SNITCH-BUG-01` | Investigate and resolve any remaining build consistency issues. | TBD | `Planned` |

### QA & Testing Tasks
| Task ID | Description | Owner | Status |
|---|---|---|---|
| `SNITCH-TEST-01` | Create comprehensive unit tests for all Go packages (>90% coverage). | TBD | `Planned` |
| `SNITCH-TEST-02` | Develop and integrate an automated end-to-end auth flow test into CI. | TBD | `Planned` |
| `SNITCH-QA-01` | Perform manual security verification of the entire IPC channel. | TBD | `Planned` |

### Documentation Tasks
| Task ID | Description | Owner | Status |
|---|---|---|---|
| `SNITCH-DOC-01` | Update `snitch/README.md` to document the new secure usage. | TBD | `Planned` |
| `SNITCH-DOC-02` | Update all `snitch/docs` to reflect the hardened architecture. | TBD | `Planned` |

---

## 5. Security & Compliance

- **Replay Attack Prevention:** The secure IPC mechanism must include a nonce or timestamp to ensure that a captured payload cannot be replayed. This is a core requirement of the Zero Trust design.
- **Sniffing Attack Prevention:** While the communication is on localhost, payload encryption via TLS will mitigate the risk of local process sniffing attacks.
- **Compliance:** The Snitch module itself does not handle or persist PII, but its role in the authentication flow is critical for the platform's overall GDPR compliance. Its security and reliability are paramount.

---

## 6. Tracking & Updates

This document is a living plan and will be updated as work progresses.

| Milestone | Status |
|---|---|
| Basic Functionality | ✅ `Completed` |
| State Validation | ✅ `Completed` |
| Code Refactor | ✅ `Completed` |
| Secure POST Handoff | ✅ `Completed` |
| **Phase 2: Hardening** | |
| Define Secure Comms | ❌ `Not Started` |
| Implement Replay Protection | ❌ `Not Started` |
| Implement TLS Support | ❌ `Not Started` |
| Dynamic Port Allocation | ❌ `Not Started` |
| Automated Integration Test | ❌ `Not Started` |
| >90% Unit Test Coverage | ❌ `Not Started` |
| Update README Usage | ❌ `Not Started` |

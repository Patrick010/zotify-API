<!-- ID: API-260 -->
# Snitch Development Phases

This document provides a more detailed breakdown of the tasks required for each development phase.

---

## Phase 1 – Bootstrap and Listener

**Goal:** Establish the basic project structure and a functional, temporary HTTP listener.

- **Tasks:**
    - [x] Initialize a new `snitch` directory in the Zotify-API repository.
    - [x] Create the standard Go project layout: `cmd/`, `internal/`.
    - [x] Create the `docs/` directory for project documentation.
    - [x] Initialize a Go module (`go mod init`).
    - [ ] Implement a `main` function in `cmd/snitch/main.go`.
    - [ ] Create a `listener` package in `internal/`.
    - [ ] In the `listener` package, implement a function to start an HTTP server on port `21371`.
    - [ ] Add a handler for the `/callback` route.
    - [ ] The handler must extract the `code` query parameter from the request URL.
    - [ ] If a `code` is present, print it to `stdout` and trigger a graceful server shutdown.
    - [ ] If no `code` is present, return an HTTP 400 error.
    - [ ] Implement a 2-minute timer that forcefully shuts down the server if no successful callback is received.
    - [x] Create `README.md` with a project description and usage instructions.
    - [x] Create `PROJECT_PLAN.md`, `ROADMAP.md`, `MILESTONES.md`, `STATUS.md`, and this `PHASES.md` file.

---

## Phase 2 – IPC Integration

**Goal:** Integrate Snitch with a parent process using basic Inter-Process Communication (IPC).

- **Tasks:**
    - [ ] Design a simple protocol for the parent process (Zotify-API) to execute the Snitch binary.
    - [ ] The parent process must be able to read the `stdout` stream from the Snitch subprocess.
    - [ ] Create a test script or program that simulates the parent process to validate the integration.
    - [ ] Document the IPC mechanism.

---

## Phase 3 – Randomized Port + IPC Handshake

**Goal:** Enhance security by removing the reliance on a fixed port and implementing a secure handshake.

- **Tasks:**
    - [ ] Modify Snitch to bind to a random, available TCP port instead of the fixed port `21371`.
    - [ ] Modify the IPC protocol to communicate the chosen port from Snitch back to the parent process. `stdout` can be used for this initial communication.
    - [ ] Design a simple, secure handshake mechanism (e.g., a shared secret passed as a command-line argument).
    - [ ] Snitch will expect this secret and must validate it before proceeding.
    - [ ] The parent process will generate and pass this secret when launching Snitch.
    - [ ] Update documentation to reflect the new security features.

---

## Phase 4 – Packaging and Cross-Platform Runner

**Goal:** Package Snitch as a standalone binary and ensure it can be run across different operating systems.

- **Tasks:**
    - [ ] Create a build script (`Makefile` or similar) to automate the build process.
    - [ ] Configure the build script to cross-compile Snitch for Windows, macOS, and Linux (x86_64).
    - [ ] Create a "runner" module or script within the main Zotify-API project.
    - [ ] This runner will be responsible for locating the correct Snitch binary for the current platform and executing it.
    - [ ] The packaged binaries should be stored within the Zotify-API project structure.

---

## Phase 5 – Integration into Zotify CLI Flow

**Goal:** Fully integrate the packaged Snitch binary into the end-to-end Zotify-API authentication workflow.

- **Tasks:**
    - [ ] Replace any mock or test authentication flows in Zotify-API with the real Snitch runner.
    - [ ] Ensure the entire process—from launching Snitch to receiving the `code` and exchanging it for a token—is seamless.
    - [ ] Conduct end-to-end testing on all supported platforms.
    - [ ] Update the main Zotify-API documentation to describe the new authentication process for users.

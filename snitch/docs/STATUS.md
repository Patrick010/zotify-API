# Snitch Project Status

This document provides a live view of the project's progress.

- ✅ = Done
- 🔄 = In Progress
- ⏳ = Pending

## Phase 1: Bootstrap and Listener
- [✅] Create project directory structure.
- [✅] Initialize Go module.
- [🔄] Implement basic HTTP listener on port 21371.
- [🔄] Add logic to capture `code` parameter and print to `stdout`.
- [🔄] Implement 2-minute shutdown timeout.
- [✅] Create initial project documentation (`README.md`, `PROJECT_PLAN.md`, etc.).
- [⏳] Manually test listener with a browser redirect.

## Phase 2: IPC Integration
- [⏳] Design basic IPC mechanism.
- [⏳] Implement Snitch launching from parent process.
- [⏳] Implement `stdout` capture in parent process.

## Phase 3: Randomized Port + IPC Handshake
- [⏳] Implement random port selection.
- [⏳] Implement mechanism to communicate port to parent.
- [⏳] Design and implement secure handshake.

## Phase 4: Packaging and Cross-Platform Runner
- [⏳] Set up cross-compilation build scripts.
- [⏳] Create runner script/function in Zotify-API.

## Phase 5: Integration into Zotify CLI Flow
- [⏳] Integrate Snitch runner into auth workflow.
- [⏳] Perform end-to-end testing.

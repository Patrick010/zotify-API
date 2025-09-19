# Snitch Development Roadmap

This document outlines the high-level, phased development plan for the Snitch subproject.

## Phase 1 – Bootstrap and Listener
- **Goal:** Establish the basic project structure and a functional, temporary HTTP listener.
- **Key Deliverables:**
    - Go module and directory layout.
    - HTTP server on port 21371 that captures the `code` parameter.
    - Server prints the code to `stdout` and shuts down on success or after a 2-minute timeout.
    - Initial documentation.

## Phase 2 – IPC Integration
- **Goal:** Integrate Snitch with a parent process using basic Inter-Process Communication (IPC).
- **Key Deliverables:**
    - A simple mechanism for the parent Zotify-API process to launch and read from Snitch's `stdout`.
    - Initial integration tests.

## Phase 3 – Randomized Port + IPC Handshake
- **Goal:** Enhance security by removing the reliance on a fixed port and implementing a secure handshake.
- **Key Deliverables:**
    - Snitch starts on a random, available port.
    - The chosen port number is communicated back to the parent process.
    - A shared secret is used in a simple handshake to verify that Snitch is communicating with the correct parent process.

## Phase 4 – Packaging and Cross-Platform Runner
- **Goal:** Package Snitch as a standalone binary and ensure it can be run across different operating systems.
- **Key Deliverables:**
    - Cross-compilation builds for Windows, macOS, and Linux.
    - A runner script or function within Zotify-API to manage the Snitch binary.

## Phase 5 – Integration into Zotify CLI Flow
- **Goal:** Fully integrate the packaged Snitch binary into the end-to-end Zotify-API authentication workflow.
- **Key Deliverables:**
    - A seamless user experience for authentication via the CLI.
    - Final documentation and usage instructions.

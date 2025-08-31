# Proposal: Low-Code/No-Code Platform Integration

**Date:** 2025-08-18
**Author:** Jules
**Status:** Proposed

## 1. Problem Statement

The Zotify API is becoming a powerful platform for developers. However, its full potential can only be unlocked by users comfortable with writing code to interact with a REST API. To make the platform's capabilities accessible to a wider audience of power-users, citizen developers, and automators, we need to provide integrations with popular low-code/no-code platforms.

## 2. Proposed Solution

This document proposes the official endorsement and creation of a dedicated integration for low-code platforms, with **Node-RED** serving as the primary reference implementation.

This would involve creating a new, separate project: a Node-RED "contrib" package (e.g., `node-red-contrib-zotify`). This package would provide a set of pre-built, user-friendly nodes that can be used in the Node-RED visual flow editor.

### 2.1. How It Will Work

The Zotify API server itself requires no changes to support this. The integration happens at the client layer.

1.  **Custom Node-RED Nodes:** A developer would create a set of nodes for the Node-RED palette. Each node would represent a core piece of Zotify API functionality. Examples include:
    -   **Search Tracks:** A node with an input for a search query that outputs a list of track objects.
    -   **Download Track:** A node that takes a track ID as input and initiates a download.
    -   **Get Playlist:** A node that takes a playlist ID and outputs the list of tracks.
    -   **API Trigger:** A node that listens for specific events from the Zotify API (requires a webhook system, see `FUTURE_ENHANCEMENTS.md`).

2.  **API Interaction:** Under the hood, each of these nodes would simply be a well-designed HTTP client that makes the appropriate calls to the Zotify API endpoints. It would handle authentication, error handling, and data parsing, presenting a simple interface to the Node-RED user.

3.  **User Experience:** The end-user can simply drag and drop these nodes, wire them together, and connect them to other nodes (like MQTT, email, or home automation nodes) to create powerful, custom automation flows without writing a single line of code.

### 2.2. Use Case Example: Automated Playlist Email

A user could create a Node-RED flow that does the following:
1.  An `Inject` node triggers the flow once a week.
2.  It connects to a `Get Playlist` Zotify node to fetch the user's "Discover Weekly" playlist.
3.  The output (a list of tracks) is passed to a `Template` node that formats the track list into a clean HTML email.
4.  The HTML is passed to an `Email` node that sends the weekly playlist summary to the user's inbox.

## 3. Benefits

-   **Increased Accessibility:** Makes the power of the Zotify API accessible to non-programmers.
-   **Rapid Prototyping:** Allows for the rapid creation of complex automation workflows.
-   **Ecosystem Growth:** Fosters a community of users who can share and build upon each other's flows and ideas, driving adoption of the core API.
-   **Synergy with Plugin System:** The more powerful the backend API becomes (through the Python plugin system), the more powerful the Node-RED nodes can be.

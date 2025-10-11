<!-- ID: DOC-051 -->
# Proposal: Home Automation Platform Integration

**Date:** 2025-08-18
**Author:** Jules
**Status:** Proposed

## 1. Problem Statement

A significant number of power-users and hobbyists use home automation platforms like Home Assistant, Homey, and voice assistants like Google Home to orchestrate their smart homes. The Zotify API, with its ability to control music playback and manage a media library, is a natural fit for this ecosystem. However, without a dedicated integration, connecting Zotify to these platforms is a manual process requiring users to craft their own API calls and automations from scratch.

## 2. Proposed Solution

This document proposes the official endorsement and creation of a dedicated integration for home automation platforms, with **Home Assistant** serving as the primary reference implementation.

The goal is to create a custom Home Assistant "Integration" (component) that would expose Zotify entities and services directly within the Home Assistant UI.

### 2.1. How It Will Work

This integration would be a new, separate Python project, developed according to the standards of the target home automation platform.

1.  **Home Assistant Component:** A developer would create a `zotify` custom component for Home Assistant. This component would be responsible for communicating with the Zotify API.

2.  **Configuration:** Within Home Assistant's UI, users would add the Zotify integration and configure it with the URL of their Zotify API instance and their Admin API Key.

3.  **Exposed Entities:** The component would create several entities within Home Assistant:
    -   A `media_player.zotify` entity that represents the current playback state. Users could use this to see what's playing and perform basic actions like play, pause, skip, and volume control.
    -   A `sensor.zotify_last_downloaded` entity that shows the name of the last successfully downloaded track.
    -   `switch` entities for each playlist to enable/disable syncing for that playlist.

4.  **Exposed Services:** The component would also register new services that can be called from automations:
    -   `zotify.download_track`: Takes a track ID and starts a download.
    -   `zotify.sync_playlist`: Takes a playlist ID and starts a sync.
    -   `zotify.search`: A service to perform a search and return the results as a variable.

### 2.2. Use Case Example: "Dinner Time" Automation

A user could create an automation in Home Assistant's UI:
-   **Trigger:** When a "Dinner Time" input boolean is turned on.
-   **Action:**
    1.  Call the `zotify.download_track` service with the ID of a specific dinner music playlist.
    2.  Call the `media_player.play_media` service on their smart speaker, targeting the newly downloaded playlist.
    3.  Call a `light.turn_on` service to dim the dining room lights.

## 3. Benefits

-   **Seamless Integration:** Brings Zotify's powerful media management capabilities directly into the user's smart home dashboard.
-   **Powerful Automations:** Unlocks countless new automation possibilities by combining Zotify events and services with other smart home devices (lights, switches, sensors).
-   **Increased Adoption:** Taps into the large and enthusiastic home automation community, driving adoption and awareness of the Zotify API.

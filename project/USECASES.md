<!-- ID: DOC-022 -->
# Zotify API – User-Driven Use Cases (Spotify Provider Only)

This document captures realistic, demanding user scenarios that the API should ideally support.
These use cases go beyond basic search and download, covering complex playlist operations,
advanced audio handling, and end-to-end synchronization between local and Spotify resources.

---

## 1. Merge and Sync Local + Spotify Playlists
**Scenario:**
A user has multiple local `.m3u` playlists stored on their server, and several Spotify playlists in their account. They want to:
- Merge a local playlist and a Spotify playlist into a single master playlist
- Remove duplicates regardless of source (local or Spotify)
- Push the merged playlist back to Spotify as a new playlist
- Save a local `.m3u` copy for offline use

**Requirements:**
- Read and parse `.m3u` playlists from local storage
- Read Spotify playlists and track metadata
- Deduplicate across providers
- Create new Spotify playlists
- Export merged playlist to `.m3u`

---

## 2. Remote Playlist Rebuild Based on Filters
**Scenario:**
A user wants to rebuild one of their Spotify playlists entirely based on new criteria:
- Keep only tracks released in the last 5 years
- Remove songs under 2 minutes or over 10 minutes
- Replace removed tracks with recommendations from Spotify’s related artist/track API
- Overwrite the existing Spotify playlist with the new version

**Requirements:**
- Access and edit Spotify playlists
- Apply track metadata filters (duration, release date)
- Fetch and insert recommendations
- Allow overwrite or save-as-new

---

## 3. Cross-Device, Server-Side Upload of Local Tracks to Spotify Library
**Scenario:**
A user has a collection of rare MP3s stored on their media server. They want to:
- Upload them to their Spotify library so they’re accessible on all devices through Spotify
- Automatically match metadata from local tags to Spotify’s catalog for better integration

**Requirements:**
- Upload local tracks to Spotify (using local files feature)
- Match metadata automatically against Spotify DB
- Provide manual correction options for unmatched tracks

---

## 4. Smart Auto-Download and Sync for Road Trips
**Scenario:**
A user wants to maintain a “Road Trip” playlist both locally and on Spotify:
- Whenever the playlist changes on Spotify, automatically download the new tracks locally
- Remove local files for tracks that are no longer in the playlist
- Ensure local filenames and tags are normalized for in-car playback

**Requirements:**
- Spotify playlist change detection (webhooks or polling)
- Download new tracks from Spotify
- Delete removed tracks locally
- Tag and normalize filenames

---

## 5. Collaborative Playlist Hub with Version History
**Scenario:**
A group of friends shares a collaborative Spotify playlist. They want:
- A server-side history of all changes (add/remove) over time
- Ability to roll back to a previous playlist state and re-publish to Spotify
- Export changes as a changelog (date, track added/removed, by whom)

**Requirements:**
- Pull playlist changes with timestamps and user info
- Maintain historical snapshots
- Restore playlist from a previous snapshot
- Publish restored playlist back to Spotify

---

## 6. Bulk Playlist Re-Tagging for Themed Events
**Scenario:**
A user is planning a “Summer 90s Party” and wants to:
- Take an existing Spotify playlist
- Automatically replace all track titles in the playlist with a custom “theme tag” in their local `.m3u` export (e.g., `[90s Party]`)
- Keep the Spotify playlist untouched, but create a new themed copy locally and optionally as a private Spotify playlist

**Requirements:**
- Read Spotify playlist
- Modify local playlist metadata without affecting Spotify original
- Export `.m3u` with modified titles
- Create optional new Spotify playlist with modified names

---

## 7. Multi-Format, Multi-Quality Library for Audiophiles
**Scenario:**
A user wants a single API call to:
- Download Spotify tracks in the **highest available quality**
- Convert to multiple formats at once: MP3 (320 kbps), AAC (256 kbps), FLAC (lossless), ALAC (lossless Apple), and AC3 (5.1)
- Organize outputs into separate directories for each format

**Requirements:**
- Download in best source quality
- Batch conversion to multiple formats in parallel
- Configurable output structure
- Retain metadata across all conversions

---

## 8. Fine-Grained Conversion Settings for Audio Engineers
**Scenario:**
A user wants advanced control over conversion parameters:
- Manually set bitrates (CBR, VBR, ABR)
- Choose specific sample rates (44.1kHz, 48kHz, 96kHz)
- Control channel layouts (mono, stereo, 5.1 downmix)
- Set custom compression parameters per format

**Requirements:**
- Accept detailed transcoding parameters per request
- Support FFmpeg advanced flags or equivalent in backend
- Validate parameters for compatibility with chosen codec

---

## 9. Codec Flexibility Beyond FFmpeg Defaults
**Scenario:**
A user wants to use a **non-FFmpeg codec** for certain formats:
- Use `qaac` for AAC encoding (better quality for iTunes users)
- Use `flac` CLI encoder for reference-level lossless FLAC
- Use `opusenc` for low-bitrate speech-optimized files
- Specify encoder binary path in API request or configuration

**Requirements:**
- Support multiple encoder backends (FFmpeg, qaac, flac, opusenc, etc.)
- Allow per-job selection of encoder backend
- Detect encoder availability and fail gracefully if missing

---

## 10. Automated Downmixing for Multi-Device Environments
**Scenario:**
A user has a 5.1 surround track but wants multiple derived versions:
- Keep original 5.1 FLAC for home theater
- Downmix to stereo AAC for phone playback
- Downmix to mono MP3 for voice-focused devices

**Requirements:**
- Multi-channel audio handling in downloads and conversions
- Automated generation of alternate mixes
- Ensure each mix retains correct metadata and loudness normalization

---

## 11. Size-Constrained Batch Conversion for Portable Devices
**Scenario:**
A user wants to fit a large playlist onto a small portable player:
- Convert all tracks to Opus 96 kbps or MP3 128 kbps
- Target total playlist size (e.g., 2 GB max)
- Optionally reduce bitrate further if size exceeds target

**Requirements:**
- Allow bitrate targeting by total output size
- Dynamically adjust compression to meet constraints
- Maintain playable format for target device

---

## 12. Quality Upgrade Watchdog
**Scenario:**
A user maintains a local FLAC archive from Spotify sources. They want:
- To be notified if higher-quality versions of a track become available
- Automatic re-download and reconversion into all existing formats with original metadata preserved

**Requirements:**
- Detect higher-quality source availability
- Auto-replace lower-quality files
- Re-run all configured conversions without user intervention

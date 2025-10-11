<!-- ID: DOC-023 -->
# Gap Analysis – Zotify API vs. User Use Cases

This document compares the **desired capabilities** from `USECASES.md` with the **current** Zotify API implementation.
The goal is to identify missing or partial functionality that must be addressed to meet user expectations.

---

## Legend
- ✅ **Supported** – Feature is already implemented and functional.
- 🟡 **Partial** – Some capability exists, but not full requirements.
- ❌ **Missing** – No current implementation.
- 🔍 **Needs Verification** – Unclear if current implementation covers this.

---

## 1. Merge and Sync Local + Spotify Playlists
**Status:** ❌ Missing
**Gaps:**
- No current ability to read `.m3u` playlists from local storage.
- No deduplication across sources.
- No playlist creation in Spotify from merged data.
- No `.m3u` export after merging.

---

## 2. Remote Playlist Rebuild Based on Filters
**Status:** ❌ Missing
**Gaps:**
- No track filtering based on metadata (duration, release date).
- No integration with Spotify recommendations.
- No overwrite/save-as-new playlist functionality.

---

## 3. Cross-Device, Server-Side Upload of Local Tracks to Spotify Library
**Status:** ❌ Missing
**Gaps:**
- No upload/local file sync to Spotify feature.
- No metadata matching against Spotify DB.
- No manual metadata correction system.

---

## 4. Smart Auto-Download and Sync for Road Trips
**Status:** 🟡 Partial
**Existing:**
- Can download Spotify playlists manually.
**Gaps:**
- No automatic change detection for playlists.
- No auto-download/remove workflow.
- No filename/tag normalization step.

---

## 5. Collaborative Playlist Hub with Version History
**Status:** ❌ Missing
**Gaps:**
- No playlist change tracking or version history.
- No rollback to previous versions.
- No changelog export.

---

## 6. Bulk Playlist Re-Tagging for Themed Events
**Status:** ❌ Missing
**Gaps:**
- No metadata modification for `.m3u` exports.
- No ability to duplicate playlists with modified titles.

---

## 7. Multi-Format, Multi-Quality Library for Audiophiles
**Status:** 🟡 Partial
**Existing:**
- MP3 output via FFmpeg (basic).
**Gaps:**
- No multiple simultaneous format outputs.
- No FLAC/ALAC/AC3 output support.
- No directory structuring per format.

---

## 8. Fine-Grained Conversion Settings for Audio Engineers
**Status:** ❌ Missing
**Gaps:**
- No advanced transcoding parameter support (bitrate modes, sample rates, channel layouts).
- No backend exposure of FFmpeg advanced flags.

---

## 9. Codec Flexibility Beyond FFmpeg Defaults
**Status:** ❌ Missing
**Gaps:**
- No support for alternate encoders (`qaac`, `flac`, `opusenc`).
- No backend switching or binary path configuration.

---

## 10. Automated Downmixing for Multi-Device Environments
**Status:** ❌ Missing
**Gaps:**
- No multi-channel audio support.
- No automated downmix workflows.

---

## 11. Size-Constrained Batch Conversion for Portable Devices
**Status:** ❌ Missing
**Gaps:**
- No size-targeted bitrate adjustment.
- No compression optimization based on total playlist size.

---

## 12. Quality Upgrade Watchdog
**Status:** ❌ Missing
**Gaps:**
- No detection of higher-quality track availability.
- No auto-replacement or reconversion.

---

## Summary of Gaps
- **Playlist handling:** Local `.m3u` integration, merging, filtering, metadata editing, versioning, sync automation.
- **Advanced audio processing:** Multi-format, high-quality/lossless, alternate codecs, fine-grained control, size constraints, downmixing.
- **Automation & intelligence:** Change detection, quality upgrades, recommendation-based playlist rebuilds.
- **Spotify integration depth:** Upload/local file sync, playlist creation and overwriting, historical rollback.

**Overall Coverage Estimate:** ~15–20% of desired functionality currently exists in partial form.

---

## Recommendations
1. **Phase Next:** Implement playlist handling capabilities (local `.m3u` read/write, Spotify playlist write, merge/dedup) — these unlock multiple use cases at once.
2. Add **conversion framework** upgrades to handle multi-format, advanced parameters, and alternate codecs.
3. Expand **automation layer** to include playlist change detection and quality upgrade triggers.

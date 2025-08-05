# API Test Scripts

This directory contains bash scripts for running integration sanity checks on the dev server.

## Usage

First, make sure the API server is running. Then, from the `api` directory, you can run the scripts individually:

```bash
# Run health checks
bash tests/test_health.sh

# Run playlists and tracks tests
bash tests/test_playlists_tracks.sh

# Run user and system tests
bash tests/test_user_system.sh

# Run all endpoint checks
bash tests/test_all_endpoints.sh
```

Note: `test_playlists_tracks.sh` requires `jq` to be installed on the server.

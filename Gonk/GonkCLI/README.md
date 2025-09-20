# Gonk CLI

## Overview

The Gonk Command Line Interface (CLI) is a tool for interacting with the Zotify API from the command line. It is intended for developers and power users who want to script interactions with the Zotify platform.

## Installation

The CLI is part of the Gonk project and does not require a separate installation, as long as the main project dependencies are installed.

## Authentication

Before using most commands, you must log in to the Zotify API. The CLI will automatically save your authentication token to a file named `.gonk_token` in your home directory.

**Login:**
```bash
python Gonk/GonkCLI/main.py login <username> <password>
```
Example:
```bash
python Gonk/GonkCLI/main.py login testuser password123
```
This will create the `.gonk_token` file, and subsequent commands will use it automatically.

## Usage

All commands are run from the root of the project directory.

### Get User Profile
```bash
python Gonk/GonkCLI/main.py get-profile
```

### Update User Preferences
```bash
python Gonk/GonkCLI/main.py update-prefs --theme light --language en --notifications true
```
-   `--theme`: (Optional) `light` or `dark`.
-   `--language`: (Optional) Two-letter language code (e.g., `en`, `fr`).
-   `--notifications`: (Optional) `true` or `false`.

### Get Liked Tracks
```bash
python Gonk/GonkCLI/main.py get-liked
```

### Get Listening History
```bash
python Gonk/GonkCLI/main.py get-history
```

### Clear Listening History
```bash
python Gonk/GonkCLI/main.py clear-history
```

### Verbose Output

All commands support a `--verbose` flag for more detailed output, including error stack traces.
```bash
python Gonk/GonkCLI/main.py get-profile --verbose
```

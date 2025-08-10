# Zotify REST API

This project provides a REST API for the [Zotify](https://github.com/Googolplexed0/zotify) music and podcast downloader, with features for playlist management, search, and downloading.

## What This Is (and What It Isn't)

The Zotify API is an automation and developer framework built on top of the original Zotify CLI. It uses Librespot (an open-source Spotify client library) to handle authentication and download media directly from Spotify's servers.

This project is **not** a reimplementation of the official Spotify Web API.

Instead, its purpose is to expose powerful functionality that is difficult or impossible to achieve with the standard Spotify API, such as:
- Automated track and playlist downloading.
- Offline media caching and library management.
- Advanced, scriptable control over the download queue.

Think of it as a developer platform for building applications that need to programmatically acquire and manage Spotify content, powered by the battle-tested Zotify CLI and Librespot library.

## Project Files

- **[Installation Guide](./api/docs/INSTALLATION.md)**: Detailed setup instructions.
- **[Changelog](./api/docs/CHANGELOG.md)**: A log of all API version changes.
- **[Contributing Guide](./api/docs/CONTRIBUTING.md)**: Guidelines for contributing to the API.
- **[LICENSE](./api/docs/LICENSE)**: The software license.
- **[OpenAPI Spec (JSON)](./api/docs/zotify-openapi-external-v1.json)**: The machine-readable API specification.
- **[OpenAPI Spec (YAML)](./api/docs/zotify-openapi-external-v1.yaml)**: The human-friendly API specification.

## API Usage

> [!NOTE]
> The API is built for Zotify v0.6.x. Using it with other versions may not work as expected.

### Dependencies

- Python 3.10 or greater
- FFmpeg
- Zotify (the original CLI tool)

### Installation

For detailed setup instructions, including prerequisites and different installation methods (Git Clone, Install Script, .deb Package, Docker), please see the [Installation Guide](./api/docs/INSTALLATION.md).

### Running the Server

To run the API server, first install the API in editable mode from the project root, then start the server:

```bash
# From the project root directory (containing api/ and zotify/)
pip install -e ./api
uvicorn zotify_api.main:app --reload --host 0.0.0.0 --port 8080
```

The server will be accessible at `http://<your-host>:8080`.

### Testing the API

You can test that the API is running by sending a request to the `/ping` endpoint:

```bash
curl http://127.0.0.1:8080/ping
```

The expected response is:

```json
{"pong":true}
```

## Disclaimer

This API is intended solely for educational, private, and lawful use. It interacts with Spotify exclusively through official, existing Spotify user accounts and authorized interfaces made available by Spotify itself. The contributors do not endorse, encourage, or facilitate any activity that would violate Spotify's Terms of Service or applicable copyright law. Use of this API must comply with all relevant laws and platform rules. The maintainers accept no responsibility for misuse or unauthorized application of the source code or resulting services.

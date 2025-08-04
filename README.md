# Zotify REST API

This project provides a REST API for the [Zotify](https://github.com/Googolplexed0/zotify) music and podcast downloader, with features for playlist management, search, and downloading.

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

To run the API server, execute the following command from the project's root directory:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
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

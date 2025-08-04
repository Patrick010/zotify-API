# Zotify REST API

This project provides a REST API for the [Zotify](https://github.com/Googolplexed0/zotify) music and podcast downloader.

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

This software is provided strictly for educational and personal use. It does not facilitate or promote the circumvention of any technological protection measures, and it is not intended for use in violation of copyright laws, including the DMCA or any equivalent legislation. Use of this software is entirely at your own risk. The authors and contributors disclaim all liability for any direct or indirect misuse, and do not condone or support any illegal activity involving this codebase.

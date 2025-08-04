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

To use the API, you must first install the required Python packages:

```bash
pip install fastapi uvicorn
```

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

This API is intended to be used in compliance with DMCA, Section 1201, for educational, private and fair use. The contributors are not responsible for any misuse of the program or source code.

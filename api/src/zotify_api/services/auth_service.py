import logging
import secrets
import string
import subprocess
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional
import json

log = logging.getLogger(__name__)

class IPCServer(threading.Thread):
    """
    A one-shot HTTP server that runs in a background thread to receive the
    OAuth code from the Snitch subprocess.
    """

    def __init__(self, ipc_token: str):
        super().__init__()
        self.host = "127.0.0.1"
        self.port = 9999  # In a real scenario, this should be randomized.
        self.ipc_token = ipc_token
        self.captured_code: Optional[str] = None
        self._server = HTTPServer((self.host, self.port), self._make_handler())

    def run(self):
        log.info(f"IPC server starting on http://{self.host}:{self.port}")
        self._server.handle_request()  # Handle one request and exit.
        log.info("IPC server has shut down.")

    def _make_handler(self):
        # Closure to pass instance variables to the handler
        ipc_server_instance = self
        class RequestHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.path != "/zotify/receive-code":
                    self.send_error(404, "Not Found")
                    return

                auth_header = self.headers.get("Authorization")
                expected_header = "Bearer " + ipc_server_instance.ipc_token
                if auth_header != expected_header:
                    self.send_error(401, "Unauthorized")
                    return

                try:
                    content_len = int(self.headers.get("Content-Length"))
                    post_body = self.rfile.read(content_len)
                    data = json.loads(post_body)
                    ipc_server_instance.captured_code = data.get("code")
                except Exception as e:
                    log.error(f"Error processing IPC request: {e}")
                    self.send_error(400, "Bad Request")
                    return

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))

            def log_message(self, format, *args):
                # Suppress default logging to stdout
                return

        return RequestHandler


def generate_secure_token(length=32):
    """Generates a URL-safe random token."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def start_authentication_flow():
    """
    Starts the full authentication flow:
    1. Generates tokens.
    2. Starts the IPC server.
    3. Launches Snitch.
    4. Returns the Spotify URL for the user.
    """
    state = generate_secure_token()
    ipc_token = generate_secure_token()

    # Start IPC Server
    ipc_server = IPCServer(ipc_token=ipc_token)
    ipc_server.start()

    # Launch Snitch
    try:
        snitch_command = [
            "./snitch/snitch", # This path needs to be correct relative to execution dir
            f"-state={state}",
            f"-ipc-token={ipc_token}",
            f"-ipc-port={ipc_server.port}",
        ]
        log.info(f"Launching Snitch with command: {' '.join(snitch_command)}")
        # In a real app, you'd handle stdout/stderr better.
        subprocess.Popen(snitch_command)
    except FileNotFoundError:
        log.error("Could not find the 'snitch' executable. Make sure it is built and in the correct path.")
        return {"error": "Snitch executable not found."}

    # Construct Spotify URL (dummy client_id for now)
    client_id = "YOUR_CLIENT_ID" # This should come from config
    redirect_uri = "http://127.0.0.1:21371/callback"
    spotify_url = (
        f"https://accounts.spotify.com/authorize?response_type=code"
        f"&client_id={client_id}"
        f"&scope=user-read-private%20user-read-email"
        f"&redirect_uri={redirect_uri}"
        f"&state={state}"
    )

    return {"spotify_auth_url": spotify_url, "ipc_server_thread": ipc_server}

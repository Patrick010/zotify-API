import os
import subprocess  # nosec B404
import argparse
from flask import Flask, jsonify, send_from_directory, render_template

app = Flask(__name__, static_folder="static")
sqlite_web_process = None


@app.route("/")
def index():
    # Use the same default dev key as the main API for convenience
    admin_api_key = os.environ.get("ADMIN_API_KEY", "zotify-admin-key-dev")
    return render_template(
        "index.html", api_url=args.api_url, admin_api_key=admin_api_key
    )


@app.route("/<path:path>")
def static_proxy(path):
    """Serve static files."""
    return send_from_directory("static", path)


@app.route("/launch-sqlite-web", methods=["POST"])
def launch_sqlite_web():
    global sqlite_web_process
    if sqlite_web_process:
        return (
            jsonify({"status": "error", "message": "sqlite-web is already running."}),
            400,
        )

    database_uri = os.environ.get("DATABASE_URI")
    if not database_uri or not database_uri.startswith("sqlite:///"):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "DATABASE_URI environment variable must be set to a valid SQLite URI (e.g., sqlite:///../api/storage/zotify.db).",
                }
            ),
            400,
        )

    db_path = database_uri.replace("sqlite:///", "")
    db_abs_path = os.path.join(os.path.dirname(__file__), "..", db_path)

    if not os.path.exists(db_abs_path):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Database file not found at {db_abs_path}",
                }
            ),
            400,
        )

    try:
        command = ["sqlite_web", db_abs_path, "--port", "8081", "--no-browser"]
        sqlite_web_process = subprocess.Popen(command)  # nosec B603
        return jsonify(
            {
                "status": "success",
                "message": f"sqlite-web launched on port 8081 for database {db_abs_path}. PID: {sqlite_web_process.pid}",
            }
        )
    except Exception as e:
        return (
            jsonify(
                {"status": "error", "message": f"Failed to launch sqlite-web: {e}"}
            ),
            500,
        )


@app.route("/stop-sqlite-web", methods=["POST"])
def stop_sqlite_web():
    global sqlite_web_process
    if not sqlite_web_process:
        return (
            jsonify({"status": "error", "message": "sqlite-web is not running."}),
            400,
        )

    try:
        sqlite_web_process.terminate()
        sqlite_web_process.wait()
        sqlite_web_process = None
        return jsonify({"status": "success", "message": "sqlite-web stopped."})
    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Failed to stop sqlite-web: {e}"}),
            500,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Gonk Test UI server.")
    parser.add_argument(
        "--ip",
        default="0.0.0.0",
        help="The IP address to bind the server to. Defaults to 0.0.0.0.",
    )  # nosec B104
    parser.add_argument(
        "--port",
        type=int,
        default=8082,
        help="The port to run the server on. Defaults to 8082.",
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="The base URL of the Zotify API. Defaults to http://localhost:8000.",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug mode. Defaults to False."
    )
    args = parser.parse_args()

    app.run(host=args.ip, port=args.port, debug=args.debug)

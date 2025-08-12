import os
import subprocess
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='static')
sqlite_web_process = None

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/<path:path>")
def static_proxy(path):
    """Serve static files."""
    return send_from_directory('static', path)

@app.route("/launch-sqlite-web", methods=["POST"])
def launch_sqlite_web():
    global sqlite_web_process
    if sqlite_web_process:
        return jsonify({"status": "error", "message": "sqlite-web is already running."}), 400

    database_uri = os.environ.get("DATABASE_URI")
    if not database_uri or not database_uri.startswith("sqlite:///"):
        return jsonify({"status": "error", "message": "DATABASE_URI environment variable must be set to a valid SQLite URI (e.g., sqlite:///../api/storage/zotify.db)."}), 400

    db_path = database_uri.replace("sqlite:///", "")
    db_abs_path = os.path.join(os.path.dirname(__file__), "..", db_path)

    if not os.path.exists(db_abs_path):
        return jsonify({"status": "error", "message": f"Database file not found at {db_abs_path}"}), 400

    try:
        command = ["sqlite_web", db_abs_path, "--port", "8081", "--no-browser"]
        sqlite_web_process = subprocess.Popen(command)
        return jsonify({"status": "success", "message": f"sqlite-web launched on port 8081 for database {db_abs_path}. PID: {sqlite_web_process.pid}"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to launch sqlite-web: {e}"}), 500

@app.route("/stop-sqlite-web", methods=["POST"])
def stop_sqlite_web():
    global sqlite_web_process
    if not sqlite_web_process:
        return jsonify({"status": "error", "message": "sqlite-web is not running."}), 400

    try:
        sqlite_web_process.terminate()
        sqlite_web_process.wait()
        sqlite_web_process = None
        return jsonify({"status": "success", "message": "sqlite-web stopped."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to stop sqlite-web: {e}"}), 500


if __name__ == "__main__":
    # Note: The port is hardcoded here for simplicity. In a real app,
    # this might also come from config.
    app.run(port=8082, debug=True)

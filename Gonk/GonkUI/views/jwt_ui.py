from flask import Blueprint, request, jsonify
from GonkCLI.modules.jwt_mock import JWTClient

jwt_ui = Blueprint("jwt_ui", __name__, url_prefix="/jwt")

# This is a simple in-memory client for the test UI.
# In a real multi-user app, this would be handled differently.
client = JWTClient(api_base_url="http://localhost:8000")


@jwt_ui.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        result = client.register(data["username"], data["password"])
        return jsonify({"status": "success", "data": result})
    except Exception as e:
        # It's good practice to log the actual error on the server
        # For the UI, we'll return a generic error message
        print(f"Registration failed: {e}")
        # Check if the exception has a response attribute
        if hasattr(e, 'response') and e.response is not None:
             # Try to parse the JSON error from the upstream API
            try:
                error_detail = e.response.json().get("detail", "An unknown error occurred.")
                return jsonify({"status": "error", "message": error_detail}), 400
            except ValueError: # If the response is not JSON
                error_detail = e.response.text
                return jsonify({"status": "error", "message": f"An upstream error occurred: {error_detail}"}), 500
        return jsonify({"status": "error", "message": "An internal error occurred."}), 500


@jwt_ui.route("/login", methods=["POST"])
def login():
    data = request.json
    try:
        token = client.login(data["username"], data["password"])
        return jsonify({"status": "success", "token": token})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@jwt_ui.route("/profile", methods=["GET"])
def get_profile():
    try:
        profile = client.get_profile()
        return jsonify(profile)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@jwt_ui.route("/preferences", methods=["PATCH"])
def update_preferences():
    data = request.json
    try:
        preferences = client.update_preferences(
            theme=data.get("theme"),
            language=data.get("language"),
            notifications_enabled=data.get("notifications_enabled"),
        )
        return jsonify(preferences)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@jwt_ui.route("/liked", methods=["GET"])
def get_liked():
    try:
        liked = client.get_liked_tracks()
        return jsonify(liked)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@jwt_ui.route("/history", methods=["GET"])
def get_history():
    try:
        history = client.get_history()
        return jsonify(history)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@jwt_ui.route("/history", methods=["DELETE"])
def clear_history():
    try:
        success = client.clear_history()
        if success:
            return jsonify({"status": "success", "message": "History cleared."})
        else:
            return jsonify({"status": "error", "message": "Failed to clear history."}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

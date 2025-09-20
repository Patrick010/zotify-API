import argparse
import json
from pathlib import Path
from GonkCLI.modules.jwt_mock import JWTClient

TOKEN_FILE = Path.home() / ".gonk_token"

def save_token(token):
    TOKEN_FILE.write_text(token)

def load_token():
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text()
    return None

def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser(description="Gonk CLI - A tool for interacting with the Zotify API.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Login command
    login_parser = subparsers.add_parser("login", help="Login to the Zotify API.")
    login_parser.add_argument("username", help="Your username.")
    login_parser.add_argument("password", help="Your password.")

    # Profile command
    subparsers.add_parser("get-profile", help="Get your user profile.")

    # Preferences command
    prefs_parser = subparsers.add_parser("update-prefs", help="Update your user preferences.")
    prefs_parser.add_argument("--theme", choices=["light", "dark"], help="Set the UI theme.")
    prefs_parser.add_argument("--language", help="Set the language.")
    prefs_parser.add_argument("--notifications", type=str_to_bool, help="Enable or disable notifications (true/false).")

    # Liked tracks command
    subparsers.add_parser("get-liked", help="Get your liked tracks.")

    # History commands
    subparsers.add_parser("get-history", help="Get your listening history.")
    subparsers.add_parser("clear-history", help="Clear your listening history.")

    args = parser.parse_args()

    client = JWTClient()
    token = load_token()
    if token:
        client.token = token

    try:
        if args.command == "login":
            token = client.login(args.username, args.password)
            save_token(token)
            print("Login successful. Token saved.")
            if args.verbose:
                print(f"Token: {token}")

        elif args.command == "get-profile":
            profile = client.get_profile()
            print(json.dumps(profile, indent=2))

        elif args.command == "update-prefs":
            prefs = client.update_preferences(
                theme=args.theme,
                language=args.language,
                notifications_enabled=args.notifications,
            )
            print("Preferences updated:")
            print(json.dumps(prefs, indent=2))

        elif args.command == "get-liked":
            liked = client.get_liked_tracks()
            print(json.dumps(liked, indent=2))

        elif args.command == "get-history":
            history = client.get_history()
            print(json.dumps(history, indent=2))

        elif args.command == "clear-history":
            if client.clear_history():
                print("History cleared successfully.")
            else:
                print("Failed to clear history.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()

import sys
import secrets
from api.src.zotify_api.services import user_service

HELP_TEXT = """
Gonk User Service CLI with JWT Simulation
-----------------------------------------

Commands:

1. create <username> <key=value> [...]      Create a new user
2. get <username>                           Fetch user data
3. update <username> <key=value> [...]      Update user data
4. login <username>                          Simulate login and get a JWT token
5. token <username>                          Generate a token for a user without login
6. list                                      List all users
7. clear                                     Clear all users
8. help                                      Show this help
9. exit                                      Quit CLI

Token Notes:
- Tokens are random strings for simulation only; not secure.
- Use the issued token to test Phase 3a protected endpoints.
- Auto-apply tokens in TestUI is supported (if implemented).
"""

# In-memory store of issued tokens
issued_tokens = {}

def parse_key_values(args):
    data = {}
    for kv in args:
        if "=" in kv:
            key, value = kv.split("=", 1)
            data[key] = value
    return data

def generate_token(username):
    token = secrets.token_hex(16)
    issued_tokens[username] = token
    return token

def main():
    print(HELP_TEXT)
    while True:
        try:
            cmd_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting CLI.")
            break

        if not cmd_input:
            continue

        parts = cmd_input.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == "create":
            if len(args) < 1:
                print("Usage: create <username> <key=value> ...")
                continue
            username = args[0]
            data = parse_key_values(args[1:])
            user_service.create_user(username, data)
            print(f"User '{username}' created with data: {data}")

        elif cmd == "get":
            if len(args) != 1:
                print("Usage: get <username>")
                continue
            user_data = user_service.get_user(args[0])
            print(user_data or "User not found")

        elif cmd == "update":
            if len(args) < 2:
                print("Usage: update <username> <key=value> ...")
                continue
            username = args[0]
            data = parse_key_values(args[1:])
            updated = user_service.update_user(username, data)
            print("Updated" if updated else "User not found")

        elif cmd == "login":
            if len(args) != 1:
                print("Usage: login <username>")
                continue
            username = args[0]
            if user_service.get_user(username):
                token = generate_token(username)
                print(f"Login simulated. Token for {username}: {token}")
            else:
                print("User not found")

        elif cmd == "token":
            if len(args) != 1:
                print("Usage: token <username>")
                continue
            username = args[0]
            if user_service.get_user(username):
                token = generate_token(username)
                print(f"Token generated for {username}: {token}")
            else:
                print("User not found")

        elif cmd == "list":
            all_users = user_service.list_users()
            for u in all_users:
                print(f"{u}: {user_service.get_user(u)}")

        elif cmd == "clear":
            user_service.clear_all_users()
            issued_tokens.clear()
            print("All users and tokens cleared.")

        elif cmd == "help":
            print(HELP_TEXT)

        elif cmd == "exit":
            print("Exiting CLI.")
            break

        else:
            print("Unknown command. Type 'help' for list of commands.")

if __name__ == "__main__":
    main()

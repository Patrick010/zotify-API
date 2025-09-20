Gonk JWT Mock CLI – User Service + Token Simulation
Purpose

The CLI allows developers to:

    Create, fetch, and update mock users.

    Generate JWT tokens for testing Phase 3a protected endpoints (/profile, /preferences, /liked, /history).

    Simulate login flows.

    Test endpoints without needing the real backend.

    Quickly debug user-specific functionality.

    ⚠️ Tokens are for testing only; they are random strings, not secure JWTs.

Installation / Setup

Place the module in your project:
gonk/modules/user_service_cli.py

Ensure user_service is importable from api.src.zotify_api.services.

Run the CLI:

python gonk/modules/user_service_cli.py

Commands
Command	Description	Example
create <username> <key=value> [...]	Create a new user	create alice bio=Test age=30
get <username>	Fetch user data	get alice
update <username> <key=value> [...]	Update user data	update alice bio="Updated bio"
login <username>	Simulate login and generate a token	login alice
token <username>	Generate a token without login	token alice
list	List all users and their data	list
clear	Clear all users and tokens	clear
help	Show help text	help
exit	Quit CLI	exit
Example Session

> create alice bio=Test age=30
User 'alice' created with data: {'bio': 'Test', 'age': '30'}

> login alice
Login simulated. Token for alice: 4f7a9b2e0d1f4c1e93a2d5b6c7e8f9a0

> token alice
Token generated for alice: 1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p

> get alice
{'bio': 'Test', 'age': '30'}

> update alice bio="Updated bio"
Updated

> list
alice: {'bio': 'Updated bio', 'age': '30'}

> clear
All users and tokens cleared.

> exit
Exiting CLI.

Token Notes

    Tokens simulate JWT authentication; they are random strings.

    Use tokens in your API requests via the Authorization: Bearer <TOKEN> header.

    Auto-apply tokens in TestUI is supported for seamless endpoint testing.

    Tokens expire only when clear is run or the CLI is restarted.

Tips for Developers

    Use create to populate mock users before testing protected endpoints.

    Use login to simulate real authentication flows.

    Use token if you want to test endpoints without simulating login.

    Use update to test PATCH endpoints.

    Use list to verify users and tokens at any time.

    Always clear between test runs to avoid stale data.

Visual Workflow

Developer CLI/TestUI → User Service CLI → In-Memory User Store
           │                 │
           │             Issue JWT Token
           ▼                 │
     TestUI CLI (auto-apply) │
           │                 ▼
           │        Protected Endpoints
           │        (/profile, /preferences, /liked, /history)
           ▼
        JSON Response → Developer

    CLI/TestUI: Developer interacts with Gonk CLI.

    User Service CLI: Handles mock users and token issuance.

    In-Memory Store: Stores mock user data and issued tokens.

    Protected Endpoints: API endpoints requiring JWT authentication.

    JSON Response: Returns user-specific data to developer.

This manual ensures that any developer can immediately understand the purpose, commands, and workflow for testing Phase 3a endpoints using the Gonk CLI.

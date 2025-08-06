# Operator Guide

This guide provides instructions for operators on how to manage the Zotify API.

## Admin API Key Management

The Zotify API uses a dynamic, auto-generated admin API key to protect administrative endpoints. This key is generated on the first startup of the application if no key is already configured.

### Finding the Admin API Key

On the first startup, the generated admin API key will be printed to the console. The key will also be stored in the `.admin_api_key` file in the `api` directory.

**Example console output:**
```
Generated new admin API key: 1234567890abcdef1234567890abcdef
Stored in: /path/to/zotify/api/.admin_api_key
```

It is recommended to store this key in a secure location, such as a password manager or a secure note.

### Using the Admin API Key

To make requests to protected endpoints, include the API key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-secret-key" http://0.0.0.0:8080/api/some-protected-endpoint
```

### Key Rotation and Reset

To rotate or reset the admin API key, you have two options:

1.  **Delete the key file:** Delete the `.admin_api_key` file and restart the application. A new key will be generated and printed to the console.
2.  **Set the environment variable:** Set the `ADMIN_API_KEY` environment variable to a new value. This will override the key in the `.admin_api_key` file.

### Production Environments

In a production environment, it is strongly recommended to set the `ADMIN_API_KEY` environment variable to a securely generated, random key. This will prevent the application from generating a new key on every restart if the `.admin_api_key` file is not persisted across deployments.

The application will refuse to start in a production environment (`app_env="production"`) unless an admin API key is provided. This behavior can be disabled by setting `REQUIRE_ADMIN_API_KEY_IN_PROD=false`, but this is not recommended.

## User Data

User profile and preference data is stored in the `api/storage/user_data.json` file. It is recommended to back up this file regularly.

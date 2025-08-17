# Zotify API - User Manual

This manual explains how to use the Zotify REST API to manage media downloads. This guide is intended for end-users consuming the API.

---

## 1. Authentication

For all protected endpoints, you must provide your API key in the `X-API-Key` header. There is no separate login step.

---

## 2. Core API Workflow

### 2.1. Add a Track for Download

#### Purpose
To submit a new track to the download queue.

#### Endpoint
`POST /api/download`

#### Request Example
\`\`\`bash
curl -X POST "https://zotify.yourdomain.com/api/download" \
  -H "X-API-Key: your_secret_admin_key" \
  -H "Content-Type: application/json" \
  -d '{"track_ids": ["spotify:track:3n3Ppam7vgaVa1iaRUc9Lp"]}'
\`\`\`

#### Response Example
\`\`\`json
[
  {
    "job_id": "a1b2c3d4-...",
    "track_id": "spotify:track:3n3Ppam7vgaVa1iaRUc9Lp",
    "status": "pending",
    "progress": 0.0,
    "created_at": "2025-08-17T16:00:00Z",
    "error_message": null
  }
]
\`\`\`

### 2.2. Check Download Queue Status

#### Purpose
To retrieve the status of all current and past download jobs.

#### Endpoint
`GET /api/download/status`

#### Request Example
\`\`\`bash
curl -X GET "https://zotify.yourdomain.com/api/download/status" \
  -H "X-API-Key: your_secret_admin_key"
\`\`\`

#### Response Example
\`\`\`json
{
  "total_jobs": 1,
  "pending": 1,
  "completed": 0,
  "failed": 0,
  "jobs": [
    {
      "job_id": "a1b2c3d4-...",
      "track_id": "spotify:track:3n3Ppam7vgaVa1iaRUc9Lp",
      "status": "pending",
      "progress": 0.0,
      "created_at": "2025-08-17T16:00:00Z",
      "error_message": null
    }
  ]
}
\`\`\`

---

## 3. Error Handling

When an API request fails, you will receive a JSON response with a specific error code.

| Status Code | Error Code | Description                                                                 |
| ----------- | ---------- | --------------------------------------------------------------------------- |
| `401`       | `E40101`   | Authentication failed. Your `X-API-Key` is missing or incorrect.            |
| `404`       | `E40401`   | The requested resource (e.g., a specific job ID) could not be found.        |
| `422`       | `E42201`   | Invalid request payload. The request body is missing required fields or has incorrect data types. |
| `500`       | `E50001`   | An unexpected error occurred on the server.                                 |

**Example Error Response:**
\`\`\`json
{
  "error": {
    "code": "E40101",
    "message": "Authentication failed: Invalid or missing API key.",
    "timestamp": "2025-08-17T16:05:00Z",
    "request_id": "uuid-..."
  }
}
\`\`\`

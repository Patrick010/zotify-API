# Project API Endpoints Reference

## Overview

This file lists all public API endpoints for the <PROJECT_NAME>, generated from the OpenAPI schema. It provides a high-level reference for developers, operators, and auditors.

### Notes:

-   Authentication requirements are noted for each endpoint.
-   This file is auto-generated. Do not edit it manually. To update this file, run the appropriate script to re-generate it from your project's OpenAPI specification.

---

## <PROJECT_NAME> API Endpoints

### `auth` (Example)
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/auth/status` | Get authentication status | Yes |
| POST | `/api/auth/login` | Log in to the service | No |
| POST | `/api/auth/logout` | Log out from the service | Yes |

### `resource` (Example)
| Method | Path | Summary | Auth Required |
|---|---|---|---|
| GET | `/api/resource` | List all resources | Yes |
| GET | `/api/resource/{id}` | Get a specific resource | Yes |
| POST | `/api/resource` | Create a new resource | Yes |
| DELETE | `/api/resource/{id}` | Delete a resource | Yes |

---

## [Add More Endpoint Groups as Documented in Your OpenAPI Spec]

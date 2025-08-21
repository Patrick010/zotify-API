import json

def generate_endpoints_md():
    with open("openapi.json", "r") as f:
        openapi_spec = json.load(f)

    endpoints_by_tag = {}
    for path, path_item in openapi_spec.get("paths", {}).items():
        for method, operation in path_item.items():
            if "tags" in operation and operation["tags"]:
                tag = operation["tags"][0]
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []

                auth_required = False
                if "parameters" in operation:
                    for param in operation["parameters"]:
                        if param.get("name") == "X-API-Key":
                            auth_required = True
                            break

                # Also check security at operation level
                if "security" in operation:
                    # A bit simplistic, but good enough for this purpose
                    auth_required = True

                summary = operation.get("summary", "")
                endpoints_by_tag[tag].append(
                    f"| {method.upper()} | `{path}` | {summary} | {'Yes' if auth_required else 'No'} |"
                )

    markdown_content = """# Project API Endpoints Reference

## Overview

This file lists all public API endpoints for the Zotify API project, generated from the OpenAPI schema. It provides a high-level reference for developers, operators, and auditors.

### Notes:

-   Authentication requirements are noted for each endpoint.
-   This file is auto-generated. Do not edit it manually.

---

## Zotify API Endpoints
"""

    for tag in sorted(endpoints_by_tag.keys()):
        markdown_content += f"\n### `{tag}`\n"
        markdown_content += "| Method | Path | Summary | Auth Required |\n"
        markdown_content += "|---|---|---|---|\n"
        markdown_content += "\n".join(sorted(endpoints_by_tag[tag]))
        markdown_content += "\n"

    with open("project/ENDPOINTS.md", "w") as f:
        f.write(markdown_content)

    print("project/ENDPOINTS.md generated successfully.")

if __name__ == "__main__":
    generate_endpoints_md()

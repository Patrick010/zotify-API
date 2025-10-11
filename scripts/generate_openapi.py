# ID: OPS-012
import json
import os
import sys
from pathlib import Path

# Set app environment to testing
os.environ["APP_ENV"] = "testing"

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from api.src.zotify_api.main import app


def generate_openapi_spec():
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=2)
    print("openapi.json generated successfully.")


if __name__ == "__main__":
    generate_openapi_spec()

import json
import sys
from pathlib import Path

from api.src.zotify_api.main import app

# Add project root to path
project_root = Path(__file__).parent
api_src_path = project_root / "api" / "src"
sys.path.insert(0, str(api_src_path))
sys.path.insert(0, str(project_root))


def generate_openapi_spec():
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=2)
    print("openapi.json generated successfully.")


if __name__ == "__main__":
    generate_openapi_spec()

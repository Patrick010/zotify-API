# save as list_routes.py and run with `python list_routes.py`

import importlib
from fastapi import FastAPI

# Adjust this to your actual app import path:
app_module = "zotify_api.main"
app_attr = "app"

def main():
    module = importlib.import_module(app_module)
    app: FastAPI = getattr(module, app_attr)

    print("Registered routes:")
    for route in app.routes:
        methods = ",".join(route.methods) if route.methods else "N/A"
        print(f"{methods:10} {route.path}")

if __name__ == "__main__":
    main()

import importlib
import os
import httpx
from fastapi import FastAPI

# Adjust this to your actual app import path:
app_module = "zotify_api.main"
app_attr = "app"
BASE_URL = "http://127.0.0.1:8000"


def main():
    """
    Dynamically imports the FastAPI app, discovers all GET routes that
    don't require path parameters, and then sends a request to each one
    to check its status.
    """
    print(f"--- Starting API Audit for {app_module} ---")
    print(f"--- Target Base URL: {BASE_URL} ---")

    # Set the app environment to development to avoid startup errors
    os.environ["APP_ENV"] = "development"

    try:
        module = importlib.import_module(app_module)
        app: FastAPI = getattr(module, app_attr)
    except Exception as e:
        print(f"Error: Could not import FastAPI app '{app_attr}' from module '{app_module}'.")
        print(f"Details: {e}")
        return

    ok_routes = []
    error_routes = []

    with httpx.Client(base_url=BASE_URL, follow_redirects=True) as client:
        for route in app.routes:
            # We can only automatically test GET routes that have no path parameters
            if "GET" in route.methods and "{" not in route.path:
                path = route.path
                print(f"Testing GET {path}...")
                try:
                    response = client.get(path)
                    if response.status_code == 200:
                        ok_routes.append(path)
                    else:
                        error_routes.append(f"{path} (Status: {response.status_code})")
                except httpx.RequestError as e:
                    error_routes.append(f"{path} (Request Error: {e})")

    print("\n--- API Audit Summary ---")
    if ok_routes:
        print("✅ OK Routes:")
        for r in sorted(ok_routes):
            print(f" - {r}")

    if error_routes:
        print("\n❌ Error Routes:")
        for r in sorted(error_routes):
            print(f" - {r}")

    if not error_routes:
        print("\nAll discoverable GET routes responded successfully.")


if __name__ == "__main__":
    main()

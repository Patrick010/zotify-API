# ID: OPS-004
import inspect
from fastapi import FastAPI
from fastapi.routing import APIRoute
import sys
from pathlib import Path

# Add the project source to the Python path
project_root = Path(__file__).parent
api_src_path = project_root / "api" / "src"
sys.path.insert(0, str(api_src_path))


def analyze_route_status(app: FastAPI):
    route_status = []
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        path = route.path
        methods = route.methods
        endpoint = route.endpoint
        doc = inspect.getdoc(endpoint) or ""

        try:
            source = inspect.getsource(endpoint)
        except TypeError:
            # This can happen for functools.partial objects, etc.
            # We'll assume these are not stubs for this analysis.
            source = ""

        # Heuristic: look for '501' or 'NotImplementedError' in source code to flag stubs
        if "501" in source or "NotImplementedError" in source:
            status = "Stub"
        # Another heuristic: check for a placeholder response
        elif 'return {"status":' in source and "stub" in source:
            status = "Stub"
        else:
            status = "Functional"

        route_status.append(
            {
                "path": path,
                "methods": sorted(list(methods)),
                "status": status,
                "doc": doc.strip(),
            }
        )

    return route_status


if __name__ == "__main__":
    try:
        from zotify_api.main import app  # Adjust import path as necessary
    except ImportError as e:
        print(f"Failed to import FastAPI app: {e}")
        print(f"Current sys.path: {sys.path}")
        sys.exit(1)

    status_report = analyze_route_status(app)

    # This is not for the final report, just for me to parse
    for route in status_report:
        print(
            f"{'|'.join(route['methods'])}|{route['path']}|{route['status']}|{route['doc']}"
        )

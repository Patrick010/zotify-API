import json

def summarize_routes(file_path):
    missing = []
    empty = []
    valid = []

    with open(file_path) as f:
        # The file contains multiple JSON objects separated by newlines, parse them one by one
        for line in f:
            line = line.strip()
            if not line:
                continue
            route_obj = json.loads(line)
            route = route_obj.get("route")
            data = route_obj.get("data")

            if isinstance(data, dict) and data.get("detail") == "Not Found":
                missing.append(route)
            elif not data or (isinstance(data, dict) and len(data) == 0):
                empty.append(route)
            else:
                valid.append(route)

    print("=== API Route Audit Summary ===")
    print(f"Missing routes (Not Found): {missing}")
    print(f"Routes with empty/null data: {empty}")
    print(f"Routes with valid data: {valid}")

if __name__ == "__main__":
    summarize_routes("api_all_routes.json")

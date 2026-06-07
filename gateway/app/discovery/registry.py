import json
import os

def load_services():
    registry_path = os.getenv("REGISTRY_PATH", "/app/registry/registry.json")
    try:
        with open(registry_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading registry: {e}")
        return {}

SERVICES = load_services()

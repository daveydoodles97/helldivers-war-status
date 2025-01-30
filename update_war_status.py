import requests
import json
import datetime

# API URLs
TRAINING_MANUAL_API = "https://helldiverstrainingmanual.com/api/v1/war/status"
HELLHUB_API_BASE = "https://api-hellhub-collective.koyeb.app/api"

# Additional data sources
ADDITIONAL_APIS = {
    "orders": f"{HELLHUB_API_BASE}/orders",
    "assignments": f"{HELLHUB_API_BASE}/assignments",
    "reports": f"{HELLHUB_API_BASE}/reports"
}

# HellHub endpoints
HELLHUB_ENDPOINTS = {
    "planets": f"{HELLHUB_API_BASE}/planets",
    "war": f"{HELLHUB_API_BASE}/war",
    "contributions": f"{HELLHUB_API_BASE}/contributions",
    "factions": f"{HELLHUB_API_BASE}/factions",
    "events": f"{HELLHUB_API_BASE}/events"
}

JSON_FILE = "war_status.json"

def fetch_latest_api_data(url):
    """Fetch only the latest data from an API without paginating."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data[0]  # Return only the latest entry
            return data  # If it's not a list, return as is
        else:
            return {"error": f"Failed to fetch data, status: {response.status_code}"}
    except Exception as e:
        return {"error": f"API request failed: {str(e)}"}

def load_previous_data():
    """Load previously stored data from JSON file."""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return empty if file is corrupted
    return {}
    
def update_war_status():
    """Fetch only the latest data and update JSON if necessary."""
    previous_data = load_previous_data()

    new_training_manual_data = fetch_latest_api_data(TRAINING_MANUAL_API)
    new_hellhub_data = {key: fetch_latest_api_data(url) for key, url in HELLHUB_ENDPOINTS.items()}
    new_additional_data = {key: fetch_latest_api_data(url) for key, url in ADDITIONAL_APIS.items()}

    new_combined_data = {
        "last_updated": datetime.datetime.utcnow().isoformat() + " UTC",
        "TrainingManual": new_training_manual_data,
        "HellHub": new_hellhub_data,
        "OrdersAssignmentsReports": new_additional_data
    }

    # Update only if new data differs from previous data
    if previous_data != new_combined_data:
        with open(JSON_FILE, "w") as file:
            json.dump(new_combined_data, file, indent=4)
        print("✅ War status updated with the latest data!")
    else:
        print("🔄 No new updates, keeping previous data.")


# Run the update process
update_war_status()

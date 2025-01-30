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

def fetch_api_data(url):
    """Fetch data from an API and return the JSON response."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch data, status: {response.status_code}"}
    except Exception as e:
        return {"error": f"API request failed: {str(e)}"}

def update_war_status():
    """Fetch data from multiple APIs, merge, and save to JSON file."""
    training_manual_data = fetch_api_data(TRAINING_MANUAL_API)
    hellhub_data = {key: fetch_api_data(url) for key, url in HELLHUB_ENDPOINTS.items()}
    additional_data = {key: fetch_api_data(url) for key, url in ADDITIONAL_APIS.items()}

    combined_data = {
        "last_updated": datetime.datetime.utcnow().isoformat() + " UTC",
        "TrainingManual": training_manual_data,
        "HellHub": hellhub_data,
        "OrdersAssignmentsReports": additional_data
    }

    with open(JSON_FILE, "w") as file:
        json.dump(combined_data, file, indent=4)
    
    print("✅ War status updated!")

# Run the update process
update_war_status()

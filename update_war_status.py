import requests
import json
import datetime

# Fetch war data from Helldivers Training Manual API
API_URL = "https://helldiverstrainingmanual.com/api/v1/war/status"
JSON_FILE = "war_status.json"

def fetch_war_status():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            data["last_updated"] = datetime.datetime.utcnow().isoformat() + " UTC"
            return data
        else:
            return {"error": f"Failed to fetch data, status: {response.status_code}"}
    except Exception as e:
        return {"error": f"API request failed: {str(e)}"}

# Save the updated data
def update_json_file():
    data = fetch_war_status()
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)
    print("War status updated!")

# Run update
update_json_file()

import requests
import json
import datetime
import os

# Trusted Super Earth APIs
TRAINING_MANUAL_API = "https://helldiverstrainingmanual.com/api/v1/war/status"
WAR_NEWS_API = "https://helldiverstrainingmanual.com/api/v1/war/news"
NEWS_MESSAGES_API = "https://helldiverstrainingmanual.com/api/v1/war/news-messages"  # NEW API
MAJOR_ORDERS_API = "https://helldiverstrainingmanual.com/api/v1/war/major-orders"
CAMPAIGN_PLANETS_API = "https://helldiverstrainingmanual.com/api/v1/war/campaign"

# Helldivers-2 API Sources
HELLDIVERS_2_API_BASE = "https://helldivers-2.github.io/api/v1/war"
HELLDIVERS_2_ENDPOINTS = {
    "status": f"{HELLDIVERS_2_API_BASE}/status",
    "orders": f"{HELLDIVERS_2_API_BASE}/orders",
    "events": f"{HELLDIVERS_2_API_BASE}/events",
    "planets": f"{HELLDIVERS_2_API_BASE}/planets"
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
    """Fetch new data and only update if there are changes."""
    previous_data = load_previous_data()

    # Super Earth Verified Data
    new_war_news = fetch_api_data(WAR_NEWS_API)
    new_news_messages = fetch_api_data(NEWS_MESSAGES_API)  # NEW DATA
    new_major_orders = fetch_api_data(MAJOR_ORDERS_API)
    new_campaign_planets = fetch_api_data(CAMPAIGN_PLANETS_API)
    
    # Helldivers-2 API Data
    new_helldivers_2_data = {key: fetch_api_data(url) for key, url in HELLDIVERS_2_ENDPOINTS.items()}

    new_combined_data = {
        "last_updated": datetime.datetime.utcnow().isoformat() + " UTC",
        "SuperEarth": {
            "WarNews": new_war_news,
            "NewsMessages": new_news_messages,  # NEW DATA
            "MajorOrders": new_major_orders,
            "CampaignPlanets": new_campaign_planets
        },
        "Helldivers2": new_helldivers_2_data
    }

    # Update only if new data differs from previous data
    if previous_data != new_combined_data:
        with open(JSON_FILE, "w") as file:
            json.dump(new_combined_data, file, indent=4)
        print("✅ War status updated with latest data from verified sources!")
    else:
        print("🔄 No new updates, keeping previous data.")

# Run the update process
update_war_status()


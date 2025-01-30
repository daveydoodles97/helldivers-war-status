import requests
import json
import datetime
import os

# Trusted Super Earth APIs
TRAINING_MANUAL_API = "https://helldiverstrainingmanual.com/api/v1/war/status"
WAR_NEWS_API = "https://helldiverstrainingmanual.com/api/v1/war/news"
NEWS_MESSAGES_API = "https://helldiverstrainingmanual.com/api/v1/war/news-messages"
MAJOR_ORDERS_API = "https://helldiverstrainingmanual.com/api/v1/war/major-orders"
CAMPAIGN_PLANETS_API = "https://helldiverstrainingmanual.com/api/v1/war/campaign"

# Helldivers 2 APIs
HELLDIVERS_2_NEWS_API = "https://api.helldivers2.dev/raw/api/NewsFeed/801"
HELLDIVERS_2_ASSIGNMENT_API = "https://api.helldivers2.dev/raw/api/v2/Assignment/War/801"  # NEW API

JSON_FILE = "war_status.json"

def fetch_api_data(url, headers=None):
    """Fetch data from an API and return the JSON response."""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"⚠️ WARNING: {url} returned 404. Skipping...")
            return None  # Ignore 404 errors
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
    new_news_messages = fetch_api_data(NEWS_MESSAGES_API)
    new_major_orders = fetch_api_data(MAJOR_ORDERS_API)
    new_campaign_planets = fetch_api_data(CAMPAIGN_PLANETS_API)
    
    # Helldivers 2 News Feed
    news_headers = {
        "accept": "application/json",
        "X-Super-Client": "c",
        "X-Super-Contact": "cf"
    }
    new_helldivers_2_news = fetch_api_data(HELLDIVERS_2_NEWS_API, headers=news_headers)

    # Helldivers 2 War Assignments (Major Orders)
    assignment_headers = {
        "accept": "application/json",
        "X-Super-Client": "rec1",
        "X-Super-Contact": "davidb"
    }
    new_helldivers_2_assignments = fetch_api_data(HELLDIVERS_2_ASSIGNMENT_API, headers=assignment_headers)

    new_combined_data = {
        "last_updated": datetime.datetime.utcnow().isoformat() + " UTC",
        "SuperEarth": {
            "WarNews": new_war_news,
            "NewsMessages": new_news_messages,
            "MajorOrders": new_major_orders,
            "CampaignPlanets": new_campaign_planets
        },
        "Helldivers2": {
            "NewsFeed": new_helldivers_2_news,
            "WarAssignments": new_helldivers_2_assignments  # NEW DATA
        }
    }

    # Update only if new data differs from previous data
    if previous_data != new_combined_data:
        with open(JSON_FILE, "w") as file:
            json.dump(new_combined_data, file, indent=4)
        print("✅ War status updated with latest assignments and news!")
    else:
        print("🔄 No new updates, keeping previous data.")

# Run the update process
update_war_status()


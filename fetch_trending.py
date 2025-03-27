
import requests
import pandas as pd
import os
from datetime import datetime
import time

# API Key should be stored securely (e.g., in environment variables)
API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"
if not API_KEY:
    raise ValueError("Missing API Key! Set YOUTUBE_API_KEY as an environment variable.")

REGION = "IN"  # Fetch trending videos for India
MAX_RESULTS = 15
CSV_FILE = "trending_videos.csv"
CATEGORY_MAP = {}  # Will store Category ID -> Name mapping

def fetch_category_mapping():
    """Fetch YouTube video category names."""
    url = f"https://www.googleapis.com/youtube/v3/videoCategories?part=snippet&regionCode={REGION}&key={API_KEY}"
    response = requests.get(url).json()
    
    global CATEGORY_MAP
    CATEGORY_MAP = {item["id"]: item["snippet"]["title"] for item in response.get("items", [])}

def fetch_trending_videos():
    """Fetch trending YouTube videos and return as a list."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    
    for attempt in range(3):  # Retry logic
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise HTTP errors
            
            data = response.json()
            if "items" not in data:
                raise ValueError("No trending videos found!")

            videos = []
            for idx, video in enumerate(data.get("items", []), start=1):
                video_id = video["id"]
                snippet = video["snippet"]
                statistics = video.get("statistics", {})

                views = int(statistics.get("viewCount", 0))
                likes = int(statistics.get("likeCount", 0))
                comments = int(statistics.get("commentCount", 0))
                engagement_rate = round((likes + comments) / views, 4) if views > 0 else 0
                
                # Get video category name
                category_id = snippet.get("categoryId", "Unknown")
                category = CATEGORY_MAP.get(category_id, "Unknown")
                
                # Get country of channel (API limitation: needs separate call)
                channel_id = snippet["channelId"]
                channel_region = fetch_channel_region(channel_id)

                videos.append({
                    "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
                    "Rank": idx,
                    "Video_ID": video_id,
                    "Title": snippet["title"],
                    "Views": views,
                    "Likes": likes,
                    "Comments": comments,
                    "Engagement_Rate": engagement_rate,
                    "Genre": category,
                    "Region": channel_region
                })

            return videos

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data (Attempt {attempt+1}/3): {e}")
            time.sleep(5)  # Wait before retrying

    return []  # Return empty list on failure

def fetch_channel_region(channel_id):
    """Fetch the country where the channel is based."""
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()
    return response.get("items", [{}])[0].get("snippet", {}).get("country", "Unknown")

def save_data():
    """Fetch data and append to CSV file."""
    fetch_category_mapping()  # Fetch category names
    videos = fetch_trending_videos()
    df = pd.DataFrame(videos)

    if os.path.exists(CSV_FILE):
        existing_df = pd.read_csv(CSV_FILE)
        df = pd.concat([existing_df, df]).drop_duplicates(subset=["Video_ID", "Trending_Date"], keep="last")

    df.to_csv(CSV_FILE, index=False)
    print(f"Fetched {len(videos)} trending videos for region {REGION}. Data saved!")

if __name__ == "__main__":
    save_data()

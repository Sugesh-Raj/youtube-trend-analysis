import requests
import pandas as pd
import os
from datetime import datetime

# YouTube API Key (Use Directly)
API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"
REGION = "IN"
MAX_RESULTS = 15
CSV_FILE = "trending_videos.csv"

# Dictionary to map common state mentions in descriptions/titles
STATES = ["Tamil Nadu", "Karnataka", "Maharashtra", "Kerala", "Delhi", "West Bengal",
          "Andhra Pradesh", "Telangana", "Uttar Pradesh", "Gujarat", "Punjab"]

def get_channel_country(channel_id):
    """Fetch country of the channel."""
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()

    return response["items"][0]["snippet"].get("country", "Unknown") if "items" in response else "Unknown"

def extract_state_from_description(description):
    """Check if any known state name is mentioned in the description."""
    for state in STATES:
        if state.lower() in description.lower():
            return state
    return "Unknown"

def fetch_trending_videos():
    """Fetch trending YouTube videos with engagement rate, genre, and state/region."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url).json()

    videos = []
    for idx, video in enumerate(response.get("items", []), start=1):
        views = int(video["statistics"].get("viewCount", 0))
        likes = int(video["statistics"].get("likeCount", 0))
        comments = int(video["statistics"].get("commentCount", 0))
        engagement_rate = round((likes + comments) / views, 4) if views > 0 else 0
        genre = video["snippet"].get("categoryId", "Unknown")
        
        # Extract possible state/region info
        channel_id = video["snippet"]["channelId"]
        country = get_channel_country(channel_id)
        state = extract_state_from_description(video["snippet"].get("description", ""))

        videos.append({
            "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
            "Rank": idx,
            "Video_ID": video["id"],
            "Title": video["snippet"]["title"],
            "Views": views,
            "Likes": likes,
            "Comments": comments,
            "Engagement_Rate": engagement_rate,
            "Genre": genre,
            "Country": country,
            "State": state if state != "Unknown" else country  # Fallback to country if state is unknown
        })

    return videos

def save_data():
    """Fetch data and append to CSV file."""
    videos = fetch_trending_videos()
    df = pd.DataFrame(videos)

    # Append data if file exists, otherwise create a new file
    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)
    else:
        df.to_csv(CSV_FILE, index=False)

    print("Trending videos data saved!")

if __name__ == "__main__":
    save_data()


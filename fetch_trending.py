import requests
import pandas as pd
import os
from datetime import datetime

# YouTube API Key (Replace with your actual key)
API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"
REGION = "IN"
MAX_RESULTS = 15
CSV_FILE = "trending_videos.csv"

# Category ID to Genre Mapping
CATEGORY_MAPPING = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "How-to & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism"
}

def get_channel_location(channel_id):
    """Fetch country and state (if available) of a channel."""
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()
    
    country = "Unknown"
    state = "Unknown"

    if "items" in response and len(response["items"]) > 0:
        snippet = response["items"][0]["snippet"]
        country = snippet.get("country", "Unknown")

        # Extract state if mentioned in the location
        location = snippet.get("customUrl", "")
        if "," in location:
            state = location.split(",")[-1].strip()
    
    return country, state

def fetch_trending_videos():
    """Fetch trending YouTube videos and return as a list with additional data."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url).json()

    videos = []
    for idx, video in enumerate(response.get("items", []), start=1):
        video_id = video["id"]
        snippet = video["snippet"]
        stats = video.get("statistics", {})

        channel_id = snippet["channelId"]
        country, state = get_channel_location(channel_id)  # Fetch country & state

        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))

        # Get Category ID and map it to Genre Name
        category_id = snippet["categoryId"]
        genre = CATEGORY_MAPPING.get(category_id, "Unknown")

        # Engagement Rate Formula
        engagement_rate = round((likes + comments) / views, 4) if views > 0 else 0

        videos.append({
            "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
            "Rank": idx,
            "Video_ID": video_id,
            "Title": snippet["title"],
            "Views": views,
            "Likes": likes,
            "Comments": comments,

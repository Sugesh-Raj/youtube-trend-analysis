import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import isodate  # For parsing video duration

# YouTube API Key (Replace with your actual key)
API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"
REGION = "IN"  # Fetching videos from India
MAX_RESULTS = 15
CSV_FILE = "trending_videos.csv"

def get_channel_location(channel_id):
    """Fetch country & state information of the video uploader"""
    url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={channel_id}&key={API_KEY}"
    response = requests.get(url).json()
    
    try:
        country = response["items"][0]["snippet"].get("country", "Unknown")
        title = response["items"][0]["snippet"].get("title", "")
        
        # If the title contains a city or state name, extract it
        state = title.split("|")[-1].strip() if "|" in title else "Unknown"
        return country, state
    except (KeyError, IndexError):
        return "Unknown", "Unknown"

def get_video_details(video_id):
    """Fetch video length (duration) and category"""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails,snippet&id={video_id}&key={API_KEY}"
    response = requests.get(url).json()
    
    try:
        details = response["items"][0]
        duration = details["contentDetails"]["duration"]
        category_id = details["snippet"]["categoryId"]
        
        # Convert ISO 8601 duration to readable format
        readable_duration = convert_duration(duration)

        return readable_duration, category_id
    except (KeyError, IndexError):
        return "Unknown", "Unknown"

def convert_duration(duration):
    """Convert ISO 8601 duration (PT5M30S) to human-readable format (5m 30s)"""
    try:
        parsed_duration = isodate.parse_duration(duration)
        total_seconds = int(parsed_duration.total_seconds())

        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        if hours:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"
    except:
        return "Unknown"

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

        # Engagement Rate Formula: (Likes + Comments) / Views
        engagement_rate = round((likes + comments) / views, 4) if views > 0 else 0

        # Fetch video length and category
        video_length, category_id = get_video_details(video_id)

        videos.append({
            "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
            "Rank": idx,
            "Video_ID": video_id,
            "Title": snippet["title"],
            "Views": views,
            "Likes": likes,
            "Comments": comments,
            "Engagement_Rate": engagement_rate,
            "Video_Length": video_length,
            "Genre": category_id,  # Placeholder (categoryId needs mapping)
            "Country": country,
            "State": state
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



import requests
import pandas as pd
import os
from datetime import datetime

# Directly use API Key
API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"
REGION = "IN"
MAX_RESULTS = 15
CSV_FILE = "trending_videos.csv"

def fetch_trending_videos():
    """Fetch trending YouTube videos with engagement rate, genre, and region."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url).json()

    videos = []
    for idx, video in enumerate(response.get("items", []), start=1):
        views = int(video["statistics"].get("viewCount", 0))
        likes = int(video["statistics"].get("likeCount", 0))
        comments = int(video["statistics"].get("commentCount", 0))
        engagement_rate = round((likes + comments) / views, 4) if views > 0 else 0
        genre = video["snippet"].get("categoryId", "Unknown")  # YouTube API provides category ID
        region = video["snippet"]["channelTitle"]  # Approximate source of region

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
            "Region": region
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

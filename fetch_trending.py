import os
import requests
import pandas as pd
from datetime import datetime

# YouTube API Key (Use environment variable for security)
API_KEY = os.getenv("YOUTUBE_API_KEY")
REGION = "IN"
MAX_RESULTS = 50
CSV_FILE = "trending_videos.csv"

def fetch_trending_videos():
    """Fetch trending YouTube videos and return as a list."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url).json()

    videos = []
    for idx, video in enumerate(response.get("items", []), start=1):
        videos.append({
            "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
            "Rank": idx,
            "Video_ID": video["id"],
            "Title": video["snippet"]["title"],
            "Views": int(video["statistics"].get("viewCount", 0)),
            "Likes": int(video["statistics"].get("likeCount", 0)),
            "Comments": int(video["statistics"].get("commentCount", 0)),
            "Genre": video["snippet"].get("categoryId", "Unknown"),
            "Region": REGION,
            "Upload_Date": video["snippet"]["publishedAt"][:10],
            "Engagement_Rate": int(video["statistics"].get("likeCount", 0)) / (int(video["statistics"].get("commentCount", 0)) + 1)  # Avoid division by zero
        })
    return videos

def save_data():
    """Fetch data and append to CSV file."""
    videos = fetch_trending_videos()
    df = pd.DataFrame(videos)

    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)
    else:
        df.to_csv(CSV_FILE, index=False)
    
    print("Trending videos data saved!")

if __name__ == "__main__":
    save_data()
    

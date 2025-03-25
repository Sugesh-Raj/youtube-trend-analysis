import os
import requests
import pandas as pd
from datetime import datetime

# Get API key from environment variable
API_KEY = os.getenv("AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4")  # Use a proper environment variable name
if not API_KEY:
    raise ValueError("⚠️ API Key not found! Set the 'YOUTUBE_API_KEY' environment variable.")

REGION = "IN"
MAX_RESULTS = 50
CSV_FILE = "trending_videos.csv"

def fetch_trending_videos():
    """Fetch trending YouTube videos and return as a list."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"❌ API Request Failed! Status Code: {response.status_code} | Response: {response.text}")

    data = response.json()
    videos = []

    for idx, video in enumerate(data.get("items", []), start=1):
        like_count = int(video["statistics"].get("likeCount", 0))
        comment_count = int(video["statistics"].get("commentCount", 0))

        videos.append({
            "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
            "Rank": idx,
            "Video_ID": video["id"],
            "Title": video["snippet"]["title"],
            "Views": int(video["statistics"].get("viewCount", 0)),
            "Likes": like_count,
            "Comments": comment_count,
            "Genre": video["snippet"].get("categoryId", "Unknown"),
            "Region": REGION,
            "Upload_Date": video["snippet"]["publishedAt"][:10],
            "Engagement_Rate": like_count / (comment_count + 1)  # Avoid division by zero
        })

    return videos

def save_data():
    """Fetch data and append to CSV file."""
    videos = fetch_trending_videos()
    df = pd.DataFrame(videos)

    abs_path = os.path.abspath(CSV_FILE)
    print(f"📁 Saving trending data to: {abs_path}")

    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)
    else:
        df.to_csv(CSV_FILE, index=False)

    print("✅ Trending videos data saved successfully!")

if __name__ == "__main__":
    save_data()

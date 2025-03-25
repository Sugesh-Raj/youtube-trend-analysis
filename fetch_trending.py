import os
import requests
import pandas as pd
from datetime import datetime

# YouTube API Key (Use environment variable for security)
API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"  # Make sure to set this in GitHub Secrets or locally
REGION = "IN"
MAX_RESULTS = 50
CSV_FILE = "trending_videos.csv"  # Save CSV directly in the project directory

# Category ID to Genre Mapping (for India "IN")
CATEGORY_MAP = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "21": "Videoblogging",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
    "30": "Movies",
    "31": "Anime/Animation",
    "32": "Action/Adventure",
    "33": "Classics",
    "34": "Comedy",
    "35": "Documentary",
    "36": "Drama",
    "37": "Family",
    "38": "Foreign",
    "39": "Horror",
    "40": "Sci-Fi/Fantasy",
    "41": "Thriller",
    "42": "Shorts",
    "43": "Shows",
    "44": "Trailers"
}

def fetch_trending_videos():
    """Fetch trending YouTube videos and return as a list."""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url).json()

    # Check if API response is valid
    if "items" not in response:
        print("❌ Error fetching data:", response)
        return []

    videos = []
    for idx, video in enumerate(response["items"], start=1):
        category_id = video["snippet"].get("categoryId", "Unknown")
        genre = CATEGORY_MAP.get(category_id, "Unknown")

        videos.append({
            "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
            "Rank": idx,
            "Video_ID": video["id"],
            "Title": video["snippet"]["title"],
            "Views": int(video["statistics"].get("viewCount", 0)),
            "Likes": int(video["statistics"].get("likeCount", 0)),
            "Comments": int(video["statistics"].get("commentCount", 0)),
            "Genre": genre,  # Replaced category ID with actual genre
            "Region": REGION,
            "Upload_Date": video["snippet"]["publishedAt"][:10],
            "Engagement_Rate": int(video["statistics"].get("likeCount", 0)) / (int(video["statistics"].get("commentCount", 0)) + 1)  # Avoid division by zero
        })
    return videos

def save_data():
    """Fetch data and save to CSV file."""
    videos = fetch_trending_videos()
    if not videos:
        print("❌ No data to save. Exiting...")
        return

    df = pd.DataFrame(videos)
    df.to_csv(CSV_FILE, index=False)
    print(f"✅ Trending videos data saved at {CSV_FILE}")

if __name__ == "__main__":
    save_data()

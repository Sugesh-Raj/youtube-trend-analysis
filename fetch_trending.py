import requests
import pandas as pd
import os
from datetime import datetime

# YouTube API Key (Replace with your actual key)
API_KEY = "AIzaSyCbE9LwgnK_lGlMTpQpItxi58WCkhfwit4"
REGION = "IN"
MAX_RESULTS = 15
CSV_FILE = "trending_videos.csv"

# YouTube Video Categories Mapping
CATEGORY_MAPPING = {
    "1": "Film & Animation", "2": "Autos & Vehicles", "10": "Music", "15": "Pets & Animals",
    "17": "Sports", "18": "Short Movies", "19": "Travel & Events", "20": "Gaming",
    "22": "People & Blogs", "23": "Comedy", "24": "Entertainment", "25": "News & Politics",
    "26": "How-to & Style", "27": "Education", "28": "Science & Technology", "30": "Movies",
    "31": "Anime/Animation", "32": "Action/Adventure", "33": "Classics", "34": "Comedy",
    "35": "Documentary", "36": "Drama", "37": "Family", "38": "Foreign", "39": "Horror",
    "40": "Sci-Fi/Fantasy", "41": "Thriller", "42": "Shorts", "43": "Shows", "44": "Trailers"
}

def fetch_trending_videos():
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={REGION}&maxResults={MAX_RESULTS}&key={API_KEY}"
    response = requests.get(url).json()

    videos = []
    for idx, video in enumerate(response.get("items", []), start=1):
        snippet = video["snippet"]
        stats = video.get("statistics", {})

        category_id = snippet.get("categoryId", "Unknown")
        genre = CATEGORY_MAPPING.get(category_id, "Unknown")
        upload_date = snippet["publishedAt"][:10]  # Extract only YYYY-MM-DD
        
        views = int(stats.get("viewCount", 0))
        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))
        
        # Engagement Rate Calculation (likes/comments, avoiding division by zero)
        engagement_rate = round(likes / comments if comments > 0 else 0, 2)

        videos.append({
            "Trending_Date": datetime.now().strftime("%Y-%m-%d"),
            "Rank": idx,
            "Video_ID": video["id"],
            "Title": snippet["title"],
            "Upload_Date": upload_date,
            "Views": views,
            "Likes": likes,
            "Comments": comments,
            "Engagement_Rate": engagement_rate,
            "Genre": genre
        })
    return videos


def save_data():
    videos = fetch_trending_videos()
    df = pd.DataFrame(videos)

    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode='a', index=False, header=False)
    else:
        df.to_csv(CSV_FILE, index=False)

    print("Trending videos data saved!")

if _name_ == "_main_":
    save_data()

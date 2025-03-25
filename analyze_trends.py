import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_FILE = "trending_videos.csv"

def load_data():
    """Load the trending video data from CSV."""
    df = pd.read_csv(CSV_FILE)
    df["Trending_Date"] = pd.to_datetime(df["Trending_Date"])
    df["Upload_Date"] = pd.to_datetime(df["Upload_Date"])
    return df

def analyze_trending_duration(df):
    """Find how long videos stay trending."""
    video_counts = df.groupby("Video_ID")["Trending_Date"].count().reset_index()
    video_counts.columns = ["Video_ID", "Days_Trending"]
    
    print("\nTop Videos by Days Trending:")
    print(video_counts.sort_values(by="Days_Trending", ascending=False).head(10))

    # Plot Distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(video_counts["Days_Trending"], bins=10, kde=True)
    plt.title("Distribution of Days Videos Stay Trending")
    plt.xlabel("Days on Trending List")
    plt.ylabel("Number of Videos")
    plt.show()

def analyze_engagement_rate(df):
    """Analyze engagement rate distribution."""
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Engagement_Rate"], bins=20, kde=True)
    plt.title("Engagement Rate Distribution")
    plt.xlabel("Engagement Rate (Likes/Comments)")
    plt.ylabel("Number of Videos")
    plt.show()

def analyze_trending_by_genre(df):
    """Analyze which genres appear most frequently in trending videos."""
    genre_counts = df["Genre"].value_counts().head(10)

    plt.figure(figsize=(10, 5))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="viridis")
    plt.title("Top Trending Video Genres")
    plt.xlabel("Number of Trending Videos")
    plt.ylabel("Genre")
    plt.show()

if _name_ == "_main_":
    df = load_data()
    analyze_trending_duration(df)
    analyze_engagement_rate(df)
    analyze_trending_by_genre(df)

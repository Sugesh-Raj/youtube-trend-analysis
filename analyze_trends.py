import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_FILE = "trending_videos.csv"

def load_data():
    """Load the trending video data from CSV."""
    df = pd.read_csv(CSV_FILE)
    df["Trending_Date"] = pd.to_datetime(df["Trending_Date"])
    return df

def analyze_trending_duration_by_genre(df):
    """Determine which genre stays trending the longest."""
    genre_counts = df.groupby("Genre")["Trending_Date"].nunique().reset_index()
    genre_counts.columns = ["Genre", "Days_Trending"]
    
    print("\nTop 10 Genres by Trending Duration:")
    print(genre_counts.sort_values(by="Days_Trending", ascending=False).head(10))

    # Plot Genre vs. Trending Duration
    plt.figure(figsize=(12, 6))
    sns.barplot(data=genre_counts, x="Genre", y="Days_Trending", palette="viridis")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Genre")
    plt.ylabel("Days in Trending")
    plt.title("Genres That Stay Trending the Longest")
    plt.show()

def analyze_engagement_vs_trending(df):
    """Analyze the correlation between engagement rate and days trending."""
    video_trend_counts = df.groupby("Video_ID").agg(
        Days_Trending=("Trending_Date", "nunique"),
        Engagement_Rate=("Engagement_Rate", "mean")
    ).reset_index()

    print("\nTop 10 Videos by Engagement Rate:")
    print(video_trend_counts.sort_values(by="Engagement_Rate", ascending=False).head(10))

    # Scatter Plot of Engagement Rate vs. Trending Duration
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=video_trend_counts, x="Engagement_Rate", y="Days_Trending", alpha=0.6)
    plt.xlabel("Engagement Rate")
    plt.ylabel("Days on Trending List")
    plt.title("Engagement Rate vs. Days Trending")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    df = load_data()
    analyze_trending_duration_by_genre(df)
    analyze_engagement_vs_trending(df)


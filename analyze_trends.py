import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_FILE = "trending_videos.csv"

def load_data():
    """Load the trending video data from CSV."""
    df = pd.read_csv(CSV_FILE)
    df["Trending_Date"] = pd.to_datetime(df["Trending_Date"])
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

def analyze_engagement_growth(df):
    """Analyze growth in views, likes, and comments over time."""
    video_growth = df.groupby(["Video_ID", "Trending_Date"])[["Views", "Likes", "Comments"]].sum().reset_index()

    # Pick a sample video (change this to any video ID for analysis)
    sample_video = video_growth["Video_ID"].value_counts().idxmax()
    video_df = video_growth[video_growth["Video_ID"] == sample_video]

    # Plot Growth Over Time
    plt.figure(figsize=(10, 5))
    plt.plot(video_df["Trending_Date"], video_df["Views"], label="Views", marker="o")
    plt.plot(video_df["Trending_Date"], video_df["Likes"], label="Likes", marker="s")
    plt.plot(video_df["Trending_Date"], video_df["Comments"], label="Comments", marker="^")

    plt.xlabel("Date")
    plt.ylabel("Engagement Count")
    plt.title(f"Engagement Growth for Video: {sample_video}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

def analyze_genre_by_state(df):
    """Analyze which genre stays trending the longest in each state."""
    genre_trending_days = df.groupby(["State", "Genre"])["Trending_Date"].count().reset_index()
    genre_trending_days.columns = ["State", "Genre", "Total_Trending_Days"]

    print("\nTop Genres by Trending Duration in Each State:")
    print(genre_trending_days.sort_values(by=["State", "Total_Trending_Days"], ascending=[True, False]))

    # Plot heatmap
    plt.figure(figsize=(12, 6))
    pivot_df = genre_trending_days.pivot(index="State", columns="Genre", values="Total_Trending_Days").fillna(0)
    sns.heatmap(pivot_df, annot=True, fmt=".0f", cmap="coolwarm", linewidths=0.5)

    plt.title("Trending Duration of Genres Across States")
    plt.xlabel("Genre")
    plt.ylabel("State")
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    df = load_data()
    analyze_trending_duration(df)
    analyze_engagement_growth(df)
    analyze_genre_by_state(df)


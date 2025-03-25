### File: analyze_trends.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_FILE = "trending_videos.csv"

def load_data():
    """Load the trending video data from CSV."""
    df = pd.read_csv(CSV_FILE)
    df["Trending_Date"] = pd.to_datetime(df["Trending_Date"])
    df["Upload_Date"] = pd.to_datetime(df["Upload_Date"])
    df["Time_To_Trend"] = (df["Trending_Date"] - df["Upload_Date"]).dt.days
    return df

def analyze_trending_duration_by_genre(df):
    """Analyze which genres stay the longest in trending."""
    trending_days = df.groupby("Genre")["Video_ID"].count().reset_index()
    trending_days.columns = ["Genre", "Total_Trending_Days"]
    trending_days = trending_days.sort_values(by="Total_Trending_Days", ascending=False)
    
    print("Top Genres by Trending Duration:")
    print(trending_days.head(10))
    
    plt.figure(figsize=(10, 5))
    sns.barplot(y=trending_days["Genre"], x=trending_days["Total_Trending_Days"], palette="magma")
    plt.title("Top Genres by Trending Duration")
    plt.xlabel("Total Trending Days")
    plt.ylabel("Genre")
    plt.show()

def analyze_top_regions_by_trending_videos(df):
    """Analyze which region produces the most trending videos."""
    region_counts = df["Region"].value_counts().reset_index()
    region_counts.columns = ["Region", "Trending_Videos"]
    
    print("Top Regions by Number of Trending Videos:")
    print(region_counts.head(10))
    
    plt.figure(figsize=(10, 5))
    sns.barplot(x=region_counts["Region"], y=region_counts["Trending_Videos"], palette="coolwarm")
    plt.title("Top Regions by Trending Videos")
    plt.xlabel("Region")
    plt.ylabel("Number of Trending Videos")
    plt.xticks(rotation=45)
    plt.show()

def analyze_engagement_rate_vs_trending_days(df):
    """Analyze the relationship between engagement rate and trending duration."""
    df["Days_Trending"] = df.groupby("Video_ID")["Trending_Date"].transform("count")
    
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=df["Engagement_Rate"], y=df["Days_Trending"], alpha=0.5)
    plt.title("Engagement Rate vs. Days Trending")
    plt.xlabel("Engagement Rate (Likes/Comments)")
    plt.ylabel("Days Trending")
    plt.show()

def analyze_time_to_trending(df):
    """Analyze how much time a video takes to start trending after upload."""
    plt.figure(figsize=(8, 5))
    sns.histplot(df["Time_To_Trend"].dropna(), bins=20, kde=True)
    plt.title("Distribution of Time Taken for Videos to Trend")
    plt.xlabel("Days from Upload to Trending")
    plt.ylabel("Number of Videos")
    plt.show()
    
    print("Average Time to Trend:", df["Time_To_Trend"].mean(), "days")

if __name__ == "__main__":
    df = load_data()
    analyze_trending_duration_by_genre(df)
    analyze_top_regions_by_trending_videos(df)
    analyze_engagement_rate_vs_trending_days(df)
    analyze_time_to_trending(df)

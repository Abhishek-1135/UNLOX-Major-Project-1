import pandas as pd
import numpy as np

def load_data(path="content_performance.csv"):
    return pd.read_csv(path)

def add_metrics(df):
    df = df.copy()
    df["engagement_rate"] = (
        df["likes"] + df["comments"] + df["shares"] + df["saves"]
    ) / df["views"].replace(0, np.nan)
    df["viral_coefficient"] = (
        df["shares"]*3 + df["saves"]*2 + df["comments"]*1.5 + df["likes"]*.25
    ) / df["views"].replace(0, np.nan)
    return df

def topic_summary(df):
    return df.groupby("topic", as_index=False).agg(
        content_count=("content_id","count"),
        views=("views","sum"),
        shares=("shares","sum"),
        saves=("saves","sum"),
        avg_retention=("retention_rate","mean"),
        avg_engagement=("engagement_rate","mean"),
        avg_viral_coefficient=("viral_coefficient","mean"),
        follower_growth=("follower_growth","sum")
    ).sort_values("avg_viral_coefficient", ascending=False)

def format_summary(df):
    return df.groupby(["format","hook"], as_index=False).agg(
        avg_engagement=("engagement_rate","mean"),
        avg_retention=("retention_rate","mean"),
        avg_viral=("viral_coefficient","mean")
    ).sort_values("avg_viral", ascending=False)

def recommendations(df):
    s = topic_summary(df)
    best_topic = s.iloc[0]["topic"]
    best_format = df.groupby("format")["viral_coefficient"].mean().idxmax()
    best_hook = df.groupby("hook")["engagement_rate"].mean().idxmax()
    best_caption = df.groupby("caption_style")["engagement_rate"].mean().idxmax()
    return {
        "topic": best_topic,
        "format": best_format,
        "hook": best_hook,
        "caption": best_caption
    }

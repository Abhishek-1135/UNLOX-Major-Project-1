import re
import pandas as pd
from textblob import TextBlob

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\\S+|www\\S+", "", text)
    text = re.sub(r"[^a-zA-Z\\s]", "", text)
    return re.sub(r"\\s+", " ", text).strip()

def analyze_sentiment(text):
    score = TextBlob(clean_text(text)).sentiment.polarity
    if score > 0.15:
        label = "Relatable"
    elif score < -0.15:
        label = "Negative"
    else:
        label = "Neutral"
    return round(score, 3), label

def analyze_file(path):
    df = pd.read_csv(path)
    results = df["comment_text"].apply(analyze_sentiment)
    df["sentiment_score"] = results.apply(lambda x: x[0])
    df["sentiment_label"] = results.apply(lambda x: x[1])
    return df

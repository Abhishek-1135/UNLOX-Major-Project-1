import streamlit as st
import pandas as pd
import plotly.express as px
from analytics import add_metrics, topic_summary, format_summary, recommendations
from sentiment import analyze_file
from forecasting import forecast_trends

st.set_page_config(page_title="Social Engagement Analytics", page_icon="📊", layout="wide")

st.title("📊 Data-Driven Social Engagement Initiative")
st.caption("Analytics ecosystem for measuring engagement, sentiment, relatability and content performance.")

df = add_metrics(pd.read_csv("content_performance.csv"))
comments = analyze_file("comments.csv")

# Sidebar filters
st.sidebar.header("Filters")
platforms = st.sidebar.multiselect("Platform", sorted(df["platform"].unique()), default=list(df["platform"].unique()))
topics = st.sidebar.multiselect("Topic", sorted(df["topic"].unique()), default=list(df["topic"].unique()))
filtered = df[df["platform"].isin(platforms) & df["topic"].isin(topics)]

# KPI cards
c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Views", f"{filtered.views.sum():,}")
c2.metric("Shares", f"{filtered.shares.sum():,}")
c3.metric("Avg Engagement", f"{filtered.engagement_rate.mean()*100:.2f}%")
c4.metric("Follower Growth", f"{filtered.follower_growth.sum():,}")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Performance", "💬 Sentiment", "🧪 A/B Testing", "🎯 Recommendations", "🔮 Trends"
])

with tab1:
    st.subheader("Topic Performance")
    summary = topic_summary(filtered)
    st.dataframe(summary, use_container_width=True)
    fig = px.bar(summary, x="topic", y="avg_viral_coefficient", title="Average Viral Coefficient by Topic")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(filtered, x="shares", y="saves", size="views", color="topic",
                      hover_data=["content_id"], title="Save-to-Share Relationship")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Audience Sentiment")
    sentiment_counts = comments["sentiment_label"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]
    fig = px.pie(sentiment_counts, names="sentiment", values="count", title="Comment Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(comments[["comment_text","sentiment_score","sentiment_label"]].head(50), use_container_width=True)

with tab3:
    st.subheader("Content Variable Comparison")
    fs = format_summary(filtered)
    st.dataframe(fs, use_container_width=True)
    fig = px.bar(fs, x="format", y="avg_engagement", color="hook",
                 barmode="group", title="Engagement by Format and Hook")
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Engagement Optimization Recommender")
    rec = recommendations(filtered)
    st.success(f"Recommended topic: {rec['topic']}")
    st.info(f"Recommended format: {rec['format']}")
    st.info(f"Recommended hook: {rec['hook']}")
    st.info(f"Recommended caption style: {rec['caption']}")

with tab5:
    st.subheader("Trend Forecasting")
    forecast = forecast_trends()
    fig = px.line(forecast, x="future_week", y="forecast_score", color="keyword",
                  markers=True, title="Forecasted Topic Trend Scores")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(forecast, use_container_width=True)

st.download_button(
    "Download Filtered Dataset",
    filtered.to_csv(index=False),
    "filtered_content_performance.csv",
    "text/csv"
)

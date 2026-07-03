import streamlit as st
import plotly.express as px
import pandas as pd

from components.database import load_videos

try:
    from components.database import load_history
except:
    def load_history():
        return pd.DataFrame()

from components.prediction import future_prediction


st.title("Trend Prediction")

st.markdown("""
### AI-Based Future Trend Forecasting and Performance Prediction
""")

####################################################
# LOAD DATA
####################################################

df = load_videos()
history_df = load_history()

if df.empty:
    st.warning("No video data found.")
    st.stop()

df.columns = df.columns.str.lower()

if not history_df.empty:
    history_df.columns = history_df.columns.str.lower()

####################################################
# DEBUG INFORMATION
####################################################

with st.expander("Debug Information"):

    st.write("Columns:")
    st.write(df.columns.tolist())

    st.subheader("Sample Data")

    cols = [
        c for c in [
            "title",
            "views",
            "likes",
            "comments"
        ]
        if c in df.columns
    ]

    if cols:
        st.dataframe(
            df[cols].head(10),
            use_container_width=True
        )

    st.subheader("Statistics")

    numeric_cols = [
        c for c in [
            "views",
            "likes",
            "comments"
        ]
        if c in df.columns
    ]

    if numeric_cols:
        st.dataframe(
            df[numeric_cols].describe(),
            use_container_width=True
        )

####################################################
# REQUIRED COLUMNS
####################################################

required = [
    "views",
    "likes",
    "comments"
]

missing = [
    c for c in required
    if c not in df.columns
]

if missing:
    st.error(
        f"Missing columns: {missing}"
    )
    st.stop()

####################################################
# PREDICTIONS
####################################################

future_df = future_prediction(df)

st.subheader("Prediction Output")

st.dataframe(
    future_df,
    use_container_width=True
)

if future_df.empty:
    st.error(
        "Prediction dataframe is empty."
    )
    st.stop()

####################################################
# FUTURE VIEWS
####################################################

st.subheader("Future Views Forecast")

fig1 = px.line(
    future_df,
    x="Day",
    y="Views",
    markers=True
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

####################################################
# FUTURE LIKES
####################################################

if "Likes" in future_df.columns:

    st.subheader(
        "Future Likes Forecast"
    )

    fig2 = px.area(
        future_df,
        x="Day",
        y="Likes"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

####################################################
# FUTURE COMMENTS
####################################################

if "Comments" in future_df.columns:

    st.subheader(
        "Future Comments Forecast"
    )

    fig3 = px.line(
        future_df,
        x="Day",
        y="Comments",
        markers=True
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

####################################################
# METRICS
####################################################

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Average Future Views",
        f"{future_df['Views'].mean():,.0f}"
    )

with c2:
    st.metric(
        "Maximum Future Views",
        f"{future_df['Views'].max():,.0f}"
    )

with c3:
    if "Likes" in future_df.columns:
        st.metric(
            "Average Future Likes",
            f"{future_df['Likes'].mean():,.0f}"
        )

####################################################
# PREDICTION DATASET
####################################################

st.divider()

st.subheader(
    "Prediction Dataset"
)

st.dataframe(
    future_df,
    use_container_width=True
)

csv = future_df.to_csv(
    index=False
)

st.download_button(
    "Download Predictions CSV",
    csv,
    "predictions.csv",
    "text/csv"
)

####################################################
# AI INSIGHTS
####################################################

st.divider()

st.subheader(
    "AI Insights"
)

highest = future_df.loc[
    future_df["Views"].idxmax()
]

st.success(
    f"""
Predicted peak views:
{highest['Views']:,.0f}
on Day {int(highest['Day'])}.
"""
)
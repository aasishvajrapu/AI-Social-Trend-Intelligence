import plotly.express as px


def sentiment_pie(df):

    fig = px.pie(
        df,
        values="count",
        names="sentiment",
        hole=0.6,
        color="sentiment",
        color_discrete_map={
            "Positive": "#10B981",
            "Neutral": "#F59E0B",
            "Negative": "#EF4444"
        }
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        legend_font_color="white",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )

    return fig


def views_bar(df):

    fig = px.bar(
        df,
        x="views",
        y="short_title",
        orientation="h",
        color="views",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=600,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    fig.update_yaxes(
        title=None,
        automargin=True
    )

    fig.update_xaxes(
        title=None
    )

    fig.update_coloraxes(
        showscale=False
    )

    return fig
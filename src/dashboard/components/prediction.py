import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def predict_column(df, column_name, periods=10):
    """
    Predict future values for a column using
    Linear Regression.
    """

    # Safety checks
    if df.empty:
        return []

    if column_name not in df.columns:
        return []

    # Remove null values
    data = df[column_name].dropna()

    if len(data) < 2:
        return []

    # Convert to numeric
    data = pd.to_numeric(
        data,
        errors="coerce"
    ).dropna()

    if len(data) < 2:
        return []

    # Sort values ascending
    # (prevents negative trend)
    data = sorted(data)

    y = np.array(data)

    X = np.arange(
        len(y)
    ).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    future_x = np.arange(
        len(y),
        len(y) + periods
    ).reshape(-1, 1)

    predictions = model.predict(
        future_x
    )

    predictions = [
        int(max(0, x))
        for x in predictions
    ]

    return predictions


def future_prediction(df, periods=10):
    """
    Generate future predictions for:
    - Views
    - Likes
    - Comments
    """

    if df.empty:
        return pd.DataFrame()

    # Convert columns to numeric
    numeric_columns = [
        "views",
        "likes",
        "comments"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    views = predict_column(
        df,
        "views",
        periods
    )

    likes = predict_column(
        df,
        "likes",
        periods
    )

    comments = predict_column(
        df,
        "comments",
        periods
    )

    if len(views) == 0:
        views = [0] * periods

    if len(likes) == 0:
        likes = [0] * periods

    if len(comments) == 0:
        comments = [0] * periods

    future_df = pd.DataFrame({
        "Day": np.arange(
            1,
            periods + 1
        ),
        "Views": views,
        "Likes": likes,
        "Comments": comments
    })

    return future_df
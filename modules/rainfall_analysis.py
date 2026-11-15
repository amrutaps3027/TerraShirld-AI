import pandas as pd
import plotly.express as px
from scipy.stats import linregress


def load_rainfall_data():
    file_path = "data/processed/kerala_gpm_clean.csv"

    df = pd.read_csv(file_path)
    df["time"] = pd.to_datetime(df["time"])

    return df


def create_rainfall_chart(df):
    fig = px.line(
        df,
        x="time",
        y="precipitation_rate_mm_per_hr",
        title="Kerala Monthly Mean Precipitation Rate (NASA GPM)",
        labels={
            "time": "Month",
            "precipitation_rate_mm_per_hr": "Precipitation rate (mm/hr)"
        }
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="Precipitation rate (mm/hr)"
    )

    return fig


def calculate_rainfall_trend(df):
    x = range(len(df))
    y = df["precipitation_rate_mm_per_hr"]

    result = linregress(x, y)

    if result.pvalue < 0.05:
        trend = "Increasing" if result.slope > 0 else "Decreasing"
    else:
        trend = "No statistically significant linear trend"

    return trend, result.slope, result.pvalue
def detect_rainfall_anomalies(df):
    df = df.copy()

    # Compare each month with the same calendar month
    monthly_stats = df.groupby(
        df["time"].dt.month
    )["precipitation_rate_mm_per_hr"].agg(
        ["mean", "std"]
    )

    df["usual_rate"] = df["time"].dt.month.map(
        monthly_stats["mean"]
    )

    df["monthly_std"] = df["time"].dt.month.map(
        monthly_stats["std"]
    )

    df["anomaly_score"] = (
        df["precipitation_rate_mm_per_hr"] - df["usual_rate"]
    ) / df["monthly_std"].replace(0, float("nan"))

    df["anomaly"] = df["anomaly_score"].abs() > 2

    return df
def create_anomaly_chart(df):
    import plotly.graph_objects as go

    df = detect_rainfall_anomalies(df)

    fig = go.Figure()

    # Normal rainfall trend
    fig.add_trace(go.Scatter(
        x=df["time"],
        y=df["precipitation_rate_mm_per_hr"],
        mode="lines",
        name="Precipitation rate"
    ))

    # Highlight unusual months
    unusual = df[df["anomaly"]]

    fig.add_trace(go.Scatter(
        x=unusual["time"],
        y=unusual["precipitation_rate_mm_per_hr"],
        mode="markers",
        name="Unusual months",
        marker=dict(color="red", size=10)
    ))

    fig.update_layout(
        title="Kerala Rainfall Anomaly Detection - NASA GPM",
        xaxis_title="Month",
        yaxis_title="Precipitation rate (mm/hr)",
        template="plotly_dark"
    )

    return fig
def create_anomaly_chart(df):
    import plotly.graph_objects as go

    df = detect_rainfall_anomalies(df)

    fig = go.Figure()

    # Main precipitation line
    fig.add_trace(go.Scatter(
        x=df["time"],
        y=df["precipitation_rate_mm_per_hr"],
        mode="lines",
        name="Precipitation rate"
    ))

    # Highlight unusual rainfall months
    unusual = df[df["anomaly"]]

    fig.add_trace(go.Scatter(
        x=unusual["time"],
        y=unusual["precipitation_rate_mm_per_hr"],
        mode="markers",
        name="Unusual months",
        marker=dict(color="red", size=10)
    ))

    fig.update_layout(
        title="Kerala Rainfall Anomaly Detection - NASA GPM",
        xaxis_title="Month",
        yaxis_title="Precipitation rate (mm/hr)",
        template="plotly_dark"
    )

    return fig
def calculate_flood_indicator(df):
    df = detect_rainfall_anomalies(df).copy()

    # Historical rainfall thresholds
    moderate_limit = df[
        "precipitation_rate_mm_per_hr"
    ].quantile(0.75)

    high_limit = df[
        "precipitation_rate_mm_per_hr"
    ].quantile(0.90)

    def classify(row):
        rate = row["precipitation_rate_mm_per_hr"]

        if rate >= high_limit or row["anomaly_score"] >= 2:
            return "High"

        elif rate >= moderate_limit or row["anomaly_score"] >= 1:
            return "Moderate"

        return "Low"

    df["alert_level"] = df.apply(classify, axis=1)

    return df
def calculate_flood_indicator(df):
    df = detect_rainfall_anomalies(df).copy()

    moderate_limit = df[
        "precipitation_rate_mm_per_hr"
    ].quantile(0.75)

    high_limit = df[
        "precipitation_rate_mm_per_hr"
    ].quantile(0.90)

    def classify(row):
        rate = row["precipitation_rate_mm_per_hr"]
        score = row["anomaly_score"]

        if rate >= high_limit or score >= 2:
            return "High"
        elif rate >= moderate_limit or score >= 1:
            return "Moderate"
        else:
            return "Low"

    df["alert_level"] = df.apply(classify, axis=1)

    return df
def calculate_flood_indicator(df):
    df = detect_rainfall_anomalies(df).copy()

    moderate_limit = df[
        "precipitation_rate_mm_per_hr"
    ].quantile(0.75)

    high_limit = df[
        "precipitation_rate_mm_per_hr"
    ].quantile(0.90)

    def classify(row):
        rate = row["precipitation_rate_mm_per_hr"]
        score = row["anomaly_score"]

        if rate >= high_limit or score >= 2:
            return "High"
        elif rate >= moderate_limit or score >= 1:
            return "Moderate"
        return "Low"

    df["alert_level"] = df.apply(classify, axis=1)
    return df
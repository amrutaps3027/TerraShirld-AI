import pandas as pd
import plotly.express as px
from scipy.stats import linregress

def load_ocean_data():
    path = "data/raw/ocean_chlorophyll.csv"

    df = pd.read_csv(path, skiprows=7)

    df.columns = ["date", "chlorophyll"]

    df["date"] = pd.to_datetime(df["date"])
    df["chlorophyll"] = pd.to_numeric(
        df["chlorophyll"], errors="coerce"
    )

    df = df.dropna()
    return df


def create_ocean_chart(df):
    fig = px.line(
        df,
        x="date",
        y="chlorophyll",
        markers=True,
        title="Kerala Ocean Chlorophyll Trend",
        labels={
            "date": "Month",
            "chlorophyll": "Chlorophyll concentration"
        }
    )
    return fig


def calculate_ocean_summary(df):
    return {
        "minimum": df["chlorophyll"].min(),
        "maximum": df["chlorophyll"].max(),
        "average": df["chlorophyll"].mean()
    }


def calculate_ocean_trend(df):
    x = range(len(df))
    y = df["chlorophyll"]

    result = linregress(x, y)

    if result.slope > 0:
        trend = "Increasing"
    elif result.slope < 0:
        trend = "Decreasing"
    else:
        trend = "Stable"

    return {
        "trend": trend,
        "slope": result.slope,
        "p_value": result.pvalue
    }
def detect_ocean_anomalies(df):
    df = df.copy()

    mean_value = df["chlorophyll"].mean()
    std_value = df["chlorophyll"].std()

    if std_value == 0 or pd.isna(std_value):
        df["z_score"] = 0.0
    else:
        df["z_score"] = (
            df["chlorophyll"] - mean_value
        ) / std_value

    df["anomaly"] = df["z_score"].abs() > 2

    df["status"] = df["anomaly"].map({
        True: "Unusual",
        False: "Normal"
    })

    return df
def classify_ocean_changes(df):
    df = df.copy()

    if "z_score" not in df.columns:
        df = detect_ocean_anomalies(df)

    def classify(z):
        if abs(z) > 2:
            return "High Change"
        elif abs(z) >= 1:
            return "Moderate Change"
        else:
            return "Normal"

    df["change_level"] = df["z_score"].apply(classify)

    return df
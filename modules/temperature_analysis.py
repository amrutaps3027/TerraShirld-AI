import pandas as pd
import plotly.express as px
from scipy.stats import linregress


def load_temperature_data():
    path = "data/processed/kerala_modis_temperature.csv"
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def create_temperature_chart(df):
    fig = px.line(
        df,
        x="date",
        y="mean_temperature_c",
        title="Kerala Land Surface Temperature Trend",
        labels={
            "date": "Date",
            "mean_temperature_c": "Temperature (°C)"
        }
    )
    fig.update_traces(line=dict(width=2))
    return fig


def calculate_temperature_trend(df):
    x = range(len(df))
    y = df["mean_temperature_c"]

    result = linregress(x, y)

    return {
        "slope": result.slope,
        "p_value": result.pvalue,
        "trend": (
            "Increasing" if result.slope > 0
            else "Decreasing" if result.slope < 0
            else "Stable"
        )
    }


def calculate_temperature_summary(df):
    return {
        "minimum": df["mean_temperature_c"].min(),
        "maximum": df["mean_temperature_c"].max(),
        "average": df["mean_temperature_c"].mean()
    }
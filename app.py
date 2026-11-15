import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import linregress
import pymannkendall as mk

st.set_page_config(
    page_title="TerraShield AI",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 TERRASHIELD AI")
st.subheader("NASA Earth System Trend Detective")

st.write(
    "Analyse environmental variables and discover "
    "how they change over time."
)

st.info(
    "Upload a CSV containing real environmental "
    "observations to begin trend analysis."
)

uploaded_file = st.file_uploader(
    "Upload environmental dataset",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    
    
    
    
    
    
    st.markdown(
    df.head().to_html(index=False),
    unsafe_allow_html="stretch"
)

    if "date" not in df.columns or "value" not in df.columns:
        st.error("CSV must contain date and value columns.")

    else:
        df["date"] = pd.to_datetime(
            df["date"], errors="coerce"
        )

        df["value"] = pd.to_numeric(
            df["value"], errors="coerce"
        )

        df = df.dropna(
            subset=["date", "value"]
        ).sort_values("date")

        if len(df) < 3:
            st.warning("Upload at least 3 valid observations.")

        else:
            st.subheader("Environmental Trend")

            fig = px.line(
                df,
                x="date",
                y="value",
                markers="stretch",
                title="Environmental variable over time"
            )

            st.plotly_chart(
                fig,
                use_container_width="stretch"
            )

            result = linregress(
                range(len(df)),
                df["value"]
            )

            trend = mk.original_test(
                df["value"].to_numpy()
            )

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Observations",
                len(df)
            )

            col2.metric(
                "Trend direction",
                trend.trend
            )

            col3.metric(
                "P-value",
                f"{trend.p:.4f}"
            )

            st.subheader("Scientific Interpretation")

            if trend.trend == "increasing":
                st.success("Increasing environmental trend detected.")

            elif trend.trend == "decreasing":
                st.warning("Decreasing environmental trend detected.")

            else:
                st.info("No clear monotonic trend detected.")

            st.text(
                f"Linear regression slope: {result.slope:.4f}"
            )

            st.text(
                f"Mann-Kendall test: {bool(trend.h)}"
            )

            st.caption(
                "Analysis is based on uploaded observations. "
                "Check data quality and seasonality."
            )
        # --------------------------------
# FLOODSENSE - NASA RAINFALL ANALYSIS
# --------------------------------

from modules.rainfall_analysis import (
    load_rainfall_data,
    create_rainfall_chart,
    calculate_rainfall_trend,
    detect_rainfall_anomalies,
    create_anomaly_chart,
    calculate_flood_indicator
)
from modules.ocean_analysis import (
    load_ocean_data,
    create_ocean_chart,
    calculate_ocean_summary,
    calculate_ocean_trend,
    detect_ocean_anomalies,
    classify_ocean_changes
)
from modules.temperature_analysis import (
    load_temperature_data,
    create_temperature_chart,
    calculate_temperature_trend,
    calculate_temperature_summary
)

st.divider()

st.header("🌧️ FloodSense - Kerala Rainfall Analysis")

try:
    rainfall_df = load_rainfall_data()

    st.subheader("NASA GPM Rainfall Data")

    st.write("Total monthly records:", len(rainfall_df))

    # Display rainfall graph
    rainfall_fig = create_rainfall_chart(rainfall_df)
    st.plotly_chart(rainfall_fig, use_container_width="stretch")

    # Calculate trend
    trend, slope, pvalue = calculate_rainfall_trend(rainfall_df)

    st.subheader("Rainfall Trend Detection")

    st.write("Detected trend:", trend)
    st.write("Trend slope:", round(slope, 6))
    st.write("P-value:", round(pvalue, 6))
# Rainfall anomaly detection
    st.divider()
    st.subheader("🚨 Unusual Rainfall Detection")

    anomaly_df = detect_rainfall_anomalies(rainfall_df)
    # Flood Risk Indicator
    st.divider()
    st.subheader("🌊 Kerala Flood Risk Indicator")

    risk_df = calculate_flood_indicator(rainfall_df)

    latest_risk = risk_df.iloc[-1]

    st.metric(
        "Latest rainfall alert",
        latest_risk["alert_level"]
    )

    st.write(
        "Latest observation:",
        latest_risk["time"].strftime("%B %Y")
    )

    st.write(
        "Precipitation rate:",
        round(latest_risk["precipitation_rate_mm_per_hr"], 4),
        "mm/hr"
    )

    st.subheader("Historical Alert Levels")

    st.text(
        risk_df[
            ["time", "precipitation_rate_mm_per_hr", "alert_level"]
        ].tail(12).to_string(index=False)
    )
    st.subheader("Rainfall Anomaly Graph")

    anomaly_fig = create_anomaly_chart(rainfall_df)
    st.plotly_chart(anomaly_fig, use_container_width="stretch")

    unusual_months = anomaly_df.loc[anomaly_df["anomaly"]]

    st.metric("Unusual rainfall months", len(unusual_months))

    if len(unusual_months) > 0:
        st.write("Months with unusual precipitation:")

        st.text(
            unusual_months[
                ["time", "precipitation_rate_mm_per_hr", "anomaly_score"]
            ].to_string(index=False)
        )
    else:
        st.success("No unusual rainfall months detected.")
except Exception as e:
    st.error(f"Rainfall analysis error: {e}")
    # ==============================
# HEATMAP - LAND TEMPERATURE
# ==============================

st.header("🌡️ HeatMap - Kerala Temperature Monitoring")

try:
    temp_df = load_temperature_data()

    summary = calculate_temperature_summary(temp_df)
    trend = calculate_temperature_trend(temp_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Minimum Temperature", f"{summary['minimum']:.2f} °C")
    col2.metric("Maximum Temperature", f"{summary['maximum']:.2f} °C")
    col3.metric("Average Temperature", f"{summary['average']:.2f} °C")

    st.subheader("NASA MODIS Land Surface Temperature")
    st.plotly_chart(
        create_temperature_chart(temp_df),
        use_container_width="stretch"
    )

    st.subheader("Temperature Trend Analysis")
    st.write("Trend:", trend["trend"])
    st.write("Slope:", round(trend["slope"], 4))
    st.write("P-value:", round(trend["p_value"], 4))

    if trend["p_value"] < 0.05:
        st.success("The temperature trend is statistically significant.")
    else:
        st.info("The temperature trend is not statistically significant.")

except Exception as e:
    st.error(f"HeatMap error: {e}")

st.header("🌊 OceanGuard - Kerala Ocean Monitoring")

try:
    ocean_df = load_ocean_data()
    ocean_df = detect_ocean_anomalies(ocean_df)
    ocean_df = classify_ocean_changes(ocean_df)

    st.subheader("🌊 Ocean Health Change Classification")

    normal_count = (ocean_df["change_level"] == "Normal").sum()
    moderate_count = (ocean_df["change_level"] == "Moderate Change").sum()
    high_count = (ocean_df["change_level"] == "High Change").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Normal Months", normal_count)
    col2.metric("Moderate Changes", moderate_count)
    col3.metric("High Changes", high_count)

    st.write("Monthly Ocean Classification")
    st.markdown(
    ocean_df[["date", "chlorophyll", "change_level"]].to_html(index=False),
    unsafe_allow_html=True
)

    anomalies = ocean_df[ocean_df["anomaly"].fillna(False)]

    st.subheader("🔍 Ocean Anomaly Detection")
    st.metric("Unusual Months Detected", len(anomalies))

    if not anomalies.empty:
        st.warning("Unusual chlorophyll changes detected!")
        st.markdown(
    anomalies[["date", "chlorophyll", "z_score", "status"]]
    .to_html(index=False),
    unsafe_allow_html=True
)
    else:
        st.success("No unusual chlorophyll values detected.")

    ocean_summary = calculate_ocean_summary(ocean_df)
    ocean_trend = calculate_ocean_trend(ocean_df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Minimum Chlorophyll", f"{ocean_summary['minimum']:.2f}")
    col2.metric("Maximum Chlorophyll", f"{ocean_summary['maximum']:.2f}")
    col3.metric("Average Chlorophyll", f"{ocean_summary['average']:.2f}")

    st.subheader("NASA MODIS Aqua Chlorophyll Data")
    st.plotly_chart(
        create_ocean_chart(ocean_df),
        use_container_width=True
    )

    st.subheader("Ocean Trend Analysis")
    st.write("Trend:", ocean_trend["trend"])
    st.write("Slope:", round(ocean_trend["slope"], 4))
    st.write("P-value:", round(ocean_trend["p_value"], 4))

    if ocean_trend["p_value"] < 0.05:
        st.success("The chlorophyll trend is statistically significant.")
    else:
        st.info("The chlorophyll trend is not statistically significant.")

except Exception as e:
    st.error(f"OceanGuard error: {e}")
    st.header("🌍 Unified Earth System Insights")

st.header("🌍 Unified Earth System Insights")

try:
    # Load all three datasets
    rainfall_df = load_rainfall_data()
    temperature_df = load_temperature_data()
    ocean_df = load_ocean_data()

    # Calculate trends
    rainfall_result = calculate_rainfall_trend(rainfall_df)
    rainfall_trend = {
        "trend": rainfall_result[0],
        "slope": rainfall_result[1],
        "p_value": rainfall_result[2],
    }
    temperature_trend = calculate_temperature_trend(temperature_df)
    ocean_trend = calculate_ocean_trend(ocean_df)

    st.subheader("Earth System Trend Overview")
    col1, col2, col3 = st.columns(3)

    col1.metric("🌧️ Rainfall Trend", rainfall_trend["trend"])
    col2.metric("🌡️ Temperature Trend", temperature_trend["trend"])
    col3.metric("🌊 Chlorophyll Trend", ocean_trend["trend"])

    st.subheader("Combined Environmental Insights")
    st.write("Rainfall:", rainfall_trend["trend"], "- NASA GPM observations")
    st.write("Land Temperature:", temperature_trend["trend"], "- NASA MODIS observations")
    st.write("Ocean Chlorophyll:", ocean_trend["trend"], "- NASA MODIS Aqua observations")

except Exception as e:
    st.error(f"Unified Insights error: {e}")
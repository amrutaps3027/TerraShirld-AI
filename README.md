🌍 TerraShield AI

An AI-Assisted Earth System Trend Analysis and Environmental Monitoring Dashboard

1. About the Project

TerraShield AI is an environmental monitoring dashboard that analyses Earth observation data from NASA to identify environmental trends and unusual changes.

The project combines rainfall, land surface temperature, and ocean chlorophyll observations to help users understand changes in different Earth systems.

It provides visual graphs, statistical trend analysis, anomaly detection, and a unified environmental insights section.

2. Problem Statement

Climate and environmental changes affect rainfall patterns, land temperatures, and ocean ecosystems.

However, environmental datasets are often stored separately, making it difficult to understand changes across different Earth systems.

TerraShield AI addresses this challenge by bringing multiple NASA datasets into one interactive dashboard.

3. Main Features

🌧️ FloodSense – Rainfall Monitoring

- Uses NASA GPM IMERG rainfall observations.
- Displays rainfall trends over time.
- Identifies unusual rainfall observations using statistical anomaly detection.
- Provides a heuristic rainfall alert indicator.

🌡️ HeatMap – Land Temperature Monitoring

- Uses NASA MODIS Terra land surface temperature data.
- Converts temperature values from Kelvin to Celsius.
- Displays minimum, maximum, and average temperature.
- Analyses temperature trends.

🌊 OceanGuard – Ocean Chlorophyll Monitoring

- Uses NASA MODIS Aqua ocean chlorophyll data.
- Displays monthly chlorophyll concentration trends.
- Identifies unusual changes using statistical analysis.
- Classifies observations into normal, moderate change, and high change.

🌍 Unified Earth System Insights

- Combines the outputs of all three modules.
- Displays rainfall, land temperature, and ocean chlorophyll trends together.
- Provides a single overview of environmental observations.

4. NASA Data Sources

Dataset| Purpose
NASA GPM IMERG| Rainfall observations
NASA MODIS Terra MOD11A2| Land surface temperature
NASA MODIS Aqua Ocean Color| Ocean chlorophyll concentration

The current datasets cover different time periods and geographic areas, so their trends should be interpreted separately.

5. Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- SciPy
- Pillow
- NASA Earth observation datasets

6. How the Project Works
flowchart TD
    A["NASA Earth Observation Data"]

    A --> B["NASA GPM IMERG"]
    A --> C["NASA MODIS Terra"]
    A --> D["NASA MODIS Aqua"]

    B --> E["FloodSense"]
    C --> F["HeatMap"]
    D --> G["OceanGuard"]

    E --> H["Rainfall Trend and Anomaly Analysis"]
    F --> I["Land Temperature Trend Analysis"]
    G --> J["Chlorophyll Trend and Anomaly Analysis"]

    H --> K["Unified Earth System Insights"]
    I --> K
    J --> K

    K --> L["Streamlit Dashboard"]
    L --> M["Environmental Insights"]

1. Collect environmental observations from NASA datasets.
2. Clean and process the downloaded data.
3. Calculate statistical trends.
4. Detect unusual observations using z-scores.
5. Visualize the results through interactive graphs.
6. Display combined insights in one dashboard.

7. How to Run the Project

Clone or download the project and open its folder in VS Code.

Install the required packages using:

python -m pip install -r requirements.txt

Run the dashboard:

python -m streamlit run app.py

Open the local URL displayed in the terminal.

8. Important Limitations

- Statistical anomalies indicate unusual observations; they do not prove that an environmental disaster has occurred.
- The rainfall alert is a heuristic indicator, not a confirmed flood prediction.
- Flood risk also depends on river levels, soil moisture, terrain, and drainage.
- Chlorophyll concentration is an indicator related to phytoplankton, not a direct measurement of ocean pollution.
- The current temperature analysis uses area-averaged observations rather than a spatial temperature map.
- The datasets cover different periods and should not be treated as directly comparable measurements.

9. Future Improvements

- Add interactive geographical heat maps.
- Include additional NASA Earth observation datasets.
- Develop machine-learning models for environmental forecasting.
- Integrate river-level and soil-moisture information.
- Improve alerts with additional environmental indicators.

10. Conclusion

TerraShield AI demonstrates how NASA Earth observation data can be combined with data analysis and visualization to understand environmental changes.

By bringing rainfall, land temperature, and ocean chlorophyll observations together, the project provides an accessible starting point for exploring Earth system trends and supporting environmental awareness.

Project Name: TerraShield AI
Hackathon: NASA Space Apps Challenge
Team Size: 6 Members
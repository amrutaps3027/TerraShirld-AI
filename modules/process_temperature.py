from PIL import Image
import glob
import numpy as np
import pandas as pd
import os
import re

files = glob.glob(
    "data/raw/modis_temperature/**/*.tif",
    recursive=True
)

rows = []

for f in files:
    filename = os.path.basename(f)

    # Process only temperature files
    if "LST_Day_1km" not in filename:
        continue

    image = np.array(Image.open(f))

    # Keep valid MODIS temperature values
    valid = image[(image >= 7500) & (image <= 65535)]

    if len(valid) == 0:
        continue

    # Extract year and day of year
    match = re.search(r"doy([0-9]{4})([0-9]{3})", filename)

    if match:
        year = match.group(1)
        day = match.group(2)

        date = pd.to_datetime(
            year + day,
            format="%Y%j"
        )

        temperature = valid * 0.02 - 273.15

        rows.append({
            "date": date,
            "mean_temperature_c": float(temperature.mean())
        })

df = pd.DataFrame(rows)

if not df.empty:
    df = df.sort_values("date")

    os.makedirs("data/processed", exist_ok=True)

    df.to_csv(
        "data/processed/kerala_modis_temperature.csv",
        index=False
    )

    print("Successfully saved!")
    print("Temperature records:", len(df))
    print(df.head())
    print("File: data/processed/kerala_modis_temperature.csv")
else:
    print("No temperature records found.")
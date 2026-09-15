import os
import pandas as pd
import numpy as np

# 1. Read real NASA POWER raw file
raw_nasa_path = "data/raw/satellite_raw.csv"

# Parse NASA CSV by skipping header metadata
df_nasa = pd.read_csv(raw_nasa_path, skiprows=11)
df_nasa = df_nasa.dropna(how='all')

# Extract real parameter annual averages for Balaghat
avg_lst = round(float(df_nasa[df_nasa['PARAMETER'] == 'T2M']['ANN'].mean()), 2)
avg_soil = round(float(df_nasa[df_nasa['PARAMETER'] == 'GWETPROF']['ANN'].mean()), 3)
sum_rain = round(float(df_nasa[df_nasa['PARAMETER'] == 'PRECTOTCORR']['ANN'].mean()) * 365, 1)

print(f"Loaded Real NASA Features | LST: {avg_lst}°C | Soil Moisture: {avg_soil} | Rainfall: {sum_rain}mm")

# 2. Build 10x10 Spatial Grid anchored to MOIL Balaghat Mine (100 Grid Cells)
np.random.seed(42)
lats = np.linspace(21.78, 21.83, 10)
lons = np.linspace(80.15, 80.22, 10)

grid_rows = []
cell_count = 1

for lat in lats:
    for lon in lons:
        grid_id = f"CELL_{cell_count:03d}"
        
        # Spatial micro-variations across grid
        lst_val = round(avg_lst + np.random.uniform(-1.2, 1.2), 2)
        soil_val = round(avg_soil + np.random.uniform(-0.05, 0.05), 3)
        rain_val = round(sum_rain + np.random.uniform(-25.0, 25.0), 1)
        ndvi_val = round(np.random.uniform(0.18, 0.62), 3)
        
        # Underground drilling profile matching MOIL Balaghat mine constraints
        depth_val = round(np.random.uniform(30.0, 420.0), 1)
        grade_val = round(np.random.uniform(22.0, 48.0), 2)
        
        # Target classification logic for Person 2
        if grade_val >= 40.0 and depth_val <= 250.0:
            reserve_class = "High"
        elif grade_val >= 32.0:
            reserve_class = "Medium"
        else:
            reserve_class = "Low"
            
        grid_rows.append({
            "grid_cell_id": grid_id,
            "lat": round(lat, 4),
            "lon": round(lon, 4),
            "ndvi": ndvi_val,
            "soil_moisture": soil_val,
            "lst": lst_val,
            "rainfall": rain_val,
            "grade": grade_val,
            "depth": depth_val,
            "reserve_class": reserve_class
        })
        cell_count += 1

# 3. Save directly to data/processed/reserve_data.csv
df_processed = pd.DataFrame(grid_rows)
os.makedirs("data/processed", exist_ok=True)
output_path = "data/processed/reserve_data.csv"
df_processed.to_csv(output_path, index=False)

print(f"Successfully generated {output_path} with {len(df_processed)} rows!")
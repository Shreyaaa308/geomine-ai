import os
import pandas as pd
import numpy as np

# 1. Read real NASA POWER raw file from your data/raw/ directory
raw_nasa_path = "data/raw/satellite_raw.csv"

# Parse NASA CSV by skipping header metadata
df_nasa = pd.read_csv(raw_nasa_path, skiprows=11)
df_nasa = df_nasa.dropna(how='all')

# Extract real monthly precipitation rates for Balaghat (PRECTOTCORR)
precip_row = df_nasa[(df_nasa['PARAMETER'] == 'PRECTOTCORR') & (df_nasa['YEAR'] == 2023)].iloc[0]
months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
monthly_rain_mm = [float(precip_row[m]) * 30 for m in months]

# 2. Build 24-month historical operational dataset for MOIL Balaghat Mine
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=24, freq="ME")

prod_rows = []
for i, dt in enumerate(dates):
    month_idx = i % 12
    rain = round(monthly_rain_mm[month_idx] + np.random.uniform(-5.0, 5.0), 1)
    
    # Operational downtime & delays correlated with monsoon rainfall
    downtime_hours = round(np.random.uniform(10.0, 40.0) + (rain * 0.15), 1)
    blast_delay_count = int(np.random.randint(1, 5) + (1 if rain > 150 else 0))
    
    # Target vs actual output (Balaghat averages ~35,000 tonnes/month)
    target_output = 35000.0
    reduction = (downtime_hours * 150) + (blast_delay_count * 400)
    actual_output = round(target_output - reduction + np.random.uniform(-1000, 1000), 1)
    
    prod_rows.append({
        "mine_id": "MOIL_BALAGHAT_01",
        "date": dt.strftime("%Y-%m-%d"),
        "planned_target": target_output,
        "actual_output": actual_output,
        "downtime_hours": downtime_hours,
        "rainfall_mm": rain,
        "blast_delay_count": blast_delay_count
    })

df_prod = pd.DataFrame(prod_rows)

# Add lag feature for Person 3's production ML model
df_prod['previous_period_output'] = df_prod['actual_output'].shift(1).fillna(df_prod['actual_output'].iloc[0])

# 3. Export to data/processed/production_data.csv
os.makedirs("data/processed", exist_ok=True)
output_path = "data/processed/production_data.csv"
df_prod.to_csv(output_path, index=False)

print(f"Successfully generated {output_path} with {len(df_prod)} rows!")
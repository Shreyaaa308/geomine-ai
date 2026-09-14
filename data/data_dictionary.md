# Data Dictionary — Geomine AI

## 1. Reserve Data (`data/processed/reserve_data.csv`)
* **grid_cell_id** (string): Grid identifier (`CELL_001` to `CELL_100`).
* **lat** (float): Latitude coordinate (MOIL Balaghat belt).
* **lon** (float): Longitude coordinate.
* **ndvi** (float): Vegetation index.
* **soil_moisture** (float): Profile soil wetness index.
* **lst** (float): Land Surface Temp (°C)[cite: 1].
* **rainfall** (float): Accumulated precipitation (mm)[cite: 1].
* **grade** (float): Manganese ore percentage (`Mn %`)[cite: 1].
* **depth** (float): Borehole sample depth (meters)[cite: 1].
* **reserve_class** (string): Classification label (`High`, `Medium`, `Low`)[cite: 1].

---

## 2. Production Data (`data/processed/production_data.csv`)
* **mine_id** (string): Mine identifier (`MOIL_BALAGHAT_01`)[cite: 1].
* **date** (string): Monthly date record (`YYYY-MM-DD`)[cite: 1].
* **planned_target** (float): Monthly target output (tonnes)[cite: 1].
* **actual_output** (float): Historical output volume (tonnes)[cite: 1].
* **downtime_hours** (float): Equipment downtime duration (hours)[cite: 1].
* **rainfall_mm** (float): Monthly rainfall total (mm)[cite: 1].
* **blast_delay_count** (integer): Frequency of operational blasting delays[cite: 1].
* **previous_period_output** (float): Output volume from the prior month (lag feature)[cite: 1].
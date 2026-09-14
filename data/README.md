# Geomine AI — Data Architecture & Pipeline

This module handles raw data ingestion, feature extraction, and schema enforcement for predictive mining models anchored at MOIL Balaghat ($21.8016^\circ\text{ N}, 80.1847^\circ\text{ E}$).

## Pipeline Execution
Run the following scripts from the project root:
```bash
python data/scripts/build_reserve_pipeline.py
python data/scripts/build_production_pipeline.py
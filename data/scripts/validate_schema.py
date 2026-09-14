import os
import pandas as pd

def validate_datasets():
    reserve_path = "data/processed/reserve_data.csv"
    production_path = "data/processed/production_data.csv"
    
    assert os.path.exists(reserve_path), "reserve_data.csv missing!"
    assert os.path.exists(production_path), "production_data.csv missing!"
    
    df_res = pd.read_csv(reserve_path)
    df_prod = pd.read_csv(production_path)
    
    assert len(df_res) == 100, f"Expected 100 rows in reserve data, got {len(df_res)}"
    assert len(df_prod) == 24, f"Expected 24 rows in production data, got {len(df_prod)}"
    
    print("All dataset schemas and row counts successfully validated!")

if __name__ == "__main__":
    validate_datasets()
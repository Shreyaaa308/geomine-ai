# Production Model Metrics

## Model

Random Forest Regressor

## Dataset

- Total records: 24
- Training records: 18
- Testing records: 6
- Date range: 2023-01-31 to 2024-12-31

## Evaluation Metrics

- MAE: 1206.66
- RMSE: 1260.77

## Features

- `downtime_hours`
- `rainfall_mm`
- `blast_delay_count`
- `previous_period_output`
- `month`

## Feature Importance

| Feature | Importance |
|---|---:|
| downtime_hours | 0.6128 |
| rainfall_mm | 0.2397 |
| previous_period_output | 0.0689 |
| blast_delay_count | 0.0553 |
| month | 0.0234 |

## Output Files

- `production_model.pkl` - trained Random Forest model
- `production_predictions.csv` - test-period predictions
- `actual_vs_predicted.png` - actual vs predicted plot

## Note

The dataset contains 24 monthly records for one mine. A chronological 75/25 train-test split was used so that later months are evaluated as unseen future observations.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/processed/production_data.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort chronologically
df = df.sort_values("date").reset_index(drop=True)

# Extract month as a feature
df["month"] = df["date"].dt.month

print("Data loaded successfully")
print("Dataset shape:", df.shape)


# ============================================================
# 2. DEFINE FEATURES AND TARGET
# ============================================================

features = [
    "downtime_hours",
    "rainfall_mm",
    "blast_delay_count",
    "previous_period_output",
    "month"
]

target = "actual_output"

X = df[features]
y = df[target]


# ============================================================
# 3. CHRONOLOGICAL TRAIN/TEST SPLIT
# ============================================================

# First 18 months -> training
# Last 6 months -> testing

split_index = int(len(df) * 0.75)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 4. TRAIN RANDOM FOREST REGRESSOR
# ============================================================

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

print("\nRandom Forest model trained successfully")


# ============================================================
# 5. PREDICT TEST DATA
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# 6. MODEL EVALUATION
# ============================================================

mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nModel Evaluation")
print("----------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))


# ============================================================
# 7. ACTUAL VS PREDICTED PLOT
# ============================================================

test_dates = df["date"].iloc[split_index:]

plt.figure(figsize=(10, 5))

plt.plot(
    test_dates,
    y_test.values,
    marker="o",
    label="Actual Output"
)

plt.plot(
    test_dates,
    y_pred,
    marker="o",
    label="Predicted Output"
)

plt.xlabel("Date")
plt.ylabel("Production Output")
plt.title("Actual vs Predicted Production Output")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plot_path = "ml/production/actual_vs_predicted.png"

plt.savefig(plot_path, dpi=300)
plt.close()

print("\nActual vs predicted plot saved to:")
print(plot_path)


# ============================================================
# 8. FEATURE IMPORTANCE
# ============================================================

feature_importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    "importance",
    ascending=False
)

print("\nFeature Importance")
print(feature_importance)


# ============================================================
# 9. SAVE TRAINED MODEL
# ============================================================

model_path = "ml/production/production_model.pkl"

joblib.dump(model, model_path)

print("\nModel saved to:")
print(model_path)


# ============================================================
# 10. CREATE PREDICTIONS CSV
# ============================================================

predictions_df = df.iloc[split_index:].copy()

predictions_df["predicted_output"] = y_pred

predictions_df = predictions_df.rename(columns={
    "date": "period",
    "downtime_hours": "downtime",
    "rainfall_mm": "rainfall",
    "blast_delay_count": "blast_delay"
})

predictions_df = predictions_df[
    [
        "mine_id",
        "period",
        "predicted_output",
        "planned_target",
        "downtime",
        "rainfall",
        "blast_delay"
    ]
]

predictions_path = "ml/production/production_predictions.csv"

predictions_df.to_csv(
    predictions_path,
    index=False
)

print("\nPredictions saved to:")
print(predictions_path)


# ============================================================
# 11. CREATE MODEL METRICS REPORT
# ============================================================

metrics_path = "ml/production/production_model_metrics.md"

with open(metrics_path, "w", encoding="utf-8") as f:

    f.write("# Production Model Metrics\n\n")

    f.write("## Model\n\n")
    f.write("Random Forest Regressor\n\n")

    f.write("## Dataset\n\n")
    f.write(f"- Total records: {len(df)}\n")
    f.write(f"- Training records: {len(X_train)}\n")
    f.write(f"- Testing records: {len(X_test)}\n")
    f.write(f"- Date range: {df['date'].min().date()} to {df['date'].max().date()}\n\n")

    f.write("## Evaluation Metrics\n\n")
    f.write(f"- MAE: {mae:.2f}\n")
    f.write(f"- RMSE: {rmse:.2f}\n\n")

    f.write("## Features\n\n")

    for feature in features:
        f.write(f"- `{feature}`\n")

    f.write("\n## Feature Importance\n\n")
    f.write("| Feature | Importance |\n")
    f.write("|---|---:|\n")

    for _, row in feature_importance.iterrows():
        f.write(
            f"| {row['feature']} | {row['importance']:.4f} |\n"
        )

    f.write("\n## Output Files\n\n")
    f.write("- `production_model.pkl` - trained Random Forest model\n")
    f.write("- `production_predictions.csv` - test-period predictions\n")
    f.write("- `actual_vs_predicted.png` - actual vs predicted plot\n")

    f.write("\n## Note\n\n")
    f.write(
        "The dataset contains 24 monthly records for one mine. "
        "A chronological 75/25 train-test split was used so that "
        "later months are evaluated as unseen future observations."
    )

print("\nMetrics report saved to:")
print(metrics_path)

print("\n========================================")
print("PRODUCTION MODEL PIPELINE COMPLETED")
print("========================================")
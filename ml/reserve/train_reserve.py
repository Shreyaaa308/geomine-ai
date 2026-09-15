import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Anchor all paths to this script's own location, not the terminal's cwd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))


def run_reserve_pipeline():
    # 1. Load processed dataset
    data_path = os.path.join(REPO_ROOT, 'data', 'processed', 'reserve_data.csv')

    if not os.path.exists(data_path):
        print(f"Error: Could not find {data_path}. Make sure the CSV file exists.")
        return

    df = pd.read_csv(data_path)
    print("Dataset successfully loaded!")

    # 2. Define features and target
    features = ['lat', 'lon', 'grade', 'depth', 'ndvi', 'soil_moisture', 'lst', 'rainfall']
    target = 'reserve_class'

    X = df[features]
    y = df[target]

    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Initialize and train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    print("Model training completed successfully.")

    # 5. Evaluate model
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # 6. Save trained model artifact (into ml/reserve/, next to this script)
    model_filename = os.path.join(SCRIPT_DIR, 'reserve_model.pkl')
    joblib.dump(model, model_filename)
    print(f"Trained model saved to {model_filename}")

    # 7. Generate predictions for the whole dataset & save output CSV safely mapped to model.classes_
    grid_output = df[['grid_cell_id']].copy()
    full_probabilities = model.predict_proba(X)

    for i, cls in enumerate(model.classes_):
        grid_output[f'probability_{str(cls).lower()}'] = full_probabilities[:, i]
        
    grid_output['predicted_class'] = model.predict(X)

    predictions_filename = os.path.join(SCRIPT_DIR, 'reserve_predictions.csv')
    grid_output.to_csv(predictions_filename, index=False)
    print(f"Saved grid predictions to {predictions_filename}")


if __name__ == "__main__":
    run_reserve_pipeline()
import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PREDICTIONS_FILE = BASE_DIR / "ml" / "reserve" / "reserve_predictions.csv"
RESERVE_DATA_FILE = BASE_DIR / "data" / "processed" / "reserve_data.csv"
OUTPUT_FILE = BASE_DIR / "geo" / "reserve_heatmap.geojson"


def load_csv(path):
    with open(path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def main():
    predictions = load_csv(PREDICTIONS_FILE)
    reserve_data = load_csv(RESERVE_DATA_FILE)

    coordinates = {
        row["grid_cell_id"]: {
            "lat": float(row["lat"]),
            "lon": float(row["lon"]),
        }
        for row in reserve_data
    }

    features = []

    for prediction in predictions:
        cell_id = prediction["grid_cell_id"]

        if cell_id not in coordinates:
            raise ValueError(
                f"Missing coordinates for grid cell: {cell_id}"
            )

        lat = coordinates[cell_id]["lat"]
        lon = coordinates[cell_id]["lon"]

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat],
            },
            "properties": {
                "grid_cell_id": cell_id,
                "probability_high": float(prediction["probability_high"]),
                "probability_medium": float(prediction["probability_medium"]),
                "probability_low": float(prediction["probability_low"]),
                "predicted_class": prediction["predicted_class"],
            },
        }

        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(geojson, file, indent=2)

    print(f"Created: {OUTPUT_FILE}")
    print(f"Features: {len(features)}")


if __name__ == "__main__":
    main()
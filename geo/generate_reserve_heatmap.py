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


def calculate_boundaries(values):
    values = sorted(values)

    if len(values) < 2:
        raise ValueError("At least two grid coordinates are required.")

    boundaries = []

    for index, value in enumerate(values):
        if index == 0:
            next_value = values[index + 1]
            lower = value - (next_value - value) / 2
        else:
            previous_value = values[index - 1]
            lower = (previous_value + value) / 2

        if index == len(values) - 1:
            previous_value = values[index - 1]
            upper = value + (value - previous_value) / 2
        else:
            next_value = values[index + 1]
            upper = (value + next_value) / 2

        boundaries.append((lower, upper))

    return dict(zip(values, boundaries))


def main():
    predictions = load_csv(PREDICTIONS_FILE)
    reserve_data = load_csv(RESERVE_DATA_FILE)

    grid_rows = [
        {
            "grid_cell_id": row["grid_cell_id"],
            "lat": float(row["lat"]),
            "lon": float(row["lon"]),
        }
        for row in reserve_data
    ]

    latitudes = sorted({row["lat"] for row in grid_rows})
    longitudes = sorted({row["lon"] for row in grid_rows})

    lat_boundaries = calculate_boundaries(latitudes)
    lon_boundaries = calculate_boundaries(longitudes)

    coordinates = {
        row["grid_cell_id"]: {
            "lat": row["lat"],
            "lon": row["lon"],
        }
        for row in grid_rows
    }

    features = []

    for prediction in predictions:
        cell_id = prediction["grid_cell_id"]

        if cell_id not in coordinates:
            raise ValueError(f"Missing coordinates for grid cell: {cell_id}")

        lat = coordinates[cell_id]["lat"]
        lon = coordinates[cell_id]["lon"]

        lat_min, lat_max = lat_boundaries[lat]
        lon_min, lon_max = lon_boundaries[lon]

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [lon_min, lat_min],
                        [lon_max, lat_min],
                        [lon_max, lat_max],
                        [lon_min, lat_max],
                        [lon_min, lat_min],
                    ]
                ],
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
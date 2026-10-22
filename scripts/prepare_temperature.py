
import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path

# MMA3001 - Temperature Data Preparation

SENSOR_ID = "6012002000869"

INPUT_FILE = Path(
    "data/raw/5EnvSensor_MayToDec2024_180kRows.csv"
)

OUTPUT_FILE = Path("data/processed/temperature_clean.csv")


def prepare_temperature_data():
    """Extract and clean measurements for one temperature sensor."""

    readings = {}
    duplicates = 0
    conflicts = 0

    with INPUT_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["sensorid"] != SENSOR_ID:
                continue

            payload = json.loads(row["jsondata"])

            for item in payload:

                variable = item.get("variable") or {}

                if variable.get("name") != "Temperature":
                    continue

                for observation in item.get("values", []):

                    timestamp = int(observation["time"])
                    temperature = float(observation["value"])

                    if not math.isfinite(temperature):
                        continue

                    if timestamp in readings:
                        duplicates += 1

                        if readings[timestamp] != temperature:
                            conflicts += 1
                    else:
                        readings[timestamp] = temperature

    if conflicts:
        raise ValueError(
            f"Found {conflicts} conflicting duplicate readings"
        )

    if not readings:
        raise ValueError("No valid temperature readings found")

    # Sort all measurements chronologically
    sorted_readings = sorted(readings.items())

    # Calculate time intervals in seconds
    intervals = [
        sorted_readings[i + 1][0] - sorted_readings[i][0]
        for i in range(len(sorted_readings) - 1)
    ]

    # Count gaps greater than 20 minutes
    large_gaps = sum(gap > 1200 for gap in intervals)

    # Create output folder
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save cleaned data
    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "datetime_utc",
            "temperature_c"
        ])

        for timestamp, temperature in sorted_readings:

            date = datetime.fromtimestamp(
                timestamp, tz=timezone.utc
            ).isoformat()

            writer.writerow([
                timestamp,
                date,
                temperature
            ])

    print("\n===== TEMPERATURE DATA PREPARATION =====")
    print("Selected sensor:", SENSOR_ID)
    print("Unique readings:", len(sorted_readings))
    print("Duplicate observations removed:", duplicates)
    print("Conflicting duplicate observations:", conflicts)
    print("Time gaps greater than 20 minutes:", large_gaps)

    if intervals:
        print(
            "Largest observed interval:",
            round(max(intervals) / 3600, 2),
            "hours"
        )

    print("Cleaned file saved to:", OUTPUT_FILE)
    print("===== PREPARATION COMPLETE =====")


if __name__ == "__main__":
    prepare_temperature_data()
    

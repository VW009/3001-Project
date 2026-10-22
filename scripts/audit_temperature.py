print("MMA3001 Temperature Project Started!")

import csv
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

# MMA3001 - Missing Temperature Data Reconstruction
# Stage 1: Dataset Inspection

print("MMA3001 Temperature Project Started!")

# Location of the original dataset
DATA_FILE = Path("data/raw/5EnvSensor_MayToDec2024_180kRows.csv")


def format_time(timestamp):
    """Convert a Unix timestamp into a readable UTC date."""
    return datetime.fromtimestamp(
        timestamp, tz=timezone.utc
    ).strftime("%Y-%m-%d %H:%M")


def audit_temperature_data(file_path):
    """Extract and inspect temperature sensor measurements."""

    # Store unique measurements for each sensor
    sensors = defaultdict(dict)

    total_rows = 0
    readings = 0
    duplicates = 0
    conflicts = 0
    invalid_json = 0
    invalid_readings = 0

    # Open the supplied CSV
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            total_rows += 1

            # Decode sensor measurements stored as JSON
            try:
                payload = json.loads(row["jsondata"])

                if not isinstance(payload, list):
                    raise ValueError("Unexpected JSON structure")

            except (ValueError, TypeError, KeyError):
                invalid_json += 1
                continue

            sensor_id = row["sensorid"]

            # Find temperature measurements
            for item in payload:
                if not isinstance(item, dict):
                    continue

                variable = item.get("variable") or {}

                if variable.get("name") != "Temperature":
                    continue

                for observation in item.get("values", []):
                    try:
                        timestamp = int(observation["time"])
                        temperature = float(observation["value"])

                        if not math.isfinite(temperature):
                            raise ValueError("Invalid temperature")

                    except (ValueError, TypeError, KeyError):
                        invalid_readings += 1
                        continue

                    readings += 1

                    # Check for repeated timestamps
                    previous = sensors[sensor_id].get(timestamp)

                    if timestamp in sensors[sensor_id]:
                        duplicates += 1

                        if previous != temperature:
                            conflicts += 1
                    else:
                        sensors[sensor_id][timestamp] = temperature

    # Display dataset summary
    print("\n========== DATASET SUMMARY ==========")
    print("Total CSV rows:", total_rows)
    print("Temperature observations:", readings)
    print("Unique sensors:", len(sensors))
    print("Duplicate observations:", duplicates)
    print("Conflicting duplicate values:", conflicts)
    print("Invalid JSON rows:", invalid_json)
    print("Invalid temperature readings:", invalid_readings)

    # Rank sensors by number of unique observations
    ranked_sensors = sorted(
        sensors.items(),
        key=lambda item: len(item[1]),
        reverse=True
    )

    print("\n========== TOP 10 SENSORS ==========")

    for sensor_id, measurements in ranked_sensors[:10]:

        times = sorted(measurements)

        if len(times) < 2:
            continue

        intervals = [
            times[i + 1] - times[i]
            for i in range(len(times) - 1)
        ]

        temperatures = list(measurements.values())

        print(f"\nSensor ID: {sensor_id}")
        print(f"Unique readings: {len(times)}")
        print(f"First reading: {format_time(times[0])}")
        print(f"Last reading: {format_time(times[-1])}")
        print(f"Median interval: {median(intervals):.1f} seconds")
        print(f"Minimum temperature: {min(temperatures):.2f} °C")
        print(f"Maximum temperature: {max(temperatures):.2f} °C")

    print("\n========== AUDIT COMPLETE ==========")


if __name__ == "__main__":

    if not DATA_FILE.exists():
        print(f"ERROR: Dataset not found at {DATA_FILE}")
    else:
        audit_temperature_data(DATA_FILE)

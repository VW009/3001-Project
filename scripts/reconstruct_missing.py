
import csv
from datetime import datetime, timezone
from pathlib import Path

from interpolation_experiment import linear_interpolation

# MMA3001 - Reconstruct Actual Missing Temperature Data

INPUT_FILE = Path("data/processed/temperature_clean.csv")
OUTPUT_FILE = Path("results/reconstructed_missing.csv")

EXPECTED_INTERVAL = 600  # 10 minutes
TOLERANCE = 120           # Allow small timestamp differences
MAX_MISSING = 2           # Up to two missing readings


def reconstruct_missing():
    """Estimate temperatures missing between recorded observations."""

    readings = []

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            readings.append((
                int(row["timestamp"]),
                float(row["temperature_c"])
            ))

    readings.sort()

    predictions = []
    skipped_gaps = 0

    # Compare consecutive recorded measurements
    for i in range(len(readings) - 1):

        t0, temp0 = readings[i]
        t1, temp1 = readings[i + 1]

        gap_seconds = t1 - t0

        # Estimate the number of absent 10-minute observations
        missing_count = round(
            gap_seconds / EXPECTED_INTERVAL
        ) - 1

        if missing_count < 1:
            continue

        expected_gap = (
            missing_count + 1
        ) * EXPECTED_INTERVAL

        # Avoid unsupported gaps or irregular intervals
        if (
            missing_count > MAX_MISSING
            or abs(gap_seconds - expected_gap) > TOLERANCE
        ):
            skipped_gaps += 1
            continue

        for j in range(1, missing_count + 1):

            estimate_time = t0 + j * EXPECTED_INTERVAL

            if estimate_time >= t1:
                continue

            estimated_temp = linear_interpolation(
                t0, temp0,
                t1, temp1,
                estimate_time
            )

            readable_time = datetime.fromtimestamp(
                estimate_time,
                tz=timezone.utc
            ).isoformat()

            predictions.append([
                estimate_time,
                readable_time,
                round(estimated_temp, 4),
                gap_seconds
            ])

    OUTPUT_FILE.parent.mkdir(
        parents=True, exist_ok=True
    )

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "timestamp",
            "datetime_utc",
            "estimated_temperature_c",
            "original_gap_seconds"
        ])

        writer.writerows(predictions)

    print("===== MISSING DATA RECONSTRUCTION =====")
    print("Original measurements:", len(readings))
    print("Temperatures reconstructed:", len(predictions))
    print("Unsupported gaps skipped:", skipped_gaps)
    print("Output:", OUTPUT_FILE)
    print("===== RECONSTRUCTION COMPLETE =====")


if __name__ == "__main__":
    reconstruct_missing()

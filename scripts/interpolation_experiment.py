
import csv
import math
import random
from pathlib import Path

# MMA3001 - Missing Temperature Data Reconstruction
# Linear Interpolation and Validation

INPUT_FILE = Path("data/processed/temperature_clean.csv")
OUTPUT_FILE = Path("results/interpolation_metrics.csv")

GAP_SIZES = [1, 3, 6, 12]
TRIALS = 40
MAX_INTERVAL = 900  # 15 minutes in seconds
RANDOM_SEED = 42


def load_data():
    """Load cleaned temperature measurements."""

    data = []

    with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            timestamp = int(row["timestamp"])
            temperature = float(row["temperature_c"])

            if math.isfinite(temperature):
                data.append((timestamp, temperature))

    data.sort(key=lambda x: x[0])
    return data


def linear_interpolation(t0, y0, t1, y1, t):
    """Estimate temperature between two known readings."""

    if t1 <= t0:
        raise ValueError("Invalid time interval")

    return y0 + (y1 - y0) * (t - t0) / (t1 - t0)


def valid_windows(data, gap_size):
    """Find windows without large existing time gaps."""

    candidates = []

    for start in range(len(data) - gap_size - 1):
        end = start + gap_size + 1

        intervals = [
            data[i + 1][0] - data[i][0]
            for i in range(start, end)
        ]

        if all(0 < dt <= MAX_INTERVAL for dt in intervals):
            candidates.append(start)

    return candidates


def run_experiment():
    """Compare interpolation with a forward-fill baseline."""

    data = load_data()
    print("===== MMA3001 INTERPOLATION =====")
    print("Measurements loaded:", len(data))

    rng = random.Random(RANDOM_SEED)
    used_indices = set()
    results = []

    for gap_size in sorted(GAP_SIZES, reverse=True):

        candidates = valid_windows(data, gap_size)
        rng.shuffle(candidates)

        errors = []
        baseline_errors = []
        completed_trials = 0

        for start in candidates:
            end = start + gap_size + 1
            indices = set(range(start, end + 1))

            if indices & used_indices:
                continue

            t0, y0 = data[start]
            t1, y1 = data[end]

            # Hide intermediate readings and reconstruct them
            for i in range(start + 1, end):
                t, actual = data[i]

                predicted = linear_interpolation(
                    t0, y0, t1, y1, t
                )

                baseline = y0

                errors.append(actual - predicted)
                baseline_errors.append(actual - baseline)

            used_indices.update(indices)
            completed_trials += 1

            if completed_trials >= TRIALS:
                break

        if not errors:
            print(f"No valid windows for gap size {gap_size}")
            continue

        n = len(errors)

        mae = sum(abs(e) for e in errors) / n
        rmse = math.sqrt(sum(e**2 for e in errors) / n)

        baseline_mae = sum(abs(e) for e in baseline_errors) / n
        baseline_rmse = math.sqrt(
            sum(e**2 for e in baseline_errors) / n
        )

        results.append([
            gap_size,
            completed_trials,
            n,
            mae,
            rmse,
            baseline_mae,
            baseline_rmse
        ])

    results.sort(key=lambda row: row[0])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "gap_size",
            "trials",
            "predictions",
            "linear_mae_c",
            "linear_rmse_c",
            "baseline_mae_c",
            "baseline_rmse_c"
        ])

        writer.writerows(results)

    print("\n===== RESULTS =====")

    for row in results:
        gap, trials, n, mae, rmse, base_mae, base_rmse = row

        print(f"\nMissing readings: {gap}")
        print(f"Trials completed: {trials}")
        print(f"Linear MAE: {mae:.4f} °C")
        print(f"Linear RMSE: {rmse:.4f} °C")
        print(f"Baseline MAE: {base_mae:.4f} °C")
        print(f"Baseline RMSE: {base_rmse:.4f} °C")

    print("\nResults saved to:", OUTPUT_FILE)
    print("===== EXPERIMENT COMPLETE =====")


if __name__ == "__main__":
    run_experiment()

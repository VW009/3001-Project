
import csv
from pathlib import Path
import matplotlib.pyplot as plt

# MMA3001 - Temperature Reconstruction
# Plot interpolation accuracy against missing-data gap length

INPUT_FILE = Path("results/interpolation_metrics.csv")
OUTPUT_FOLDER = Path("results/figures")

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

gaps = []
linear_mae = []
baseline_mae = []
linear_rmse = []
baseline_rmse = []

# Read actual experimental results
with INPUT_FILE.open("r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        gaps.append(int(row["gap_size"]))
        linear_mae.append(float(row["linear_mae_c"]))
        baseline_mae.append(float(row["baseline_mae_c"]))
        linear_rmse.append(float(row["linear_rmse_c"]))
        baseline_rmse.append(float(row["baseline_rmse_c"]))

if not gaps:
    raise ValueError("No experiment results found.")

# Graph 1: Mean Absolute Error
plt.figure(figsize=(7, 4))
plt.plot(gaps, linear_mae, "o-", label="Linear Interpolation")
plt.plot(gaps, baseline_mae, "s--", label="Forward-Fill")
plt.xlabel("Number of Missing Readings")
plt.ylabel("Mean Absolute Error (°C)")
plt.title("Temperature Reconstruction - MAE")
plt.xticks(gaps)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_FOLDER / "mae_comparison.png", dpi=300)
plt.close()

# Graph 2: Root Mean Squared Error
plt.figure(figsize=(7, 4))
plt.plot(gaps, linear_rmse, "o-", label="Linear Interpolation")
plt.plot(gaps, baseline_rmse, "s--", label="Forward-Fill")
plt.xlabel("Number of Missing Readings")
plt.ylabel("Root Mean Squared Error (°C)")
plt.title("Temperature Reconstruction - RMSE")
plt.xticks(gaps)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_FOLDER / "rmse_comparison.png", dpi=300)
plt.close()

print("Graphs generated successfully!")
print("Saved to:", OUTPUT_FOLDER)

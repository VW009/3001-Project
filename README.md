**MMA3001 — Missing Temperature Data Reconstruction**

1. **Project Overview**

This project investigates the reconstruction of missing temperature measurements using numerical interpolation. The investigation uses environmental sensor data from the provided dataset.

The main objective is to evaluate the accuracy of linear interpolation in estimating missing temperature readings and investigate how the length of missing-data gaps affects reconstruction performance.

The results are compared against a forward-fill baseline method.

2. **Dataset Description**

The original dataset contains 179,447 sensor records, including temperature, humidity, CO₂ and other environmental measurements.

An initial dataset audit identified 136,604 repeated temperature observations. These duplicate records were removed to prevent repeated measurements from affecting the numerical analysis.

**Selected Sensor**

Sensor ID: 6012002000869

Sensor label: EMS107

Building: 60

Room: G.38

Location: Compactus_upper

Unique temperature readings: 13,800

Median sampling interval: 10 minutes

Recorded temperature range: 19.0–28.5°C

The sensor location was identified using the supplementary Sensor ID and Locations dataset.

This sensor was selected because it provided sufficient measurements for numerical analysis over a relatively continuous recording period.

3. **Numerical Methods**

Linear Interpolation

Linear interpolation estimates missing temperature measurements between two known observations.

The mathematical expression is:

T(t)=T_1+\frac{T_2-T_1}{t_2-t_1}(t-t_1)

where:

(T(t)) is the estimated temperature.

(T_1,T_2) are known temperature measurements.

(t_1,t_2) are their corresponding timestamps.

(t) is the timestamp being estimated.

**Forward-Fill Baseline**

Forward-fill estimates a missing temperature by using the most recent available measurement.

This method provides a simple baseline for evaluating whether linear interpolation improves reconstruction accuracy.

4. **Data Processing**

The dataset was prepared using Python.

The processing procedure involved:

1) Extracting temperature measurements from the original nested JSON data.

2) Selecting the required environmental sensor.

3) Identifying and removing duplicate observations.

4) Sorting measurements chronologically.

5) Identifying irregular sampling intervals and missing-data gaps.

6) Exporting a cleaned temperature dataset.

The selected sensor contained 13,800 unique temperature observations after cleaning.

5. **Validation and Performance Evaluation**

To evaluate reconstruction accuracy, known temperature measurements were deliberately hidden and then estimated using linear interpolation.

Four missing-data gap lengths were investigated:

1 missing reading

3 consecutive missing readings

6 consecutive missing readings

12 consecutive missing readings

The experiment used 40 trials per gap length, with a fixed random seed for reproducibility.

Accuracy was evaluated using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE).

Linear interpolation produced lower reconstruction errors than forward-fill in these experiments.

The recorded results also indicate that reconstruction error increased for the longer missing-data gap.

These results are based on the selected experimental windows and should not be interpreted as guaranteed accuracy for all missing observations.

6. **Reconstruction of Actual Missing Measurements**

Following validation, linear interpolation was applied to gaps in the original temperature record.

The program generated 1,391 estimated temperature measurements from the selected sensor's data.

The reconstructed values were saved to results/reconstructed_missing.csv.

These values are numerical estimates rather than original measured temperatures. Reconstruction assumes an approximately 10-minute sampling interval and is restricted to short gaps.

7. **Numerical Verification**

Five automated verification tests were implemented using Python's unit-test framework.

The tests evaluate:

1) Midpoint interpolation accuracy

2) Interpolation with irregular time intervals

3) Correct reproduction of known endpoints

4) Handling of invalid time intervals

5) Rejection of unsupported large gaps

All fof the above verification tests passed.

8. **Project Files**

The main scripts are located in the scripts directory.

1) audit_temperature.py — Initial dataset investigation

2) prepare_temperature.py — Temperature extraction and cleaning

3) interpolation_experiment.py — Numerical interpolation and baseline comparison

4) plot_results.py — Generation of MAE and RMSE graphs

5) reconstruct_missing.py — Reconstruction of actual missing observations

The tests directory contains numerical verification tests and the test report.

The results directory contains experimental metrics and graphical results.

9. **Running the Project**

Requirements:

Python 3 and the packages specified in requirements.txt are required.

Install dependencies using:

python -m pip install -r requirements.txt

Dataset:

Place the original sensor dataset at:

data/raw/5EnvSensor_MayToDec2024_180kRows.csv

The raw data is excluded from Git version control. It needs to be obtained separately.

**Running the Python Scripts**

Execute the following commands in order from the main project directory:

python scripts/audit_temperature.py

python scripts/prepare_temperature.py

python scripts/interpolation_experiment.py

python scripts/plot_results.py

python scripts/reconstruct_missing.py

Running Tests

python -m unittest discover -s tests -v

10. **Limitations**

The investigation was conducted using measurements from a single environmental sensor. Results may not represent the performance of the method for other rooms, sensors or operating conditions.

Linear interpolation assumes a linear temperature variation between surrounding measurements and may be less accurate when rapid temperature fluctuations occur.


11. **Future Improvements**

Future work could extend the investigation by applying the reconstruction method to additional environmental sensors.

Alternative interpolation techniques, such as cubic spline interpolation, could also be investigated to determine whether they offer improved accuracy.

Further sensitivity analysis could examine longer missing-data intervals and different sensor operating conditions.

12. **AI Assistance**

AI tools assisted with aspects of project planning, Python implementation and debugging. Numerical methods were evaluated using known-value verification tests and comparisons against recorded sensor measurements.

The project report includes a more detailed reflection on AI use, validation and individual learning.
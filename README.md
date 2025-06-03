
# Randomized Battery Usage – State of Health (SOH) Analysis

This repository contains a full pipeline for analyzing the State of Health (SOH) of lithium-ion batteries using the NASA PCoE Randomized Battery Dataset. The project includes structured data extraction, anomaly removal, normalization, and visual analysis of degradation trends.

---

## Dataset

This project uses the NASA PCoE “Randomized Battery Usage” dataset.

- Each `.mat` file represents a single battery tested under varied charge/discharge conditions.
- Data columns include: voltage, current, temperature, relative time, and operation type (C, D, R).
- Files are grouped by temperature and load profiles.

### Features:
| Feature         | Description                           |
|----------------|---------------------------------------|
| `voltage`       | Measured terminal voltage             |
| `current`       | Load/discharge current                |
| `temperature`   | Internal battery temperature          |
| `relative_time` | Timestamps for sampled measurements   |
| `cycle`         | Discharge cycle index (derived)       |
| `subgroup`      | Subgrouping for analysis (A/B packs)  |

> ⚠️ Note: The dataset is **not uploaded to Git** due to its large size. You must manually place the original `.mat` files in `DataSet/1) Raw/`.

### Folder Layout

```
Randomized Battery Usage/
├── Data_Pipeline/
│   ├── 1_Extraction/
│   ├── 2_Transformation/
│   └── 3_Analysis/
│
├── DataSet/   ← Not tracked by Git (external download)
│   ├── 1) Raw/
│   │   ├── Battery_Uniform_Distribution_*
│   │   ├── RW_Skewed_High_40C_DataSet_2Post/
│   ├── 2) Interim/
│   │   ├── flatten.csv
│   └── 3) Processed/
│       ├── flatten_fully_cleaned.csv
│       ├── normalized_flattened.csv
│       └── subgroups.csv
```

---

## Workflow

### 1. Extraction

Initial extraction is performed using scripts in `1_Extraction/`.

- `Data_Sampling.ipynb` is used to quickly inspect one `.mat` file and validate the flattening logic.
- `data_Extraction.py` and `Data_Extraction_parallel.py` process full folders.

Key highlights:
- Uses **nested loops** to traverse multiple experiments within each `.mat` file.
- Can **parallelize** processing using multiprocessing for large-scale batch conversion.
- Designed to automatically scan and ingest all files within a selected directory.

### 2. Transformation

#### EDA Insights

Exploratory data analysis was performed to understand distribution and quality:

```python
sns.boxplot(x='type', y='temperature', data=df)
```

This revealed extreme outliers like `-4000°C` in temperature, which were filtered.

#### Key Issues Identified

- Abnormally long `relative_time` durations (>100,000 sec)
- Negative temperatures
- Voltage spikes above 4.3V
- Current mismatch by `type` (e.g., charge currents > 0 A)

#### Transformation Scripts

- `anomalies.py`: Detects and removes outliers based on thresholds per feature and operation type.
- `normalization.py`: Applies min-max scaling on voltage, current, temperature, and time.
- `EDA.ipynb`: Contains visual plots (boxplots, scatterplots, histograms) to guide filtering logic.

Example anomaly fix:

```python
df = df[(df["temperature"] > 0) & (df["temperature"] < 100)]
df = df[df["voltage"].between(3.0, 4.3)]
```

---

### 3. SOH Analysis

SOH (State of Health) is calculated as the ratio of current cycle discharge capacity to the first:

```python
SOH = (current_capacity / initial_capacity) * 100
```

#### Our Approach

- `relative_time` is used to segment cycles by detecting time resets
- Capacity per cycle is calculated via trapezoidal integration
- SOH is plotted over `cycle_id` for each battery

```python
plt.plot(df["cycle_id"], df["SOH"])
plt.axhline(80, linestyle='--', label="End-of-life threshold")
```

#### Example Result

![SOH Curve](/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/Data_Pipeline/5_Reporting/SOH/SOH.png)

The chart shows degradation curves for different battery configurations, where SOH falls below 80%—indicating end of useful life.

---

## How to Run

1. Place `.mat` files in `DataSet/1) Raw/`
2. Run extraction scripts to generate interim CSVs
3. Clean and normalize the data using transformation scripts
4. Open `SOH_Analysis.ipynb` to run the SOH computation and view plots

---

## Requirements

- Python 3.8+
- pandas, numpy, scipy, matplotlib, seaborn
- scikit-learn

## 👨‍🔬 Author & Acknowledgements

**Author**: Tarun Shyam  
**Institution**: Brandenburg Technical University – MSc in Artificial Intelligence 

## Concepts Covered

- SOH & battery degradation estimation
- Trapezoidal numerical integration
- Feature scaling and normalization
- Visual EDA and hypothesis formulation

## License

This project is for academic and educational use. Please cite the original NASA dataset if using this work in publications.



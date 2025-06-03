
# 🔋 Randomized Battery Usage – SOH Analysis using NASA Dataset

This repository presents a structured ETL-based analysis pipeline for **State of Health (SOH)** estimation of Li-ion batteries using the **NASA PCoE Randomized Battery Dataset**. It explores data extraction, transformation, feature analysis, and visual diagnostics aimed at improving predictive maintenance through battery health tracking.

---

## 📂 Project Structure

```
Randomized Battery Usage/
├── SOH_Analysis_NASA.ipynb              # Top-level orchestration and analysis notebook
├── ETL/
│   ├── Extraction/
│   │   ├── data_Extraction.py           # Extract and flatten MATLAB battery data
│   │   ├── Data_Sampling.ipynb          # Initial inspection and sample generation
│   │   └── Data_Extraction_parallel.py  # Parallelized data loader (if applicable)
│   └── Transformation/
│       ├── transform.py                 # Preprocessing & data transformation logic
│       ├── soh.py                       # SOH computation module
│       ├── soh_results.csv              # Output capacity/SOH values (generated)
│       ├── EDA.ipynb                    # Exploratory Data Analysis notebook
│       ├── Standard.ipynb               # Normalization and standardization
│       └── EDA_Data.ipynb               # Extended visual/data insights
```

---

## 📊 Dataset Description

- **Source**: NASA Prognostics Center of Excellence (PCoE)  
- **Dataset**: *Battery_Uniform_Distribution_2Post*  
- **Files**: `.mat` files with recorded battery cycles, voltage, current, temperature over time  
- **Goal**: Derive degradation trends, estimate SOH per cycle, and prepare for RUL modeling  

### 📈 Features:
| Feature         | Description                           |
|----------------|---------------------------------------|
| `voltage`       | Measured terminal voltage             |
| `current`       | Load/discharge current                |
| `temperature`   | Internal battery temperature          |
| `relative_time` | Timestamps for sampled measurements   |
| `cycle`         | Discharge cycle index (derived)       |
| `subgroup`      | Subgrouping for analysis (A/B packs)  |

---

## ⚙️ Methods & Workflow

### ✅ 1. **Data Extraction**
- Extracts MATLAB battery `.mat` files
- Flattens nested structures into tabular form
- Parallelized logic for faster loading (`Data_Extraction_parallel.py`)

### ✅ 2. **Transformation & Cleaning**
- Filters only discharge cycles
- Calculates capacity (Ah) via trapezoidal integration of current over time
- SOH computed as:
  \[
  \text{SOH} = \frac{\text{Current Capacity}}{\text{Initial Capacity}} \times 100
  \]

### ✅ 3. **Exploratory Data Analysis**
- Distribution of SOH across subgroups
- Visualization of degradation trends
- Identification of abnormal values (e.g., voltage spikes, -100°C errors)

### ✅ 4. **Normalization**
- Scales voltage, temperature, and current for comparative analysis
- Prepares features for downstream modeling (if extended to ML)

---

## 📌 Results & Observations

- **SOH trends** reveal predictable linear and non-linear degradation across different battery packs.
- **Subgroup variations** are visualized (`soh_folder_a.png`, `soh_folder_b.png`).
- **Capacity loss** shows meaningful decay, useful for RUL prediction models.

---

## 📦 Requirements

You can install dependencies via:

```bash
pip install -r requirements.txt
```

Typical dependencies include:
- `numpy`, `pandas`, `matplotlib`, `scipy`
- `mat73` (if using `.mat` v7.3 files)

---

## 🚀 How to Run

1. Place the NASA `.mat` files into the appropriate data directory.
2. Run the notebooks in order:
   - `Data_Sampling.ipynb` for an overview
   - `EDA_Data.ipynb` for initial exploration
   - `transform.py` and `soh.py` for computing SOH
   - `SOH_Analysis_NASA.ipynb` to consolidate and visualize

3. Results will be saved to:  
   `ETL/Transformation/soh_results.csv`

---

## 📚 Concepts Covered

- SOH & battery degradation estimation
- Trapezoidal numerical integration
- Feature scaling and normalization
- Snakemake-ready modular pipeline (if expanded)
- Visual EDA and hypothesis formulation

---

## 👨‍🔬 Author & Acknowledgements

**Author**: Tarun Shyam  
**Institution**: Brandenburg Technical University – MSc in Artificial Intelligence  
**Dataset Credit**:  
Saha, B. and Goebel, K. (2007). “Battery Data Set”, NASA Prognostics Data Repository, NASA Ames Research Center

---

## 📜 License

This project is for academic and educational use. Please cite the original NASA dataset if using this work in publications.

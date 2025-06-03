import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === 1. Load data ===
file_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/3_Processed/flatten_fully_cleaned.csv"  # Adjust if needed
df = pd.read_csv(file_path)

# === 2. Filter for discharge cycles ===
df_discharge = df[df["type"] == "D"].copy()

# === 3. Compute capacity (Ah) per source_file and subgroup ===
def compute_capacity(group):
    current = group["current"].values
    time = group["relative_time"].values
    if len(current) < 2:
        return np.nan  # avoid error
    capacity_coulombs = np.sum(current[:-1] * np.diff(time))  # in Coulombs
    capacity_ah = capacity_coulombs / 3600  # convert to Ah
    return capacity_ah

capacity_df = df_discharge.groupby(["source_file", "subgroup"]).apply(compute_capacity).reset_index()
capacity_df.columns = ["source_file", "subgroup", "capacity_ah"]

# === 4. Normalize to first cycle to get SOH ===
capacity_df["SOH"] = capacity_df.groupby("source_file")["capacity_ah"].transform(
    lambda x: (x / x.iloc[0]) * 100
)

# === 5. Plot SOH curves by battery group ===
folder_A = ["RW1.mat", "RW2.mat", "RW3.mat", "RW4.mat"]
folder_B = ["RW5.mat", "RW6.mat", "RW7.mat", "RW8.mat"]

def plot_soh_curves(folder_batteries, title, file_name):
    plt.figure(figsize=(10, 6))
    for battery in folder_batteries:
        subset = capacity_df[capacity_df["source_file"] == battery]
        plt.plot(subset["subgroup"], subset["SOH"], label=battery)
    plt.title(title)
    plt.xlabel("Discharge Cycle")
    plt.ylabel("SOH (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()

plot_soh_curves(folder_A, "SOH Curves - Folder A", "soh_folder_a.png")
plot_soh_curves(folder_B, "SOH Curves - Folder B", "soh_folder_b.png")

# === 6. Save computed SOH values ===
capacity_df.to_csv("soh_results.csv", index=False)

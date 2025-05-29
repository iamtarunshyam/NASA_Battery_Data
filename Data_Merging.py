import os
import pandas as pd

# Base folder where .csv files were created
base_dir = 'dataset/1. BatteryAgingARC-FY08Q4'  # Adjust if needed

# Container for all dataframes
merged_data = []

# Walk through subfolders and find all *_discharge.csv files
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('_discharge.csv'):
            file_path = os.path.join(root, file)
            try:
                df = pd.read_csv(file_path)
                df['Battery_ID'] = os.path.splitext(file)[0].split('_')[0]
                merged_data.append(df)
                print(f"Merged: {file}")
            except Exception as e:
                print(f"Error reading {file}: {e}")

# Concatenate into one DataFrame
if merged_data:
    master_df = pd.concat(merged_data, ignore_index=True)
    output_path = os.path.join(base_dir, 'battery_discharge_master.csv')
    master_df.to_csv(output_path, index=False)
    print(f"\n✅ Master file created: {output_path}")
else:
    print("⚠️ No discharge CSVs found.")

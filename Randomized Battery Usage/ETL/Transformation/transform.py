import pandas as pd
import os

# === CONFIGURATION ===
input_csv_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/ETL/Transformation/flattened_battery_data_scaled.csv"
output_dir = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/ETL/Processed_By_Source"
os.makedirs(output_dir, exist_ok=True)

# === LOAD ENTIRE CSV INTO MEMORY ===
print("Reading full CSV into memory (this may take a few minutes)...")
df = pd.read_csv(input_csv_path)
print(f"Total records: {len(df)}")

# === SEGREGATE BY source_file ===
unique_sources = df['source_file'].unique()
print(f"Found {len(unique_sources)} unique source_file(s):", unique_sources)

for source in unique_sources:
    print(f"\nProcessing source_file: {source}")

    # Filter data
    df_sub = df[df['source_file'] == source].copy()

    # Optional: Reset index
    df_sub.reset_index(drop=True, inplace=True)

    # Optional: Assign a placeholder 'cycle_id' (can be updated later)
    df_sub['cycle_id'] = None  # TODO: Replace with real cycle logic if known

    # Generate clean filename
    filename = f"{source.replace('.mat','').replace('/', '_')}_processed.csv"
    file_path = os.path.join(output_dir, filename)

    # Save to CSV
    df_sub.to_csv(file_path, index=False)
    print(f"Saved {len(df_sub)} rows to: {file_path}")

print("\n All source files processed and saved individually.")

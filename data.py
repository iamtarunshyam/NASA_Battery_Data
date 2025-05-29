import os
import scipy.io
import pandas as pd
import numpy as np

base_dir = 'dataset/1. BatteryAgingARC-FY08Q4'
summary_rows = []

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.mat'):
            mat_path = os.path.join(root, file)
            try:
                mat = scipy.io.loadmat(mat_path)
                key = [k for k in mat.keys() if not k.startswith("__")][0]
                cycles = mat[key][0, 0]["cycle"][0]

                print(f"Processing {file}")
                for i, cycle in enumerate(cycles):
                    ctype = cycle["type"][0]
                    if isinstance(ctype, (np.ndarray, list)):
                        ctype = ctype[0]
                    if isinstance(ctype, bytes):
                        ctype = ctype.decode("utf-8")

                    if ctype == "discharge":
                        ambient_temp = cycle["ambient_temperature"][0][0]
                        start_time = cycle["time"][0][0]
                        data = cycle["data"]

                        voltage = data[0][0][0].flatten()
                        current = data[0][0][1].flatten()
                        time = data[0][0][3].flatten()

                        # Estimate capacity (approximate as sum of current*time)
                        delta_time = np.diff(time, prepend=time[0])
                        capacity = np.sum(current * delta_time)

                        summary_rows.append({
                            "battery_id": os.path.splitext(file)[0],
                            "cycle_index": i + 1,
                            "start_time": start_time,
                            "ambient_temperature": ambient_temp,
                            "Capacity": capacity
                        })
            except Exception as e:
                print(f"Error in {file}: {e}")

# Create summary DataFrame
summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv(os.path.join(base_dir, 'battery_discharge_summary.csv'), index=False)
print("Cycle-level summary file created.")

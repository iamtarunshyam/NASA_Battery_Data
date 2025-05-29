import os
import scipy.io
import pandas as pd
import numpy as np

# Base directory with .mat files
base_dir = 'dataset/1. BatteryAgingARC-FY08Q4'  # Adjust if needed

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.mat'):
            mat_path = os.path.join(root, file)
            try:
                # Load the .mat file
                mat = scipy.io.loadmat(mat_path)
                key = [k for k in mat.keys() if not k.startswith("__")][0]
                cycles = mat[key][0, 0]["cycle"][0]

                discharge_data = []

                print(f"\nProcessing {file}")
                for i, cycle in enumerate(cycles):
                    ctype = cycle["type"][0]
                    if isinstance(ctype, (np.ndarray, list)):
                        ctype = ctype[0]
                    if isinstance(ctype, bytes):
                        ctype = ctype.decode("utf-8")

                    if ctype == "discharge":
                        data = cycle["data"]
                        voltage = data[0][0][0].flatten()
                        current = data[0][0][1].flatten()
                        temp = data[0][0][2].flatten()
                        time = data[0][0][3].flatten()

                        df = pd.DataFrame({
                            "Voltage": voltage,
                            "Current": current,
                            "Temperature": temp,
                            "Time": time
                        })
                        df["Cycle_Index"] = i + 1
                        discharge_data.append(df)

                if discharge_data:
                    result = pd.concat(discharge_data, ignore_index=True)
                    out_name = os.path.splitext(file)[0] + "_discharge.csv"
                    result.to_csv(os.path.join(root, out_name), index=False)
                    print(f"  Saved: {out_name}")
                else:
                    print(f"  No discharge data found in {file}")
            except Exception as e:
                print(f"Error in {file}: {e}")

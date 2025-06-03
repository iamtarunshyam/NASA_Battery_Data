import os
import glob
import scipy.io
import pandas as pd
from pathlib import Path
import numpy as np

def extract_from_mat(file_path):
    try:
        mat = scipy.io.loadmat(file_path, struct_as_record=False, squeeze_me=True)
        if 'data' not in mat:
            return []

        data = mat['data']
        if not hasattr(data, 'step'):
            return []

        steps_array = data.step
        if not isinstance(steps_array, (list, tuple, np.ndarray)):
            steps_array = [steps_array]

        results = []
        for step in steps_array:
            try:
                record = {
                    "type": getattr(step, 'type', None),
                    "relative_time": getattr(step, 'relativeTime', None),
                    "voltage": getattr(step, 'voltage', None),
                    "current": getattr(step, 'current', None),
                    "temperature": getattr(step, 'temperature', None),
                }
                results.append(record)
            except Exception:
                continue

        return results

    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
        return []

def get_subgroup_from_path(path):
    parts = Path(path).parts
    for p in parts:
        if "DataSet" in p or "Battery" in p:
            return p.replace("_2Post", "").replace(".mat", "")
    return "Unknown"

base_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/1) Raw"
all_mat_files = glob.glob(os.path.join(base_path, "**", "*.mat"), recursive=True)

all_data = []
for file_path in all_mat_files:
    print(f"Processing {Path(file_path).name}...")
    records = extract_from_mat(file_path)
    subgroup = get_subgroup_from_path(file_path)
    for r in records:
        r["source_file"] = Path(file_path).name
        r["subgroup"] = subgroup
        all_data.append(r)

if all_data:
    df = pd.DataFrame(all_data)
    output_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/2) Processed/RW_all_subgroups_output.csv"
    df.to_csv(output_path, index=False)
    print("Done. Rows extracted:", len(df))
    print(f"Saved to {output_path}")
else:
    print("No valid data extracted. Please check the structure.")
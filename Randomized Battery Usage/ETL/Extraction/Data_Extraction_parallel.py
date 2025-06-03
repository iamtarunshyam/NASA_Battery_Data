import os
import glob
import csv
import scipy.io
import numpy as np
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_file(file_path):
    try:
        mat = scipy.io.loadmat(file_path, struct_as_record=False, squeeze_me=True)
        if 'data' not in mat:
            return []

        data = mat['data']
        if not hasattr(data, 'step'):
            return []

        steps = data.step
        if not isinstance(steps, (list, tuple, np.ndarray)):
            steps = [steps]

        rows = []
        for step in steps:
            try:
                step_type = getattr(step, 'type', None)
                time = getattr(step, 'relativeTime', None)
                voltage = getattr(step, 'voltage', None)
                current = getattr(step, 'current', None)
                temp = getattr(step, 'temperature', None)

                if all(hasattr(x, '__len__') for x in [time, voltage, current, temp]):
                    for t, v, c, tm in zip(time, voltage, current, temp):
                        rows.append({
                            "type": step_type,
                            "relative_time": t,
                            "voltage": v,
                            "current": c,
                            "temperature": tm,
                            "source_file": Path(file_path).name,
                            "subgroup": Path(file_path).parts[-4]
                        })
            except Exception:
                continue
        return rows

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return []

# === MAIN ===
if __name__ == "__main__":
    base_dir = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/1) Raw"
    output_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/2) Processed/flatten_fully_cleaned.csv"

    all_files = glob.glob(os.path.join(base_dir, "**/*.mat"), recursive=True)

    with open(output_path, mode='w', newline='') as csvfile:
        writer = None
        header_written = False

        # Limit number of workers to 2–4 based on your system
        with ProcessPoolExecutor(max_workers=4) as executor:
            future_to_file = {executor.submit(process_file, file): file for file in all_files}

            for i, future in enumerate(as_completed(future_to_file)):
                file_path = future_to_file[future]
                try:
                    rows = future.result()
                    if rows:
                        print(f" [{i+1}/{len(all_files)}] Processed: {file_path} | Rows: {len(rows)}")

                        if not header_written:
                            writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
                            writer.writeheader()
                            header_written = True

                        writer.writerows(rows)
                    else:
                        print(f" [{i+1}/{len(all_files)}] No valid rows in: {file_path}")

                except Exception as e:
                    print(f" Failed: {file_path} | Error: {e}")

    print(f"\n All files processed. Flattened data saved to:\n{output_path}")

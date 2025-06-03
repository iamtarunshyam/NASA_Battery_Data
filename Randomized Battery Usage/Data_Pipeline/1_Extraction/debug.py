import os
import glob
import scipy.io
from pathlib import Path

base_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet"
all_mat_files = glob.glob(os.path.join(base_path, "**", "*.mat"), recursive=True)

def deep_debug_step(file_path):
    print("=" * 80)
    print(f"Inspecting: {file_path}")
    try:
        mat = scipy.io.loadmat(file_path, struct_as_record=False, squeeze_me=True)

        if 'data' not in mat:
            print("  'data' key not found in this file.")
            return

        data = mat['data']

        if not hasattr(data, 'step'):
            print("  'step' attribute not found in 'data'")
            return

        steps = data.step
        if not isinstance(steps, (list, tuple)):
            steps = [steps]

        print(f"  Total steps: {len(steps)}")
        print(f"  step[0] type: {type(steps[0])}")
        print(f"  step[0] raw content:\n{repr(steps[0])}")

    except Exception as e:
        print(f"  Error processing file: {e}")

# Trying on the first file for clarity
deep_debug_step(all_mat_files[0])

import pandas as pd

file_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/3_Processed/flatten_fully_cleaned.csv"
df = pd.read_csv(file_path)

# Temperature filter: (0°C to 100°C) 
df = df[(df["temperature"] > 0) & (df["temperature"] < 100)]

# Voltage filter: typical Li-ion operating range (3.0V to 4.3V)
df = df[df["voltage"].between(3.0, 4.3)]

# Current filter: type-specific ranges
df = df[
    ((df["type"] == "D") & (df["current"].between(0, 5))) |
    ((df["type"] == "C") & (df["current"].between(-2.5, 0))) |
    ((df["type"] == "R") & (df["current"].abs() < 0.05))
]

# Filter long duration cycles (e.g., relative_time < 100000s)
df = df[df["relative_time"] < 100000]

# Saving cleaned dataset 
output_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/3_Processed/cleaned.csv"
df.to_csv(output_path, index=False)

print("Cleaned dataset saved to:")
print(output_path)
print("Remaining rows:", len(df))

import pandas as pd
from sklearn.preprocessing import MinMaxScaler  # or StandardScaler

file_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/3_Processed/cleaned.csv"
df = pd.read_csv(file_path)

# Selecting columns to normalize
columns_to_normalize = ["voltage", "current", "temperature", "relative_time"]

# Applying Min-Max normalization
scaler = MinMaxScaler()
df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])

# Optional: Z-score standardization
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])

# === Save normalized dataset ===
output_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/3_Processed/normalized_flattened.csv"
df.to_csv(output_path, index=False)

print(" Normalized dataset saved to:")
print(output_path)
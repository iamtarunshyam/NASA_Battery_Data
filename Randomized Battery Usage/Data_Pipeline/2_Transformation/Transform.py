import pandas as pd


file_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/3_Processed/flatten_fully_cleaned.csv"
df = pd.read_csv(file_path)

folders_to_keep = [
    "Battery_Uniform_Distribution_Discharge_Room_Temp_DataSet_2Post",
    "Battery_Uniform_Distribution_Variable_Charge_Room_Temp_DataSet_2Post"
]

filtered_df = df[df["subgroup"].isin(folders_to_keep)].copy()

output_path = "/Users/tarunshyam/Learning/NASA_Battery_data/Randomized Battery Usage/DataSet/3_Processed/subgroups.csv"
filtered_df.to_csv(output_path, index=False)

print(" Filtered file saved to:")
print(output_path)
print("Rows retained:", len(filtered_df))
print("Included subgroups:", filtered_df['subgroup'].unique())
import pandas as pd
import matplotlib.pyplot as plt

# Load the merged data
df = pd.read_csv('dataset/1. BatteryAgingARC-FY08Q4/battery_discharge_master.csv')

# Plot voltage over time for a single cycle (e.g., first cycle of B0005)
battery_id = 'B0005'
cycle_index = 1

subset = df[(df['Battery_ID'] == battery_id) & (df['Cycle_Index'] == cycle_index)]

plt.figure(figsize=(10, 5))
plt.plot(subset['Time'], subset['Voltage'])
plt.title(f'Voltage vs Time for {battery_id}, Cycle {cycle_index}')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.show()

# Group by battery and cycle, compute average voltage
avg_voltage_per_cycle = df.groupby(['Battery_ID', 'Cycle_Index'])['Voltage'].mean().reset_index()

# Plot for one battery
battery_data = avg_voltage_per_cycle[avg_voltage_per_cycle['Battery_ID'] == battery_id]

plt.figure(figsize=(10, 5))
plt.plot(battery_data['Cycle_Index'], battery_data['Voltage'])
plt.title(f'Average Voltage per Cycle for {battery_id}')
plt.xlabel('Cycle Index')
plt.ylabel('Average Voltage (V)')
plt.grid(True)
plt.show()

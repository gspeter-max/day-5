'''
Problem 1: NumPy - Efficient Subarray Transformation
Problem Statement:
You are given a large 2D NumPy array A of shape (N, M), where N ≈ 10⁶ and M ≈ 100. Each row represents a sequence of sensor readings over time.

You must perform the following transformations efficiently:
Normalize each row using Z-score normalization:
For each row, find the longest contiguous subarray where the absolute values of elements are ≤ 1.5.

Return an array result of shape (N, 2), where result[i] = (start_idx, end_idx) represents the start and end indices (0-based) of the longest valid subarray for row i. If multiple such subarrays exist, return the one with the smallest start_idx.

Constraints:
You must use vectorized NumPy operations as much as possible. Avoid Python loops.
The solution must run in O(NM) or better.
You cannot use explicit for-loops over rows.
'''

import numpy as np
# Simulating the sensor data (for testing purposes, use np.load('sensor_data.npy') in production)
np.random.seed(42)
A = np.random.normal(loc=50, scale=10, size=(10, 100))  # A smaller example dataset

# 1. Z-score Normalization: (A - mean) / std for each row
means = A.mean(axis=1, keepdims=True)
stds = A.std(axis=1, keepdims=True)
A_normalized = (A - means) / stds

# 2. Find the longest contiguous subarray where all elements are <= 1.5 in absolute value
def find_longest_valid_subarray(row):
    # Find indices where the absolute value is <= 1.5
    valid_indices = np.abs(row) <= 1.5
    
    # Identify contiguous segments of valid indices
    max_length = 0
    start_idx = -1
    end_idx = -1
    current_start = None
    
    for i, is_valid in enumerate(valid_indices):
        if is_valid:
            if current_start is None:
                current_start = i  # New valid segment starts
        else:
            if current_start is not None:
                length = i - current_start
                if length > max_length:
                    max_length = length
                    start_idx = current_start
                    end_idx = i - 1
                current_start = None  # Reset the start index
    
    # Final check for the last segment if it's valid till the end
    if current_start is not None:
        length = len(valid_indices) - current_start
        if length > max_length:
            start_idx = current_start
            end_idx = len(valid_indices) - 1
    
    return start_idx, end_idx

# Apply the function row-wise
result = np.array([find_longest_valid_subarray(row) for row in A_normalized])

# Output: a 2D array with the start and end indices of the longest subarray per row
print(result)


'''
roblem 2: Pandas - Optimized Event Detection in Time-Series Data
Problem Statement:
You are given a huge Pandas DataFrame df with billions of rows containing IoT device logs. Each row records an event from a sensor.

DataFrame Schema:
timestamp (datetime)	device_id (int)	temperature (float)	pressure (float)
2024-01-01 00:00:01	1001	24.5	101.2
2024-01-01 00:00:02	1002	30.1	102.5
...	...	...	...
Your Task:
Identify device failure events: A device is considered to have failed if, for any 30-second window, both conditions hold:

The mean temperature in the window exceeds 50°C.
The standard deviation of pressure in the window exceeds 5

pd.DataFrame({
    "device_id": [...],    # Unique device IDs that failed
    "first_failure_time": [...]  # First timestamp where the failure was detected
})
Constraints:
The dataset is massive (~500 million rows).
The solution should be efficient. Avoid explicit looping over timestamps.
Use rolling window functions, groupby, and vectorized operations to achieve optimal performance.
'''

import pandas as pd
import numpy as np

np.random.seed(42)

num_devices = 10**4  # 10,000 unique devices
num_rows = 5 * 10**6  # 5 million rows (adjustable for testing)
start_time = pd.Timestamp("2024-01-01")

timestamps = start_time + pd.to_timedelta(np.random.randint(0, 864000, num_rows), unit="s")
device_ids = np.random.choice(range(1, num_devices + 1), num_rows)

temperature = np.random.normal(loc=45, scale=10, size=num_rows)
pressure = np.random.normal(loc=100, scale=3, size=num_rows)

failure_indices = np.random.choice(num_rows, size=int(0.01 * num_rows), replace=False)
temperature[failure_indices] += np.random.uniform(10, 20, size=len(failure_indices))
pressure[failure_indices] += np.random.uniform(5, 10, size=len(failure_indices))

df = pd.DataFrame({
    "timestamp": timestamps,
    "device_id": device_ids,
    "temperature": temperature,
    "pressure": pressure
})

df = df.sort_values(by="timestamp").reset_index(drop=True)


df['rolling_window'] = df.groupby('device_id')["temperature"].rolling(window = 30, min_periods = 1).mean().reset_index(drop = True )  
df['std_pressure'] = df.groupby('device_id')['pressure'].rolling(window = 30, min_periods = 1).std().reset_index( drop = True) 

df  = df[(df['rolling_window'] > 50) & (df['std_pressure'] > 5)][['device_id','timestamp']]
df.columns = ['device_id','first_failure_time']

df = df.groupby('device_id').first().reset_index() 
print(df)

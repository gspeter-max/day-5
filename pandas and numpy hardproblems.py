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

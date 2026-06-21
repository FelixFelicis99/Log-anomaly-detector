# make_features.py
import pandas as pd
import numpy as np
import os

csv_path = "parsed_logs.csv"
output_npy_path = "features.npy"

if not os.path.exists(csv_path):
    print(f"Error: Could not find '{csv_path}'. Please run local_parse.py first.")
    exit()

print("loading parsed log data...")
df = pd.read_csv(csv_path)

# Parameters for windowing
WINDOW_SIZE = 20  # Group 20 log lines into a single sequence "event"
STEP_SIZE = 5     # Slide forward by 5 lines for the next window

# Dynamically find how many unique templates Drain3 discovered
num_templates = int(df["template_id"].max() + 1)
print(f"total unique log templates identified by Drain3: {num_templates}")

windows = []
print("engineering sliding window feature vectors...")

# Slide down the dataframe rows
for i in range(0, len(df) - WINDOW_SIZE + 1, STEP_SIZE):
    window_subset = df.iloc[i : i + WINDOW_SIZE]
    
    # Create an empty frequency vector (Bag of Words) for this specific window
    feature_vector = np.zeros(num_templates)
    
    for tid in window_subset["template_id"]:
        if 0 <= tid < num_templates:
            feature_vector[int(tid)] += 1
            
    windows.append(feature_vector)

# Convert list to a highly compressed NumPy array matrix
X = np.array(windows)
np.save(output_npy_path, X)

print(f"Feature matrix successfully created")
print(f"saved to '{output_npy_path}'")
print(f"Matrix Dimensions: {X.shape} -> ({X.shape[0]} windows, {X.shape[1]} features each)")
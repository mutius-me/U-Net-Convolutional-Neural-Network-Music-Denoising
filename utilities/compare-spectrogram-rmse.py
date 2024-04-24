##############################################################################
# NAME: compare-spectrogram-rmse.py
# DESCRIPTION: This module takes in two directories of spectrograms with
# identical file structures and naming, and returns a statistical analysis
# of the MSE and RMSE between corresponding spectrogams.
###############################################################################

import os
import numpy as np
import random

def calculate_mse(array1, array2):
    """Calculate the Mean Squared Error between two numpy arrays."""
    return np.mean((array1 - array2) ** 2)

def calculate_rmse(mse):
    """Calculate the Root Mean Squared Error from MSE."""
    return np.sqrt(mse)


def compare_arrays(root_dir1, root_dir2):
    """Compare arrays in mirrored directory structures and compute statistics."""
    mse_values = []
    similarity_results = {}
    
    # Walk through the first directory tree
    for dirpath, _, filenames in os.walk(root_dir1):
        # Construct the corresponding directory path in the second tree
        path_correspondence = os.path.join(root_dir2, os.path.relpath(dirpath, root_dir1))
        
        # Check if the corresponding directory exists in the second tree
        if os.path.exists(path_correspondence):
            for filename in filenames:
                if filename.endswith('.npy'):  # Assuming the files are numpy arrays saved as .npy
                    file_path1 = os.path.join(dirpath, filename)
                    file_path2 = os.path.join(path_correspondence, filename)
                    
                    if os.path.exists(file_path2):
                        # Load the arrays
                        array1 = np.load(file_path1)
                        array2 = np.load(file_path2)
                        
                        # Calculate MSE
                        mse = calculate_mse(array1, array2)
                        mse_values.append(mse)
                        
                        # Store results
                        similarity_results[file_path1] = {'mse': mse, 'file_path2': file_path2}
                    else:
                        print(f"File {filename} not found in both trees.")
        else:
            print(f"Directory {path_correspondence} does not exist in {root_dir2}.")

    # Calculate overall statistics
    mse_array = np.array(mse_values)
    mean_mse = np.mean(mse_array)
    std_mse = np.std(mse_array)
    mean_rmse = calculate_rmse(mean_mse)
    
    # Statistics results
    stats = {
        'mean_mse': mean_mse,
        'std_mse': std_mse,
        'mean_rmse': mean_rmse
    }
    
    return similarity_results, stats


def load_random_arrays(dir_path, num_samples=1):
    """Load random .npy files from a given directory."""
    npy_files = [f for f in os.listdir(dir_path) if f.endswith('.npy')]
    selected_files = random.sample(npy_files, num_samples)
    arrays = [np.load(os.path.join(dir_path, file)) for file in selected_files]
    return arrays

def compare_random_arrays(root_dir1, root_dir2, num_comparisons=10):
    """Compare random arrays between two directory trees."""
    random_mse = []
    
    for _ in range(num_comparisons):
        # Select random directory from root_dir1
        dir1 = random.choice([x[0] for x in os.walk(root_dir1)])
        dir2 = random.choice([x[0] for x in os.walk(root_dir2)])
        
        try:
            array1 = load_random_arrays(dir1, 1)[0]
            array2 = load_random_arrays(dir2, 1)[0]
            mse = calculate_mse(array1, array2)
            random_mse.append(mse)
        except ValueError:
            print(f"Not enough files to sample in {dir1} or {dir2}.")
            continue

    return np.mean(random_mse), np.std(random_mse)


dir1 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/spectrogram-128-frames'
dir2 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/spectrogram-128-frames'

results, statistics = compare_arrays(dir1, dir2)

# Print results
for key, value in results.items():
    print(f"Comparison for {key} and {value['file_path2']}: MSE = {value['mse']}")
    
# Print statistics
print("\nStatistical Analysis of MSE across all comparisons:")
print(f"Mean MSE: {statistics['mean_mse']}")
print(f"Standard Deviation of MSE: {statistics['std_mse']}")
print(f"Mean RMSE: {statistics['mean_rmse']}")


random_mean_mse, random_std_mse = compare_random_arrays(dir1, dir2, 100)

# Print results
print("\nRandom Comparison Statistics:")
print(f"Mean MSE for random comparisons: {random_mean_mse}")
print(f"Standard Deviation for random MSE: {random_std_mse}")


##############################################################################
# NAME: get_spectrogram_metadata.py
# DESCRIPTION: A module that prints metadata of spectrograms in an inputted
# directory.
###############################################################################

import os
import numpy as np

def traverse_and_compare_shapes(root_dir):
    first_shape = None
    is_first = True
    
    # Walk through all directories and files in the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.npy'):
                file_path = os.path.join(dirpath, filename)
                
                try:
                    # Load the numpy array from .npy file
                    array = np.load(file_path)
                except Exception as e:
                    print(f"Failed to load {file_path}: {e}")
                    continue
                
                # If first numpy array, record its shape
                if is_first:
                    first_shape = array.shape
                    is_first = False
                    print(f"Reference array shape {first_shape} found at {file_path}")
                
                # Compare the shape of the current array with the first array
                elif array.shape != first_shape:
                    print(f"Shape mismatch {array.shape} found at {file_path}")

def calculate_array_statistics(root_dir):
    """Calculate statistics for 3D numpy arrays stored in a directory tree."""
    stats = {
        'min': [],
        'max': [],
        'mean': [],
        'median': [],
        'std': []
    }
    
    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.npy'):  # Assuming the files are numpy arrays saved as .npy
                file_path = os.path.join(dirpath, filename)
                array = np.load(file_path)
                
                # Compute statistics for this array
                stats['min'].append(np.min(array))
                stats['max'].append(np.max(array))
                stats['mean'].append(np.mean(array))
                stats['median'].append(np.median(array))
                stats['std'].append(np.std(array))

    # Aggregate statistics
    overall_stats = {
        'min': np.min(stats['min']),
        'max': np.max(stats['max']),
        'global_mean': np.mean(stats['mean']),
        'global_median': np.median(stats['median']),
        'global_std': np.mean(stats['std'])
    }
    
    return overall_stats

# Clean input
# root_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/spectrogram-128-frames'

# Mixed input
root_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/spectrogram-256-frames'

# Output from model
# root_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/spectrogram-128-frames/english-horn/clarinet_A3_1_forte_normal'


# Check for shape consistency
traverse_and_compare_shapes(root_directory)

# Array statistics
array_stats = calculate_array_statistics(root_directory)

print("\nArray Statistics:")
for key, value in array_stats.items():
    print(f"{key.capitalize()}: {value}")

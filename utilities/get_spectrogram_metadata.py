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

# Clean
root_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/spectrogram-128-frames'

# Mixed
# root_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/spectrogram'

traverse_and_compare_shapes(root_directory)

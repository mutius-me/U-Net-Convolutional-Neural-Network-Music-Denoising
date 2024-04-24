import numpy as np
import os

def load_array_from_file(file_path):
    # Attempt to load the file if it exists
    if os.path.isfile(file_path):
        try:
            return np.load(file_path)
        except Exception as e:
            print(f"Failed to load the file: {e}")
            return None
    else:
        print("File does not exist.")
        return None

def pretty_print_ndarray(arr, second_dim):
    # Check if the second dimension is valid
    if second_dim not in (128, 256):
        print("Second dimension must be either 128 or 256.")
        return
    
    # Check the shape of the array
    if arr.shape[1] != second_dim or arr.shape[2] != 2:
        print(f"The array does not have the expected dimensions (1024x{second_dim}x2).")
        return
    
    max_slices = 10  # Maximum number of slices to display
    max_rows = 5     # Maximum number of rows per slice to display
    max_cols = 5     # Maximum number of columns per row to display
    
    for slice_index in range(min(max_slices, arr.shape[0])):
        print(f"Slice {slice_index}:")
        for row_index in range(min(max_rows, arr.shape[1])):
            row_str = ', '.join([f"{arr[slice_index, row_index, col_index]:.2f}" for col_index in range(min(max_cols, arr.shape[2]))])
            print(f"  Row {row_index}: [{row_str}]")
        print("\n")

# Example usage
if __name__ == "__main__":
    # file_path = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/spectrogram-128-frames/english-horn/clarinet_A3_025_fortissimo_normal/1_clarinet_A3_025_fortissimo_normal_mixed_denoised.npy'

    file_path = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/spectrogram-128-frames/flute/flute_As5_15_mezzo-piano_normal/1_flute_As5_15_mezzo-piano_normal.npy'

    second_dim = int(input("Enter the second dimension (128 or 256): "))
    
    spectrogram_array = load_array_from_file(file_path)
    if spectrogram_array is not None:
        pretty_print_ndarray(spectrogram_array, second_dim)

##############################################################################
# NAME: get_duration_metadata.py
# DESCRIPTION: A module with various functions to get metadata about duration
# in a dataset, including both MP3 and WAV file processing.
###############################################################################

import os
import numpy as np
import scipy.stats as stats

# For MP3 processing
from mutagen.mp3 import MP3

# For WAV processing
import wave

#######
# MP3 #
#######

def find_mp3_files_and_total_duration(start_path):
    """Find MP3 files and calculate their total duration."""
    total_duration = 0  # in seconds
    mp3_count = 0
    
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(".mp3"):
                mp3_count += 1
                try:
                    audio = MP3(os.path.join(root, file))
                    total_duration += audio.info.length
                except Exception as e:
                    print(f"Error processing file {file}: {e}")

    return mp3_count, total_duration

#######
# WAV #
#######

def calculate_wav_length(file_path):
    """Calculate the length of a WAV file in seconds."""
    with wave.open(file_path, 'r') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        length = frames / float(rate)
    return length

def find_wav_files(root_dir):
    """Find all WAV files in the directory tree."""
    wav_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.wav'):
                wav_files.append(os.path.join(root, file))
    return wav_files

def count_files_within_std_dev_ranges(lengths, mean_length, std_dev, num_std_devs=4):
    """Count files within each range of standard deviations from the mean."""
    counts = {}
    for i in range(1, num_std_devs + 1):
        lower_bound = mean_length - i * std_dev
        upper_bound = mean_length + i * std_dev
        count_within_range = sum(lower_bound < length <= upper_bound for length in lengths)
        counts[f"{i} SD"] = count_within_range
    return counts

def analyze_lengths(lengths, sd_count=4):
    """Calculate and display the percentages of files within ranges defined by standard deviations."""
    mean_length = np.mean(lengths)
    std_dev = np.std(lengths)
    max_length = np.max(lengths)
    min_length = np.min(lengths)
    range_length = max_length - min_length
    mode_length = stats.mode(lengths)
    total_files = len(lengths)

    print(f"Mean length: {mean_length:.2f} seconds")
    print(f"Standard deviation: {std_dev:.2f} seconds")
    print(f"Max length: {max_length:.2f} seconda")
    print(f"Min length: {min_length:.2f} seconds")
    print(f"Range: {range_length:.2f} seconds")
    print(f"Mode: {mode_length[0]:.2f} seconds, {mode_length[1]} instances")
    print(f"Total files: {total_files} files\n")

    # Count files more than 4 standard deviations below the mean (if any are > 0 seconds)
    min_length = mean_length - sd_count * std_dev
    if min_length > 0:
        below_n_std_dev_count = sum(length <= min_length for length in lengths)
        below_n_std_dev_percent = (below_n_std_dev_count / total_files) * 100
        print(f"% of files more than {sd_count} standard deviations below the mean (longer than {min_length:.2f} seconds): {below_n_std_dev_percent:.2f}%")
    else:
        min_length = 0

    # Process standard deviations below the mean, avoiding negative values and redundant ranges
    for i in range(sd_count):
        lower = max(mean_length - (i + 1) * std_dev, 0)
        upper = max(mean_length - i * std_dev, 0)
        if lower == upper == 0:
            continue
        count = sum(lower < length <= upper for length in lengths)
        percent = (count / total_files) * 100
        print(f"Files between {lower:.2f} and {(upper * (i + 1)):.2f} seconds ({-i - 1} standard deviation(s)): {percent:.2f}%")

    # Process standard deviations above the mean
    for i in range(sd_count):
        lower = mean_length + i * std_dev
        upper = mean_length + (i + 1) * std_dev
        count = sum(lower < length <= upper for length in lengths)
        percent = (count / total_files) * 100
        print(f"Files between {lower:.2f} and {upper:.2f} seconds ({i + 1} standard deviation(s)): {percent:.2f}%")

    # Count files more than 4 standard deviations above the mean
    above_n_std_dev_count = sum(length > mean_length + 4 * std_dev for length in lengths)
    above_n_std_dev_percent = (above_n_std_dev_count / total_files) * 100
    print(f"Files longer than {(mean_length + 4 * std_dev):.2f} seconds (>{sd_count} standard deviation(s)): {above_n_std_dev_percent:.2f}%")


def process_wav_files(root_dir):
    """Process WAV files to calculate and analyze their lengths, and calculate the total duration."""
    wav_files = find_wav_files(root_dir)
    lengths = [calculate_wav_length(file) for file in wav_files]
    total_duration = sum(lengths)  # Calculate the total duration of all WAV files

    # Print the total duration
    print(f"Total duration of all WAV files: {total_duration:.2f} seconds")
    
    # Proceed with analysis
    analyze_lengths(lengths)
    

if __name__ == "__main__":
    # Uncomment for WAV files processing
    # root_dir = "saxophone_Gs5_long_forte_major-trill.wav"  # Replace with the actual path
    root_dir = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/audio/'
    root_dir = '/Users/Leo/Developer/Local/senior-project/dataset/raw/data/philharmonia'

    process_wav_files(root_dir)

    
    # Example for MP3 files processing
    # path = '/path/to/your/music/directory'  # Replace with the actual path
    # count, duration = find_mp3_files_and_total_duration(path)
    # hours = duration // 3600
    # minutes = (duration % 3600) // 60
    # seconds = duration % 60
    # print(f"Total MP3 files: {count}")
    # print(f"Total duration: {int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds")

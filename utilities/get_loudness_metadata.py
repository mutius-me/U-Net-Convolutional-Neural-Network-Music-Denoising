##############################################################################
# NAME: get_loudness_metadata.py
# DESCRIPTION: A module used to get metadata about loudness in a dataset. Each
# sample is measured individually using RMS.
###############################################################################

import os
import librosa
import numpy as np

def calculate_rms(audio):
    """Calculate the RMS level of the audio in dB."""
    return 20 * np.log10(np.sqrt(np.mean(np.square(audio))))

def analyze_audio(directory, print_all_levels=False):
    rms_levels = []
    file_paths = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                audio, sr = librosa.load(file_path, sr=None, mono=True)
                rms = calculate_rms(audio)
                rms_levels.append(rms)
                file_paths.append(file_path)

    if rms_levels:
        average_rms = np.mean(rms_levels)
        std_dev_rms = np.std(rms_levels)
        min_rms = np.min(rms_levels)
        max_rms = np.max(rms_levels)

        print("RMS Level Analysis Report:")
        print(f"Average RMS: {average_rms:.2f} dB")
        print(f"Standard Deviation: {std_dev_rms:.2f} dB")
        print(f"Minimum RMS: {min_rms:.2f} dB")
        print(f"Maximum RMS: {max_rms:.2f} dB")

        if print_all_levels:
            print("\nDetailed RMS Levels by File:")
            for path, level in zip(file_paths, rms_levels):
                print(f"{path}: {level:.2f} dB")
    else:
        print("No .wav files found or processed.")


############
# ATTEMPT 1#
############
# Clean flute samples
# directory = '/Users/Leo/Developer/Local/senior-project/dataset/raw/philharmonia-wav/flute' 

# Unadulterated, non-animated ground loop noise from myNoise
# directory = '/Users/Leo/Developer/Local/senior-project/dataset/raw/noise-samples/not-animated/wav'

# ground loop injected into flute samples
# directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/pre-processed/'

############
# ATTEMPT 2#
############

# Clean flute samples
# directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio/flute' 


# Ground loop noise generated in SuperCollider
# directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/raw/sc3/'

# Pre-processed ground loop noise generated in SuperCollider
directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/pre-processed/sc3/'
directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/raw/sc3/'



#Attempt-2, -40db ground loop injected into flute sample
# directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio/flute'

analyze_audio(directory)



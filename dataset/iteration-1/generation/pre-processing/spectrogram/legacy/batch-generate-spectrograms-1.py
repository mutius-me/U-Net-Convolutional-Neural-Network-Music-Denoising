##############################################################################
# NAME: batch-generate-spectrograms.py
# DESCRIPTION: Batch generates spectrograms from an input directory and saves 
# them into an output directory. The directory tree is specified using 
# relative paths to ensure code portability. 
#
# #TODO: adjust this to the actual structure of the directory
# The script assumes the following directory structure:
# root
#   --> utilities
#      --> this script
#   --> dataset
#      --> clean
#         --> sounds
#         --> spectrograms
#      --> noisy
#         --> sounds
#         --> spectrograms
#

import librosa
import numpy as np
import os
import glob
import argparse


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # Adjust based on actual project structure

# DEFAULT_INPUT_PATH = os.path.join(BASE_DIR, "dataset") ##TODO adjust structure as needed
# DEFAULT_OUTPUT_PATH = os.path.join(BASE_DIR, "dataset") ##TODO adjust structure as needed


PLOT_FLAG = False
DEFAULT_SPECTROGRAM_TYPE = 'stft'

def create_spectrograms_from_directory(input_dir, output_dir, spectrogram_type=DEFAULT_SPECTROGRAM_TYPE):
    categories = ["CLEAN", "NOISY"]
    for category in categories:
        sound_dir = os.path.join(input_dir, category, "SOUNDS")
        spectrogram_dir = os.path.join(output_dir, category, "SPECTROGRAMS")
        os.makedirs(spectrogram_dir, exist_ok=True)

        # Supporting different audio file types
        supported_extensions = ['*.wav', '*.mp3', '*.flac', '*.ogg']  # Add or remove as needed ##TODO use only .wav
        for extension in supported_extensions:
            for file_path in glob.glob(os.path.join(sound_dir, extension)):
                if not os.path.isfile(file_path):
                    continue
                filename = os.path.basename(file_path)
                # Removing original extension and appending .npy
                output_filename = os.path.splitext(filename)[0] + '.npy'
                output_path = os.path.join(spectrogram_dir, output_filename)

                y, sr = librosa.load(file_path, sr=None)
                if spectrogram_type == 'mel':
                    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
                    S_dB = librosa.power_to_db(S, ref=np.max)
                else:  # Default to 'stft'
                    S = librosa.stft(y)
                    S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)

                np.save(output_path, S_dB)  # Save spectrogram data as numpy array

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Batch processing for dataset creation: Spectrogram generation.')
    parser.add_argument('-c', '--config', type=str, help='Path to the config txt file specifying input/output directories.')

    args = parser.parse_args()

    if args.config:
        # Correctly adjusting the path to the config file based on script location
        config_path = os.path.join(SCRIPT_DIR, args.config)
        with open(config_path, 'r') as file:
            lines = file.readlines()
            input_path = os.path.abspath(os.path.join(BASE_DIR, lines[0].strip()))
            output_path = os.path.abspath(os.path.join(BASE_DIR, lines[1].strip()))
    else:
        input_path = DEFAULT_INPUT_PATH
        output_path = DEFAULT_OUTPUT_PATH

    create_spectrograms_from_directory(input_path, output_path, spectrogram_type=DEFAULT_SPECTROGRAM_TYPE)

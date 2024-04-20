import librosa
import numpy as np
import os
import argparse

def generate_spectrogram(file_path, output_path, spectrogram_type='stft'):
    y, sr = librosa.load(file_path, sr=None)
    if spectrogram_type == 'mel':
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_dB = librosa.power_to_db(S, ref=np.max)
    elif spectrogram_type == 'stft':
        S = librosa.stft(y)
        S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    else:
        raise ValueError("Unsupported spectrogram type:", spectrogram_type)
    np.save(output_path, S_dB)  # Save spectrogram data as numpy array

def process_directory(input_dir, output_dir, spectrogram_type='stft'):
    for root, dirs, files in os.walk(input_dir):
        # Determine the equivalent output directory
        rel_path = os.path.relpath(root, input_dir)
        current_output_dir = os.path.join(output_dir, rel_path)
        os.makedirs(current_output_dir, exist_ok=True)

        for file in files:
            if file.endswith(('.wav', '.mp3', '.flac', '.ogg')):
                file_path = os.path.join(root, file)
                output_filename = os.path.splitext(file)[0] + '.npy'
                output_path = os.path.join(current_output_dir, output_filename)
                generate_spectrogram(file_path, output_path, spectrogram_type)


# Clean
# INPUT_DIR = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented'
# OUTPUT_DIR = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/spectrogram'

# Mixed
INPUT_DIR = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio-segmented'
OUTPUT_DIR = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/spectrogram'

process_directory(INPUT_DIR, OUTPUT_DIR, "stft")

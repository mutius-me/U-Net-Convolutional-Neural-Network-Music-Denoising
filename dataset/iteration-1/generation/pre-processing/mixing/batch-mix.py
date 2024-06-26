##############################################################################
# NAME: batch-mix.py
# DESCRIPTION: This module is used to combine pre-generated noise with clean
# audio to generate noisy audio for model training. It mixes in batch, meaning
# that it traverses the clean audio directory and generates an output 'mixed'
# directory with a mirrored file structure to the original source directory.
# Noise samples are picked at random from random points from the noise
# directory.
###############################################################################

import os
import numpy as np
import librosa
import soundfile as sf
import random

## TODO: To make this code more versatile, I need to have a global file for the iteration that stores:
## TODO:  - Sample rates; bit-depth; 

def mix_audio(clean_file_path, noise_dir, output_dir, mixing_ratio=0.75):
    # Load the clean audio file
    clean_audio, sr = librosa.load(clean_file_path, sr=None) # defaults to 32float depth
    clean_length = clean_audio.shape[0]

    # Randomly select a noise file
    noise_files = [f for f in os.listdir(noise_dir) if f.endswith('.wav')]
    selected_noise_file = random.choice(noise_files)
    noise_path = os.path.join(noise_dir, selected_noise_file)

    # Load the noise audio file
    noise_audio, _ = librosa.load(noise_path, sr=sr)

    # Ensure noise audio matches the length of the clean audio
    if len(noise_audio) < clean_length:
        repeats = int(np.ceil(clean_length / len(noise_audio)))
        noise_audio = np.tile(noise_audio, repeats)[:clean_length]
    else:
        start_point = random.randint(0, len(noise_audio) - clean_length)
        noise_audio = noise_audio[start_point:start_point + clean_length]

    # Mix the audio files
    mixed_audio = mixing_ratio * clean_audio + (1 - mixing_ratio) * noise_audio
    # mixed_audio = mixed_audio / np.max(np.abs(mixed_audio))  # Normalize

    # Save the mixed audio file
    base_clean_filename = os.path.basename(clean_file_path)
    output_file_path = os.path.join(output_dir, f"{os.path.splitext(base_clean_filename)[0]}{os.path.splitext(base_clean_filename)[1]}")
    sf.write(output_file_path, mixed_audio, sr, format='WAV', subtype='FLOAT')

def process_directory(clean_dir, noise_dir, output_dir):
    # Traverse the directory tree
    for root, dirs, files in os.walk(clean_dir):
        for file in files:
            if file.endswith('.wav'):
                clean_file_path = os.path.join(root, file)
                mix_audio(clean_file_path, noise_dir, output_dir)

# Example usage
clean_dir = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio'
noise_dir = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/pre-processed/sc3'

output_dir = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio'

instruments = ['flute', 'oboe', 'clarinet', 'saxophone', 'cor anglais']
total_instrument_count = len(instruments)

for i, instrument in enumerate(instruments, start=1):
    ith_clean_dir = clean_dir + '/' + instrument
    ith_output_dir = output_dir + '/' + instrument

    # Check if the output directory exists, if not, create it
    if not os.path.exists(ith_output_dir):
        os.makedirs(ith_output_dir)


    process_directory(ith_clean_dir, noise_dir, ith_output_dir)
    print(f"Completed mixing for {instrument}; {i}/{total_instrument_count} completed.")

print("Batch mixing completed.")
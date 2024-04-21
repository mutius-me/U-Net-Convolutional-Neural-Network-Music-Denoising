##############################################################################
# NAME: batch_compare_original_and_reconstructed_audio.py
# DESCRIPTION: This module can be executed directly from the terminal. It
# takes in two directories, and outputs the SNR (Signal-to-Noise) ratio 
# of all identically-named files in both directories. It is useful for
# verifying  where noise may be introduced throughout the data generation 
# pipeline (e.g. converting audio to and from spectrograms).
###############################################################################

import librosa
import numpy as np
import os
import soundfile as sf


def calculate_snr(original, reconstructed):
    """Calculate the Signal-to-Noise Ratio (SNR) between the original and reconstructed signals."""
    min_len = min(len(original), len(reconstructed))
    original = original[:min_len]
    reconstructed = reconstructed[:min_len]
    
    signal_power = np.sum(original**2)
    noise_power = np.sum((original - reconstructed)**2)
    snr = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
    return snr


def compare_directories(original_dir, reconstructed_dir):
    """Compare audio files in two directories and calculate SNR for each pair."""
    snr_results = []
    for root, dirs, files in os.walk(original_dir):
        # Find the corresponding directory in the reconstructed directory
        rel_path = os.path.relpath(root, original_dir)
        corresponding_dir = os.path.join(reconstructed_dir, rel_path)

        for file in files:
            if file.endswith(('.wav', '.mp3', '.flac', '.ogg')):
                original_path = os.path.join(root, file)
                reconstructed_path = os.path.join(corresponding_dir, file)
                
                if os.path.exists(reconstructed_path):
                    # Load audio files
                    original_audio, sr_orig = librosa.load(original_path, sr=None, mono=True, duration=2)
                    reconstructed_audio, sr_recon = librosa.load(reconstructed_path, sr=None, mono=True, duration=2)
                    
                    # Calculate SNR
                    snr = calculate_snr(original_audio, reconstructed_audio)
                    snr_results.append((original_path, reconstructed_path, snr))
                    print(f"SNR for {original_path} and {reconstructed_path}: {snr:.2f} dB")
                else:
                    print(f"Reconstructed file {reconstructed_path} does not exist.")

    return snr_results

if __name__ == "__main__":
    # Comparing original with one-off testing reconstruction
    original_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented/clarinet/clarinet_A3_1_forte_normal/'
    reconstructed_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/audio'

    # Comparing original with batch'd reconstruction
    # original_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented/clarinet/clarinet_A3_1_forte_normal/'
    # reconstructed_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/test-128-frames-reconstructed/clarinet/clarinet_A3_1_forte_normal/'


    # Comparing the two reconstructions --> inf dB
    # original_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/audio'
    # reconstructed_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/test-128-frames-reconstructed/clarinet/clarinet_A3_1_forte_normal/'

    # Run the comparison
    results = compare_directories(original_directory, reconstructed_directory)
    print("Comparison complete.")

    # debug_audio_properties(original_audio, "Original Audio")
    # debug_audio_properties(reconstructed_audio, "Reconstructed Audio")

##############################################################################
# NAME: ompare_original_and_reconstructed_audio.py
# DESCRIPTION: This module can be executed directly from the terminal. It
# takes in two file path, and outputs the SNR (Signal-to-Noise) ratio 
# of the two files. It is useful for verifying  where noise may be introduced
# throughout the data generation  pipeline (e.g. converting audio to and from 
# spectrograms).
###############################################################################

import librosa
import numpy as np
import soundfile as sf

def load_audio(file_path):
    """Load a mono audio clip at its original sample rate."""
    audio, sr = librosa.load(file_path, sr=None, mono=True)
    return audio, sr

def calculate_snr(original, reconstructed):
    """Calculate the Signal-to-Noise Ratio (SNR) between the original and reconstructed signals."""
    min_len = min(len(original), len(reconstructed))
    original = original[:min_len]
    reconstructed = reconstructed[:min_len]
    
    signal_power = np.sum(original ** 2)
    noise_power = np.sum((original - reconstructed) ** 2)
    if noise_power == 0:
        return float('inf')  # Avoid division by zero
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

def compare_snr(file_path1, file_path2):
    """Compare two audio files and calculate their SNR."""
    # Load audio files
    audio1, sr1 = load_audio(file_path1)
    audio2, sr2 = load_audio(file_path2)

    # Resample if necessary to ensure same sample rate
    if sr1 != sr2:
        higher_sr = max(sr1, sr2)
        if sr1 != higher_sr:
            audio1 = librosa.resample(audio1, orig_sr=sr1, target_sr=higher_sr)
        else:
            audio2 = librosa.resample(audio2, orig_sr=sr2, target_sr=higher_sr)

    # Calculate SNR
    snr = calculate_snr(audio1, audio2)
    print(f"SNR between {file_path1} and {file_path2}: {snr:.2f} dB")

# Original and one-off test script
# file_path1 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented/clarinet/clarinet_A3_1_forte_normal/1_clarinet_A3_1_forte_normal.wav'
# file_path2 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/audio/1_clarinet_A3_1_forte_normal.wav'

# One-off test script and batch generated
file_path1 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/audio/1_clarinet_A3_1_forte_normal.wav'
file_path2 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/test-128-frames-reconstructed/clarinet/clarinet_A3_1_forte_normal/1_clarinet_A3_1_forte_normal.wav'

compare_snr(file_path1, file_path2)

import librosa
import numpy as np
import soundfile as sf

def load_audio(file_path, duration=2.0):
    """Load a 2-second mono audio clip."""
    audio, sr = librosa.load(file_path, sr=None, mono=True, duration=duration)
    return audio, sr

def compute_and_save_spectrogram(audio, sr, output_path, fft_size=2048, hop_length=512):
    """Compute the STFT of the audio, separate it into magnitude and phase, and save as a 3D array."""
    S = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length)
    magnitude = np.abs(S)
    phase = np.angle(S)
    spectrogram_3d = np.stack((magnitude, phase), axis=-1)  # Stack magnitude and phase as separate channels
    np.save(output_path, spectrogram_3d)  # Save the 3D spectrogram array to disk
    return sr

def load_spectrogram(input_path):
    """Load a 3D spectrogram array from disk."""
    spectrogram_3d = np.load(input_path)
    magnitude = spectrogram_3d[..., 0]  # First channel is magnitude
    phase = spectrogram_3d[..., 1]  # Second channel is phase
    return magnitude, phase

def reconstruct_spectrogram_and_save(magnitude, phase, sr, file_path, original_length):
    """Reconstruct the complex spectrogram from magnitude and phase, ensuring it matches the original length, and save the audio."""
    S_reconstructed = magnitude * np.exp(1j * phase)
    audio_reconstructed = librosa.istft(S_reconstructed, length=original_length)
    sf.write(file_path, audio_reconstructed, sr)
    return audio_reconstructed

def calculate_snr(original, reconstructed):
    """Calculate the Signal-to-Noise Ratio (SNR) between the original and reconstructed signals."""
    # Ensure same length for fair comparison
    min_len = min(len(original), len(reconstructed))
    original = original[:min_len]
    reconstructed = reconstructed[:min_len]
    
    noise = original - reconstructed
    signal_power = np.sum(original ** 2)
    noise_power = np.sum(noise ** 2)
    snr = 10 * np.log10(signal_power / noise_power)
    return snr

# File paths
input_file = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio/oboe/oboe_As4_1_piano_normal.wav'  
spectrogram_file = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/spectrogram/spectrogram.npy'  # Path to save/load the spectrogram
output_file =  '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/audio/reconstructed_audio.wav'

# Main processing
audio, sr = load_audio(input_file)
original_length = len(audio)  # Save original length for reconstruction
compute_and_save_spectrogram(audio, sr, spectrogram_file)
magnitude, phase = load_spectrogram(spectrogram_file)
audio_reconstructed = reconstruct_spectrogram_and_save(magnitude, phase, sr, output_file, original_length)

# Calculate SNR
snr = calculate_snr(audio, audio_reconstructed)
print("Processing complete. Reconstructed audio saved to:", output_file)
print("Signal-to-Noise Ratio (SNR):", snr, "dB")

import librosa
import numpy as np
import soundfile as sf

def load_audio(file_path, duration=2):
    """Load a 2-second mono audio clip."""
    audio, sr = librosa.load(file_path, sr=None, mono=True, duration=duration)
    return audio, sr

def compute_and_save_spectrogram(audio, sr, output_path, fft_size=2048, hop_length=345):
    """Compute the STFT of the audio, separate it into magnitude and phase, and save as a 3D array."""
    S = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length)
    magnitude = np.abs(S)
    phase = np.angle(S)
    spectrogram_3d = np.stack((magnitude, phase), axis=-1)  # Stack magnitude and phase as separate channels
    np.save(output_path, spectrogram_3d)  # Save the 3D spectrogram array to disk
    return sr

def load_spectrogram(input_path, print_shape=True):
    """Load a 3D spectrogram array from disk."""
    spectrogram_3d = np.load(input_path)
    if print_shape:
        print(np.shape(spectrogram_3d))
    magnitude = spectrogram_3d[..., 0]  # First channel is magnitude
    phase = spectrogram_3d[..., 1]  # Second channel is phase
    return magnitude, phase

def reconstruct_spectrogram_and_save(magnitude, phase, sr, file_path, original_length):
    """Reconstruct the complex spectrogram from magnitude and phase, ensuring it matches the original length, and save the audio."""
    S_reconstructed = magnitude * np.exp(1j * phase)
    audio_reconstructed = librosa.istft(S_reconstructed, length=original_length, hop_length=345)
    # sf.write(file_path, audio_reconstructed, sr) #! Without the format and subtype arguments, this line was degrading audio quality.
    sf.write(file_path, audio_reconstructed, sr, format='WAV', subtype='FLOAT')

    return audio_reconstructed

def calculate_snr(original, reconstructed):
    """Calculate the Signal-to-Noise Ratio (SNR) between the original and reconstructed signals."""
    min_len = min(len(original), len(reconstructed))
    original = original[:min_len]
    reconstructed = reconstructed[:min_len]
    
    signal_power = np.sum(original**2)
    noise_power = np.sum((original - reconstructed)**2)
    snr = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
    return snr

# File paths
# input_file = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio/oboe/oboe_As4_1_piano_normal.wav'  
input_file = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented/clarinet/clarinet_A3_1_forte_normal/1_clarinet_A3_1_forte_normal.wav'
spectrogram_file = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/spectrogram/spectrogram.npy'  # Path to save/load the spectrogram
output_file =  '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing/spectrogram/testing/3-channel/audio/reconstructed_audio.wav'

# Main processing
audio, sr = load_audio(input_file)
original_length = len(audio)  # Save original length for reconstruction
compute_and_save_spectrogram(audio, sr, spectrogram_file)
magnitude, phase = load_spectrogram(spectrogram_file)
audio_reconstructed = reconstruct_spectrogram_and_save(magnitude, phase, sr, output_file, original_length)

# Calculate SNR between original audio file and the reconstruction from the spectrogram
snr = calculate_snr(audio, audio_reconstructed)
print("Processing complete. Reconstructed audio saved to:", output_file)
print("Signal-to-Noise Ratio (SNR) between original and reconstruction:", snr, "dB")


# ! Debugging
# def debug_audio_properties(audio, label="Audio"):
#     """Prints out properties of the audio array to help with debugging."""
#     print(f"{label}: Length = {len(audio)}, Max = {np.max(audio)}, Min = {np.min(audio)}, Mean = {np.mean(audio)}")

# debug_audio_properties(audio, "Original Audio")
# debug_audio_properties(audio_reconstructed, "Reconstructed Audio")


print("\n~~DEBUGGING~~\n")
# This part of the code c

def load_audio(file_path):
    """Load a mono audio clip at its original sample rate."""
    audio, sr = librosa.load(file_path, sr=None, mono=True, duration=2, dtype=np.float32)
    return audio, sr


reconstructed_audio_2, sr = load_audio(output_file)
snr = calculate_snr(audio_reconstructed, reconstructed_audio_2)
print("Signal-to-Noise Ratio (SNR) between original and reconstruction *saved to disk*:", snr, "dB")




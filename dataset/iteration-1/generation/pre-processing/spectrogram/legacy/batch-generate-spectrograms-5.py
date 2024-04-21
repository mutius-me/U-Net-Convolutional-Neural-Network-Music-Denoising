import librosa
import numpy as np
import os
import soundfile as sf
import math

def process_audio_file(input_path, output_path, fft_size=2048, target_frames=256, sr=44100):
    """Process an individual audio file to compute and save its spectrogram."""

    # Load audio file with fixed sample rate of 44100 Hz
    audio, _ = librosa.load(input_path, sr=sr, mono=True)
    num_samples = len(audio)

    # Calculate hop length to get exactly the target number of frames
    hop_length = num_samples // target_frames
    while math.ceil(num_samples / hop_length) > target_frames:
        hop_length += 1

    # Save global variable to print
    print(f"Hop length: {hop_length}")

    # Perform STFT
    S = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length)

    # Get magnitude and phase, discard the Nyquist bin to have exactly 1024 bins
    magnitude = np.abs(S[:-1])
    phase = np.angle(S[:-1])

    # Stack magnitude and phase as separate channels
    spectrogram_3d = np.stack((magnitude, phase), axis=-1)
    np.save(output_path, spectrogram_3d)  # Save the 3D spectrogram array to disk

def process_directory_tree(input_dir, output_dir, target_frames=256):
    """Traverse the directory tree and process each audio file found."""
    for root, dirs, files in os.walk(input_dir):
        # Determine the equivalent output directory
        rel_path = os.path.relpath(root, input_dir)
        current_output_dir = os.path.join(output_dir, rel_path)
        os.makedirs(current_output_dir, exist_ok=True)

        for file in files:
            if file.endswith(('.wav', '.mp3', '.flac', '.ogg')):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(current_output_dir, os.path.splitext(file)[0] + '.npy')
                process_audio_file(input_file_path, output_file_path, target_frames=target_frames)
                print(f"Processed {input_file_path} to {output_file_path}")

# Define input and output directories
input_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented'
output_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/test-128-frames'

# Example usage for different target frames
target_frames = 128 
process_directory_tree(input_directory, output_directory, target_frames=target_frames)
print("Batch processing complete.")

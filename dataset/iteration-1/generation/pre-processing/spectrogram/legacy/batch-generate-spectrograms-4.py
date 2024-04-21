# This script is used to batch-generate spectrograms that output very specific spectrogram sizes: 1024x256x2.

import librosa
import numpy as np
import os
import soundfile as sf

def process_audio_file(input_path, output_path, fft_size=2048, target_frames=256):
    """Process an individual audio file to compute and save its spectrogram with adjusted bins and frames."""
    # Load audio file
    audio, sr = librosa.load(input_path, sr=None, mono=True)
    num_samples = len(audio)

    # Calculate appropriate hop length to achieve the desired number of time frames
    hop_length = max(1, int((num_samples - fft_size) / (target_frames - 1)))

    # Perform STFT
    S = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length)

    # Calculate magnitude and phase
    magnitude = np.abs(S)
    phase = np.angle(S)

    # Merge the last two bins to make sure we have exactly 1024 frequency bins
    magnitude[-2] += magnitude[-1]  # Merge magnitude of the last two bins
    phase[-2] = (phase[-2] + phase[-1]) / 2  # Average phase of the last two bins

    # Discard the last bin to get exactly 1024 bins
    magnitude = magnitude[:-1]
    phase = phase[:-1]

    # Verify the size and reshape if necessary (especially if the audio is not exactly 2 seconds)
    if magnitude.shape[1] != target_frames:
        # Pad or trim to the required number of frames
        magnitude = magnitude[:, :target_frames] if magnitude.shape[1] > target_frames else np.pad(magnitude, ((0,0), (0, target_frames - magnitude.shape[1])), 'constant')
        phase = phase[:, :target_frames] if phase.shape[1] > target_frames else np.pad(phase, ((0,0), (0, target_frames - phase.shape[1])), 'constant')

    # Stack magnitude and phase as separate channels
    spectrogram_3d = np.stack((magnitude, phase), axis=-1)
    np.save(output_path, spectrogram_3d)  # Save the 3D spectrogram array to disk

def process_directory_tree(input_dir, output_dir):
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
                process_audio_file(input_file_path, output_file_path)
                print(f"Processed {input_file_path} to {output_file_path}")

# Define input and output directories
input_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented'  # Change to your input directory path
output_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/test'  # Change to your output directory path

# Run the processing
process_directory_tree(input_directory, output_directory)
print("Batch processing complete.")

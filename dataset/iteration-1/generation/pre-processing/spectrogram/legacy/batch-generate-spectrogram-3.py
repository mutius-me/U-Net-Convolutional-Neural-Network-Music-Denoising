import librosa
import numpy as np
import os
import soundfile as sf

def process_audio_file(input_path, output_path, fft_size=2048, hop_length=512):
    """Process an individual audio file to compute and save its spectrogram."""
    audio, sr = librosa.load(input_path, sr=None, mono=True)
    S = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length)
    magnitude = np.abs(S)
    phase = np.angle(S)
    spectrogram_3d = np.stack((magnitude, phase), axis=-1)  # Stack magnitude and phase as separate channels
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
input_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented'
output_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/spectrogram'  

# Run the processing
process_directory_tree(input_directory, output_directory)
print("Batch processing complete.")

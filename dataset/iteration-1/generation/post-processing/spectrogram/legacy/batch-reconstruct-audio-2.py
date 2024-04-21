import librosa
import numpy as np
import os
import soundfile as sf

def reconstruct_audio_from_spectrogram(input_path, output_path, sr=44100, hop_length=512):
    """Reconstruct an audio signal from a 3D numpy spectrogram array and save it."""
    spectrogram_3d = np.load(input_path)
    magnitude = spectrogram_3d[..., 0]
    phase = spectrogram_3d[..., 1]
    S_reconstructed = magnitude * np.exp(1j * phase)
    audio_reconstructed = librosa.istft(S_reconstructed, hop_length=hop_length, length=None)
    sf.write(output_path, audio_reconstructed, sr)


def reconstruct_directory_tree(input_dir, output_dir, hop_length):
    """Traverse the directory tree and reconstruct audio from each numpy array found."""
    for root, dirs, files in os.walk(input_dir):
        # Determine the equivalent output directory
        rel_path = os.path.relpath(root, input_dir)
        current_output_dir = os.path.join(output_dir, rel_path)
        os.makedirs(current_output_dir, exist_ok=True)

        for file in files:
            if file.endswith('.npy'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(current_output_dir, os.path.splitext(file)[0] + '.wav')
                reconstruct_audio_from_spectrogram(input_file_path, output_file_path, hop_length=hop_length)
                print(f"Reconstructed audio from {input_file_path} to {output_file_path}")

# Mixed
# input_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/spectrogram'  
# output_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/audio-segmented' 


# Clean — TESTING PURPOSES ONLY
input_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/test-256-frames'  
output_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/test-256-frames-reconstructed' 

# Run the reconstruction
# reconstruct_directory_tree(input_directory, output_directory)
reconstruct_directory_tree(input_directory, output_directory, hop_length=690)
print("Batch reconstruction complete.")

import librosa
import numpy as np
import os
import soundfile as sf
import math

SAMPLE_RATE = 44100 # All audio files currently utilize a sample rate of 44100.
DURATION = 2.0 # All audio files are currently 2 seconds in lenght.

def reconstruct_audio_from_spectrogram(input_path, output_path, hop_length, sr=44100,):
    """Reconstruct an audio signal from a 3D numpy spectrogram array and save it."""
    spectrogram_3d = np.load(input_path)
    magnitude = spectrogram_3d[..., 0]
    phase = spectrogram_3d[..., 1]
    S_reconstructed = magnitude * np.exp(1j * phase)
    audio_reconstructed = librosa.istft(S_reconstructed, hop_length=hop_length) # ? Is this call to librosa.istft() missing length=2.0 arg? Could this be degrading the quality?
    sf.write(output_path, audio_reconstructed, sr, format='WAV', subtype='FLOAT') # ! Do a test with a small batch of these to check that this script is not lossy.

def reconstruct_directory_tree(input_dir, output_dir, hop_length):
    """Traverse the directory tree and reconstruct audio from each numpy array found."""
    for root, dirs, files in os.walk(input_dir):
        current_output_dir = os.path.join(output_dir, os.path.relpath(root, input_dir))
        os.makedirs(current_output_dir, exist_ok=True)
        for file in files:
            if file.endswith('.npy'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(current_output_dir, os.path.splitext(file)[0] + '.wav')
                reconstruct_audio_from_spectrogram(input_file_path, output_file_path, hop_length)
                print(f"Reconstructed audio from {input_file_path} to {output_file_path}")

#*#######################
#* SELECT TARGET FRAMES #
#*#######################

#* Select target frames before running——this will determine the magnitude of the second dimension of the outputted n-dimensional array
target_frames = 256

input_directory = f'/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/spectrogram-{target_frames}-frames' 
output_directory = f'/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/audio-segmented-{target_frames}-frames' 

total_sample_count = SAMPLE_RATE * DURATION

hop_length = total_sample_count // target_frames
while math.ceil(total_sample_count / hop_length) > target_frames:
    hop_length += 1

hop_length = int(hop_length)

print(f"This is a script to batch reconstruct audio from spectrogram input.")
print(f"Sample Rate: {SAMPLE_RATE}\nDuration: {DURATION} seconds")
print(f"Target Frames: {target_frames}\nHop length: {hop_length}\nPress anything to continue.")
input()

reconstruct_directory_tree(input_directory, output_directory, hop_length=hop_length)

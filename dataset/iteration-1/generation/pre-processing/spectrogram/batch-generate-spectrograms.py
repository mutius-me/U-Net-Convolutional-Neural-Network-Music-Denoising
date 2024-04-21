import librosa
import numpy as np
import os
import soundfile as sf
import math

SAMPLE_RATE = 44100 # All audio files currently utilize a sample rate of 44100.
DURATION = 2.0 # All audio files are currently 2 seconds in lenght.

def process_audio_file(input_path, output_path, fft_size=2048, hop_length=512):
    """Process an individual audio file to compute and save its spectrogram."""
    # Load a 2-second audio clip at a fixed sample rate of 44100 Hz
    audio, sr = librosa.load(input_path, sr=SAMPLE_RATE, mono=True, duration=DURATION)
    # Perform STFT
    S = librosa.stft(audio, n_fft=fft_size, hop_length=hop_length)
    # Trim topmost frequency bin, responsible for 20k+ Hertz range, in order to have a dim. of 1024
    S = S[:-1, :]
    magnitude = np.abs(S)
    phase = np.angle(S)
    spectrogram_3d = np.stack((magnitude, phase), axis=-1)
    np.save(output_path, spectrogram_3d)  # Save the 3D spectrogram array to disk

def process_directory_tree(input_dir, output_dir, fft_size=2048, hop_length=512):
    """Traverse the directory tree and process each audio file found."""
    for root, dirs, files in os.walk(input_dir):
        current_output_dir = os.path.join(output_dir, os.path.relpath(root, input_dir))
        os.makedirs(current_output_dir, exist_ok=True)
        for file in files:
            if file.lower().endswith(('.wav', '.mp3', '.flac', '.ogg')):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(current_output_dir, os.path.splitext(file)[0] + '.npy')
                process_audio_file(input_file_path, output_file_path, fft_size=fft_size, hop_length=hop_length)
                print(f"Processed {input_file_path} to {output_file_path}")



#*#######################
#* SELECT TARGET FRAMES #
#*#######################

#* Select target frames before running——this will determine the magnitude of the second dimension of the outputted n-dimensional array
target_frames = 256

# Example usage
input_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented'
output_directory = f'/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/spectrogram-{target_frames}-frames'

total_sample_count = SAMPLE_RATE * DURATION

hop_length = total_sample_count // target_frames
while math.ceil(total_sample_count / hop_length) > target_frames:
    hop_length += 1

hop_length = int(hop_length)

print(f"This is a script to batch generate spectrograms from audio input.")
print(f"Sample Rate: {SAMPLE_RATE}\nDuration: {DURATION} seconds")
print(f"Target Frames: {target_frames}\nHop length: {hop_length}\nPress anything to continue.")
input()

process_directory_tree(input_directory, output_directory, hop_length=hop_length)

print("Batch processing completed.")
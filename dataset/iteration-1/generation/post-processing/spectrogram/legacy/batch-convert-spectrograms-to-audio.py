import os
import numpy as np
import librosa
import soundfile as sf
import argparse


# Sample Rate 
##TODO: ensure there is a global sample rate stored at the root direction of each iteration, from which this sample rate can be "pulled"
# temporarily hardcoded
SAMPLE_RATE = 44100


import os
import numpy as np
import librosa
import soundfile as sf

# Correctly setting sample rate
SAMPLE_RATE = 44100

def convert_spectrogram_to_audio(S_array):
    """
    Converts an STFT spectrogram back to a stereo audio signal, assuming S_array is a 2D array for a single channel.
    """
    if S_array.ndim != 2:
        print("Error: Expected a 2D array for the spectrogram, got shape", S_array.shape)
        return None  # Return None to indicate an error in processing

    # librosa.istft expects a 2D array; we assume S_array is already in the correct form
    audio = librosa.istft(S_array)
    return audio

def save_audio_to_disk(audio, sr, file_path):
    sf.write(file_path, audio.T, sr)

def reconstruct_audio_from_spectrogram(source_dir, target_dir, sample_rate):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.npy'):
                spectrogram_path = os.path.join(root, file)
                audio_save_path = os.path.join(target_dir, os.path.relpath(root, source_dir), file[:-4] + '.wav')
                
                S_array = np.load(spectrogram_path)
                # print("Loaded spectrogram path:", spectrogram_path)  # Diagnostic print
                # print("Immediately after loading - Spectrogram shape:", S_array.shape)  # Diagnostic print

                audio = convert_spectrogram_to_audio(S_array)
                if audio is None:  # Check if conversion was successful
                    print("Conversion failed for", spectrogram_path)
                    continue

                # Ensure the target directory exists
                os.makedirs(os.path.dirname(audio_save_path), exist_ok=True)
                
                # Save the audio file to disk
                save_audio_to_disk(audio, sample_rate, audio_save_path)





# Clean
source_dir = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/spectrogram'
target_dir = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/test'

# Mixed


reconstruct_audio_from_spectrogram(source_dir, target_dir, SAMPLE_RATE)

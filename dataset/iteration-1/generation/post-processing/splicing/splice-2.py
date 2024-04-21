##############################################################################
# NAME: splice-2.py
# DESCRIPTION: This is the 2nd iteration of the splice.py module. It leverages
# librosa to splice together audio files. It is intended to be used after the
# spectrograms outputted by the model have been converted to (segmented)
# audio, which needs to be spliced to its original length.
###############################################################################

import librosa
import soundfile as sf
import numpy as np
import os

def load_audio(file_path):
    """Load an audio file as a floating point time series."""
    audio, sr = librosa.load(file_path, sr=None, dtype='float32')
    return audio, sr

def save_audio(audio, file_path, sr):
    """Save the audio file from a floating point time series."""
    sf.write(file_path, audio, sr, format='WAV', subtype='FLOAT')

def splice_segments_in_directory(source_dir, target_dir):
    """Splice all audio segments in a directory into one audio file."""
    for root, dirs, files in os.walk(source_dir):
        if not dirs:  # This means 'root' is a leaf directory
            sorted_files = sorted(files, key=lambda x: int(x.split('_')[0]))
            full_audio = None
            sample_rate = None

            for file in sorted_files:
                file_path = os.path.join(root, file)
                audio, sr = load_audio(file_path)
                
                if full_audio is None:
                    full_audio = audio
                    sample_rate = sr
                else:
                    # Ensure all files have the same sample rate
                    if sr != sample_rate:
                        raise ValueError("Sample rates do not match. Ensure all audio files have the same sample rate.")
                    full_audio = np.concatenate((full_audio, audio))

            # Calculate the correct target path
            relative_path = os.path.relpath(root, source_dir)
            target_file_dir = os.path.join(target_dir, os.path.dirname(relative_path))
            os.makedirs(target_file_dir, exist_ok=True)
            
            # The filename is based on the directory name
            output_file_name = f"{os.path.basename(root)}.wav"
            output_file_path = os.path.join(target_file_dir, output_file_name)
            save_audio(full_audio, output_file_path, sample_rate)

            # Optional: Delete the processed subdirectory
            # shutil.rmtree(root)

def reverse_process_directory(source_dir, target_dir):
    splice_segments_in_directory(source_dir, target_dir)

#TODO: Update directory paths
source_directory = '/path/to/source/directory'
target_directory = '/path/to/target/directory'

reverse_process_directory(source_directory, target_directory)

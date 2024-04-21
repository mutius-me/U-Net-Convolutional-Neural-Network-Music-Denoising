##############################################################################
# NAME: attenuate-.py
# DESCRIPTION: This module takes in a directory, and attenuates all of the 
# soundfiles in it to a pre-determined dB level. This script is used as part 
# of the treatment of the noise generated in SuperCollider, which is later
# mixed in with clean audio to generate the noise-added audio.
###############################################################################

import os
import librosa
import soundfile as sf
import numpy as np

def calculate_rms(audio):
    """Calculate the RMS level of the audio in dB."""
    return 20 * np.log10(np.sqrt(np.mean(np.square(audio))))

def attenuate_audio_to_target_rms(audio, current_rms, target_rms):
    """Attenuate the audio to the target RMS level."""
    required_db_change = target_rms - current_rms
    factor = 10 ** (required_db_change / 20)
    return audio * factor

def process_directory(source_dir, target_dir, target_rms):
    """Process all WAV files in the source directory and save them to the target directory."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)  # Create target directory if it doesn't exist

    for subdir, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.wav'):
                source_path = os.path.join(subdir, file)
                target_path = os.path.join(target_dir, os.path.relpath(source_path, source_dir))

                # Ensure the target subdirectory exists
                os.makedirs(os.path.dirname(target_path), exist_ok=True)

                audio, sr = librosa.load(source_path, sr=None, mono=True)
                current_rms_db = calculate_rms(audio)
                adjusted_audio = attenuate_audio_to_target_rms(audio, current_rms_db, target_rms)
                
                # Save the adjusted audio
                sf.write(target_path, adjusted_audio, sr, format='WAV', subtype='FLOAT')
                print(f"Processed and saved: {target_path}")

# Example usage
source_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/raw/sc3' #TODO: convert to relative path
target_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/pre-processed/sc3'
target_db = -30.0  # Target RMS dB level

process_directory(source_directory, target_directory, target_db)

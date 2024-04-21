##############################################################################
# NAME: linear-fade-segment.py
# DESCRIPTION: This module traverses a soundfile (.wav) directory tree and 
# generates a new directory tree with a mirrored hierarchy. The new directory
# replaces every soundfile in the original directory with a subdirectory named
# after the soundfile. Inside this subdirectory, the soundfile is split into
# as many 2-second segments as needed to cover its full length. Each segment's 
# name is  prefixed with its position in the ordered sequence of 2-second
# segments.
# 
# For instance, a 3 second .wav sample entitled "clarinet_A3_forte" would be 
# replaced in the new directory by a subdirectory "clarinet_A3_forte" in the 
# same location. The segments would be called '1_clarinet_A3_forte' and 
# ; 2_clarinet_A3 forte'; both would be exactly 2 seconds long. 
# Since the original .wav is 3 second long, the last second of the second 
# segment would be filled by silence.
###############################################################################

import os
from pydub import AudioSegment
import shutil

## TODO: verify if AudioSegment is degrading audio quality 

def process_wav_file(source_path, target_dir):
    audio = AudioSegment.from_wav(source_path)
    duration_ms = len(audio)
    segment_duration_ms = 2000  # 2000 milliseconds = 2 seconds
    fade_duration_ms = 10  # 10 milliseconds fade duration

    # Calculate the number of full segments and the remaining time
    num_full_segments = duration_ms // segment_duration_ms
    remainder_ms = duration_ms % segment_duration_ms

    # Create segments, apply short fades, and save them
    for i in range(num_full_segments):
        start_ms = i * segment_duration_ms
        segment = audio[start_ms:start_ms + segment_duration_ms]
        # Apply a short fade in and fade out
        segment = segment.fade_in(fade_duration_ms).fade_out(fade_duration_ms)
        segment.export(os.path.join(target_dir, f"{i+1}_{os.path.basename(source_path)}"), format="wav")

    # Handle the remaining part, if any
    if remainder_ms > 0:
        last_segment = audio[-remainder_ms:]
        # Padding to make it exactly 2 seconds
        last_segment = last_segment + AudioSegment.silent(duration=segment_duration_ms - remainder_ms)
        # Apply a short fade in and fade out
        last_segment = last_segment.fade_in(fade_duration_ms).fade_out(fade_duration_ms)
        last_segment.export(os.path.join(target_dir, f"{num_full_segments+1}_{os.path.basename(source_path)}"), format="wav")

def process_directory(source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".wav"):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_dir)
                target_path = os.path.join(target_dir, relative_path, file[:-4])
                os.makedirs(target_path, exist_ok=True)
                process_wav_file(source_path, target_path)

source_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio'
target_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio-segmented'

process_directory(source_directory, target_directory)

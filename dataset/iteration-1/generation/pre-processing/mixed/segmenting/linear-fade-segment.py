import os
from pydub import AudioSegment
import shutil

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

source_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio/flute'
target_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio-segmented/flute'

process_directory(source_directory, target_directory)

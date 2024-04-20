import os
from pydub import AudioSegment
import shutil

def splice_segments_in_directory(source_dir, target_dir):
    # Navigate through each subdirectory in the source directory
    for root, dirs, files in os.walk(source_dir):
        if not dirs:  # This means 'root' is a leaf directory
            # Sort files to ensure they are merged in the correct order
            sorted_files = sorted(files, key=lambda x: int(x.split('_')[0]))
            full_audio = None
            
            for file in sorted_files:
                file_path = os.path.join(root, file)
                segment = AudioSegment.from_wav(file_path)
                
                if full_audio is None:
                    full_audio = segment
                else:
                    full_audio += segment
            
            # Calculate the correct target path which is the parent directory of the original subdirectory
            relative_path = os.path.relpath(root, source_dir)
            target_file_dir = os.path.join(target_dir, os.path.dirname(relative_path))
            os.makedirs(target_file_dir, exist_ok=True)
            
            # The filename is based on the directory name
            output_file_name = f"{os.path.basename(root)}.wav"
            full_audio.export(os.path.join(target_file_dir, output_file_name), format="wav")
            
            # Delete the processed subdirectory (optional: ensure it's empty or remove regardless)
            shutil.rmtree(root)

def reverse_process_directory(source_dir, target_dir):
    splice_segments_in_directory(source_dir, target_dir)

# Example usage
source_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/audio-segmented'
target_directory = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/audio'

reverse_process_directory(source_directory, target_directory)

import os
import subprocess

def convert_mp3_to_wav(source_dir, target_dir, log_file):
    """
    Recursively converts all .mp3 files found in source_dir and its subdirectories to .wav format,
    saving the converted files in the target_dir while maintaining the directory structure.
    Files that fail to convert are logged in a text file at the root of source_dir.
    """
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".mp3"):
                mp3_path = os.path.join(root, file)
                relative_path = os.path.relpath(mp3_path, source_dir)
                wav_path = os.path.join(target_dir, os.path.splitext(relative_path)[0] + ".wav")
                
                # Ensure the target directory exists
                os.makedirs(os.path.dirname(wav_path), exist_ok=True)
                
                try:
                    # Convert mp3 to wav using ffmpeg
                    subprocess.run(["ffmpeg", "-i", mp3_path, wav_path], check=True)
                    print(f"Converted {mp3_path} to {wav_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to convert {mp3_path}. Error: {e}")
                    # Log the failed file conversion
                    with open(log_file, 'a') as log:
                        log.write(f"{mp3_path}\n")

# Example usage:
source_directory = "/Users/Leo/Developer/local/senior-project/dataset/raw/philharmonia-mp3"  # Change this to your source directory ##TODO use relative paths, or replace with empty string
target_directory = "/Users/Leo/Developer/local/senior-project/dataset/raw/philharmonia-wav"  # Change this to your target directory ## TODO use relative paths, or replace with empty string
log_file_path = os.path.join(os.path.dirname(target_directory), "failed-conversion-files.txt")  # Log file for failed conversions

convert_mp3_to_wav(source_directory, target_directory, log_file_path)

print("failed-conversion-files.txt can be found at:\n" +log_file_path)

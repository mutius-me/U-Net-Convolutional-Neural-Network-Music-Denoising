import os
import subprocess
import argparse

def convert_audio_to_wav(source_dir, target_dir, log_file):
    """
    Recursively converts all .mp3 and .m4a files found in source_dir and its subdirectories to .wav format,
    saving the converted files in the target_dir while maintaining the directory structure.
    Files that fail to convert are logged in a text file at the root of source_dir.
    """
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith((".mp3", ".m4a")):
                audio_path = os.path.join(root, file)
                relative_path = os.path.relpath(audio_path, source_dir)
                wav_path = os.path.join(target_dir, os.path.splitext(relative_path)[0] + ".wav")
                
                # Ensure the target directory exists
                os.makedirs(os.path.dirname(wav_path), exist_ok=True)
                
                try:
                    # Convert audio to wav using ffmpeg
                    subprocess.run(["ffmpeg", "-i", audio_path, wav_path], check=True)
                    print(f"Converted {audio_path} to {wav_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to convert {audio_path}. Error: {e}")
                    # Log the failed file conversion
                    with open(log_file, 'a') as log:
                        log.write(f"{audio_path}\n")

def main():
    parser = argparse.ArgumentParser(description="Convert .mp3 and .m4a files to .wav format.")
    # Changed to optional arguments
    parser.add_argument("--source_dir", default="/Users/Leo/Developer/Local/senior-project/dataset/raw/data/mynoise-samples/not-animated/m4a", help="Source directory containing the audio files to convert.")
    parser.add_argument("--target_dir", default="/Users/Leo/Developer/Local/senior-project/dataset/raw/data/mynoise-samples/not-animated/wav", help="Target directory where the converted .wav files will be saved.")
    parser.add_argument("--log_file", default="failed-conversion-files.txt", help="Path to the log file for failed conversions.")

    args = parser.parse_args()

    # No need to set empty defaults here, argparse handles defaults
    convert_audio_to_wav(args.source_dir, args.target_dir, args.log_file)
    print(f"Conversion complete. Failed conversions logged in: {args.log_file}")

if __name__ == "__main__":
    main()
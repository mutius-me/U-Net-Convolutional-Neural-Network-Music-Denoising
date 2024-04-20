import os
import wave
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def check_audio_properties(file_path):
    try:
        # Check for valid WAV file format and properties
        with wave.open(file_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
            frames = wav_file.getnframes()

            # Check for empty or potentially corrupted file
            if frames == 0:
                print(Fore.RED + f"Warning: {file_path} is empty or corrupted.")

            # Check sample rate and channels
            if sample_rate != TARGET_SAMPLE_RATE:
                print(Fore.YELLOW + f"Warning: {file_path} has a sample rate of {sample_rate} Hz, expected {TARGET_SAMPLE_RATE} Hz.")
            if channels != TARGET_CHANNELS:
                print(Fore.YELLOW + f"Warning: {file_path} has {channels} channels, expected {TARGET_CHANNELS} channels.")
    except wave.Error:
        print(Fore.RED + f"Warning: {file_path} could not be opened as a WAV file or might be corrupted.")

def traverse_directory(directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if ((filename.lower().endswith('.ds_store')) 
                or (filename.lower().endswith('.md'))):
                continue

            elif filename.lower().endswith('.wav'):
                check_audio_properties(file_path)
            else:
                print(Fore.CYAN + f"Warning: {file_path} is not a WAV file.")

if __name__ == "__main__":
    TARGET_SAMPLE_RATE = 44100  # Example target sample rate
    TARGET_CHANNELS = 1         # Example target for stereo channels
    
    directories = [
        '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio', ##TODO use relative paths
        '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio'
    ]
    count = len(directories)
    for i, directory in enumerate(directories, start=1):
        print(Fore.GREEN + f"Now checking: {directory}")
        traverse_directory(directory)
        print(Fore.GREEN + f"Processing complete for directory ({i}/{count}):\n{directory}")
        print("\n")

    print(Style.RESET_ALL + "Check complete.")

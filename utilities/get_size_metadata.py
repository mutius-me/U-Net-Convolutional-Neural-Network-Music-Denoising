import os

def count_wav_files(directory):
    wav_count = 0
    # os.walk iterates through the directory tree
    for root, dirs, files in os.walk(directory):
        # Filter and count only .wav files
        wav_count += len([file for file in files if file.endswith('.wav')])
    return wav_count

# Specify the directory to search
directory_to_search = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio'
wav_file_count = count_wav_files(directory_to_search)
print(f"There are {wav_file_count} .wav files in the directory tree '{directory_to_search}'.")

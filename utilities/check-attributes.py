import argparse
import wave
from pydub import AudioSegment

# Dictionaries with sample paths
wav_samples = {
    "NSynth": "/Users/Leo/Developer/local/senior-project/dataset/practice/guitar_acoustic_001-060-127.wav",
}
mp3_samples = {
    "Philharmonia": "/Users/Leo/Downloads/all-samples/cello/cello_Gs5_05_forte_arco-normal.mp3",
}

def get_audio_length(file_path):
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000.0

def get_sample_rate(file_path, is_wav=True):
    if is_wav:
        with wave.open(file_path, 'r') as wav_file:
            return wav_file.getframerate()
    else:
        audio = AudioSegment.from_file(file_path)
        return audio.frame_rate

def process_files(check_length, check_sample_rate, paths):
    for file_path in paths:
        if check_length:
            print(f"The length of the audio file {file_path} is: {get_audio_length(file_path)} seconds")
        if check_sample_rate:
            is_wav = file_path.lower().endswith('.wav')
            print(f"The sample rate of the audio file {file_path} is: {get_sample_rate(file_path, is_wav)} Hz")

def read_paths_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some audio files.')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-l', '--length', action='store_true', help='Check length of the audio file')
    parser.add_argument('-s', '--samplerate', action='store_true', help='Check sample rate of the audio file')
    group.add_argument('-p', '--path', type=str, help='Direct path to the audio file')
    group.add_argument('-f', '--file', type=str, help='Read paths from a text file')
    
    args = parser.parse_args()

    # Determine source of paths
    paths = []
    if args.file:
        paths = read_paths_from_file(args.file)
    elif args.path:
        paths = [args.path]
    else:
        # Default to using the predefined dicts
        # Combine WAV and MP3 paths
        combined_samples = {**wav_samples, **mp3_samples}
        paths.extend(combined_samples.values())
    
    process_files(args.length, args.samplerate, paths)

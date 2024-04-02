import argparse
import wave
from pydub import AudioSegment
import librosa  # Import librosa for audio analysis

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

def get_channel_info(file_path):
    """
    Checks if the audio is mono or stereo.
    """
    y, sr = librosa.load(file_path, sr=None, mono=False)  # Load with librosa
    if y.ndim == 1 or y.shape[0] == 1:  # Mono
        return "Mono"
    else:  # Stereo
        return "Stereo"
    

def process_files(check_length, check_sample_rate, check_channels, paths):
    for file_path in paths:
        if check_length:
            print(f"The length of the audio file {file_path} is: {get_audio_length(file_path)} seconds")
        if check_sample_rate:
            is_wav = file_path.lower().endswith('.wav')
            print(f"The sample rate of the audio file {file_path} is: {get_sample_rate(file_path, is_wav)} Hz")
        if check_channels:
            print(f"The channel configuration of the audio file {file_path} is: {get_channel_info(file_path)}")

def read_paths_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some audio files.')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-l', '--length', action='store_true', help='Check length of the audio file')
    parser.add_argument('-s', '--samplerate', action='store_true', help='Check sample rate of the audio file')
    parser.add_argument('-c', '--channels', action='store_true', help='Check if the audio file is mono or stereo')
    parser.add_argument('-a', '--all', action='store_true', help='Shorthand to call --length, --samplerate, and --channels args')
    group.add_argument('-ip', '--input', type=str, help='Direct path to the input audio file')
    group.add_argument('-f', '--file', type=str, help='Read paths from a text file')
    group.add_argument('-d', '--default', action='store_true', help='Use default dicts in module as input to the checks.')
    
    args = parser.parse_args()

    if args.all:
        args.length = args.samplerate = args.channels = True

    # Determine source of paths
    paths = []
    if args.file:
        paths = read_paths_from_file(args.file)
    elif args.input: 
        paths = [args.input]
    elif args.default:
        # Combine WAV and MP3 paths
        combined_samples = {**wav_samples, **mp3_samples}
        paths.extend(combined_samples.values())
    else:
        # If none of the specific options were selected, ask the user for a path
        user_input_dir = input("Please enter the directory of the audio file: ")
        user_input_filename = input("Please enter the filename (with extension): ")
        paths = [(user_input_dir + '/' + user_input_filename)]
    
    process_files(args.length, args.samplerate, args.channels, paths)
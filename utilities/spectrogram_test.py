import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf 
import argparse

DEFAULT_INPUT_DIR = "/Users/Leo/Developer/local/senior-project/dataset/practice/instruments/piano-v1"
DEFAULT_INPUT_FILE = 'clean_001.wav'
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT_DIR ## Change this if needed

def create_spectrogram(file_path, spectrogram_type='stft', start_time=0.0, duration=None, plot=False):
    """
    Generates and plots a spectrogram (STFT, Mel, or CQT) for an audio file.
    
    Parameters:
    - file_path: Path to the audio file.
    - spectrogram_type: Type of spectrogram ('stft', 'mel', 'cqt').
    - start_time: Start time for the segment in seconds.
    - duration: Duration of the segment in seconds. None means full duration.
    """
    y, sr = librosa.load(file_path, offset=start_time, duration=duration)

    if spectrogram_type == 'mel':
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_dB = librosa.power_to_db(S, ref=np.max)
        axis_type = 'mel'
    elif spectrogram_type == 'cqt':
        S = np.abs(librosa.cqt(y, sr=sr))
        S_dB = librosa.amplitude_to_db(S, ref=np.max)
        axis_type = 'cqt_hz'
    elif spectrogram_type == 'stft':
        S = librosa.stft(y)
        S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)
        axis_type = 'log'
    else:
        raise ValueError("Unsupported spectrogram type '" + spectrogram_type + "'.")
    
    if plot:
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis=axis_type)
        plt.colorbar(format='%+2.0f dB')
        plt.title(f'{spectrogram_type.capitalize()}-frequency spectrogram')
        plt.tight_layout()
        plt.show()

    return S, sr

def convert_spectrogram_to_audio(S, sr, spectrogram_type='stft'):
    """
    Converts a spectrogram back to an audio signal.
    
    Parameters:
    - S: Spectrogram (STFT, Mel, or CQT).
    - sr: Sample rate of the original audio.
    - spectrogram_type: Type of spectrogram ('stft', 'mel', 'cqt').
    """
    if spectrogram_type == 'mel' or spectrogram_type == 'cqt':
        # Inverse transform for mel or cqt is complex; using Griffin-Lim as a fallback for demonstration.
        # Note: This won't perfectly reconstruct audio for mel or cqt, but illustrates the process.
        S = librosa.feature.inverse.mel_to_audio(S, sr=sr) if spectrogram_type == 'mel' else librosa.griffinlim(S)
    else:  # Default to 'stft'
        S = librosa.istft(S)

    return S

def save_audio_to_disk(audio, sr, file_path='output_audio.wav'):
    """
    Saves an audio signal to disk.
    
    Parameters:
    - audio: Audio signal to save.
    - sr: Sample rate of the audio.
    - file_path: Path to save the audio file.
    """
    sf.write(file_path, audio, sr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an audio file to create and convert spectrograms.')
    parser.add_argument('-ip', '--input', type=str, help='Input path to the audio file.')
    parser.add_argument('-t', '--type', type=str, default='stft', help='Type of spectrogram to generate (stft, mel, cqt).')
    parser.add_argument('-s', '--start', type=float, help='Start time in seconds.', default=0.0)
    parser.add_argument('-d', '--duration', type=float, help='Duration in seconds.')
    parser.add_argument('-op', '--output', type=str, help='Output path for the audio file.', default='output_audio.wav')
    parser.add_argument('-p', '--plot', action='store_true', help='Indicates that the spectrogram should be plotted using matplotlib.')

    args = parser.parse_args()

    input = args.input if args.input else (DEFAULT_INPUT_DIR + '/' + DEFAULT_INPUT_FILE)
    spectrogram_type = args.type if args.type else 'stft'
    start_time = args.start if args.start else 0.0
    duration = args.duration if args.duration else None
    output = args.output if args.output else DEFAULT_OUTPUT_DIR
    plot = args.plot if args.plot else False



    # Generate spectrogram
    S, sr = create_spectrogram(input, spectrogram_type, start_time, duration, plot)
    
    # Convert back to audio
    audio = convert_spectrogram_to_audio(S, sr, spectrogram_type=args.type)
    
    # Save the audio to disk
    save_audio_to_disk(audio, sr, output)

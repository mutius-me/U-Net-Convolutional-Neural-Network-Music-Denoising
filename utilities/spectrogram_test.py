import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf 
import argparse

def create_spectrogram(file_path, spectrogram_type='stft', start_time=0.0, duration=None):
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
    else:  # Default to 'stft'
        S = librosa.stft(y)
        S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)
        axis_type = 'log'
    
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
    parser.add_argument('-p', '--path', type=str, help='Path to the audio file.')
    parser.add_argument('-t', '--type', type=str, default='stft', help='Type of spectrogram to generate (stft, mel, cqt).')
    parser.add_argument('-s', '--start', type=float, help='Start time in seconds.', default=0.0)
    parser.add_argument('-d', '--duration', type=float, help='Duration in seconds.')
    parser.add_argument('-o', '--output', type=str, help='Output path for the audio file.', default='output_audio.wav')

    args = parser.parse_args()

    # Generate spectrogram
    S, sr = create_spectrogram(args.path, spectrogram_type=args.type, start_time=args.start, duration=args.duration)
    
    # Convert back to audio
    audio = convert_spectrogram_to_audio(S, sr, spectro

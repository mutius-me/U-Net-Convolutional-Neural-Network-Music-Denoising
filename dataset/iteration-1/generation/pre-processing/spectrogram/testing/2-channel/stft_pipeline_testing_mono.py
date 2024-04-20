##############################################################################
# NAME: stft_pipeline_testing.py
# DESCRIPTION: A script to test whether the audio-spectrogram pipeline works.
# This script now processes the audio file exclusively in mono.
###############################################################################

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import argparse
import os

DEFAULT_INPUT_DIR = "/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio/oboe"
DEFAULT_INPUT_FILE = 'oboe_As4_15_forte_normal.wav'
DEFAULT_OUTPUT_DIR = "/Users/Leo/Developer/Local/senior-project/"
DEFAULT_OUTPUT_FILE = DEFAULT_INPUT_FILE[0:-4] + "_reconstructed" + DEFAULT_INPUT_FILE[-4:]
DEFAULT_SPECTROGRAM_DIR = "___"

def create_spectrogram(file_path, start_time=0.0, duration=None, plot=False):
    """
    Generates and plots an STFT spectrogram for a mono audio file.
    
    Parameters:
    - file_path: Path to the audio file.
    - start_time: Start time for the segment in seconds.
    - duration: Duration of the segment in seconds. None means full duration.
    - plot: Whether to plot the spectrogram.
    """
    y, sr = librosa.load(file_path, sr=None, mono=True, offset=start_time, duration=duration)
    S = librosa.stft(y)
    S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    
    if plot:
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.title('STFT Spectrogram')
        plt.tight_layout()
        plt.show()

    return S, sr

def convert_spectrogram_to_audio(S, sr):
    """
    Converts an STFT spectrogram back to a mono audio signal.
    
    Parameters:
    - S: STFT spectrogram.
    - sr: Sample rate of the original audio.
    """
    audio = librosa.istft(S)
    return audio

def save_audio_to_disk(audio, sr, file_path):
    """
    Saves a mono audio signal to disk.
    
    Parameters:
    - audio: Mono audio signal to save.
    - sr: Sample rate of the audio.
    - file_path: Path to save the audio file.
    """
    sf.write(file_path, audio, sr)

def save_spectrogram_to_disk(spectrogram, save_dir, file_name):
    np.save(os.path.join(save_dir, file_name), spectrogram)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an audio file to create and convert STFT spectrograms.')
    parser.add_argument('-ip', '--input', type=str, default=DEFAULT_INPUT_DIR + '/' + DEFAULT_INPUT_FILE, help='Input path to the audio file.')
    parser.add_argument('-s', '--start', type=float, default=0.0, help='Start time in seconds.')
    parser.add_argument('-d', '--duration', type=float, help='Duration in seconds.')
    parser.add_argument('-op', '--output', type=str, default=DEFAULT_OUTPUT_DIR + '/' + DEFAULT_OUTPUT_FILE, help='Output path for the audio file.')
    parser.add_argument('-p', '--plot', action='store_true', help='Plot the STFT spectrogram.')
    parser.add_argument('-save-spec', '--save-spectrogram', action='store_true', help='Save the numpy spectrogram array to disk.')

    args = parser.parse_args()

    # Generate spectrogram
    S, sr = create_spectrogram(args.input, args.start, args.duration, args.plot)
    
    # Convert spectrogram back to mono audio
    audio = convert_spectrogram_to_audio(S, sr)
    
    # Save the mono audio to disk
    save_audio_to_disk(audio, sr, args.output)

    # Optionally save the spectrogram to disk
    if args.save_spectrogram:
        spectrogram_file_name = os.path.splitext(DEFAULT_INPUT_FILE)[0] + '_spectrogram.npy'
        save_spectrogram_to_disk(S, DEFAULT_SPECTROGRAM_DIR, spectrogram_file_name)
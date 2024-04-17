##############################################################################
# NAME: stft_pipeline_testing.py
# DESCRIPTION: A script to test whether the audio-spectrogram pipeline works.
# In this script, an audio file is converted into a STFT spectrogram, then
# converted back into an audio file.
#
# The outcome of this test showed that the pipeline is sound. 
###############################################################################

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
import argparse
import os

DEFAULT_INPUT_DIR = "/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio/flute"
DEFAULT_INPUT_FILE = 'cello_C2_phrase_mezzo-forte_arco-col-legno-tratto.mp3'
DEFAULT_OUTPUT_DIR = "/Users/Leo/Developer/Local/senior-project/utilities"
DEFAULT_OUTPUT_FILE = DEFAULT_INPUT_FILE[0:-4] + "_reconstructed" + DEFAULT_INPUT_FILE[-4:]
DEFAULT_SPECTROGRAM_DIR = "___"

def create_spectrogram(file_path, start_time=0.0, duration=None, plot=False):
    """
    Generates and plots STFT spectrograms for both channels of a stereo audio file.
    
    Parameters:
    - file_path: Path to the audio file.
    - start_time: Start time for the segment in seconds.
    - duration: Duration of the segment in seconds. None means full duration.
    - plot: Whether to plot the spectrogram.
    """
    y, sr = librosa.load(file_path, sr=None, mono=False, offset=start_time, duration=duration)

    # Ensure y is stereo (2 channels)
    if y.ndim == 1:
        y = np.tile(y, (2, 1))

    channel_spectrograms = []
    for channel in range(y.shape[0]):
        S = librosa.stft(y[channel])
        S_dB = librosa.amplitude_to_db(np.abs(S), ref=np.max)
        channel_spectrograms.append(S)
        
        if plot:
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='log')
            plt.colorbar(format='%+2.0f dB')
            plt.title(f'Channel {channel+1}: STFT Spectrogram')
            plt.tight_layout()
            plt.show()

    spectrograms_array = np.array(channel_spectrograms)
    return spectrograms_array, sr

def convert_spectrogram_to_audio(S_array, sr):
    """
    Converts STFT spectrograms back to a stereo audio signal.
    
    Parameters:
    - S_array: Array of STFT spectrograms for both channels.
    - sr: Sample rate of the original audio.
    """
    channels_audio = []
    for S in S_array:
        audio = librosa.istft(S)
        channels_audio.append(audio)

    # Combine the channels back into a stereo signal
    stereo_audio = np.vstack(channels_audio)
    return stereo_audio

def save_audio_to_disk(audio, sr, file_path):
    """
    Saves a stereo audio signal to disk.
    
    Parameters:
    - audio: Stereo audio signal to save.
    - sr: Sample rate of the audio.
    - file_path: Path to save the audio file.
    """
    sf.write(file_path, audio.T, sr)  # Transpose the array to fit soundfile's format

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

    # Generate spectrograms for both channels
    S, sr = create_spectrogram(args.input, args.start, args.duration, args.plot)

    # Convert spectrograms back to stereo audio
    audio = convert_spectrogram_to_audio(S, sr)

    # Save the stereo audio to disk
    save_audio_to_disk(audio, sr, args.output)

    # Optionally save the spectrogram to disk
    if args.save_spectrogram:
        spectrogram_file_name = os.path.splitext(DEFAULT_INPUT_FILE)[0] + '_spectrogram.npy'
        save_spectrogram_to_disk(S, DEFAULT_SPECTROGRAM_DIR, spectrogram_file_name)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an audio file to create and convert STFT spectrograms.')
    parser.add_argument('-ip', '--input', type=str, default=DEFAULT_INPUT_DIR + '/' + DEFAULT_INPUT_FILE, help='Input path to the audio file.')
    parser.add_argument('-s', '--start', type=float, default=0.0, help='Start time in seconds.')
    parser.add_argument('-d', '--duration', type=float, help='Duration in seconds.')
    parser.add_argument('-op', '--output', type=str, default=DEFAULT_OUTPUT_DIR + '/' + DEFAULT_OUTPUT_FILE, help='Output path for the audio file.')
    parser.add_argument('-p', '--plot', action='store_true', help='Plot the STFT spectrogram.')

    args = parser.parse_args()

    # Generate spectrograms for both channels
    S, sr = create_spectrogram(args.input, args.start, args.duration, args.plot)
    
    # Convert spectrograms back to stereo audio
    audio = convert_spectrogram_to_audio(S, sr)
    
    # Save the stereo audio to disk
    save_audio_to_disk(audio, sr, args.output)

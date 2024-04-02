##############################################################################
# NAME: display_spectrogram.py
# DESCRIPTION: A module used to display a spectrogram for a sound file.
###############################################################################

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import argparse
from . import check_attributes


def display_spectrogram(file, start_time=0.0, duration=None):
    """
    Generates a mel-spectrogram for a segment of an audio file, then plots and displays it.
    
    Parameters:
    - file: Path to the audio file.
    - start_time: Start time for the segment in seconds. Defaults to 0.0.
    - duration: Duration of the segment in seconds. Defaults to None, which means the whole audio after start_time is used.
    """
    # Load the audio file (or a segment of it)
    y, sr = librosa.load(file, offset=start_time, duration=duration)

    # Create a spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

    # Convert to log scale (dB)
    S_dB = librosa.power_to_db(S, ref=np.max)

    # Plot the spectrogram
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel', fmax=8000)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    plt.show()
    


#*######################*#
#*PREVIOUSLY-USED INPUTS*#
#*######################*# 


## Piano
dir_name = '/Users/Leo/Developer/local/senior-project/dataset/practice/instruments/piano-v1'
file_name = 'clean_001.wav'

# AC Unit
# dir_name = '/Users/Leo/Developer/local/senior-project/dataset/practice/noise/real-life'
# file_name = 'ac-unit.mp3'

## Piano + AC Unit
# dir_name = '/Users/Leo/Developer/local/senior-project/dataset/practice'
# file_name = 'practice.wav'
        
## 60 Hz
# Obs.: weird spike at aroudn 6 seconds; start at 7 for clean
# dir_name = '/Users/Leo/Developer/local/senior-project/dataset/practice/noise/60-hz'
# file_name = '001.mp3'

# Piano + 60 Hz
dir_name = '/Users/Leo/Developer/local/senior-project/dataset/practice/combinations'
file_name = '/60hz+piano.wav'
piano_path = '/Users/Leo/Developer/local/senior-project/dataset/practice/instruments/piano-v1/clean_001.wav'

full_path = dir_name + '/' + file_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a frequency spectrogram for an audio file.')
    parser.add_argument('-p', '--path', type=str, help='Check length of the audio file')
    parser.add_argument('-d', '--duration', type=float, help='Specifies duration.')
    parser.add_argument('-s', '--start', type=float, help='Specifies start time.')

    args = parser.parse_args()

    if args.path:
        if args.duration and args.start:
            display_spectrogram(args.path, duration=args.duration, start=args.start)
        elif args.duration and not args.start:
            display_spectrogram(args.path, duration=args.duration)
        elif not args.duration and args.start:
            display_spectrogram(args.path, start=args.start)
        else:
            display_spectrogram(args.path)
    else:
        # Use default file
        if piano_path:
            display_spectrogram(full_path, start_time=0, duration=check_attributes.get_audio_length(piano_path))
        else: 
            display_spectrogram(full_path)

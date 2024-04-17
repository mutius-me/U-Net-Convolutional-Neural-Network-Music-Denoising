##############################################################################
# NAME: display_spectrogram.py
# DESCRIPTION: A module used to visually display a spectrogram for a sound 
# file.
###############################################################################

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import argparse
# from . import get_audio_attributes ##TODO: fix this relative import issue
from pydub import AudioSegment ##TODO remove this import once relative import issue is resolved



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


## TODO: Delete and fix import
def get_audio_length(file_path):
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000.0

#*######################*#
#*PREVIOUSLY-USED INPUTS*#
#*######################*# 

piano_path = None

## Piano
# dir_name = '/Users/Leo/Developer/local/senior-project/dataset/practice/instruments/piano-v1'
# file_name = 'clean_001.wav'

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
# dir_name = '/Users/Leo/Developer/local/senior-project/dataset/practice/combinations'
# file_name = '/60hz+piano.wav'
# piano_path = '/Users/Leo/Developer/local/senior-project/dataset/practice/instruments/piano-v1/clean_001.wav'


# Ground loop
dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/raw'
file_name = "ground-loop.wav"

# semi-random flute sample
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio/flute'
# file_name = 'flute_A4_1_forte_normal.wav'

# semi-random sax sample
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio/saxophone'
# file_name = 'saxophone_E6_15_piano_normal.wav'

# static
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/raw/data/mynoise-samples/not-animated/wav'
# file_name = 'static-15m.wav'


path = dir_name + '/' + file_name

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a frequency spectrogram for an audio file.')
    parser.add_argument('-p', '--path', type=str, help='Check length of the audio file')
    parser.add_argument('-s', '--start', type=float, help='Specifies start time.')
    parser.add_argument('-d', '--duration', type=float, help='Specifies duration.')


    args = parser.parse_args()

    duration = get_audio_length(path)
    start = 0.0

    if args.path:
        path = args.path

    if args.start:
        start = args.start

    if args.duration:
        duration = args.duration

    display_spectrogram(path, start, duration)

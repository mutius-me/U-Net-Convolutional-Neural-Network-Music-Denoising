##############################################################################
# NAME: display_spectrogram.py
# DESCRIPTION: A module used to visually display a spectrogram for a sound 
# file. Required input is a path to a .wav file. 
###############################################################################

import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def display_spectrogram(file, start_time=0.0, duration=None, title=None, spectrogram_type='stft'):
    """
    Generates a spectrogram (STFT or Mel) for a segment of an audio file, then plots and displays it
    with additional information like title, colorbar, and axis labels.

    Parameters:
    - file: Path to the audio file.
    - start_time: Start time for the segment in seconds. Defaults to 0.0.
    - duration: Duration of the segment in seconds. Defaults to None, which means the whole audio after start_time is used.
    - title: Title for the plot. Optional.
    - spectrogram_type: Type of the spectrogram ('stft' or 'mel'). Defaults to 'stft'.
    """

    # Load the audio file (or a segment of it)
    y, sr = librosa.load(file, offset=start_time, duration=duration)

    # Compute the spectrogram based on type
    if spectrogram_type == 'mel':
        # Create a Mel-scaled spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_db = librosa.amplitude_to_db(S, ref=np.max)
        y_axis_type = 'mel'
    else:
        # Compute the STFT and convert to dB
        D = librosa.stft(y)
        S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
        y_axis_type = 'log'

    # Plot the spectrogram
    figsize = (10, 4)  # Size in inches (width, height)
    dpi = 100  # Resolution in dots per inch
    plt.figure(figsize=figsize, dpi=dpi)
    img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis=y_axis_type, cmap='coolwarm')

    # Adding a colorbar
    plt.colorbar(img, format="%+2.0f dB")

    # Title and labels
    if title:
        plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")

    # Show the plot
    plt.show()

    # Calculate the number of pixels in the plot
    width_pixels = figsize[0] * dpi
    height_pixels = figsize[1] * dpi
    total_pixels = width_pixels * height_pixels
    print(f"The plot is {width_pixels:.0f} pixels wide and {height_pixels:.0f} pixels tall, totaling {total_pixels:.0f} pixels.")



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
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/noise/audio/raw/sc3'
# file_name = "ground-loop.wav"

# semi-random flute sample
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio/flute'
# file_name = 'flute_A4_1_forte_normal.wav'

# semi-random sax sample
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio/saxophone'
# file_name = 'saxophone_E6_15_piano_normal.wav'

# static
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/raw/data/mynoise-samples/not-animated/wav'
# file_name = 'static-15m.wav'


# noisfied flute
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio-segmented/flute/flute_As5_15_mezzo-piano_normal'
# file_name = '1_flute_As5_15_mezzo-piano_normal.wav'

# Outputted clarinet, v1
# dir_name = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/audio-segmented-128-frames/english-horn/clarinet_A3_1_forte_normal'
# file_name = '1_clarinet_A3_1_forte_normal_mixed_denoised.wav'




###########################
# MODEL OUTPUT COMPARISON #
###########################

# Original flute
dir_name2 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/clean/audio-segmented/flute/flute_A4_1_forte_normal'
file_name2 = '1_flute_A4_1_forte_normal.wav'
path2 = dir_name2 + '/' + file_name2


# Noisy flute
dir_name3 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/mixed/audio-segmented/flute/flute_A4_1_forte_normal'
file_name3 = '1_flute_A4_1_forte_normal.wav'
path3 = dir_name3 + '/' + file_name3


# Outputted flute, v2
dir_name1 = '/Users/Leo/Developer/Local/senior-project/dataset/iteration-1/data/output/audio-segmented-256-frames/flute/flute_A4_1_forte_normal'
# dir_name1 = '/Users/Leo/Downloads/'
file_name1 = '1_flute_A4_1_forte_normal.wav'
# file_name1 = 'test.wav'
path = dir_name1 + '/' + file_name1


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Generate a frequency spectrogram for an audio file.')
    # parser.add_argument('-p', '--path', type=str, help='Check length of the audio file')
    # parser.add_argument('-s', '--start', type=float, help='Specifies start time.')
    # parser.add_argument('-d', '--duration', type=float, help='Specifies duration.')


    # args = parser.parse_args()

    # duration = get_audio_length(path)
    # start = 0.0

    # if args.path:
    #     path = args.path

    # if args.start:
    #     start = args.start

    # if args.duration:
    #     duration = args.duration
    # 

    display_spectrogram(path2, 0, 2, title="Original clean flute sample", spectrogram_type='mel')

    display_spectrogram(path3, 0, 2, title="Noise-added flute sample", spectrogram_type='mel')


    display_spectrogram(path, 0, 2, title="Spectrogram outputted by U-Net", spectrogram_type='mel')

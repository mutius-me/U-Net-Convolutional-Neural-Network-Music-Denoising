import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def create_spectrogram(wav_file):
    # Load the audio file
    y, sr = librosa.load(wav_file)

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

# Example usage
wav_file = '/Users/Leo/Desktop/Yale/courses/cpsc-490-thesis/senior-project/dataset/practice/noisy_001.wav'
create_spectrogram(wav_file)

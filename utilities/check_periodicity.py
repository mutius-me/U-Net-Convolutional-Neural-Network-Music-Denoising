from pydub import AudioSegment
import librosa
import numpy as np
import scipy.signal

def convert_to_wav(file_path):
    # Load the .m4a file
    audio = AudioSegment.from_file(file_path, format="m4a")
    
    # Convert to .wav
    wav_path = file_path.rsplit(".", 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

def find_periodicity(file_path):
    # Convert .m4a to .wav if necessary
    if file_path.endswith('.m4a'):
        print("Converting .m4a to .wav for compatibility...")
        file_path = convert_to_wav(file_path)
    
    # Load the audio file
    y, sr = librosa.load(file_path)
    
    # The rest of the function remains the same as before...
    # Calculate the autocorrelation of the audio signal
    autocorr = np.correlate(y, y, mode='full')
    autocorr = autocorr[autocorr.size // 2:]  # Keep only the second half
    autocorr /= autocorr[0]  # Normalize
    peaks, _ = scipy.signal.find_peaks(autocorr, height=0.5)
    
    if len(peaks) == 0:
        print("No periodicity detected.")
    else:
        fundamental_period = peaks[0]
        period_time = fundamental_period / sr
        print(f"Periodicity detected. Fundamental period: {fundamental_period} samples, which is approximately {period_time:.4f} seconds.")
    
    return autocorr, peaks

# Replace 'your_audio_file.m4a' with the path to your audio file
autocorr, peaks = find_periodicity('/Users/Leo/Downloads/Noise samples/ground-loop.m4a')

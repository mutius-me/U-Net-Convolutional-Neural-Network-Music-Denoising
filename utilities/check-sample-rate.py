import wave
import pydub




# Initialization
###########
#WAV FILES#
###########
wav_samples = {}

# Add/alter paths here
wav_samples["NSynth"] = "/Users/Leo/Developer/local/senior-project/dataset/practice/guitar_acoustic_001-060-127.wav"


# Logic
for key in wav_samples:
    with wave.open(wav_samples[key], 'r') as wav_file:
        # Get the sample rate
        sample_rate = wav_file.getframerate()
        print(f"The sample rate for a random sample in dataset {key} is: {sample_rate} Hz")



###########
#MP3 FILES#
###########
from pydub import AudioSegment

#Initialization
mp3_samples = {}

# Add/alter paths here
mp3_samples["Philharmonia"] = "/Users/Leo/Downloads/all-samples/cello/cello_Gs5_05_forte_arco-normal.mp3"

#Logic
for key in mp3_samples:
    audio = AudioSegment.from_mp3(mp3_samples[key])

    # Access the sample rate
    sample_rate = audio.frame_rate  
    print(f"The sample rate for a random sample in dataset {key} is: {sample_rate} Hz")




### root/dataset/iteration-1

This iteration contains a complete dataset generation and treatment pipeline. 

### Directory structure

- The `generation` directory stores files relating to dataset generation and treatment.
- The `data`  directory stores the audio and spectrogram data used and generated in this iteration.

### Features for this iteration:

- Custom generated, stochastic 60Hz noise created in SuperCollider3
- Scripts for mixing noise with clean audio samples, then segmenting the audio into 2-second clips (using cross fading to eliminate clips), then generating frequency spectrogram
- The final form of the input dataset for the U-Net is a two part, clean-noisy dataset of frequency spectrograms, where each spectrogram has a shape (1024x256x2) and represents 2 seconds of audio (with minor preprocessing for cleanliness)
- This iteration also features scripts to convert the outputted spectrogram from the U-Net back into their original, full-length audio forms.
- 44,100 sample rate across all audio files
- 32bit float to represent each sample

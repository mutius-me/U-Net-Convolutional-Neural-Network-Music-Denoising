### /Users/Leo/Developer/Local/senior-project/dataset/iteration-1/generation/pre-processing



This directory contains subdirectories with audio processing scripts used in the pre-processing step of the generation of this dataset.



`attenuation`  contains scripts to attenuate the dB level of the soundfiles in a directory to a determined amount. It is used to prepare the noise.



`segmentation` contains scripts to split audio files in a .wav directory tree into equally-sized segments (default: 2 seconds). `linear-fade-segment.py` utilizes a 10-ms linear fade to mask clicks and pops that occur as a result of the segmentation process (when audio files are not cut at zero-crossing point, i.e. when the amplitude is 0).



`spectrogram` contains scripts to transform audio into spectograms.



`mixing` contains scripts to combine clean audio and noise to generate the mixed audio on which the dataset is trained.
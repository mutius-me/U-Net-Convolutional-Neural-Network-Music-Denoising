### senior-project/dataset/iteration-1/generation/noise

A directory for custom scripts to generate custom, randomized ground loop noise. 



- noise-generator-testing.scd contains the original experimentation for generating custom noise.

- save-noise-to-disk.scd copies the script from noise-generator-testing.scd into a SynthDef, then uses the Server object in SC3 to generate non-real-time (NRT) audio, which is then stored in /senior-project/dataset/iteration-1/data/noise/audio/raw/sc3




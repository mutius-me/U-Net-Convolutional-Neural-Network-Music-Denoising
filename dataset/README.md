### /Users/Leo/Developer/Local/senior-project/dataset

This directory contains all iterations of the dataset used in training this model. 

- Each iteration has its own `README` file delineating its scope. 
- Each iteration has a  `data` subdirectory, which itself is populated by `clean`, `noise`,  `mixed`, and `output` subdirectories, designed to store audio and spectrograms (although soundfiles and numpy arrays are not stored in GitHub).  
- Each iteration also possesses a `generation` subdirectory, which contains subdirectories housing scripts responsible for different parts of the **dataset treatment pipeline (DTP)**. The DTP is responsible for taking the clean, raw audio dataset sourced externally (i.e. the Philharmonia Orchestra Sound Sample Library), and generating a complete, robust dataset that can be used by the U-Net model. The DTP is responsible for an array of tasks including generating noise, injecting noise into clean samples to generate noise-added samples, handling all audio processing (attenuation, segmentation, splicing), and spectrogram generation and conversion.



This directory does *not* contain code used to train the U-Net model itself.
# README: Dataset/Generation/Iteration 0

Linked READMEs:

- [root/dataset/generation](../../README.md)
- [root](../../../README.md)



The code in this directory contains my original code where I experimented with noise injection for the ends of dataset generation. My original intention was to use noise generated on a Web generator (myNoise.net) to:

- Generate custom random noise
- Inject the noise into clean audio samples, creating the dataset counterpart



However, I ultimately abandoned using myNoise, because it was generating periodic noise samples and was thus compromising the generalizability of my project. This prompted the move to **Iteration 1**.****
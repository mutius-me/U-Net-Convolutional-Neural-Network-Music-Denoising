# README: Dataset/Generation/Iteration 0

Linked READMEs:

- [root/dataset/generation](../../README.md)
- [root](../../../README.md)

The code in this directory contains my original code where I experimented with for noise generation and injection for the ends of dataset generation. My original intention was to use SuperCollider to achieve the following:

- Generate custom random noise
- Inject the noise into clean audio samples
- Process audio



However, I ultimately abandoned using SuperCollider (for **Iteration 1**) for this purpose for a few reasons.

- Python libraries, namely librosa, pydub, and ffpmeg, proved to be simpler to implement without compromising versatility and quality of results.
- Noise generation with SuperCollider, while flexible and highly powerful, was time-intensive. While I have not discared it as an option for future iterations, I decided to use a [custom noise generator from the Web](mynoise.net) for **Iteration 1**, in order to speed up development and testing
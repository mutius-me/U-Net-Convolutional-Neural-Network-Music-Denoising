# To Do 

**High Priority**

- Advance the convolutional model



**Medium Priority**

- Ensure high bit-depth (float-32) throughout the project
  - Redo noise attenuation
  - Redo noisy script mixing
  - Redo segmentation; verify if float-32
  - Redo batch spectrogram generation
    - Generate both 128- and 256-frame spectrograms of shape (1024, {frame}, 2).
- Add documentation at the top of every file with a description of its function, as well as filling out README documents for each subdirectory.
- Fix existing, outdated documentation in both modules and READMEs



**Low Priority / Nonessential**

- Replace absolute paths with relative paths throughout codebase in order to make project fully exportable
- Synthesize (combine) scripts in the `utility` subdirectory that can be synthesized, to avoid clutter.


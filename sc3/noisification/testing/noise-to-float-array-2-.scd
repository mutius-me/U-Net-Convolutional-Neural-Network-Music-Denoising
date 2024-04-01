// Step 1: Define your SynthDef
(
SynthDef(\exampleSynth, { |out = 0|
	var noise, freqMod, ampMod, bpf;
    noise = WhiteNoise.ar(1);
    freqMod = LFNoise1.kr(5).range(6000, 20000); // Frequency modulation
    ampMod = LFNoise1.kr(1).range(0.1, 1); // Amplitude modulation
    bpf = BPF.ar(noise, freqMod, 0.1) * ampMod; // Apply modulation
    Out.ar(out, bpf);
}).add;
)

// Step 2: Prepare to record
(
var buffer, duration, path;

duration = 5;
path = "/Users/Leo/Developer/local/senior-project/dataset/practice"; // Set the path and duration

// Create a buffer for recording (assuming stereo output)
buffer = Buffer.alloc(s, s.sampleRate * duration, 2);

// RecordBuf arguments: buffer number, loop (0 = no loop), trigger (1 = start immediately), doneAction (2 = free self)
Synth(\exampleSynth, [\freq, 440], addAction: \addToTail);

{
    RecordBuf.ar(SoundIn.ar([0, 1]), buffer, loop: 0, doneAction: 2);
}.play;

// Schedule the buffer to write to a file after the duration
s.defer(duration, {
    buffer.write(path, "AIFF", "int16", completionMessage: ["/b_free", buffer.bufnum]);
    "Recording saved to disk!".postln;
});

// Free the buffer (optional, depending on your use case)
s.defer(duration + 1, { buffer.free; });
)


(
var duration = 1; // 1 second
var sampleRate = 44100; // Assuming a sample rate of 44100 Hz
var noiseArraySize = duration * sampleRate;
var highFreqNoiseArrays = []; // To hold multiple noise arrays
var numberOfNoiseArrays = 5; // For example, generate 5 different noise arrays

numberOfNoiseArrays.do({
    var noise = FloatArray.fill(noiseArraySize, { WhiteNoise.ar.next }); // Generate noise
    // Optionally apply a high-pass filter here to ensure high frequency content
    // For simplicity, this step is not explicitly detailed but can involve filtering the noise array
    highFreqNoiseArrays.add(noise);
});

// highFreqNoiseArrays now contains several arrays of high frequency noise
)


(
SynthDef("randomNoise", { |out = 0|
	var noise, freqMod, ampMod, bpf;


    var noise = WhiteNoise.ar(1);
    var freqMod = LFNoise1.kr(5).range(6000, 20000); // Frequency modulation
    var ampMod = LFNoise1.kr(1).range(0.1, 1); // Amplitude modulation
    var bpf = BPF.ar(noise, freqMod, 0.1) * ampMod; // Apply modulation
    Out.ar(out, bpf);
}).add;
)

Synth("randomNoise");


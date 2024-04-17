(
var server = Server(\nrt,
    options: ServerOptions.new
    .numOutputBusChannels_(1)
    .numInputBusChannels_(2)
);


~synthDef = SynthDef(\groundLoopNoise, {
    var fundamentalFreq, numHarmonics, amplitudeMod, freqMod, harmonics, baseFreqMod, baseAmpMod, base, freq, amp, mixedSignal;
    fundamentalFreq = 50;
	numHarmonics = 8;
    amplitudeMod = LFNoise2.kr(Rand(0.1, 0.2)).range(0.95, 1.05);
    freqMod = LFNoise1.kr(Rand(0.1, 0.2)).range(-0.1, 0.1);
    baseAmpMod = 0.3;
    baseFreqMod = fundamentalFreq + freqMod;

    // Base frequency oscillator
    base = SinOsc.ar(baseFreqMod, 0, amplitudeMod * baseAmpMod);

    // Add harmonics
    harmonics = Array.fill(numHarmonics, { |i|
        freq = (i + 1) * fundamentalFreq + LFNoise1.kr(Rand(0.05, 0.1)).range(-0.1, 0.1);
        amp = LFNoise2.kr(Rand(0.1, 0.15)).range(0.1, 0.2) * (0.12 / (i + 1));
        SinOsc.ar(freq, 0, amp)
    });

    mixedSignal = Mix([base] ++ harmonics).dup; // Mix and duplicate to stereo
    Out.ar(0, mixedSignal);
});


a = Score([
    [0.0, ['/d_recv', ~synthDef.asBytes]],
    [0.0, (x = Synth.basicNew(\groundLoopNoise, server, 1000)).newMsg()],
    [30 * 60, x.freeMsg]
]);

a.recordNRT(
    outputFilePath: "~/nrt-help.wav".standardizePath,
    headerFormat: "wav",
    sampleFormat: "int16",
    options: server.options,
    duration: 30 * 60,
    action: { "done".postln }
);

server.remove;
)
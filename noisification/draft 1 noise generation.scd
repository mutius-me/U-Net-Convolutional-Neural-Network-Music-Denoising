(
var srcPath = "path/to/sample.wav"; // TODO: fix path
var outputPath = "path/to/output_directory/"; // TODO: fix path
var numSamples = 5; // TODO: fix num samples

// Ensure the output directory exists
if(File.exists(outputPath).not) { File.mkdir(outputPath); };

numSamples.do { |i|
    var bitDepth, sampleRateFactor, addNoise, fileName;
    bitDepth = [8, 12, 16].choose;
    sampleRateFactor = [2, 4, 8].choose;
    addNoise = [true, false].choose;


	//file naming logic
	fileName = "sample_" ++ i.asString;
    fileName = fileName ++ "_bitDepth_" ++ bitDepth.asString;
    fileName = fileName ++ "_sampleRateFactor_" ++ sampleRateFactor.asString;
    if(addNoise) {
        fileName = fileName ++ "_noise_yes.wav";
    } else {
        fileName = fileName ++ "_noise_no.wav";
    }

    SynthDef("digitalArtifacts" ++ i, { |out=0, bufnum|
        var signal = PlayBuf.ar(1, bufnum, loop: false, doneAction: 2);
        var processed;

        // Apply sample rate reduction
        processed = Decimator.ar(signal, sampleRateFactor, bitDepth);

        // Optionally add noise
        if(addNoise) {
            processed = processed + WhiteNoise.ar(0.01);
        };

        // Write to disk
        DiskOut.ar(out, processed);
    }).add;

    s.sync; // Ensure the SynthDef is fully registered before proceeding

    Buffer.readChannel(s, srcPath, channels: [0], action: { |buf|
        var outFile = PathName(outputPath).fullPath ++ "/" ++ fileName;
        var diskBuf;

        diskBuf = Buffer.alloc(s, buf.frames, buf.numChannels, { |buffer|
            var synth = Synth.new("digitalArtifacts" ++ i, [\bufnum, buf.bufnum, \out, buffer.bufnum]);

            buffer.writeMsg(outFile, "WAV", "float", 0, completionMessage: ["/b_free", buffer.bufnum]);
        });
    });
};

"Processing complete. Files saved to: %".format(outputPath).postln;
)


FeedbackDelay
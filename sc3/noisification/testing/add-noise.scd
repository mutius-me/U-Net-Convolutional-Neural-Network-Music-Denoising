// This is a script that loads all files from a directory into Buffers, then into an array of FloatArrays.

// Global variables to be determined beforehand:
(
s.waitForBoot {
	~noiseDuration = 1;
	~numNoiseSamples = 100;
	post("noiseDuration: ");
	postln(~noiseDuration);
	post("numNoiseSamples: ");
	postln(~numNoiseSamples);
}
)

// Load all sound files from directory into float Arrays
(
s.waitForBoot {  // Make sure the server is booted before running this code
	var dir, name;
	~sampleRate = 0;
	~numChannels = 0;
	~discrepantSampleRates = List[];
	~discrepantNumChannels = List[];
    dir = PathName("/Users/Leo/Developer/local/senior-project/dataset/practice");
    name = dir.fileName;
    ~soundSamples = List[];

    post("Directory name: ");
    postln(name);

    dir.files.do { |file, i|
        Buffer.read(s, file.fullPath, numFrames: -1, action: { |buf|
            buf.loadToFloatArray(action: {|array|
				post("****");
				post(file.fileName);
				postln("****");
				post("sampleRate: ");
				postln(buf.sampleRate);
				post("NumFrames: ");
				postln(buf.numFrames);
				post("numChannels: ");
				postln(buf.numChannels);
                post("FloatArray size: ");
                postln(array.size);
				post("Duration: ");
				post(buf.numFrames / buf.numChannels / buf.sampleRate);
				postln(" seconds");
				postln("");
				if(i == 0,
					{
						~sampleRate = buf.sampleRate;
						~numChannels = buf.numChannels;
						~firstSampleName = file.fileName;
					};
				);

				//
				if(~sampleRate != buf.sampleRate,
					{~discrepantSampleRates = ~discrepantSampleRates.add([buf.sampleRate, file.fileName]);};
				);
				if(~numChannels != buf.numChannels,
					{~discrepantNumChannels = ~discrepantNumChannels.add([buf.numChannels, file.fileName]);};
				);

                // Now we add the array to the ~samples List
                ~soundSamples.add(array);
            });
        });
    };
	5.wait;

	// Logging validation for sample rates
	if(~discrepantSampleRates.size != 0,
		{
			post("Discrepant sample rates found in directory '");
			post(dir.fileName);
			postln("':");

			postln([~sampleRate, ~firstSampleName]);
			~discrepantSampleRates.do{ |tuple|
				postln(tuple);
			};
		},
		{
			postln("All files have matching sample rates.");
		};

	);

	// Logging validation for numChannels
	if(~discrepantNumChannels.size != 0,
		{
			post("Discrepant numChannels found in directory '");
			post(dir.fileName);
			postln("':");
			postln([~numChannels, ~firstSampleName]);
			~discrepantNumChannels.do{ |tuple|
				postln(tuple);
			};
		},
		{
			postln("All files have matching numChannels.");
		};
	);


	post("Number of samples loaded into array ~samples: ");
	postln(~soundSamples.size);
	post("Sample rate: ");
	postln(~sampleRate);
}
)

// Load all noise files into float arrays
(
s.waitForBoot{
	var noiseArraySize;
	noiseArraySize = ~noiseDuration * ~sampleRate;
	~noiseSamples = List[]; // To hold multiple noise arrays

	~numNoiseSamples.do({
		var noise = FloatArray.fill(noiseArraySize, { WhiteNoise.ar.next }); // Generate noise
		// Optionally apply a high-pass filter here to ensure high frequency content
		// For simplicity, this step is not explicitly detailed but can involve filtering the noise array
		~noiseSamples.add(noise);
	});


	// Log global variables determined beforehand
	post("noiseDuration: ");
	postln(~noiseDuration);
	post("numNoiseSamples: ");
	postln(~numNoiseSamples);
	5.wait;
	~noiseSamples.size.postln;
}
)
// highFreqNoiseArrays now contains several arrays of high frequency noise

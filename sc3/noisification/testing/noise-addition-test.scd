## Noise addition test


(
// Define the path to your audio file
var path = PathName("/Users/Leo/Developer/local/senior-project/dataset/practice");





path.files.do { |file|
	// postln(file);
	var soundFile, samples;


	// postln(file.fullPath);


	// postln("hi!");
	// Open the audio file for reading
	soundFile = SoundFile.openRead(file.fullPath);

	soundFile.numFrames.postln;

	samples = FloatArray.newClear(soundFile.numFrames * soundFile.numChannels);

	// samples.size.postln;
	// (samples[samples.maxIndex]).postln;
	// samples.maxIndex.postln;

	soundFile.readData(samples);

	soundFile.close;

	/*20.do { |i|
		samples[i].postln;
	};*/




};
)

~foo = [1, 2, 3, 4, 5];
~foo.maxIndex;




// Open the audio file for reading
var soundFile = SoundFile.openRead(path);

// Allocate an array of floats large enough to hold all the samples
// Multiplied by the number of channels to get all samples
var samples = FloatArray.newClear(soundFile.numFrames * soundFile.numChannels);

// Read the samples from the file into the array
soundFile.readData(samples);

// Close the sound file
soundFile.close;

// Now, `samples` contains all the samples from the audio file

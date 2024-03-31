// Test script to test insertion into Float Array with a single sample

// This script takes in a single .wav file, loads it into a buffer, and tests its sampleRate and numFrames. Then, it takes the same

(
var path, b, soundFile, sample, arr, filename;

path = "/Users/Leo/Developer/local/senior-project/dataset/practice/guitar_acoustic_001-060-127.wav";
filename = path.basename;
post("File name: ");
postln(filename);

postln("Attempting to load file into buffer...");
postln("");


// Read the buffer and define an action to execute once it's loaded
b = Buffer.read(s,
	path,
	numFrames: -1,
	action: { |buf|
		postln("File loaded succesfully.");
		postln("");

		post("**Buffer.SampleRate** is ");
		postln(buf.sampleRate);


		post("**Buffer.NumFrames** is ");
		postln(buf.numFrames);


		arr = buf.loadToFloatArray(action: {|array|
			post("**FloatArray.size** is ");
			postln(array.size);

			postln("");
		});
});
)
// This is a script that loads all files from a directory into Buffers, then into an array of FloatArrays.

(
s.waitForBoot {  // Make sure the server is booted before running this code
    var dir = PathName("/Users/Leo/Developer/local/senior-project/dataset/practice");
    var name = dir.fileName;
    ~samples = List[];

    post("Directory name: ");
    postln(name);

    dir.files.do { |file|
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

                // Now we add the array to the ~samples List
                ~samples.add(array);
            });
        });
    };
	5.wait;
	postln("******");
	post("Number of samples loaded into array ~samples: ");
	postln(~samples.size);

}
)
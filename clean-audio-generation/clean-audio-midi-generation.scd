// Initial draft of code to automate clean audio generation


MIDIClient.init; // Initialize MIDI
MIDIOut.newByName("IAC Driver", "Bus 1"); // TODO: Change "IAC Driver" and "Bus 1" to MIDI bus name




(
var midiout, channel, note, velocity, duration;
midiout = MIDIOut.newByName("IAC Driver", "Bus 1"); // ETODO: Change names
channel = 0; // MIDI channel
velocity = 64; // MIDI velocity
duration = 0.5; // Note duration in seconds

Routine.run({
    inf.do({
        note = (60..72).choose; // TODO: increase note range, currently C4 and C5
        midiout.noteOn(channel, note, velocity);
		(duration/2).wait
        midiout.noteOff(channel, note);
        (duration/2).wait; // Wait for the second half of the duration
        (0.1..0.5).choose.wait; // Random wait before the next note
    });
});
)

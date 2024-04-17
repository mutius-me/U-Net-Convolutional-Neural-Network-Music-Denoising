// This code generates a 50Hz noise.

// The fluctuation parameters were selected to approximate the fluctuation seen here: https://www.youtube.com/watch?v=e0elNU0iOMY

// Better modeling can yet be done, perhaps by consulting https://www.mainsfrequency.com/

(
s.waitForBoot {
	{

	var fundamentalFreq, numHarmonics, fundamentalAmplitudeFluctuationRange, fundamentalAmplitudeModulation, harmonicAmplitudeFluctuationRange, harmonicAmplitudeMod, frequencyFluctuationRange, frequencyModulation, base, harmonics, harmonicFreq, mixedSignal;

	fundamentalFreq = 50; // Base frequency of 60 Hz
	numHarmonics = 8;


	// AMPLITUDE MODULATION
	// (Random, small amplitude fluctuations expressed as %)

	fundamentalAmplitudeFluctuationRange = 0.05;
	fundamentalAmplitudeModulation = LFNoise2.kr(0.16).range(1-fundamentalAmplitudeFluctuationRange, 1+fundamentalAmplitudeFluctuationRange);

	harmonicAmplitudeFluctuationRange = 0.1;
	harmonicAmplitudeMod = LFNoise1.kr(0.1).range(1-harmonicAmplitudeFluctuationRange, 1+harmonicAmplitudeFluctuationRange);


	// FREQUENCY MODULATION.
	// Random, small frequency fluctuations expressed as absolute freq value
	frequencyFluctuationRange = 0.15;
	frequencyModulation = LFNoise2.kr(0.16).range(frequencyFluctuationRange,frequencyFluctuationRange);


	base = SinOsc.ar(fundamentalFreq + frequencyModulation, 0, fundamentalAmplitudeModulation * 0.3); // Adjust amplitude as needed
	harmonics = Array.fill(numHarmonics, { |i|
		harmonicFreq = (i + 1) * fundamentalFreq;
		SinOsc.ar(harmonicFreq, 0, harmonicAmplitudeMod * (0.12 / (i + 1))) // Decreasing amplitude for higher harmonics with modulation
	}
	);
		// mixedSignal = Mix([base] ++ harmonics);

		// Duplicate the mixed signal into both stereo channels
		// mixedSignal.dup
		base.dup
	}.play
}
)
s.meter;


	}
)
	(
{
    var fundamentalFreq = 60; // Base frequency of 60 Hz
    var numHarmonics = 5; // Number of harmonics to include
    var base, harmonics, amplitudeModulation, frequencyModulation;

    // Amplitude fluctuation range for fundamental and harmonics
    var fundamentalAmplitudeFluctuationRange = 0.05; // Slight fluctuation for fundamental
    var harmonicAmplitudeFluctuationRange = 0.1; // More pronounced for harmonics

    // Frequency fluctuation range for fundamental
    var frequencyFluctuationRange = 0.2; // Slight frequency fluctuation

    // Frequency modulation for the fundamental frequency
    frequencyModulation = LFNoise1.kr(0.2).range(-frequencyFluctuationRange, frequencyFluctuationRange);

    // Amplitude modulation for the fundamental frequency
    amplitudeModulation = LFNoise1.kr(0.1).range(1-fundamentalAmplitudeFluctuationRange, 1+fundamentalAmplitudeFluctuationRange);

    // Fundamental frequency with fluctuation in frequency and amplitude
    base = SinOsc.ar(fundamentalFreq + frequencyModulation, 0, amplitudeModulation * 0.3); // Adjust amplitude as needed

    // Generate harmonics with amplitude modulation
    harmonics = Array.fill(numHarmonics, { |i|
        var harmonicFreq = (i + 1) * fundamentalFreq;
        var harmonicAmplitudeMod = LFNoise1.kr(0.1).range(1-harmonicAmplitudeFluctuationRange, 1+harmonicAmplitudeFluctuationRange);
        SinOsc.ar(harmonicFreq, 0, harmonicAmplitudeMod * (0.15 / (i + 1))) // Decreasing amplitude for higher harmonics with modulation
    });

    // Mix the fundamental and the harmonics
    Mix([base] ++ harmonics)
}.play;
)
}

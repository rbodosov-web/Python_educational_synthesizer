import numpy as np

from synth.oscillator import Oscillator
from synth.envelope import ADSR


class Voice:

    def __init__(self, sample_rate=44100):

        self.sample_rate = sample_rate

        self.oscillator = Oscillator(
            sample_rate,
            waveform="sine"
        )

        self.envelope = ADSR(
            sample_rate,
            attack=0.01,
            decay=0.2,
            sustain=0.7,
            release=0.3
        )

        self.active = False
        self.frequency = 0.0

    def note_on(self, frequency):

        self.frequency = frequency

        self.oscillator.set_frequency(
            frequency
        )

        self.envelope.note_on()

        self.active = True

    def note_off(self):

        self.envelope.note_off()

    def generate(self, frames):

        wave = self.oscillator.generate(
            frames
        )

        envelope = np.array(
            self.envelope.generate(frames)
        )

        samples = wave * envelope

        # Если envelope закончился,
        # голос больше не считается активным.
        if self.envelope.state == "idle":
            self.active = False

        return samples
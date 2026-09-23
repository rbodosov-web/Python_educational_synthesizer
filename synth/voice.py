import numpy as np

from synth.oscillator import Oscillator
from synth.envelope import ADSR
from synth.filter import LowPassFilter
from synth.LFO import LFO


class Voice:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

        self.oscillator = Oscillator(
            sample_rate
        )

        self.filter = LowPassFilter(
            sample_rate,
            cutoff=2000.0
        )

        self.lfo = LFO(
            sample_rate,
            frequency=2.0
        )

        self.envelope = ADSR(
            sample_rate
        )

        self.frequency = 0.0
        self.active = False

        # -----------------------------------------------------
        # FILTER
        # -----------------------------------------------------

        self.base_cutoff = 2000.0

        # -----------------------------------------------------
        # LFO
        # -----------------------------------------------------

        self.lfo_enabled = True
        self.lfo_depth = 1500.0

    # ---------------------------------------------------------
    # NOTE
    # ---------------------------------------------------------

    def note_on(self, frequency):
        self.frequency = frequency
        self.active = True

        self.oscillator.set_frequency(
            frequency
        )

        self.envelope.note_on()

    def note_off(self):
        self.envelope.note_off()

    # ---------------------------------------------------------
    # OSCILLATOR
    # ---------------------------------------------------------

    def set_waveform(self, waveform):
        self.oscillator.set_waveform(
            waveform
        )

    # ---------------------------------------------------------
    # FILTER
    # ---------------------------------------------------------

    def set_cutoff(self, cutoff):
        self.base_cutoff = cutoff

        self.filter.set_cutoff(
            cutoff
        )

    # ---------------------------------------------------------
    # LFO
    # ---------------------------------------------------------

    def set_lfo_enabled(self, enabled):
        self.lfo_enabled = enabled

    def set_lfo_frequency(self, frequency):
        self.lfo.set_frequency(
            frequency
        )

    def set_lfo_depth(self, depth):
        self.lfo_depth = depth

    # ---------------------------------------------------------
    # ADSR
    # ---------------------------------------------------------

    def set_adsr(
        self,
        attack,
        decay,
        sustain,
        release
    ):
        self.envelope.attack = attack
        self.envelope.decay = decay
        self.envelope.sustain = sustain
        self.envelope.release = release

    # ---------------------------------------------------------
    # AUDIO
    # ---------------------------------------------------------

    def generate(self, frames):

        # -----------------------------------------------------
        # 1. OSCILLATOR
        # -----------------------------------------------------

        oscillator_signal = (
            self.oscillator.generate(
                frames
            )
        )

        # -----------------------------------------------------
        # 2. LFO
        # -----------------------------------------------------

        lfo_signal = self.lfo.generate(
            frames
        )

        if self.lfo_enabled:

            cutoff = (
                self.base_cutoff
                + lfo_signal
                * self.lfo_depth
            )

        else:

            cutoff = self.base_cutoff

        # -----------------------------------------------------
        # 3. FILTER
        # -----------------------------------------------------

        filtered_signal = (
            self.filter.process(
                oscillator_signal,
                cutoff
            )
        )

        # -----------------------------------------------------
        # 4. ADSR
        # -----------------------------------------------------

        envelope_signal = (
            self.envelope.generate(
                frames
            )
        )

        output = (
            filtered_signal
            * envelope_signal
        )

        # -----------------------------------------------------
        # 5. VOICE STATE
        # -----------------------------------------------------

        if self.envelope.state == "idle":
            self.active = False

        return output
    
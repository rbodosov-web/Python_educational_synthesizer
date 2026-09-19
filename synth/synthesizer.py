import numpy as np

from synth.voice import Voice


class Synthesizer:

    def __init__(
        self,
        sample_rate=44100,
        max_voices=8
    ):

        self.sample_rate = sample_rate
        self.max_voices = max_voices

        self.voices = [
            Voice(sample_rate)
            for _ in range(max_voices)
        ]

    def note_on(self, frequency):

        # Ищем свободный голос.
        for voice in self.voices:

            if not voice.active:

                voice.note_on(frequency)
                return

        # Если свободных голосов нет,
        # пока просто игнорируем новую ноту.

    def note_off(self, frequency):

        for voice in self.voices:

            if (
                voice.active
                and voice.frequency == frequency
            ):
                voice.note_off()
                return

    def generate(self, frames):

        output = np.zeros(frames)

        for voice in self.voices:

            if voice.active:

                output += voice.generate(
                    frames
                )

        return output
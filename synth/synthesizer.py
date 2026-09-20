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

        self.master_volume = 0.15

        self.voice_counter = 0

        self.voices = [
            Voice(sample_rate)
            for _ in range(max_voices)
        ]

    def note_on(self, key, frequency):

    # Ищем свободный Voice
        for voice in self.voices:

            if not voice.active:

                self.voice_counter += 1
                voice.start_time = self.voice_counter

                voice.note_on(frequency, key)

                return voice

        # -----------------------------------------
        # Свободных Voice нет → Voice Stealing
        # -----------------------------------------

        oldest_voice = min(
            self.voices,
            key=lambda voice: voice.start_time
        )

        print(
            f"Voice stealing: "
            f"{oldest_voice.frequency} Hz -> {frequency} Hz"
        )

        self.voice_counter += 1
        oldest_voice.start_time = self.voice_counter

        oldest_voice.note_on(frequency, key)

        return oldest_voice

    def note_off(self, key):

        for voice in self.voices:

            if voice.active and voice.key == key:
                voice.note_off()
                return

    def generate(self, frames):

        output = np.zeros(frames)

        for voice in self.voices:

            if voice.active:
                output += voice.generate(frames)

        output *= self.master_volume

        return output
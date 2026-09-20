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

        # Ищем свободный голос
        for voice in self.voices:

            if not voice.active:

                voice.note_on(frequency)

                # Возвращаем конкретный Voice,
                # который получил эту ноту
                return voice

        # Свободных голосов нет
        return None

    def note_off(self, voice):

        # Отпускаем именно тот Voice,
        # который принадлежит этой клавише
        if voice is not None:
            voice.note_off()

    def generate(self, frames):

        output = np.zeros(frames)

        for voice in self.voices:

            if voice.active:
                output += voice.generate(frames)

        return output
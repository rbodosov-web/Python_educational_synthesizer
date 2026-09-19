import numpy as np


class Oscillator:

    def __init__(self, sample_rate=44100, waveform="sine"):
        self.sample_rate = sample_rate
        self.frequency = 440.0
        self.phase = 0.0
        self.waveform = waveform

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_waveform(self, waveform):
        self.waveform = waveform

    def generate(self, frames):
        # Изменение фазы за один сэмпл
        phase_increment = (
            2 * np.pi * self.frequency / self.sample_rate
        )

        # Создаём номера сэмплов
        indices = np.arange(frames)

        # Вычисляем фазу каждого сэмпла
        phases = self.phase + indices * phase_increment

        if self.waveform == "sine":
            samples = np.sin(phases)

        elif self.waveform == "square":
            samples = np.where(
                np.sin(phases) >= 0,
                1.0,
                -1.0
            )

        elif self.waveform == "saw":
            samples = (
                2 * (phases / (2 * np.pi))
                - 1
            )

        elif self.waveform == "triangle":
            samples = (
                2 * np.abs(
                    2 * (phases / (2 * np.pi)) - 1
                ) - 1
            )

        else:
            raise ValueError(
                f"Unknown waveform: {self.waveform}"
    )
        # Запоминаем фазу,
        # на которой остановились
        self.phase = (
            phases[-1] + phase_increment
        ) % (2 * np.pi)

        return samples
    
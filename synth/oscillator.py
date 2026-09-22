import numpy as np


class Oscillator:
    def __init__(
        self,
        sample_rate=44100,
        frequency=440.0,
        waveform="sine"
    ):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.waveform = waveform
        self.phase = 0.0

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_waveform(self, waveform):
        self.waveform = waveform

    def generate(self, frames):
        # Создаём массив времени для текущего блока samples.
        time = np.arange(frames) / self.sample_rate

        # Фаза сигнала.
        phase = (
            2 * np.pi * self.frequency * time
            + self.phase
        )

        if self.waveform == "sine":
            wave = np.sin(phase)

        elif self.waveform == "square":
            wave = np.where(
                np.sin(phase) >= 0,
                1.0,
                -1.0
            )

        elif self.waveform == "saw":
            wave = 2 * (
                phase / (2 * np.pi)
                - np.floor(
                    phase / (2 * np.pi) + 0.5
                )
            )

        elif self.waveform == "triangle":
            wave = 2 * np.abs(
                2 * (
                    phase / (2 * np.pi)
                    - np.floor(
                        phase / (2 * np.pi) + 0.5
                    )
                )
            ) - 1

        else:
            # Если указана неизвестная форма,
            # используем sine.
            wave = np.sin(phase)

        # Запоминаем фазу последнего sample,
        # чтобы следующий блок продолжал предыдущий.
        self.phase = (
            phase[-1] + 2 * np.pi * self.frequency / self.sample_rate
        ) % (2 * np.pi)

        return wave
    
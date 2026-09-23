import numpy as np


class LFO:
    def __init__(
        self,
        sample_rate=44100,
        frequency=2.0
    ):
        self.sample_rate = sample_rate
        self.frequency = frequency

        self.phase = 0.0

    def set_frequency(self, frequency):
        self.frequency = frequency

    def generate(self, frames):
        # Время для текущего блока.
        time = np.arange(frames) / self.sample_rate

        phase = (
            2
            * np.pi
            * self.frequency
            * time
            + self.phase
        )

        output = np.sin(phase)

        # Сохраняем фазу для следующего блока.
        self.phase = (
            phase[-1]
            + 2
            * np.pi
            * self.frequency
            / self.sample_rate
        ) % (2 * np.pi)

        return output

import math
import numpy as np


class LowPassFilter:
    def __init__(
        self,
        sample_rate=44100,
        cutoff=2000.0
    ):
        self.sample_rate = sample_rate
        self.cutoff = cutoff

        # Состояние фильтра.
        self.previous_output = 0.0

    def set_cutoff(self, cutoff):
        """
        Устанавливает постоянный cutoff.
        """

        nyquist = self.sample_rate / 2

        self.cutoff = max(
            20.0,
            min(
                cutoff,
                nyquist - 100.0
            )
        )

    def process(
        self,
        signal,
        cutoff=None
    ):
        """
        Обрабатывает целый audio block.

        cutoff может быть:

        1. None
           Используем self.cutoff.

        2. Одно число
           Один cutoff для всего блока.

        3. numpy-массив
           Отдельный cutoff для каждого sample.
        """

        signal = np.asarray(
            signal,
            dtype=float
        )

        if cutoff is None:
            cutoff = self.cutoff

        # -----------------------------------------------------
        # Один cutoff для всего блока
        # -----------------------------------------------------

        if np.isscalar(cutoff):

            nyquist = self.sample_rate / 2

            cutoff = max(
                20.0,
                min(
                    cutoff,
                    nyquist - 100.0
                )
            )

            alpha = 1.0 - math.exp(
                -2.0
                * math.pi
                * cutoff
                / self.sample_rate
            )

            output = np.empty_like(
                signal
            )

            previous = (
                self.previous_output
            )

            for i, sample in enumerate(signal):
                previous = (
                    previous
                    + alpha * (
                        sample - previous
                    )
                )

                output[i] = previous

            self.previous_output = previous

            return output

        # -----------------------------------------------------
        # Меняющийся cutoff
        # -----------------------------------------------------

        cutoff = np.asarray(
            cutoff,
            dtype=float
        )

        nyquist = self.sample_rate / 2

        cutoff = np.clip(
            cutoff,
            20.0,
            nyquist - 100.0
        )

        alpha = (
            1.0
            - np.exp(
                -2.0
                * np.pi
                * cutoff
                / self.sample_rate
            )
        )

        output = np.empty_like(
            signal
        )

        previous = (
            self.previous_output
        )

        for i, sample in enumerate(signal):

            previous = (
                previous
                + alpha[i] * (
                    sample - previous
                )
            )

            output[i] = previous

        self.previous_output = previous

        return output
    

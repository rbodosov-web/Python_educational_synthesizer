import numpy as np


class Oscillator:

    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

        # Текущая частота осциллятора
        self.frequency = 440.0

        # Текущая фаза
        self.phase = 0.0

    def set_frequency(self, frequency):
        self.frequency = frequency

    def generate(self, frames):
        # Изменение фазы за один сэмпл
        phase_increment = (
            2 * np.pi * self.frequency / self.sample_rate
        )

        # Создаём номера сэмплов
        indices = np.arange(frames)

        # Вычисляем фазу каждого сэмпла
        phases = self.phase + indices * phase_increment

        # Генерируем синус
        samples = np.sin(phases)

        # Запоминаем фазу,
        # на которой остановились
        self.phase = (
            phases[-1] + phase_increment
        ) % (2 * np.pi)

        return samples
    
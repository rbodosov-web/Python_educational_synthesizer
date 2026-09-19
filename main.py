import numpy as np
import sounddevice as sd


# Частота дискретизации.
SAMPLE_RATE = 44100

# Частота ноты.
FREQUENCY = 440

# Продолжительность звука в секундах.
DURATION = 1


# Создаём временную шкалу.
# Получаем числа:
# 0, 1/44100, 2/44100, 3/44100, ...
time = np.arange(SAMPLE_RATE * DURATION) / SAMPLE_RATE


# Создаём синусоидальную волну.
wave = np.sin(2 * np.pi * FREQUENCY * time)


# Отправляем её на звуковое устройство.
sd.play(wave, SAMPLE_RATE)

# Ждём окончания воспроизведения.
sd.wait()

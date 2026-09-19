import numpy as np
import sounddevice as sd
from pynput import keyboard


# -------------------------
# Настройки синтезатора
# -------------------------

SAMPLE_RATE = 44100

# Сопоставляем клавиши компьютера с нотами.

KEY_TO_FREQUENCY = {
    'a': 261.63,  # C4
    's': 293.66,  # D4
    'd': 329.63,  # E4
    'f': 349.23,  # F4
    'g': 392.00,  # G4
    'h': 440.00,  # A4
    'j': 493.88,  # B4
    'k': 523.25,  # C5
}


# -------------------------
# Состояние синтезатора
# -------------------------

current_frequency = None


# -------------------------
# Обработка клавиатуры
# -------------------------

def on_press(key):
    global current_frequency

    try:
        if key.char in KEY_TO_FREQUENCY:
            current_frequency = KEY_TO_FREQUENCY[key.char]
            print(f"Playing {key.char}: {current_frequency} Hz")

    except AttributeError:
        pass


def on_release(key):
    global current_frequency

    try:
        if key.char in KEY_TO_FREQUENCY:
            current_frequency = None

    except AttributeError:
        pass

    # ESC завершает программу
    if key == keyboard.Key.esc:
        return False


# -------------------------
# Создаём аудиопоток
# -------------------------

phase = 0.0


def audio_callback(outdata, frames, time, status):
    global phase

    if status:
        print(status)

    # Пока никакая клавиша не нажата —
    # отправляем тишину.
    if current_frequency is None:
        outdata[:] = 0
        return

    # Создаём массив времени для этого блока.
    t = (
        np.arange(frames) + phase
    ) / SAMPLE_RATE

    # Генерируем синусоиду.
    wave = np.sin(
        2 * np.pi * current_frequency * t
    )

    # Немного уменьшаем громкость,
    # чтобы сигнал не был слишком сильным.
    wave *= 0.2

    # Передаём звук на выход.
    outdata[:, 0] = wave

    # Сохраняем фазу для следующего блока.
    phase += frames


# -------------------------
# Запускаем программу
# -------------------------

print("My Synth")
print("Use A S D F G H J K to play.")
print("Press ESC to exit.")


with sd.OutputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    callback=audio_callback
):
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    ) as listener:

        listener.join()
        
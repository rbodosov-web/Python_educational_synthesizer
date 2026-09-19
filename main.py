import numpy as np
import sounddevice as sd
from pynput import keyboard

from synth.oscillator import Oscillator

from synth.envelope import ADSR


# -------------------------
# Настройки синтезатора
# -------------------------

SAMPLE_RATE = 44100

oscillator = Oscillator(
    SAMPLE_RATE
)
envelope = ADSR(
    SAMPLE_RATE,
    attack=0.05,
    decay=0.2,
    sustain=0.7,
    release=0.5
)
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

            oscillator.set_frequency(current_frequency)
            envelope.note_on()
            
            print(f"Playing {key.char}: {current_frequency} Hz")

    except AttributeError:
        pass


def on_release(key):
    global current_frequency

    try:
        if key.char in KEY_TO_FREQUENCY:

            envelope.note_off()

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

    if status:
        print(status)

    wave = oscillator.generate(frames)

    envelope_signal = np.array(
        envelope.generate(frames)
    )

    wave *= envelope_signal

    wave *= 0.2

    outdata[:, 0] = wave


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
        
import sounddevice as sd
from pynput import keyboard

from synth.synthesizer import Synthesizer


SAMPLE_RATE = 44100


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


synth = Synthesizer(
    SAMPLE_RATE,
    max_voices=8
)

pressed_keys = set()

def on_press(key):
    try:
        if key.char in KEY_TO_FREQUENCY:

            if key.char in pressed_keys:
                return

            pressed_keys.add(key.char)

            frequency = KEY_TO_FREQUENCY[key.char]

            synth.note_on(
                key.char,
                frequency
            )

            print(
                f"Note ON: "
                f"{key.char} {frequency} Hz"
            )

    except AttributeError:
        pass


def on_release(key):
    try:
        if key.char in KEY_TO_FREQUENCY:

            pressed_keys.discard(key.char)

            synth.note_off(key.char)

            print(
                f"Note OFF: {key.char}"
            )

    except AttributeError:
        pass

    if key == keyboard.Key.esc:
        return False


def audio_callback(
    outdata,
    frames,
    time,
    status
):

    if status:
        print(status)

    samples = synth.generate(frames)

    outdata[:, 0] = samples


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
        
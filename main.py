import sounddevice as sd
import threading
import tkinter as tk

from synth.synthesizer import Synthesizer
from synth.gui import SynthGUI


SAMPLE_RATE = 44100


synth = Synthesizer(
    SAMPLE_RATE,
    max_voices=8
)


def audio_callback(
    outdata,
    frames,
    time,
    status
):
    if status:
        print(status)

    samples = synth.generate(
        frames
    )

    outdata[:, 0] = samples


def main():
    gui = SynthGUI(synth)

    with sd.OutputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback
    ):
        gui.run()


if __name__ == "__main__":
    main()
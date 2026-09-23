import numpy as np

from synth.voice import Voice


class Synthesizer:
    def __init__(self, sample_rate=44100, max_voices=8):
        self.sample_rate = sample_rate
        self.max_voices = max_voices

        self.voices = [
            Voice(sample_rate)
            for _ in range(max_voices)
        ]

        self.master_volume = 0.15

        self.waveform = "sine"

        # Какая клавиша сейчас играет на каком voice.
        #
        # Например:
        # {
        #     "a": 2,
        #     "d": 5
        # }
        #
        # Это означает:
        # A -> voice 2
        # D -> voice 5
        self.key_to_voice = {}

        # FILTER
        self.cutoff = 2000.0

        # LFO
        self.lfo_enabled = True
        self.lfo_frequency = 2.0
        self.lfo_depth = 1500.0

        # ADSR
        self.attack = 0.01
        self.decay = 0.1
        self.sustain = 0.7
        self.release = 0.2

        # Начальные параметры.
        for voice in self.voices:
            voice.set_waveform(self.waveform)

            voice.set_cutoff(self.cutoff)

            voice.set_lfo_frequency(
                self.lfo_frequency
            )

            voice.set_lfo_depth(
                self.lfo_depth
            )

            voice.set_lfo_enabled(
                self.lfo_enabled
            )

            voice.set_adsr(
                self.attack,
                self.decay,
                self.sustain,
                self.release
            )

    # ---------------------------------------------------------
    # OSCILLATOR
    # ---------------------------------------------------------

    def set_waveform(self, waveform):
        self.waveform = waveform

        for voice in self.voices:
            voice.set_waveform(waveform)

    # ---------------------------------------------------------
    # FILTER
    # ---------------------------------------------------------

    def set_cutoff(self, cutoff):
        self.cutoff = cutoff

        for voice in self.voices:
            voice.set_cutoff(cutoff)

    # ---------------------------------------------------------
    # LFO
    # ---------------------------------------------------------

    def set_lfo_enabled(self, enabled):
        self.lfo_enabled = enabled

        for voice in self.voices:
            voice.set_lfo_enabled(enabled)

    def set_lfo_frequency(self, frequency):
        self.lfo_frequency = frequency

        for voice in self.voices:
            voice.set_lfo_frequency(frequency)

    def set_lfo_depth(self, depth):
        self.lfo_depth = depth

        for voice in self.voices:
            voice.set_lfo_depth(depth)

    # ---------------------------------------------------------
    # ADSR
    # ---------------------------------------------------------

    def set_attack(self, attack):
        self.attack = attack

        for voice in self.voices:
            voice.set_adsr(
                attack,
                self.decay,
                self.sustain,
                self.release
            )

    def set_decay(self, decay):
        self.decay = decay

        for voice in self.voices:
            voice.set_adsr(
                self.attack,
                decay,
                self.sustain,
                self.release
            )

    def set_sustain(self, sustain):
        self.sustain = sustain

        for voice in self.voices:
            voice.set_adsr(
                self.attack,
                self.decay,
                sustain,
                self.release
            )

    def set_release(self, release):
        self.release = release

        for voice in self.voices:
            voice.set_adsr(
                self.attack,
                self.decay,
                self.sustain,
                release
            )

    # ---------------------------------------------------------
    # VOLUME
    # ---------------------------------------------------------

    def set_master_volume(self, volume):
        self.master_volume = volume

    # ---------------------------------------------------------
    # NOTES
    # ---------------------------------------------------------

    def note_on(self, frequency, key):
        # Если клавиша уже играет, не создаём
        # дополнительный voice.
        if key in self.key_to_voice:
            return

        # Ищем свободный voice.
        for index, voice in enumerate(self.voices):

            if not voice.active:
                voice.note_on(frequency)

                self.key_to_voice[key] = index

                return

        # Все voices заняты.
        #
        # Voice stealing мы специально НЕ используем.
        return

    def note_off(self, key):
        # Находим voice, которому принадлежит
        # именно эта клавиша.
        if key not in self.key_to_voice:
            return

        voice_index = self.key_to_voice.pop(key)

        voice = self.voices[voice_index]

        voice.note_off()

    # ---------------------------------------------------------
    # AUDIO
    # ---------------------------------------------------------

    def generate(self, frames):
        output = np.zeros(frames)

        for voice in self.voices:
            if voice.active:
                output += voice.generate(frames)

        output *= self.master_volume

        return output

    # ---------------------------------------------------------
    # INFORMATION FOR GUI
    # ---------------------------------------------------------

    def get_active_voice_count(self):
        return sum(
            1
            for voice in self.voices
            if voice.active
        )
    
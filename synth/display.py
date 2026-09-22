import os


class Display:
    def __init__(self, synth):
        self.synth = synth

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def draw_waveform(self):
        waveform = self.synth.waveform

        if waveform == "sine":
            return [
                "          ╭────╮          ╭────╮",
                "        ╭─╯    ╰─╮      ╭─╯    ╰─╮",
                "───────╯          ╰────╯          ╰────",
            ]

        if waveform == "square":
            return [
                "     ┌──────────┐      ┌──────────┐",
                "─────┘          └──────┘          └────",
                "     │          │      │          │",
            ]

        if waveform == "saw":
            return [
                "       ╱│       ╱│       ╱│",
                "     ╱  │     ╱  │     ╱  │",
                "───╱────│───╱────│───╱────│────────",
            ]

        if waveform == "triangle":
            return [
                "        ╱╲        ╱╲        ╱╲",
                "       ╱  ╲      ╱  ╲      ╱  ╲",
                "──────╱────╲────╱────╲────╱────╲────",
            ]

        return []

    def draw_adsr(self):
        attack = self.synth.voices[0].envelope.attack
        decay = self.synth.voices[0].envelope.decay
        sustain = self.synth.voices[0].envelope.sustain
        release = self.synth.voices[0].envelope.release

        total_width = 38

        total_time = (
            attack
            + decay
            + 1.0
            + release
        )

        attack_width = max(
            1,
            int(total_width * attack / total_time)
        )

        decay_width = max(
            1,
            int(total_width * decay / total_time)
        )

        sustain_width = max(
            1,
            int(total_width * 1.0 / total_time)
        )

        release_width = max(
            1,
            int(total_width * release / total_time)
        )

        top = (
            " " * attack_width
            + "╱"
            + "─" * decay_width
            + "╲"
        )

        middle = (
            " " * (attack_width + 1)
            + "╲"
            + "─" * sustain_width
            + "╲"
        )

        bottom = (
            "╱"
            + "─" * release_width
        )

        return [
            "1.0 ┤" + top,
            f"{sustain:.1f} ┤" + middle,
            "0.0 ┼" + bottom,
            "    └────────────────────────────────────",
            "       A        D          S          R",
        ]

    def draw_keyboard(self):
        key_names = [
            ("A", "C4"),
            ("S", "D4"),
            ("D", "E4"),
            ("F", "F4"),
            ("G", "G4"),
            ("H", "A4"),
            ("J", "B4"),
            ("K", "C5"),
        ]

        line = ""

        for key, note in key_names:
            playing = key.lower() in self.synth.playing_keys

            if playing:
                line += f"  [{key}:{note}] "
            else:
                line += f"   {key}:{note}  "

        return line

    def draw(self):
        self.clear()

        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                         M Y   S Y N T H                      ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║                                                              ║")

        print(
            f"║  OSCILLATOR                    ENVELOPE                      ║"
        )
        print("║  ──────────                    ────────                      ║")
        print("║                                                              ║")

        waveform_text = f"Waveform: {self.synth.waveform.upper()}"

        print(f"║  {waveform_text:<28} ADSR:                         ║")

        waveform = self.draw_waveform()

        for line in waveform:
            print(f"║  {line:<28}                          ║")

        print("║                                                              ║")
        print("║  [1] Sine       [2] Square                                   ║")
        print("║  [3] Saw        [4] Triangle                                 ║")

        print("║                                                              ║")
        print("╠══════════════════════════════════════════════════════════════╣")

        print("║  ENVELOPE                                                    ║")
        print("║                                                              ║")

        envelope = self.draw_adsr()

        for line in envelope:
            print(f"║    {line:<58}║")

        print("║                                                              ║")
        print("╠══════════════════════════════════════════════════════════════╣")

        print("║  KEYBOARD                                                    ║")
        print("║                                                              ║")

        keyboard_line = self.draw_keyboard()

        print(f"║  {keyboard_line:<58}║")

        print("║                                                              ║")
        print("╠══════════════════════════════════════════════════════════════╣")

        active_voices = sum(
            1
            for voice in self.synth.voices
            if voice.active
        )

        volume_bar_length = int(
            self.synth.master_volume * 20
        )

        volume_bar = (
            "█" * volume_bar_length
            + "░" * (20 - volume_bar_length)
        )

        print(
            f"║  VOICES   {active_voices} / "
            f"{self.synth.max_voices:<3}"
            f"                    VOLUME  {volume_bar}  ║"
        )

        print("║                                                              ║")
        print("║  [1-4] waveform     [A-K] play     [ESC] quit                ║")
        print("╚══════════════════════════════════════════════════════════════╝")

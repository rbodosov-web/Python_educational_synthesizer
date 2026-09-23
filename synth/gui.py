import tkinter as tk
import math


class Knob(tk.Frame):
    def __init__(
        self,
        parent,
        label,
        minimum,
        maximum,
        value,
        command,
        unit="",
        size=90
    ):
        super().__init__(
            parent,
            bg="#111111"
        )

        self.minimum = minimum
        self.maximum = maximum
        self.value = value
        self.default = value

        self.command = command
        self.unit = unit

        self.size = size

        self.drag_start_y = None
        self.drag_start_value = None

        self.canvas = tk.Canvas(
            self,
            width=size,
            height=size,
            bg="#111111",
            highlightthickness=0
        )

        self.canvas.pack()

        self.label = tk.Label(
            self,
            text=label,
            bg="#111111",
            fg="#dddddd",
            font=("Arial", 10)
        )

        self.label.pack()

        self.value_label = tk.Label(
            self,
            text="",
            bg="#111111",
            fg="#ffffff",
            font=("Consolas", 10)
        )

        self.value_label.pack()

        self.canvas.bind(
            "<Button-1>",
            self.on_press
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.on_drag
        )

        self.canvas.bind(
            "<ButtonRelease-1>",
            self.on_release
        )

        self.canvas.bind(
            "<Double-Button-1>",
            self.reset
        )

        self.draw()

    def on_press(self, event):
        self.drag_start_y = event.y
        self.drag_start_value = self.value

    def on_drag(self, event):
        if self.drag_start_y is None:
            return

        delta = (
            self.drag_start_y
            - event.y
        )

        sensitivity = (
            self.maximum
            - self.minimum
        ) / 200.0

        new_value = (
            self.drag_start_value
            + delta * sensitivity
        )

        self.set_value(
            new_value,
            call_command=True
        )

    def on_release(self, event):
        self.drag_start_y = None
        self.drag_start_value = None

    def reset(self, event):
        self.set_value(
            self.default,
            call_command=True
        )

    def set_value(
        self,
        value,
        call_command=False
    ):
        value = max(
            self.minimum,
            min(self.maximum, value)
        )

        self.value = value

        self.draw()

        if call_command:
            self.command(value)

    def draw(self):
        self.canvas.delete("all")

        center = self.size / 2

        radius = (
            self.size / 2
            - 10
        )

        # Угол:
        #
        # минимум = -135°
        # максимум = +135°
        #
        # В tkinter Canvas углы идут
        # по часовой стрелке от 3 часов.
        start_angle = -225
        total_angle = 270

        ratio = (
            self.value - self.minimum
        ) / (
            self.maximum - self.minimum
        )

        angle = (
            start_angle
            + ratio * total_angle
        )

        # Фоновая дуга.
        self.canvas.create_arc(
            center - radius,
            center - radius,
            center + radius,
            center + radius,
            start=start_angle,
            extent=total_angle,
            style=tk.ARC,
            outline="#444444",
            width=8
        )

        # Активная дуга.
        self.canvas.create_arc(
            center - radius,
            center - radius,
            center + radius,
            center + radius,
            start=start_angle,
            extent=ratio * total_angle,
            style=tk.ARC,
            outline="#ffffff",
            width=8
        )

        # Ручка.
        rad = math.radians(angle)

        knob_radius = radius - 15

        x = (
            center
            + math.cos(rad) * knob_radius
        )

        y = (
            center
            - math.sin(rad) * knob_radius
        )

        self.canvas.create_line(
            center,
            center,
            x,
            y,
            fill="#ffffff",
            width=3
        )

        # Центральная точка.
        self.canvas.create_oval(
            center - 5,
            center - 5,
            center + 5,
            center + 5,
            fill="#ffffff",
            outline=""
        )

        self.value_label.config(
            text=self.format_value()
        )

    def format_value(self):
        if self.unit == "%":
            return f"{self.value:.0f}%"

        if self.unit == "Hz":
            return f"{self.value:.0f} Hz"

        if self.unit == "s":
            return f"{self.value:.2f} s"

        return f"{self.value:.2f}"


class SynthGUI:
    def __init__(self, synth):
        self.synth = synth

        self.root = tk.Tk()

        self.root.title("MAGA synth 1.0 — by R. B.")

        self.root.geometry(
            "850x650"
        )

        self.root.configure(
            bg="#111111"
        )

        self.root.resizable(
            False,
            False
        )

        self.build_interface()

        # Клавиатура.
        self.root.bind(
            "<KeyPress>",
            self.on_key_press
        )

        self.root.bind(
            "<KeyRelease>",
            self.on_key_release
        )

        # Регулярно обновляем информацию
        # о voices.
        self.update_status()

    # ---------------------------------------------------------
    # INTERFACE
    # ---------------------------------------------------------

    def build_interface(self):

        title = tk.Label(
            self.root,
            text="M A G A  S Y N T H  1.0 — by R. B.",
            bg="#111111",
            fg="#ffffff",
            font=(
                "Arial",
                22,
                "bold"
            )
        )

        title.pack(
            pady=(20, 10)
        )

        # -----------------------------------------------------
        # OSCILLATOR
        # -----------------------------------------------------

        oscillator_frame = tk.Frame(
            self.root,
            bg="#111111"
        )

        oscillator_frame.pack(
            pady=10
        )

        tk.Label(
            oscillator_frame,
            text="OSCILLATOR",
            bg="#111111",
            fg="#aaaaaa",
            font=(
                "Arial",
                10,
                "bold"
            )
        ).pack()

        waveform_frame = tk.Frame(
            oscillator_frame,
            bg="#111111"
        )

        waveform_frame.pack(
            pady=5
        )

        self.waveform_var = tk.StringVar(
            value=self.synth.waveform
        )

        for waveform in [
            "sine",
            "square",
            "saw",
            "triangle"
        ]:
            tk.Radiobutton(
                waveform_frame,
                text=waveform.upper(),
                variable=self.waveform_var,
                value=waveform,
                command=self.change_waveform,
                bg="#111111",
                fg="#dddddd",
                selectcolor="#222222",
                activebackground="#111111",
                activeforeground="#ffffff"
            ).pack(
                side=tk.LEFT,
                padx=8
            )

        # -----------------------------------------------------
        # FILTER
        # -----------------------------------------------------

        filter_frame = tk.Frame(
            self.root,
            bg="#111111"
        )

        filter_frame.pack(
            pady=10
        )

        tk.Label(
            filter_frame,
            text="FILTER",
            bg="#111111",
            fg="#aaaaaa",
            font=(
                "Arial",
                10,
                "bold"
            )
        ).pack()

        filter_knobs = tk.Frame(
            filter_frame,
            bg="#111111"
        )

        filter_knobs.pack(
            pady=5
        )

        self.cutoff_knob = Knob(
            filter_knobs,
            "CUTOFF",
            100,
            10000,
            self.synth.cutoff,
            self.change_cutoff,
            "Hz"
        )

        self.cutoff_knob.pack(
            side=tk.LEFT,
            padx=20
        )

        self.lfo_frequency_knob = Knob(
            filter_knobs,
            "LFO FREQ",
            0.1,
            20.0,
            self.synth.lfo_frequency,
            self.change_lfo_frequency,
            "Hz"
        )

        self.lfo_frequency_knob.pack(
            side=tk.LEFT,
            padx=20
        )

        self.lfo_depth_knob = Knob(
            filter_knobs,
            "LFO DEPTH",
            0,
            5000,
            self.synth.lfo_depth,
            self.change_lfo_depth,
            "Hz"
        )

        self.lfo_depth_knob.pack(
            side=tk.LEFT,
            padx=20
        )

        # LFO switch.

        self.lfo_button = tk.Button(
            filter_frame,
            text="LFO: ON",
            command=self.toggle_lfo,
            bg="#dddddd",
            fg="#111111",
            width=12
        )

        self.lfo_button.pack(
            pady=5
        )

        # -----------------------------------------------------
        # ADSR
        # -----------------------------------------------------

        adsr_frame = tk.Frame(
            self.root,
            bg="#111111"
        )

        adsr_frame.pack(
            pady=10
        )

        tk.Label(
            adsr_frame,
            text="ADSR",
            bg="#111111",
            fg="#aaaaaa",
            font=(
                "Arial",
                10,
                "bold"
            )
        ).pack()

        adsr_knobs = tk.Frame(
            adsr_frame,
            bg="#111111"
        )

        adsr_knobs.pack(
            pady=5
        )

        self.attack_knob = Knob(
            adsr_knobs,
            "ATTACK",
            0.001,
            2.0,
            self.synth.attack,
            self.change_attack,
            "s"
        )

        self.attack_knob.pack(
            side=tk.LEFT,
            padx=10
        )

        self.decay_knob = Knob(
            adsr_knobs,
            "DECAY",
            0.001,
            2.0,
            self.synth.decay,
            self.change_decay,
            "s"
        )

        self.decay_knob.pack(
            side=tk.LEFT,
            padx=10
        )

        self.sustain_knob = Knob(
            adsr_knobs,
            "SUSTAIN",
            0,
            100,
            self.synth.sustain * 100,
            self.change_sustain,
            "%"
        )

        self.sustain_knob.pack(
            side=tk.LEFT,
            padx=10
        )

        self.release_knob = Knob(
            adsr_knobs,
            "RELEASE",
            0.001,
            3.0,
            self.synth.release,
            self.change_release,
            "s"
        )

        self.release_knob.pack(
            side=tk.LEFT,
            padx=10
        )

        # -----------------------------------------------------
        # VOLUME
        # -----------------------------------------------------

        volume_frame = tk.Frame(
            self.root,
            bg="#111111"
        )

        volume_frame.pack(
            pady=10
        )

        self.volume_knob = Knob(
            volume_frame,
            "MASTER",
            0,
            1,
            self.synth.master_volume,
            self.change_volume,
            ""
        )

        self.volume_knob.pack()

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        self.status_label = tk.Label(
            self.root,
            text="Voices: 0 / 8",
            bg="#111111",
            fg="#aaaaaa",
            font=(
                "Consolas",
                11
            )
        )

        self.status_label.pack(
            pady=10
        )

        tk.Label(
            self.root,
            text=(
                "A S D F G H J K  —  play"
                "        ESC  —  quit"
            ),
            bg="#111111",
            fg="#666666",
            font=(
                "Consolas",
                10
            )
        ).pack()

    # ---------------------------------------------------------
    # OSCILLATOR
    # ---------------------------------------------------------

    def change_waveform(self):
        self.synth.set_waveform(
            self.waveform_var.get()
        )

    # ---------------------------------------------------------
    # FILTER
    # ---------------------------------------------------------

    def change_cutoff(self, value):
        self.synth.set_cutoff(value)

    # ---------------------------------------------------------
    # LFO
    # ---------------------------------------------------------

    def change_lfo_frequency(self, value):
        self.synth.set_lfo_frequency(
            value
        )

    def change_lfo_depth(self, value):
        self.synth.set_lfo_depth(
            value
        )

    def toggle_lfo(self):
        self.synth.set_lfo_enabled(
            not self.synth.lfo_enabled
        )

        if self.synth.lfo_enabled:
            self.lfo_button.config(
                text="LFO: ON"
            )
        else:
            self.lfo_button.config(
                text="LFO: OFF"
            )

    # ---------------------------------------------------------
    # ADSR
    # ---------------------------------------------------------

    def change_attack(self, value):
        self.synth.set_attack(value)

    def change_decay(self, value):
        self.synth.set_decay(value)

    def change_sustain(self, value):
        self.synth.set_sustain(
            value / 100
        )

    def change_release(self, value):
        self.synth.set_release(value)

    # ---------------------------------------------------------
    # VOLUME
    # ---------------------------------------------------------

    def change_volume(self, value):
        self.synth.set_master_volume(
            value
        )

    # ---------------------------------------------------------
    # KEYBOARD
    # ---------------------------------------------------------

    def on_key_press(self, event):
        if event.keysym == "Escape":
            self.root.destroy()
            return

        key = event.char.lower()

        frequencies = {
            "a": 261.63,
            "s": 293.66,
            "d": 329.63,
            "f": 349.23,
            "g": 392.00,
            "h": 440.00,
            "j": 493.88,
            "k": 523.25,
            "w": 277.18,
            "e": 311.13,
            "t": 369.99,
            "y": 415.30,
            "u": 466.16,
        }

        if key in frequencies:
            self.synth.note_on(
                frequencies[key],
                key
            )

    def on_key_release(self, event):
        key = event.char.lower()

        if key in [
            "a",
            "s",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "w",
            "e",
            "t",
            "y",
            "u"
        ]:
            self.synth.note_off(key)

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def update_status(self):
        active = (
            self.synth.get_active_voice_count()
        )

        self.status_label.config(
            text=(
                f"Voices: "
                f"{active} / "
                f"{self.synth.max_voices}"
            )
        )

        self.root.after(
            50,
            self.update_status
        )

    # ---------------------------------------------------------
    # RUN
    # ---------------------------------------------------------

    def run(self):
        self.root.mainloop()
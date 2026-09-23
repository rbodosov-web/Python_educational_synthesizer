class ADSR:
    def __init__(
        self,
        sample_rate=44100,
        attack=0.01,
        decay=0.1,
        sustain=0.7,
        release=0.2
    ):
        self.sample_rate = sample_rate

        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release

        self.state = "idle"

        # Текущий уровень envelope.
        self.level = 0.0

        # Уровень, с которого начинается Release.
        self.release_start_level = 0.0

    # ---------------------------------------------------------
    # NOTE ON
    # ---------------------------------------------------------

    def note_on(self):
        self.state = "attack"

    # ---------------------------------------------------------
    # NOTE OFF
    # ---------------------------------------------------------

    def note_off(self):

        if self.state == "idle":
            return

        # Запоминаем реальный уровень envelope
        # именно в момент отпускания клавиши.
        self.release_start_level = (
            self.level
        )

        self.state = "release"

    # ---------------------------------------------------------
    # GENERATE
    # ---------------------------------------------------------

    def generate(self, frames):

        output = []

        for _ in range(frames):

            # =================================================
            # IDLE
            # =================================================

            if self.state == "idle":

                self.level = 0.0

            # =================================================
            # ATTACK
            # =================================================

            elif self.state == "attack":

                if self.attack <= 0:

                    self.level = 1.0
                    self.state = "decay"

                else:

                    self.level += (
                        1.0
                        / (
                            self.attack
                            * self.sample_rate
                        )
                    )

                    if self.level >= 1.0:

                        self.level = 1.0
                        self.state = "decay"

            # =================================================
            # DECAY
            # =================================================

            elif self.state == "decay":

                if self.decay <= 0:

                    self.level = self.sustain
                    self.state = "sustain"

                else:

                    self.level -= (
                        (
                            1.0
                            - self.sustain
                        )
                        / (
                            self.decay
                            * self.sample_rate
                        )
                    )

                    if self.level <= self.sustain:

                        self.level = self.sustain
                        self.state = "sustain"

            # =================================================
            # SUSTAIN
            # =================================================

            elif self.state == "sustain":

                self.level = self.sustain

            # =================================================
            # RELEASE
            # =================================================

            elif self.state == "release":

                if self.release <= 0:

                    self.level = 0.0
                    self.state = "idle"

                else:

                    self.level -= (
                        self.release_start_level
                        / (
                            self.release
                            * self.sample_rate
                        )
                    )

                    if self.level <= 0.0:

                        self.level = 0.0
                        self.state = "idle"

            output.append(
                self.level
            )

        return output
    
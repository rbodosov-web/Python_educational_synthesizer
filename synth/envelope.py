class ADSR:

    def __init__(
        self,
        sample_rate=44100,
        attack=1.0,
        decay=1.0,
        sustain=0.8,
        release=2.0,
    ):
        self.sample_rate = sample_rate

        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release

        self.state = "idle"
        self.level = 0.0

    def note_on(self):
        self.state = "attack"

    def note_off(self):
        self.state = "release"

    def generate(self, frames):

        output = []

        for _ in range(frames):

            if self.state == "idle":

                self.level = 0.0

            elif self.state == "attack":

                self.level += (
                    1.0 /
                    (self.attack * self.sample_rate)
                )

                if self.level >= 1.0:
                    self.level = 1.0
                    self.state = "decay"

            elif self.state == "decay":

                self.level -= (
                    (1.0 - self.sustain) /
                    (self.decay * self.sample_rate)
                )

                if self.level <= self.sustain:
                    self.level = self.sustain
                    self.state = "sustain"

            elif self.state == "sustain":

                self.level = self.sustain

            elif self.state == "release":

                self.level -= (
                    self.sustain /
                    (self.release * self.sample_rate)
                )

                if self.level <= 0.0:
                    self.level = 0.0
                    self.state = "idle"

            output.append(self.level)

        return output
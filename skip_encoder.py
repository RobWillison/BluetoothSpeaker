from encoder import Encoder

class SkipEncoder:
    def __init__(leftPin, rightPin, player):
        self.last_tick = None
        self.tick_count = 0
        self.encoder = Encoder(leftPin, rightPin, self.onChange)

    def onChange(self, value, direction):
        print(value)

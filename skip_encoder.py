from encoder import Encoder
import time

class SkipEncoder:
    def __init__(self, leftPin, rightPin, player):
        self.last_tick = 0
        self.tick_count = 0
        self.encoder = Encoder(leftPin, rightPin, self.onChange)

    def onChange(self, value, direction):
        now = time.time()
        if now > self.last_tick + 1:
            self.tick_count = 0

        self.last_tick = now
        self.tick_count += direction

        print(self.tick_count)

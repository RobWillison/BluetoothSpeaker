from encoder import Encoder
import time

class SkipNStettingEncoder:
    def __init__(self, leftPin, rightPin, button, player):
        self.last_tick = 0
        self.tick_count = 0
        self.encoder = Encoder(leftPin, rightPin, self.onChange)
        self.player = player
        self.mode = 'SKIP'

        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button, GPIO.FALLING, callback=p.togglePaused)

    def handleSkip(self, direction):
        now = time.time()
        if now > self.last_tick + 1:
            self.tick_count = 0

        self.last_tick = now
        self.tick_count += direction

        if self.tick_count < -10:
            self.tick_count = 0
            self.player.next()
            print('Next')

        if self.tick_count > 10:
            self.tick_count = 0
            self.player.prev()
            print('Prev')

    def onChange(self, value, direction):
        if self.mode == 'SKIP':
            handleSkip(direction)

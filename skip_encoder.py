from encoder import Encoder
import time
import RPi.GPIO as GPIO

class SkipNStettingEncoder:
    def __init__(self, leftPin, rightPin, button, player):
        self.last_tick = 0
        self.tick_count = 0
        self.encoder = Encoder(leftPin, rightPin, self.onChange)
        self.player = player
        self.mode = 'SKIP'

        self.button = button
        self.button_down_time = 0
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button, GPIO.BOTH, callback=player.togglePaused)

    def handlePress(self):
        if GPIO.input(button):
            self.button_down_time = time.time()
        else:
            print('Button down for' + str(time.time() - self.button_down_time))


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
            self.handleSkip(direction)

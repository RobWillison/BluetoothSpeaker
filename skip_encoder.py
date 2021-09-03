from encoder import Encoder
import time
import RPi.GPIO as GPIO

class SkipNStettingEncoder:
    def __init__(self, leftPin, rightPin, button, player, settings):
        self.last_tick = 0
        self.tick_count = 0
        self.encoder = Encoder(leftPin, rightPin, self.onChange)
        self.player = player
        self.mode = 'SKIP'

        self.button_down_time = 0
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button, GPIO.BOTH, callback=self.handlePress, bouncetime=10)

    def handlePress(self, pin):
        if GPIO.input(pin):
            self.button_down_time = time.time()
        else:
            duration = time.time() - self.button_down_time
            if duration < 2:
                self.player.togglePaused()
            else:
                self.settings.openClose()
                if self.mode == 'SKIP':
                    self.mode = 'SETTINGS'
                else:
                    self.mode = 'SKIP'


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

    def handleSettings(self, direction):
        self.settings.move(direction)

    def onChange(self, value, direction):
        if self.mode == 'SKIP':
            self.handleSkip(direction)
        if self.mode == 'SETTINGS':
            self.handleSettings(direction)

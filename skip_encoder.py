from encoder import Encoder
import time
import RPi.GPIO as GPIO

class SkipNStettingEncoder:
    def __init__(self, leftPin, rightPin, button, player, settings):
        self.last_tick = 0
        self.tick_count = 0

        self.last_click = 0
        self.encoder = Encoder(leftPin, rightPin, self.onChange)
        self.player = player
        self.settings = settings
        self.mode = 'SKIP'

        self.button_down_time = 0
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button, GPIO.RISING, callback=self.handlePress, bouncetime=500)

    def handlePress(self, pin):
        now = time.time()
        if (now - self.last_click) < 1:
            return

        self.last_click = now

        print('CLICKED')

        duration = 0
        while GPIO.input(pin):
            time.sleep(0.25)
            duration += 0.25

        if duration < 2:
            if self.mode == 'SKIP':
                self.player.togglePaused()
            if self.mode == 'SETTINGS':
                self.settings.click()
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
        print(self.tick_count)
        if self.tick_count < -5:
            self.tick_count = 0
            self.player.next()
            print('Next')

        if self.tick_count > 5:
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

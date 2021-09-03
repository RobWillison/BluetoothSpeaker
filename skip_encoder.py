from encoder import Encoder
import time
import RPi.GPIO as GPIO
import threading

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
        self.buttonLock = threading.Lock()
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button, GPIO.RISING, callback=self.handlePress, bouncetime=500)

    def handlePress(self, pin):
        print('CLICKED')
        if not self.buttonLock.acquire(False):
            return

        now = time.time()
        print(now - self.last_click)
        if (now - self.last_click) < 1:
            self.buttonLock.release()
            return

        duration = 0
        while GPIO.input(pin):
            time.sleep(0.25)
            duration += 0.25

            if duration > 2:
                self.settings.openClose()
                if self.mode == 'SKIP':
                    self.mode = 'SETTINGS'
                else:
                    self.mode = 'SKIP'
                break

        print('duration ' + str(duration))
        if duration < 2:
            if self.mode == 'SKIP':
                self.player.togglePaused()
            if self.mode == 'SETTINGS':
                self.settings.click()


        self.last_click = now
        self.buttonLock.release()


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

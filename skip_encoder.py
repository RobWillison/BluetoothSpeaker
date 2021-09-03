from encoder import Encoder
import time
import RPi.GPIO as GPIO
import threading

class SkipNStettingEncoder:
    def __init__(self, leftPin, rightPin, button):
        self.last_tick = 0
        self.tick_count = 0

        self.last_click = 0
        self.encoder = Encoder(leftPin, rightPin, self.onChange)
        self.longPress = []
        self.shortPress = []
        self.turn = []
        self.mode = 'SKIP'

        self.button_down_time = 0
        self.buttonLock = threading.Lock()
        GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(button, GPIO.RISING, callback=self.handlePress, bouncetime=500)

    def addLongPressCallback(self, callback):
        self.longPress.append(callback)

    def addShortPressCallback(self, callback):
        self.shortPress.append(callback)

    def addTurnCallback(self, callback):
        self.turn.append(callback)

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

            if duration == 2:
                [callback() for callback in self.longPress]

        print('duration ' + str(duration))
        if duration < 2:
            [callback() for callback in self.shortPress]


        self.last_click = now
        self.buttonLock.release()

    def onChange(self, value, direction):
        [callback(direction) for callback in self.turn]

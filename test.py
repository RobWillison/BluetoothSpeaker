import board
import RPi.GPIO as GPIO
import time
from player import Player
from display import Display

d = Display()
p = Player(d.trackChanged, d.pausedStatusChanged)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)

pausePlayButton = 17
GPIO.setup(pausePlayButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pausePlayButton, GPIO.FALLING, callback=p.togglePaused)

while True:
    time.sleep(1)

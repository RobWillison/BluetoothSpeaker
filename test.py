import board
import RPi.GPIO as GPIO
import time
from player import Player
from display import Display
from skip_encoder import SkipNStettingEncoder

def encoderMoved(current, change):
    print(change)

d = Display()
p = Player(d.trackChanged, d.pausedStatusChanged)
e = SkipNStettingEncoder(4, 22, 17, p)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)

while True:
    time.sleep(1)

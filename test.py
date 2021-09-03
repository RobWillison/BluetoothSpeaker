import board
import RPi.GPIO as GPIO
import time
from player import Player
from display import Display
from skip_encoder import SkipNStettingEncoder
from settings import SettingsState
from bluetooth_player_state import BluetoothPlayerState

def encoderMoved(current, change):
    print(change)

d = Display()
p = Player()
e = SkipNStettingEncoder(4, 22, 17)

s = SettingsState(d, p, e)
bp = BluetoothPlayerState(d, p, e)

bp.activate()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)

while True:
    time.sleep(1)

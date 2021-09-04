import board
import RPi.GPIO as GPIO
import time
from player import Player
from display import Display
from skip_encoder import SkipNStettingEncoder
from settings import SettingsState
from bluetooth_player_state import BluetoothPlayerState

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)

class Radio:
    def __init__(self):
        self.display = Display()
        self.player = Player()
        self.encoder = SkipNStettingEncoder(4, 22, 17)

        self.settings_state = SettingsState(self.display, self.player, self.encoder)
        self.player_state = BluetoothPlayerState(self.display, self.player, self.encoder)
        self.player_state.activate()
        self.currentState = 'PLAYER'

        self.encoder.addLongPressCallback(self.longPress)

    def longPress(self):
        if self.currentState == 'PLAYER':
            self.player_state.deactivate()
            self.settings_state.activate()
        else:
            self.settings_state.deactivate()
            self.player_state.activate()

    def run():
        while True:
            time.sleep(1)


Radio().run()

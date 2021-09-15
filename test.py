import board
import RPi.GPIO as GPIO
import time
from player import Player
from display import Display
from skip_encoder import SkipNStettingEncoder
from volume_encoder import VolumeEncoder
from settings import SettingsState
from bluetooth_player_state import BluetoothPlayerState

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)

GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.HIGH)

class Radio:
    def __init__(self):
        self.display = Display()
        self.player = Player()
        self.encoder = SkipNStettingEncoder(4, 10, 17)
        self.volume_encoder = VolumeEncoder(23, 24, 15)

        self.settings_state = SettingsState(self.display, self.player, self.encoder)
        self.player_state = BluetoothPlayerState(self.display, self.player, self.encoder, self.volume_encoder)
        self.player_state.activate()
        self.currentState = 'PLAYER'

        self.encoder.addLongPressCallback(self.longPress)

    def longPress(self):
        if self.currentState == 'PLAYER':
            self.currentState = 'SETTINGS'
            self.player_state.deactivate()
            self.settings_state.activate()
        else:
            self.currentState = 'PLAYER'
            self.settings_state.deactivate()
            self.player_state.activate()

    def run(self):
        while True:
            time.sleep(1)


Radio().run()

import time
import adafruit_max9744

class BluetoothPlayerState:
    def __init__(self, display, player, encoder, volume_encoder):
        self.display = display
        self.player = player
        self.encoder = encoder
        self.volume_encoder = volume_encoder

        self.encoder.addShortPressCallback(self.togglePause)
        self.encoder.addTurnCallback(self.onEncoderTick)
        self.player.addUpdateCallback(self.displayTrackInfo)
        self.volume_encoder.addTurnCallback(self.changeVolume)

        self.last_tick = 0
        self.tick_count = 0

        self.active = False

        # Initialize I2C bus.
        i2c = busio.I2C(board.SCL, board.SDA)

        # Initialize amplifier.
        self.amp = adafruit_max9744.MAX9744(i2c)

    def togglePause(self):
        if not self.active:
            return

        line1 = [-1]*16
        line2 = [-1]*16

        if self.player.paused:
            line1[15] = 32
        else:
            line1[15] = 0

        self.player.togglePaused()
        self.display.writeData(line1, line2)

    def activate(self):
        self.active = True
        self.displayTrackInfo()

    def deactivate(self):
        self.active = False

    def displayTrackInfo(self):
        if not self.active:
            return

        title = self.player.title
        artist = self.player.artist
        self.runTrackChangeAnimation(title, artist)

    def runTrackChangeAnimation(self, newTrack, newArtist):
        newState = [[],[]]
        newState[0] = bytearray(self.display.cropText(newTrack).ljust(16), 'utf-8')
        newState[1] = bytearray(self.display.cropText(newArtist).ljust(16), 'utf-8')

        frames = []
        for i in range(16, -1, -1):
            frame = [[], []]

            frame[0] = [-1]*i + list(newState[0][i:-1])
            frame[1] = [-1]*i + list(newState[1][i:-1])

            frames.append(frame)

        self.display.addFrames(frames)

    def onEncoderTick(self, direction):
        if not self.active:
            return

        now = time.time()
        if now - self.last_tick > 1:
            self.tick_count = 0

        self.last_tick = now
        self.tick_count -= direction

        print(self.tick_count)

        if self.tick_count > 5:
            self.player.next()
            self.tick_count = 0
        if self.tick_count < -5:
            self.player.prev()
            self.tick_count = 0

    def changeVolume(self, direction):
        if direction == 1:
            self.amp.volume_up()
        else:
            self.amp.volume_down()

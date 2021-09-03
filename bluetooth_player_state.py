

class BluetoothPlayerState:
    def __init__(self, display, player, encoder):
        self.display = display
        self.player = player
        self.encoder = encoder

        self.encoder.addShortPressCallback(self.togglePause)
        self.encoder.addTurnCallback(self.onEncoderTick)
        self.player.addUpdateCallback(self.displayTrackInfo)

        self.last_tick = 0
        self.tick_count = 0

    def togglePause(self):
        line1 = [-1]*16
        line2 = [-1]*16

        if self.player.paused:
            line1[15] = 32
        else:
            line1[15] = 0

        self.player.togglePaused()
        self.display.writeData(line1, line2)

    def activate(self):
        self.displayTrackInfo()

    def displayTrackInfo(self):
        title = self.player.title
        artist = self.player.artist

        self.display.writeText(title, artist)

    def onEncoderTick(self, direction):
        now = time.time()
        if now - self.last_tick > 1:
            self.tick_count = 0

        self.last_tick = now
        self.tick_count += direction

        print(self.tick_count)

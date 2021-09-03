

class BluetoothPlayerState:
    def __init__(self, display, player, encoder):
        self.display = display
        self.player = player
        self.encoder = encoder

        self.encoder.addShortPressCallback(self.togglePause)
        self.player.addUpdateCallback(self.displayTrackInfo)

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

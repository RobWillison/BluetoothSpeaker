

class BluetoothPlayerState:
    def __init__(self, display, player, encoder):
        self.display = display
        self.player = player
        self.encoder = encoder

    def activate(self):
        self.displayTrackInfo()

    def displayTrackInfo(self):
        title = self.player.title
        artist = self.player.artist

        self.display.writeText(title, artist)



class BluetoothPlayerState:
    def __init__(self, display, player, encoder):
        self.display = display
        self.player = player
        self.encoder = encoder

    def active(self):
        displayTrackInfo()

    def displayTrackInfo(self):
        title = self.player.title()
        artist = self.player.artist()

        newState = [[],[]]
        title = self.cropText(title).ljust(16)
        artist = self.cropText(artist).ljust(16)
        line1 = bytearray(title, 'utf-8')
        line2 = bytearray(artist, 'utf-8')

        self.display.writeData(line1, line2)

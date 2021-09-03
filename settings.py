
class Settings:
    def __init__(self, display):
        self.display = display
        self.open = False

    def openClose(self):
        if self.open:
            self.open = False
            self.display.writeTrackInfo()
        else:
            self.open = True
            self.display.writeText('Settings')

    def move(self, direction):
        return

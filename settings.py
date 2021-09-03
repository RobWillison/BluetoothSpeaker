
class Settings:
    def __init__(self, display):
        self.display = display
        self.open = False
        self.options = ['Change Colour', 'Pair Device']
        self.currentPosition = 0

    def openClose(self):
        if self.open:
            self.open = False
            self.display.writeTrackInfo()
        else:
            self.open = True
            self.display.writeText('Settings', self.options[0])

    def move(self, direction):
        self.currentPosition -= direction
        if self.currentPosition > 1:
            self.currentPosition = 1
        if self.currentPosition < 0:
            self.currentPosition = 0

        self.display.writeText('Settings', self.options[self.currentPosition])

    def click(self):
        print('Clicked')

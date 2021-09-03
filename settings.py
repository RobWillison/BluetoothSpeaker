
class Settings:
    def __init__(self, display):
        self.display = display
        self.open = False
        self.options = ['Change Colour', 'Pair Device']
        self.currentPosition = 0
        self.item_selected = False
        self.colourValue = 0

    def openClose(self):
        if self.open:
            self.open = False
            self.display.writeTrackInfo()
        else:
            self.open = True
            self.display.writeText('Settings', self.options[0])

    def move(self, direction):
        if self.item_selected:
            self.colourValue(direction)
        else:
            self.currentPosition -= direction
            if self.currentPosition > 1:
                self.currentPosition = 1
            if self.currentPosition < 0:
                self.currentPosition = 0

            self.display.writeText('Settings', self.options[self.currentPosition])

    def changeColour(self, direction):
        self.colourValue += direction
        self.display.writeText('Change Colour', '[' + ('='*self.colourValue).ljust(14) + ']')

    def pair(self):
        self.display.writeText('Pairing')

    def click(self):
        if self.item_selected:
            self.item_selected = False
            self.display.writeText('Settings', self.options[self.currentPosition])
        else:
            self.item_selected = True
            if self.currentPosition == 0:
                self.changeColour(0)
            else:
                self.pair()
        print('Clicked')

import math

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
            self.changeColour(direction)
        else:
            self.currentPosition -= direction
            if self.currentPosition > 1:
                self.currentPosition = 1
            if self.currentPosition < 0:
                self.currentPosition = 0

            self.display.writeText('Settings', self.options[self.currentPosition])

    def changeColour(self, direction):
        self.colourValue -= direction

        if self.colourValue < 0:
            self.colourValue = 0
        if self.colourValue > 14:
            self.colourValue = 14

        t = (180/14) * self.colourValue
        r = int((abs(math.sin(3.14*t/180)))*255);
        g = int((abs(math.sin(3.14*(t+60)/180)))*255);
        b = int((abs(math.sin(3.14*(t+120)/180)))*255);
        self.display.setRGB(r,g,b)

        bar = bytearray('[              ]', 'utf-8')

        bar[1..self.colourValue+1] = [1]*self.colourValue

        self.display.writeData(bytearray('Change Colour', 'utf-8'), bar)

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

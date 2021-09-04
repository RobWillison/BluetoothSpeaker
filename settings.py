import math
import json

class SettingsState:
    def __init__(self, display, player, encoder):
        self.display = display
        self.encoder = encoder
        self.player = player
        self.active = False
        self.options = ['Change Colour  <', 'Pair Device    <']
        self.currentPosition = 0
        self.item_selected = False
        self.colourValue = 0

        self.encoder.addTurnCallback(self.move)
        self.encoder.addShortPressCallback(self.click)

    def activate(self):
        self.active = True
        self.display.writeText('Settings', self.options[0])

    def deactivate(self):
        self.active = False

    def move(self, direction):
        if not self.active:
            return

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
        steps = 14*5

        if self.colourValue < 0:
            self.colourValue = 0
        if self.colourValue > steps-1:
            self.colourValue = steps-1

        t = (180/steps) * self.colourValue
        r = int((abs(math.sin(3.14*t/180)))*255);
        g = int((abs(math.sin(3.14*(t+60)/180)))*255);
        b = int((abs(math.sin(3.14*(t+120)/180)))*255);
        self.display.setRGB(r,g,b)

        bar = bytearray('[              ]', 'utf-8')

        fullSteps = math.floor(self.colourValue/5)
        bar[1:fullSteps+1] = [5]*fullSteps
        bar[1:fullSteps+1] = [5]*fullSteps

        bar[fullSteps+1] = (self.colourValue%5) + 1

        self.display.writeData(bytearray('Change Colour', 'utf-8'), bar)
        with open('settings.json', 'w') as outfile:
            json.dump({'red': r, 'green': g, 'blue': b}, outfile)

    def pair(self):
        self.display.writeText('Pairing')

    def click(self):
        if not self.active:
            return

        if self.item_selected:
            self.item_selected = False
            self.display.writeText('Settings', self.options[self.currentPosition])
        else:
            self.item_selected = True
            if self.currentPosition == 0:
                self.changeColour(0)
            else:
                self.pair()

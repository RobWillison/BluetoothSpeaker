import RGB1602

class Display:
    def __init__(self):
        self.lcd = RGB1602.RGB1602(16, 2)

        self.lcd.setRGB(10, 64, 10)
        self.lcd.setCursor(0,0)
        self.lcd.printout('Bluetooth Speaker')
        self.lcd.setCursor(0,1)
        self.lcd.printout('By Rob')

        self.lcd.createCustomSymbol(1, [31, 0, 31, 0, 31, 0, 31, 0])

    def cropText(self, text):
        if len(text) > 14:
            return text[0:11] + '...'
        return text


    def trackChanged(self, track, artist, album):
        self.lcd.clear()
        self.lcd.setCursor(0,0)
        self.lcd.printout(self.cropText(track) + u"\u23F8")
        self.lcd.setCursor(0,1)
        self.lcd.printout(self.cropText(artist))

    def pausedStatusChanged(self, paused):
        if paused:
            self.lcd.setCursor(14, 1)
            self.lcd.printCustomSymbol(1)
        else:
            self.lcd.setCursor(14, 1)
            self.lcd.printout(' ')

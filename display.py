import RGB1602

class Display:
    def __init__(self):
        self.lcd = RGB1602.RGB1602(16, 2)

        self.lcd.setRGB(10, 64, 10)
        self.lcd.setCursor(0,0)
        self.lcd.printout('Bluetooth Speaker')
        self.lcd.setCursor(0,1)
        self.lcd.printout('By Rob')


    def trackChanged(self, track, artist, album):
        self.lcd.clear()
        self.lcd.setCursor(0,0)
        self.lcd.printout(track)
        self.lcd.setCursor(0,1)
        self.lcd.printout(artist)

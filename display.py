import RGB1602
import time
import threading

class Display:
    def __init__(self):
        self.lcd = RGB1602.RGB1602(16, 2)

        self.lcd.setRGB(10, 64, 10)
        self.lcd.setCursor(0,0)
        self.lcd.printout('Bluetooth Speaker')
        self.lcd.setCursor(0,1)
        self.lcd.printout('By Rob')

        self.lcd.createCustomSymbol(0, self.pauseSymbol())
        self.lcd.createCustomSymbol(1, self.arrowSymbol())

        self.lcd.printCustomSymbol(0)
        self.lcd.printCustomSymbol(1)

        self.track = 'Unknown'
        self.artist = 'Unknown'
        self.album = 'Unknown'

        self.displayState = [bytearray('Bluetooth       ', 'utf-8'), bytearray('Bluetooth       ', 'utf-8')]
        self.displayChanged = True
        self.thread = threading.Thread(target=self.runDisplayUpdate)
        self.thread.start()

    def runDisplayUpdate(self):
        while True:
            if self.displayChanged:
                self.displayChanged = False
                self.updateDisplay()
            time.sleep(0.25)

    def updateDisplay(self):
        self.lcd.clear()
        for index, row in enumerate(self.displayState):
            self.lcd.setCursor(0, index)
            for char in row:
                self.lcd.write(char)


    def pauseSymbol(self):
        return [
            int('11011', 2),
            int('11011', 2),
            int('11011', 2),
            int('11011', 2),
            int('11011', 2),
            int('11011', 2),
            int('11011', 2),
            int('11011', 2)
        ]

    def arrowSymbol(self):
        return [
            int('10000', 2),
            int('11000', 2),
            int('01100', 2),
            int('00110', 2),
            int('00110', 2),
            int('01100', 2),
            int('11000', 2),
            int('10000', 2)
        ]

    def cropText(self, text):
        if len(text) > 14:
            return text[0:11] + '...'
        return text


    def trackChanged(self, track, artist, album):
        self.track = track
        self.artist = artist
        self.album = album
        self.writeTrackInfo()


    def pausedStatusChanged(self, paused):
        if paused:
            self.displayState[0][15] = 0
        else:
            self.displayState[0][15] = bytearray(' ', 'utf-8')[0]
        self.displayChanged = True

    def writeText(self, text):
        self.displayState[0] = text.ljust(16)
        self.displayState[1] = ''.ljust(16)
        self.displayChanged = True

    def writeTrackInfo(self):
        title = self.cropText(self.track).ljust(16)
        artist = self.cropText(self.artist).ljust(16)
        self.displayState[0] = bytearray(title, 'utf-8')
        self.displayState[1] = bytearray(title, 'utf-8')
        self.displayChanged = True

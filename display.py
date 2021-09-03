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

        self.displayState = [['=' for i in range(16)], ['=' for i in range(16)]]
        self.thread = threading.Thread(target=self.runDisplayUpdate)
        self.thread.start()

    def runDisplayUpdate(self):
        while True:
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
            self.displayState[0][15] = ' '

    def writeText(self, text):
        self.lcd.clear()
        self.lcd.setCursor(0, 0)
        self.lcd.printout(text)

    def writeTrackInfo(self):
        self.lcd.clear()
        self.lcd.setCursor(0,0)
        self.lcd.printout(self.cropText(self.track))
        self.lcd.setCursor(0,1)
        self.lcd.printout(self.cropText(self.artist))

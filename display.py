import RGB1602
import time
import threading

class Display:
    def __init__(self):
        self.lcd = RGB1602.RGB1602(16, 2)

        self.lcd.setRGB(10, 64, 10)
        self.lcd.setCursor(0,0)
        self.lcd.printout('Bluetooth       ')
        self.lcd.setCursor(0,1)
        self.lcd.printout('Speaker         ')

        self.lcd.createCustomSymbol(0, self.pauseSymbol())
        self.lcd.createCustomSymbol(1, self.arrowSymbol())

        self.lcd.printCustomSymbol(0)
        self.lcd.printCustomSymbol(1)

        self.track = 'Unknown'
        self.artist = 'Unknown'
        self.album = 'Unknown'

        self.displayState = [[bytearray('Bluetooth       ', 'utf-8'), bytearray('Speaker         ', 'utf-8')]]

        self.thread = threading.Thread(target=self.runDisplayUpdate)
        self.thread.start()

    def runDisplayUpdate(self):
        while True:
            if len(self.displayState) > 1:
                self.displayState.pop(0)
                self.updateDisplay(self.displayState[0])

            time.sleep(0.1)

    def runTrackChangeAnimation(self, newTrack, newArtist):
        newState = [[],[]]
        newState[0] = bytearray(title, 'utf-8')
        newState[1] = bytearray(artist, 'utf-8')

        for i in range(16):
            frame = [[], []]
            frame[0] = self.displayState[0][0:i] + newState[0][i:-1]
            frame[1] = self.displayState[1][0:i] + newState[1][i:-1]
            time.sleep(0.15)

    def updateDisplay(self, displayData):
        self.lcd.clear()
        for index, row in enumerate(displayData):
            self.lcd.setCursor(0, index)
            for index, char in enumerate(row):
                self.lcd.setCursor(index, index)
                if char != -1:
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
        self.runTrackChangeAnimation(track, artist)


    def pausedStatusChanged(self, paused):
        newState = self.displayState[-1]
        if paused:
            newState[0][15] = 0
        else:
            newState[0][15] = bytearray(' ', 'utf-8')[0]

        self.displayState.append(newState)

    def writeText(self, text, text2=''):
        newState = [[],[]]
        newState[0] =  bytearray(text.ljust(16), 'utf-8')
        newState[1] = bytearray(text2.ljust(16), 'utf-8')

        self.displayState.append(newState)

    def writeTrackInfo(self):
        newState = [[],[]]
        title = self.cropText(self.track).ljust(16)
        artist = self.cropText(self.artist).ljust(16)
        newState[0] = bytearray(title, 'utf-8')
        newState[1] = bytearray(artist, 'utf-8')

        self.displayState.append(newState)

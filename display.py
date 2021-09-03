import RGB1602
import time
import threading
import json

class Display:
    def __init__(self):
        self.lcd = RGB1602.RGB1602(16, 2)

        setting_data = json.load('settings.json')

        self.lcd.setRGB(setting_data['red'], setting_data['green'], setting_data['blue'])
        self.lcd.setCursor(0,0)
        self.lcd.printout('Bluetooth       ')
        self.lcd.setCursor(0,1)
        self.lcd.printout('Speaker         ')

        self.lcd.createCustomSymbol(0, self.pauseSymbol())
        self.lcd.createCustomSymbol(1, self.sliderBlock(1))
        self.lcd.createCustomSymbol(2, self.sliderBlock(2))
        self.lcd.createCustomSymbol(3, self.sliderBlock(3))
        self.lcd.createCustomSymbol(4, self.sliderBlock(4))
        self.lcd.createCustomSymbol(5, self.sliderBlock(5))

        self.lcd.printCustomSymbol(0)
        self.lcd.printCustomSymbol(1)

        self.track = 'Unknown'
        self.artist = 'Unknown'
        self.album = 'Unknown'

        self.displayState = [[bytearray('Bluetooth       ', 'utf-8'), bytearray('Speaker         ', 'utf-8')]]

        self.thread = threading.Thread(target=self.runDisplayUpdate)
        self.thread.start()

    def setRGB(self,r,g,b):
        self.lcd.setRGB(r,g,b)

    def runDisplayUpdate(self):
        while True:
            if len(self.displayState) > 0:
                self.updateDisplay(self.displayState.pop(0))

            time.sleep(0.05)

    def runTrackChangeAnimation(self, newTrack, newArtist):
        newState = [[],[]]
        newState[0] = bytearray(self.cropText(newTrack).ljust(16), 'utf-8')
        newState[1] = bytearray(self.cropText(newArtist).ljust(16), 'utf-8')

        frames = []
        for i in range(16, -1, -1):
            frame = [[], []]

            frame[0] = [-1]*i + list(newState[0][i:-1])
            frame[1] = [-1]*i + list(newState[1][i:-1])

            frames.append(frame)
        self.displayState += frames

    def updateDisplay(self, displayData):
        try:
            for row_index, row in enumerate(displayData):
                print(row)
                self.lcd.setCursor(0, row_index)
                for char_index, char in enumerate(row):
                    if char != -1:
                        self.lcd.write(char)
                    else:
                        self.lcd.setCursor(char_index+1, row_index)
        except OSError:
            self.updateDisplay(displayData)

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

    def sliderBlock(self, fullness=1):
        tmp = ('1'*fullness).ljust(5, '0')
        return [
            int(tmp, 2),
            int(tmp, 2),
            int(tmp, 2),
            int(tmp, 2),
            int(tmp, 2),
            int(tmp, 2),
            int(tmp, 2),
            int(tmp, 2)
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
        newState = [[],[]]
        if paused:
            newState[0] = [-1]*15 + [0]
        else:
            newState[0] = [-1]*15 + [32]

        self.displayState.append(newState)

    def writeText(self, text, text2=''):
        newState = [[],[]]
        newState[0] =  bytearray(text.ljust(16), 'utf-8')
        newState[1] = bytearray(text2.ljust(16), 'utf-8')

        self.displayState.append(newState)

    def writeData(self, line1, line2):
        newState = [[],[]]
        newState[0] =  line1
        newState[1] = line2

        self.displayState.append(newState)

    def writeTrackInfo(self):
        newState = [[],[]]
        title = self.cropText(self.track).ljust(16)
        artist = self.cropText(self.artist).ljust(16)
        newState[0] = bytearray(title, 'utf-8')
        newState[1] = bytearray(artist, 'utf-8')

        self.displayState.append(newState)

import RGB1602
import board
import RPi.GPIO as GPIO
import time
from player import Player

lcd = RGB1602.RGB1602(16, 2)

lcd.setRGB(10, 64, 10)
lcd.setCursor(0,0)
lcd.printout('Bluetooth Speaker')
lcd.setCursor(0,1)
lcd.printout('By Rob')

def trackChanged(track, artist, album):
    lcd.clear()
    lcd.setCursor(0,0)
    lcd.printout(track)
    lcd.setCursor(0,1)
    lcd.printout(artist)

p = Player(trackChanged)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)

pausePlayButton = 17
GPIO.setup(pausePlayButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(pausePlayButton, GPIO.FALLING, callback=p.togglePaused)

while True:
    time.sleep(1)

import RGB1602
import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
from time import sleep
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import time


lcd = RGB1602.RGB1602(16, 2)

lcd.setRGB(10, 64, 10)
lcd.setCursor(0,0)
lcd.printout('Bluetooth Speaker')
lcd.setCursor(0,1)
lcd.printout('By Rob')

paused = False

def on_property_changed(interface, changed, invalidated):
    global paused
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
            if value == 'paused':
                paused = True
            if value == 'playing':
                paused = False
        elif prop == 'Track':
            print('Music Info:')
            for key in ('Title', 'Artist', 'Album'):
                print('   {}: {}'.format(key, value.get(key, '')))
            lcd.setCursor(0,0)
            lcd.clear()
            lcd.printout(value.get('Title', ''))
            lcd.setCursor(0,1)
            lcd.printout(value.get('Artist', ''))

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pause = 17
GPIO.setup(pause, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)



def pausePlay(e):
    print(e)
    if player_iface:
        if paused:
            player_iface.Play()
        else:
            player_iface.Pause()
        print('Play/Pause')


player_iface = None

GPIO.add_event_detect(pause, GPIO.FALLING, callback=pausePlay, bouncetime=100)

if __name__ == '__main__':
    while True:
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SystemBus()
        obj = bus.get_object('org.bluez', "/")
        mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
        transport_prop_iface = None
        for path, ifaces in mgr.GetManagedObjects().items():
            if 'org.bluez.MediaPlayer1' in ifaces:
                player_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.bluez.MediaPlayer1')
            elif 'org.bluez.MediaTransport1' in ifaces:
                transport_prop_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.freedesktop.DBus.Properties')
        if not player_iface:
            print('Not connected')
            time.sleep(1)
            continue
        if not transport_prop_iface:
            sys.exit('Error: DBus.Properties iface not found.')
 
        bus.add_signal_receiver(
            on_property_changed,
            bus_name='org.bluez',
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties')
        #GLib.timeout_add(100, checkPause)
        #GLib.timeout_add(100, checkSkipTrack)
        #GLib.io_add_watch(sys.stdin, GLib.IO_IN, on_playback_control)
        print(dir(player_iface))
        GLib.MainLoop().run()

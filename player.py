import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
import busio
import threading
import time

class Player:
    def __init__(self):
        self.player_iface = None
        self.transport_prop_iface = None
        self.thread = threading.Thread(target=self.connect)
        self.thread.start()

    def connect(self):
        while True:
            dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
            bus = dbus.SystemBus()
            obj = bus.get_object('org.bluez', "/")
            mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')

            for path, ifaces in mgr.GetManagedObjects().items():
                if 'org.bluez.MediaPlayer1' in ifaces:
                    self.player_iface = dbus.Interface(
                        bus.get_object('org.bluez', path),
                        'org.bluez.MediaPlayer1')
                elif 'org.bluez.MediaTransport1' in ifaces:
                    self.transport_prop_iface = dbus.Interface(
                        bus.get_object('org.bluez', path),
                        'org.freedesktop.DBus.Properties')

            if not self.player_iface:
                print('Not connected')
                time.sleep(1)
                continue
            if not self.transport_prop_iface:
                sys.exit('Error: DBus.Properties iface not found.')

            bus.add_signal_receiver(
                self.on_property_changed,
                bus_name='org.bluez',
                signal_name='PropertiesChanged',
                dbus_interface='org.freedesktop.DBus.Properties')

            GLib.MainLoop().run()

    def on_property_changed(self, interface, changed, invalidated):
        global paused
        if interface != 'org.bluez.MediaPlayer1':
            return
        for prop, value in changed.items():
            if prop == 'Status':
                print('Playback Status: {}'.format(value))
                if value == 'paused':
                    self.paused = True
                if value == 'playing':
                    self.paused = False
            elif prop == 'Track':
                print('Music Info:')
                for key in ('Title', 'Artist', 'Album'):
                    print('   {}: {}'.format(key, value.get(key, '')))

    def play(self):
        self.player_iface.Play()

    def pause(self):
        self.player_iface.Pause()

    def togglePaused(self, _):
        if self.paused:
            self.play()
        else:
            self.pause()

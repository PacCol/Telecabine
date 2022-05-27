from emulator import emulator

if emulator:
    from emulator import gpiozero
else:
    import gpiozero

import server
import display.interface as interface

from time import sleep
from datetime import datetime, timedelta
from threading import Thread
from hardware import *

rgbLED = gpiozero.RGBLED(21, 20, 16)
primary = (0, 0, 1)
success = (0, 1, 0)
warning = (1, 0.5, 0)
danger = (1, 0, 0)

showOFF = False


def displayDaemon():

    while True:

        now = datetime.now()
        sleepDate = server.lastInteraction + timedelta(minutes=1)

        if sleepDate < now and motors.getSpeed() == 0: 
            interface.putToSleep()
            rgbLED.color = (0, 0, 0.2)

        if interface.lastReload + timedelta(minutes=1) < now and interface.isSleeping == False:
            interface.showHomeScreen()

        sleep(2)


def displayStatus():

    interface.showHomeScreen()

    if not server.sleeping:
        if motors.getSpeed() == 0:
            rgbLED.color = primary
        elif abs(motors.getSpeed()) < 3:
            rgbLED.color = danger
        elif abs(motors.getSpeed()) < 6:
            rgbLED.color = warning
        elif abs(motors.getSpeed()) < 10:
            rgbLED.color = success
        else:
            rgbLED.color = warning


def displayOFF():
    interface.displayOff()


displayStatus()

displayThread = Thread(target=displayDaemon, args=())
displayThread.start()

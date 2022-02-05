import gpiozero
import __main__
import display.oled as oled

from time import sleep
from datetime import datetime, timedelta
from threading import Thread

rgbLED = gpiozero.RGBLED(21, 20, 16)
primary = (0, 0, 1)
success = (0, 1, 0)
warning = (1, 0.5, 0)
danger = (1, 0, 0)

showOFF = False


def displayDaemon():

    global __main__, dontWait

    while True:

        now = datetime.now()
        limitDate = __main__.lastInteraction + timedelta(minutes=2)

        if limitDate < now and __main__.speed == 0: 
            oled.putToSleep()

        sleep(2)


def displayStatus():

    oled.showHomeScreen()

    if not __main__.sleeping:
        if abs(__main__.speed) < 3:
            rgbLED.color = danger
        elif abs(__main__.speed) < 6:
            rgbLED.color = warning
        elif abs(__main__.speed) < 10:
            rgbLED.color = success
        else:
            rgbLED.color = warning


def displayOFF():
    global showOFF
    showOFF = True


displayStatus()

displayThread = Thread(target=displayDaemon, args=())
displayThread.start()

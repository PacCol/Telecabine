import gpiozero
from datetime import datetime
from subprocess import check_call
from time import sleep

import __main__, display.display as display, lights

button = gpiozero.Button(24)
led = gpiozero.PWMLED(23)

led.pulse()


def changeStatus(wantToEnable):

    global __main__

    if wantToEnable:
        __main__.lightsEnabled = True
        lights.enable(True)
        display.displayStatus()
        led.off()
        led.on()
    else:
        __main__.lightsEnabled = False
        lights.enable(False)
        led.off()
        led.pulse()

    __main__.lastInteraction = datetime.now()
    display.displayStatus()

    __main__.sendStatus()


def toggleStatus():
    if __main__.lightsEnabled:
        changeStatus(False)
    else:
        changeStatus(True)
    sleep(0.4)


def shutdown():
    display.displayOFF()
    #check_call(['sudo', 'poweroff'])


button.when_released = toggleStatus
button.when_held = shutdown

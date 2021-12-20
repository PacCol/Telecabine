import gpiozero
from time import sleep

import __main__

button = gpiozero.Button(24)
led = gpiozero.PWMLED(23)

led.pulse()


def changeStatus(wantToEnable):

    global __main__

    if wantToEnable:
        __main__.lightsEnabled = True
        __main__.lights.enable(True)
        led.on()
    else:
        __main__.lightsEnabled = False
        __main__.lights.enable(False)
        led.off()
        led.pulse()

    __main__.sendStatus()


def toggleStatus():
    
    if __main__.lightsEnabled:
        changeStatus(False)
    else:
        changeStatus(True)

    sleep(1)


button.when_pressed = toggleStatus
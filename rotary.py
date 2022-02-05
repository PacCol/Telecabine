import gpiozero
from time import sleep

import __main__

rotor = gpiozero.RotaryEncoder(15, 18, wrap=False, max_steps=10)
rotor.steps = __main__.speed

rotaryButton = gpiozero.Button(14)

def changeSpeed():
    __main__.changeStatus(rotor.steps)
    sleep(0.05)

def toggleStatus():
    __main__.changeStatus(0)

rotor.when_rotated = changeSpeed
rotaryButton.when_released = toggleStatus
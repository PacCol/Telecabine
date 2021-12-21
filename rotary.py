import gpiozero

import __main__

rotor = gpiozero.RotaryEncoder(15, 18, wrap=False, max_steps=5)
rotor.steps = __main__.speed - 5

rotaryButton = gpiozero.Button(14)


def changeSpeed():
    selectedSpeed = rotor.steps + 5

    if selectedSpeed == 0:
        rotor.steps = selectedSpeed - 5
        __main__.changeStatus(False, 1)
    else:
        __main__.changeStatus(__main__.enabled, selectedSpeed)


def toggleStatus():
    if __main__.enabled:
        __main__.changeStatus(False, __main__.speed)
    else:
        __main__.changeStatus(True, __main__.speed)


rotor.when_rotated = changeSpeed
rotaryButton.when_released = toggleStatus
from datetime import datetime
from server import lastInteraction, sendStatus
from chairlift import lights, motors
from inputDevices import rotary
import display.display as display


def setStatus(speed, lightsEnabled):

    global lastInteraction
    lastInteraction = datetime.now()

    if speed != None:
        rotary.rotor.steps = speed
        motors.setSpeed(speed)
        display.displayStatus()
        sendStatus()

    if lightsEnabled != None:
        lights.enable(lightsEnabled)
        display.displayStatus()
        sendStatus()
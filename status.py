from datetime import datetime
import server
from chairlift import lights, motors
from inputDevices import rotary
import display.display as display


def setStatus(speed, lightsEnabled):

    global server
    server.lastInteraction = datetime.now()

    if speed != None:
        rotary.rotor.steps = speed
        motors.setSpeed(speed)
        display.displayStatus()
        server.sendStatus()

    if lightsEnabled != None:
        lights.enable(lightsEnabled)
        display.displayStatus()
        server.sendStatus()
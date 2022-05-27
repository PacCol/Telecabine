from datetime import datetime
import server
import hardware
import display.display as display

def setStatus(speed, lightsEnabled):

    global server
    server.lastInteraction = datetime.now()

    if speed != None:
        hardware.rotary.rotor.steps = speed
        hardware.motors.setSpeed(speed)
        display.displayStatus()
        server.sendStatus()

    if lightsEnabled != None:
        hardware.lights.enable(lightsEnabled)
        display.displayStatus()
        server.sendStatus()
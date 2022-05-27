from datetime import datetime
import server
import hardware
import display.display as display

def setOutput(speed, lightsEnabled):

    global server
    server.lastInteraction = datetime.now()

    if speed != None:
        hardware.rotary.rotor.steps = speed
        hardware.motors.setSpeed(speed)

    if lightsEnabled != None:
        hardware.lights.enable(lightsEnabled)
        hardware.illuminatedButton.showLightsEnabled(lightsEnabled)
    
    display.displayStatus()    
    server.sendStatus()
from emulator import emulator

if emulator:
    from emulator import gpiozero
    from emulator import GPIO
else:
    import gpiozero
    import RPi.GPIO as GPIO

from datetime import datetime, timedelta
from subprocess import check_call
from time import sleep
from threading import Thread

import display.display as display
from status import *

alimentation = "12v"

lights = None
motors = None
illuminatedButton = None
rotary = None


class illuminatedPushButton():

    def __init__(self):
        self.button = gpiozero.Button(24)
        self.led = gpiozero.PWMLED(23)
        self.led.pulse()

        def toggleStatus():
            if lights.getStatus():
                setOutput(None, False)
            else:
                setOutput(None, True)
            sleep(0.4)

        def shutdown():
            display.displayOFF()
            check_call(['sudo', 'poweroff'])

        self.button.when_released = toggleStatus
        self.button.when_held = shutdown

    def showLightsEnabled(self, enabled):
        if enabled:
            self.led.on()
        else:
            self.led.pulse()


class rotaryEncoder():

    def __init__(self):
        self.rotor = gpiozero.RotaryEncoder(15, 18, wrap=False, max_steps=10)
        self.rotor.steps = motors.getSpeed()
        self.rotaryButton = gpiozero.Button(14)
        self.rotor.when_rotated = self.setMotorsSpeed
        self.rotaryButton.when_released = self.stopMotors

    def setMotorsSpeed(self):
        if self.rotor.steps < 0:
            self.rotor.steps = 0
        setOutput(self.rotor.steps, None)
        sleep(0.05)

    def stopMotors(self):
        setOutput(0, None)


class Lights:

    def __init__(self):
        self.brightnessPin = 7
        self.activationPin = 1
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.brightnessPin, GPIO.OUT)
        self.brightnessPWM = GPIO.PWM(self.brightnessPin, 50)
        GPIO.setup(self.activationPin, GPIO.OUT)
        self.enabled = False

    def enable(self, enable):
        self.enabled = enable
        GPIO.output(self.activationPin, enable)
        if alimentation == "9v" and enable:
            self.brightnessPWM.start(100)
        elif enable:
            self.brightnessPWM.start(80)
        else:
            self.brightnessPWM.start(0)

    def getStatus(self):
        return self.enabled


class Motors():
    
    def __init__(self):
        self.startTime = datetime.now()
        self.speedPin = 6
        self.activationPin = 13
        self.reversePin = 12
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.speedPin, GPIO.OUT)
        GPIO.setup(self.activationPin, GPIO.OUT)
        GPIO.setup(self.reversePin, GPIO.OUT)
        self.speedPWM = GPIO.PWM(self.speedPin, 50)
        self.speed = 0

    def setSpeed(self, speed):
        if self.speed == 0:
            self.startTime = datetime.now()
        self.speed = speed
        if alimentation == "9v":
            self.speedPWM.start(self.speed * 10)
        else:
            self.speedPWM.start(int(self.speed * 10 * 0.9))
        if self.speed > 0:
            GPIO.output(self.activationPin, True)
            GPIO.output(self.reversePin, False)

    def getSpeed(self):
        return self.speed

    def getStartTime(self):
        return self.startTime


rgbLED = gpiozero.RGBLED(21, 20, 16)
primary = (0, 0, 1)
success = (0, 1, 0)
warning = (1, 0.5, 0)
danger = (1, 0, 0)


lights = Lights()
motors = Motors()
illuminatedButton = illuminatedPushButton()
rotary = rotaryEncoder()


def setOutput(speed, lightsEnabled):

    global lastInteraction
    lastInteraction = datetime.now()

    if speed != None:
        rotary.rotor.steps = speed
        motors.setSpeed(speed)

    if lightsEnabled != None:
        lights.enable(lightsEnabled)
        illuminatedButton.showLightsEnabled(lightsEnabled)
    
    displayStatus()


def displayStatus():

    if not sleeping:
        if motors.getSpeed() == 0:
            rgbLED.color = primary
        elif motors.getSpeed() < 3:
            rgbLED.color = danger
        elif motors.getSpeed() < 6:
            rgbLED.color = warning
        elif motors.getSpeed() < 10:
            rgbLED.color = success
        else:
            rgbLED.color = warning
    
    display.displayStatus(motors.getSpeed(), lights.getStatus())


def displayStatusDaemon():

    while True:

        now = datetime.now()
        sleepDate = lastInteraction + timedelta(seconds=5)

        if sleepDate < now and motors.getSpeed() == 0:
            display.putToSleep()
            rgbLED.color = (0, 0, 0.2)

        if display.lastReload + timedelta(seconds=5) < now and display.isSleeping == False:
            display.displayStatus(motors.getSpeed(), lights.getStatus())

        sleep(2)

    
displayThread = Thread(target=displayStatusDaemon, args=())
displayThread.start()
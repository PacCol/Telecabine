from emulator import emulator

if emulator:
    from emulator import gpiozero
    from emulator import GPIO
else:
    import gpiozero
    import RPi.GPIO as GPIO

from datetime import datetime
from subprocess import check_call
from time import sleep


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
                status.setStatus(None, False)
            else:
                status.setStatus(None, True)
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
        if self.rotor.steps < 0 and not motors.isBackwardAllowed():
            self.rotor.steps = 0
        else:
            status.setStatus(self.rotor.steps, None)
        sleep(0.05)

    def stopMotors(self):
        status.setStatus(0, None)


class Lights:

    def __init__(self):
        self.brightnessPin = 7
        self.activationPin = 1
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.brightnessPin, GPIO.OUT)
        GPIO.setup(self.activationPin, GPIO.OUT)
        self.brightnessPWM = GPIO.PWM(self.brightnessPin, 50)
        self.enabled = False

    def enable(self, enable):
        self.enabled = enable
        GPIO.output(self.activationPin, enable)
        GPIO.output(self.brightnessPin, enable)

    def getStatus(self):
        return self.enabled


class Motors():
    
    def __init__(self, backwardAllowed):
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
        self.backwardAllowed = backwardAllowed

    def setSpeed(self, speed):
        if self.speed == 0:
            self.startTime = datetime.now()
        self.speed = speed
        self.speedPWM.start(abs(self.speed) * 10)
        if self.speed < 0 and self.backwardAllowed:
            GPIO.output(self.activationPin, False)
            GPIO.output(self.reversePin, True)
        elif self.speed < 0 and not self.backwardAllowed:
            self.speed = 0
            GPIO.output(self.activationPin, False)
            GPIO.output(self.reversePin, False)
        elif self.speed > 0:
            GPIO.output(self.activationPin, True)
            GPIO.output(self.reversePin, False)
        else:
            GPIO.output(self.activationPin, False)
            GPIO.output(self.reversePin, False)

    def getSpeed(self):
        return self.speed

    def isBackwardAllowed(self):
        return self.backwardAllowed

    def getStartTime(self):
        return self.startTime


lights = Lights()
motors = Motors(False)
illuminatedButton = illuminatedPushButton()
rotary = rotaryEncoder()


import display.display as display
import status
import RPi.GPIO as GPIO


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
        self.speed = speed
        self.speedPWM.start(abs(self.speed) * 10)
        if self.speed < 0 and self.backwardAllowed:
            GPIO.output(self.activationPin, False)
            GPIO.output(self.reversePin, True)
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


lights = Lights()
motors = Motors(False)
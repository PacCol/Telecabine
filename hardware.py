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

from display.display import display
from status import *
from sse import sendStatus

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
            if display.getCurrentScreen() == "Home":
                if lights.getStatus():
                    setOutput(None, False)
                else:
                    setOutput(None, True)
                sleep(0.4)

        def shutdown():
            display.displayOFF()
            #check_call(['sudo', 'poweroff'])

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
        self.rotor.when_rotated_clockwise = self.scrollDown
        self.rotor.when_rotated_counter_clockwise = self.scrollUp
        self.rotaryButton.when_released = self.click
        self.rotaryButton.when_held = self.initSettings
        self.wasHeld = False

    def click(self):
        if self.wasHeld == True:
            self.wasHeld = False
        else:
            if display.getCurrentScreen() == "Home":
                self.stopMotors()
            elif display.getCurrentScreen() == "Settings":
                status = display.displaySettings(True, None, None)
                if status == "Exit":
                    self.rotor.steps = motors.getSpeed()
                    display.displayStatus(motors.getSpeed(), lights.getStatus())

    def scrollUp(self):
        self.scroll("Up")

    def scrollDown(self):
        self.scroll("Down")

    def scroll(self, direction):
        if display.getCurrentScreen() == "Home":
            self.setMotorsSpeed()
        elif display.getCurrentScreen() == "Settings":
            display.displaySettings(False, direction, None)

    def setMotorsSpeed(self):
        if self.rotor.steps < 0:
            self.rotor.steps = 0
        setOutput(self.rotor.steps, None)

    def stopMotors(self):
        setOutput(0, None)

    def initSettings(self):
        self.wasHeld = True
        display.displaySettings(False, None, "General")


def openSettings():
    if display.getCurrentScreen() != "Settings":
        display.displaySettings(False, None, "General")


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

    sendStatus(motors.getSpeed(), lights.getStatus(), motors.getStartTime())


def displayStatusDaemon():

    while True:

        now = datetime.now()

        if lastInteraction + timedelta(seconds=5) < now and motors.getSpeed() == 0 and display.getCurrentScreen == "Home":
            display.putToSleep()
            rgbLED.color = (0, 0, 0.1)
        
        elif lastInteraction + timedelta(minutes=5) < now and display.getCurrentScreen == "Settings":
            display.putToSleep()
            rgbLED.color = (0, 0, 0.1)

        if display.getLastReload() + timedelta(minutes=1) < now and display.isSleeping == False:
            if display.getCurrentScreen() == "Home":
                display.displayStatus(motors.getSpeed(), lights.getStatus())
            elif display.getCurrentScreen() == "Settings" and display.getCurrentSetting() != "UpdateStarted":
                display.displaySettings(False, None, None)

        sleep(2)

    
displayThread = Thread(target=displayStatusDaemon, args=())
displayThread.start()

displayStatus()
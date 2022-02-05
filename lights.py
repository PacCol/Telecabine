import RPi.GPIO as GPIO

brightnessPin = 7
activationPin = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(brightnessPin, GPIO.OUT)
GPIO.setup(activationPin, GPIO.OUT)

brightnessPWM = GPIO.PWM(brightnessPin, 50)

def enable(wantToEnable):
    
    GPIO.output(activationPin, wantToEnable)
    GPIO.output(brightnessPin, wantToEnable)

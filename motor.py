import RPi.GPIO as GPIO

speedPin = 6
activationPin = 13
reversePin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(speedPin, GPIO.OUT)
GPIO.setup(activationPin, GPIO.OUT)
GPIO.setup(reversePin, GPIO.OUT)

speedPWM = GPIO.PWM(speedPin, 50)

def enable(speed):

    speedPWM.start(abs(speed) * 10)
    
    if speed < 0:
        GPIO.output(activationPin, False)
        GPIO.output(reversePin, True)
    elif speed > 0:
        GPIO.output(activationPin, True)
        GPIO.output(reversePin, False)
    else:
        GPIO.output(activationPin, False)
        GPIO.output(reversePin, False)
    

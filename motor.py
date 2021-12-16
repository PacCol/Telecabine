import RPi.GPIO as GPIO

speedPin = 13
activationPin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(speedPin, GPIO.OUT)
GPIO.setup(activationPin, GPIO.OUT)

speedPWM = GPIO.PWM(speedPin, 50)

def enable(enable, speed):
    GPIO.output(activationPin, enable)
    if enable:
        speedPWM.start(speed * 10)
    else:
        speedPWM.start(0)
    

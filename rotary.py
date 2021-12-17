from RPi import GPIO
from time import sleep
from threading import Thread

import __main__

def rotary():

    global __main__

    clk = 18
    dt = 15
    sw = 14

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    clkLastState = GPIO.input(clk)

    while True:
        
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        swState = GPIO.input(sw)

        if swState != 1:
            if __main__.enabled:
                __main__.changeStatus(False, __main__.speed)
            else:
                __main__.changeStatus(True, __main__.speed)
            sleep(0.3)

        if clkState != clkLastState and clkState == 1:
            if dtState == clkState:
                if __main__.speed < 10:
                    __main__.changeStatus(__main__.enabled, __main__.speed + 1)
            else:
                if __main__.speed > 1:
                    __main__.changeStatus(__main__.enabled, __main__.speed - 1)

            sleep(0.15)

        clkLastState = clkState
        sleep(0.001)


rotaryThread = Thread(target=rotary, args=())
rotaryThread.start()
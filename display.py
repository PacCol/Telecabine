import tm1637
import __main__

from time import sleep
from datetime import datetime, timedelta
from threading import Thread

tm = tm1637.TM1637(clk=27, dio=17)

dontWait = False


def display():

    global __main__, dontWait

    while True:

        now = datetime.now()

        limitDate = __main__.lastInteraction + timedelta(0, 10)

        if limitDate < now and not __main__.enabled: 
            tm.numbers(int(now.strftime("%H")), int(now.strftime("%M")))
            if smartSleep(0.5):
                tm.numbers(int(now.strftime("%H")), int(now.strftime("%M")), False)
                smartSleep(0.5)

        else:
            if __main__.enabled:
                tm.number(__main__.speed)
                smartSleep(1)
            else:
                tm.number(__main__.speed)
                if smartSleep(0.5):
                    tm.write([0, 0, 0, 0])
                    smartSleep(0.5)


def smartSleep(time):

    global dontWait
    i = 0

    while i < time:
        if dontWait:
            dontWait = False
            return False
        else:
            sleep(0.10)
        i+=0.10

    return True


def showSpeed():
    global dontWait
    dontWait = True


displayThread = Thread(target=display, args=())
displayThread.start()
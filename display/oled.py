from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont
from threading import Thread
from datetime import datetime
from time import sleep
import __main__

serial = i2c(port=1, address=0x3c)
device = sh1106(serial, rotate=0, width=128, height=64)
device.contrast(240)

fontPath = "display/montserrat400.ttf"
font = ImageFont.truetype(fontPath, 10)
bigFont = ImageFont.truetype(fontPath, 34)

iconPath = "display/material-design-icons-round.ttf"
icon = ImageFont.truetype(iconPath, 12)
bigIcon = ImageFont.truetype(iconPath, 50)

isDisplaying = False
isSleeping = False


def showHomeScreenWithoutThreading():

    global isDisplaying, isSleeping

    if isSleeping:
        device.show()
        isSleeping = False

    while isDisplaying:
        sleep(0.1)

    isDisplaying = True

    with canvas(device) as draw:

        if __main__.lightsEnabled:
            draw.text((0, 0), "\ue518", fill=1, font=icon)

        now = datetime.now()
        time = now.strftime("%H") + ":" + now.strftime("%M")
        strLength = font.getsize(time)[0]
        draw.text(((device.width - strLength) / 2, 0), time, fill=1, font=font)

        speed = str(__main__.speed) + "/10"
        strLength = bigFont.getsize(speed)[0]
        draw.text(((device.width - strLength) / 2, 16), speed, fill=1, font=bigFont)

    isDisplaying = False


def putToSleep():
    global isSleeping
    if not isSleeping:
        device.hide()
        isSleeping = True


def showHomeScreen():
    displayThread = Thread(target=showHomeScreenWithoutThreading, args=())
    displayThread.start()


def displayOff():

    device.clear()

    with canvas(device) as draw:
        iconSize = bigIcon.getsize("\ue646")
        draw.text(((device.width - iconSize[0]) / 2, 0(device.width - iconSize[1]) / 2), "\ue518", fill=1, font=icon)
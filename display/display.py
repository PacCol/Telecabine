from emulator import emulator

if emulator:
    from emulator import gpiozero, i2c, sh1106, canvas
else:
    import gpiozero
    from luma.core.interface.serial import i2c
    from luma.oled.device import sh1106
    from luma.core.render import canvas

from time import sleep
from PIL import ImageFont
from datetime import datetime

serial = i2c(port=1, address=0x3c)
device = sh1106(serial, rotate=0, width=128, height=64)
device.contrast(240)

fontPath = "display/montserrat400.ttf"
smallFont = ImageFont.truetype(fontPath, 8)
font = ImageFont.truetype(fontPath, 10)
bigFont = ImageFont.truetype(fontPath, 32)

iconPath = "display/material-design-icons-round.ttf"
smallIcon = ImageFont.truetype(iconPath, 14)
icon = ImageFont.truetype(iconPath, 12)
bigIcon = ImageFont.truetype(iconPath, 50)


class display:

    def __init__(self):
        self.currentScreen = "Home"
        self.currentSetting = "General"
        self.contrast = 240
        self.isSleeping = False
        self.isDisplaying = False
        self.lastReload = datetime.now()
        self.scroll = 0

    def getCurrentScreen(self):
        return self.currentScreen

    def getLastReload(self):
        return self.lastReload

    def displayStatus(self, motorsSpeed, lightsEnabled):

        self.lastReload = datetime.now()

        if self.isSleeping:
            device.show()
            self.currentScreen = "Home"
            self.isSleeping = False

        if self.currentScreen != "Home":
            return

        while self.isDisplaying:
            sleep(0.05)

        self.isDisplaying = True

        with canvas(device) as draw:

            if lightsEnabled:
                draw.text((0, 0), "\ue518", fill=1, font=icon)

            now = datetime.now()
            time = now.strftime("%H") + ":" + now.strftime("%M")
            strLength = font.getsize(time)[0]
            draw.text(((device.width - strLength) / 2, 0), time, fill=1, font=font)

            speed = str(motorsSpeed) + "/10"
            strLength = bigFont.getsize(speed)[0]
            draw.text(((device.width - strLength) / 2, 18), speed, fill=1, font=bigFont)

            self.isDisplaying = False

    def displaySettings(self, click, direction, currentSetting):

        self.lastReload = datetime.now()
        self.currentScreen = "Settings"

        if currentSetting != None:
            self.currentSetting = currentSetting
            self.scroll = 0

        if direction == "Down":
            self.scroll += 1
        elif direction == "Up":
            self.scroll -= 1

        def limitScroll(scrollLimit):
            if self.scroll > scrollLimit:
                self.scroll = 0
            elif self.scroll < 0:
                self.scroll = scrollLimit

        if self.currentSetting == "General":
            limitScroll(3)
        elif self.currentSetting == "Brightness":
            limitScroll(9)

        if click:
            if self.currentSetting == "General":
                if self.scroll == 0:
                    self.currentScreen = "Home"
                    return "Exit"
                elif self.scroll == 3:
                    self.currentSetting = "Brightness"
                    self.scroll = 9
                    # set the contrast to the database value
            elif self.currentSetting == "Brightness":
                self.currentSetting = "General"
                self.scroll = 3
                limitScroll(3)

        if self.isSleeping:
            device.show()
            self.isSleeping = False

        while self.isDisplaying:
            sleep(0.05)

        self.isDisplaying = True

        with canvas(device) as draw:

            now = datetime.now()
            time = now.strftime("%H") + ":" + now.strftime("%M")
            strLength = font.getsize(time)[0]
            draw.text((device.width - strLength, 0), time, fill=1, font=font)

            if self.currentSetting == "General":

                if self.scroll == 0:
                    draw.rectangle((0, 0, 12, 12), outline=0, fill=1)
                    draw.text((0, 2), "\ue5c4", fill=0, font=icon)
                else:
                    draw.text((0, 2), "\ue5c4", fill=1, font=icon)

                draw.text((14, 0), "Paramètres", fill=1, font=font)

                if self.scroll == 1:
                    draw.rectangle((0, 17, 14, 32), outline=0, fill=1)
                    draw.text((1, 18), "\ue898", fill=0, font=smallIcon)
                else:
                    draw.text((1, 18), "\ue898", fill=1, font=smallIcon)

                draw.text((17, 19), "Mot de passe", fill=1, font=font)

                if self.scroll == 2:
                    draw.rectangle((0, 33, 14, 48), outline=0, fill=1)
                    draw.text((1, 34), "\ue923", fill=0, font=smallIcon)
                else:
                    draw.text((1, 34), "\ue923", fill=1, font=smallIcon)

                draw.text((17, 35), "Mise à jour", fill=1, font=font)

                if self.scroll == 3:
                    draw.rectangle((0, 49, 15, 65), outline=0, fill=1)
                    draw.text((1, 50), "\ue518", fill=0, font=smallIcon)
                else:
                    draw.text((1, 50), "\ue518", fill=1, font=smallIcon)

                draw.text((17, 51), "Luminosité", fill=1, font=font)

            elif self.currentSetting == "Brightness":

                draw.text((0, 0), "Luminosité", fill=1, font=font)

                draw.rectangle((0, 35, device.width - 1, 40), outline=1, fill=0)

                self.contrast = (self.scroll + 1) * 24
                device.contrast(self.contrast)

                draw.text((0, 21), "\ue15b", fill=1, font=icon)
                draw.text((58, 21), "\ue518", fill=1, font=icon)
                draw.text((116, 21), "\ue145", fill=1, font=icon)
                
                draw.rectangle((1, 36, int((self.contrast / 240) * (device.width - 2)), 39), outline=0, fill=1)

                draw.text((1, 45), "Appuyez sur la molette pour", fill=1, font=smallFont)
                draw.text((1, 56), "confirmer", fill=1, font=smallFont)

        self.isDisplaying = False

    def displayOFF(self):
        with canvas(device) as draw:
            iconSize = bigIcon.getsize("\ue646")
            draw.text(((device.width - iconSize[0]) / 2, (device.height - iconSize[1]) / 2), "\ue646", fill=1, font=bigIcon)

    def putToSleep(self):
        if not self.isSleeping:
            device.hide()
            self.isSleeping = True


display = display()

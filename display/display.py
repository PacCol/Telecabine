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
from subprocess import check_call
#import os
import sys

import update

serial = i2c(port=1, address=0x3c)
device = sh1106(serial, rotate=0, width=128, height=64)
device.contrast(180)

fontPath = "display/montserrat400.ttf"
smallFont = ImageFont.truetype(fontPath, 8)
font = ImageFont.truetype(fontPath, 10)
bigFont = ImageFont.truetype(fontPath, 32)

iconPath = "display/material-design-icons-round.ttf"
xsmallIcon = ImageFont.truetype(iconPath, 12)
smallIcon = ImageFont.truetype(iconPath, 14)
mediumIcon = ImageFont.truetype(iconPath, 18)
bigIcon = ImageFont.truetype(iconPath, 40)

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

    def getCurrentSetting(self):
        return self.currentSetting

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
                draw.text((0, 0), "\ue518", fill=1, font=xsmallIcon)

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
        elif self.currentSetting == "Update":
            limitScroll(1)
        elif self.currentSetting == "Brightness":
            limitScroll(9)

        if click:
            if self.currentSetting == "General":
                if self.scroll == 0:
                    self.currentScreen = "Home"
                    return "Exit"
                elif self.scroll == 1:
                    self.currentSetting = "Brightness"
                    self.scroll = 8
                    # set the contrast to the database value
                elif self.scroll == 2:
                    self.currentSetting = "Update"
                    self.scroll = 0
                elif self.scroll == 3:
                    self.currentSetting = "About"
                    self.scroll = 0
            elif self.currentSetting == "Brightness":
                self.currentSetting = "General"
                self.scroll = 1
            elif self.currentSetting == "Update":
                if self.scroll == 0:
                    self.currentSetting = "UpdateStarted"
                elif self.scroll == 1:
                    self.currentSetting = "General"
                    self.scroll = 2
            elif self.currentSetting == "UpdateEnded":
                self.currentSetting = "General"
                self.scroll = 2
            elif self.currentSetting == "About":
                self.currentSetting = "General"
                self.scroll = 3

        if self.isSleeping:
            device.show()
            self.isSleeping = False

        while self.isDisplaying:
            sleep(0.05)

        self.isDisplaying = True

        now = datetime.now()
        time = now.strftime("%H") + ":" + now.strftime("%M")
        strLength = font.getsize(time)[0]

        if self.currentSetting == "General":
            with canvas(device) as draw:
                draw.text((device.width - strLength, 0), time, fill=1, font=font)
                if self.scroll == 0:
                    draw.rectangle((0, 0, 12, 12), outline=0, fill=1)
                    draw.text((0, 2), "\ue5c4", fill=0, font=xsmallIcon)
                else:
                    draw.text((0, 2), "\ue5c4", fill=1, font=xsmallIcon)
                draw.text((14, 0), "Paramètres", fill=1, font=font)
                if self.scroll == 1:
                    draw.rectangle((0, 17, 14, 32), outline=0, fill=1)
                    draw.text((2, 19), "\ue518", fill=0, font=xsmallIcon)
                else:
                    draw.text((2, 19), "\ue518", fill=1, font=xsmallIcon)
                draw.text((19, 19), "Luminosité", fill=1, font=font)
                if self.scroll == 2:
                    draw.rectangle((0, 33, 14, 48), outline=0, fill=1)
                    draw.text((1, 34), "\ue923", fill=0, font=smallIcon)
                else:
                    draw.text((1, 34), "\ue923", fill=1, font=smallIcon)
                draw.text((19, 35), "Mise à jour", fill=1, font=font)
                if self.scroll == 3:
                    draw.rectangle((0, 49, 15, 65), outline=0, fill=1)
                    draw.text((2, 51), "\ue88e", fill=0, font=xsmallIcon)
                else:
                    draw.text((2, 51), "\ue88e", fill=1, font=xsmallIcon)
                draw.text((19, 51), "À propos", fill=1, font=font)

        elif self.currentSetting == "Brightness":
            with canvas(device) as draw:
                draw.text((0, 0), "Luminosité", fill=1, font=font)
                draw.rectangle((0, 35, device.width - 1, 40), outline=1, fill=0)
                self.contrast = (self.scroll + 1) * 24
                device.contrast(self.contrast)
                # set database value
                draw.text((0, 21), "\ue15b", fill=1, font=xsmallIcon)
                draw.text((58, 21), "\ue518", fill=1, font=xsmallIcon)
                draw.text((116, 21), "\ue145", fill=1, font=xsmallIcon)
                draw.rectangle((1, 36, int((self.contrast / 240) * (device.width - 2)), 39), outline=0, fill=1)
                draw.text((0, 45), "Appuyez sur la molette pour", fill=1, font=smallFont)
                draw.text((0, 56), "confirmer", fill=1, font=smallFont)

        elif self.currentSetting == "Update":
            with canvas(device) as draw:
                draw.text((0, 0), "Mise à jour", fill=1, font=font)
                if self.scroll == 0:
                    draw.rectangle((0, 28, 64, 40), outline=1, fill=1)
                    draw.rectangle((64, 28, 127, 40), outline=1, fill=0)
                    draw.text((25, 30), "OK", fill=0, font=smallFont)
                    draw.text((80, 30), "Annuler", fill=1, font=smallFont)
                elif self.scroll == 1:
                    draw.rectangle((0, 28, 64, 40), outline=1, fill=0)
                    draw.rectangle((64, 28, 127, 40), outline=1, fill=1)
                    draw.text((25, 30), "OK", fill=1, font=smallFont)
                    draw.text((80, 30), "Annuler", fill=0, font=smallFont)
                draw.text((0, 45), "Avant toute chose, vérifiez que", fill=1, font=smallFont)
                draw.text((0, 56), "votre réseau Wi-Fi est stable.", fill=1, font=smallFont)

        elif self.currentSetting == "About":
            with canvas(device) as draw:
                draw.text((device.width - strLength, 0), time, fill=1, font=font)
                draw.text((0, 0), "À propos", fill=1, font=font)
                releaseLength = smallFont.getsize("Version: " + update.getCurrentVersion()[0])[0]
                noteLength = smallFont.getsize("Note: " + update.getCurrentVersion()[1])[0]
                draw.text(((device.width - releaseLength) / 2, 29), "Version: " + update.getCurrentVersion()[0], fill=1, font=smallFont)
                draw.text(((device.width - noteLength) / 2, 41), "Note: " + update.getCurrentVersion()[1], fill=1, font=smallFont)

        elif self.currentSetting == "UpdateStarted":
            with canvas(device) as draw:
                draw.text((0, 0), "Recherche de MAJ", fill=1, font=font)
                draw.text((55, 26), "\ue8b6", fill=1, font=mediumIcon)
                draw.text((0, 54), "Ne pas interrompre l'appareil.", fill=1, font=smallFont)
            ret = update.updateCode()

            def reboot():
                sleep(2)
                #print("RESTARTING...")
                check_call(['sudo', 'reboot'])
                #os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

            if ret == "No changes":
                self.currentSetting = "UpdateEnded"
                device.clear()
                with canvas(device) as draw:
                    draw.text((0, 0), "Aucune MAJ", fill=1, font=font)
                    draw.text((55, 26), "\uea76", fill=1, font=mediumIcon)
                    draw.text((0, 54), "Cliquez pour retourner au menu.", fill=1, font=smallFont)
                
            elif ret == "Updated":
                device.clear()
                with canvas(device) as draw:
                    draw.text((0, 0), "Mise à jour installée", fill=1, font=font)
                    draw.text((55, 26), "\ue8d7", fill=1, font=mediumIcon)
                    draw.text((0, 54), "Mise à jour des modules...", fill=1, font=smallFont)
                _ret = update.updateModules()
                if _ret == "Success":
                    device.clear()
                    with canvas(device) as draw:
                        draw.text((0, 0), "Mise à jour terminée", fill=1, font=font)
                        draw.text((55, 26), "\ue876", fill=1, font=mediumIcon)
                        draw.text((0, 54), update.getCurrentVersion()[0], fill=1, font=smallFont)
                    sleep(2)
                    device.clear()
                    with canvas(device) as draw:
                        draw.text((0, 0), "Redémmarrage...", fill=1, font=font)
                        draw.text((44, 23), "\uf053", fill=1, font=bigIcon)
                        sleep(2)
                    reboot()
                elif _ret == "Network unreachable":
                    self.screen = "UpdateStarted"
                    device.clear()
                    with canvas(device) as draw:
                        draw.text((0, 0), "Erreur réseau", fill=1, font=font)
                        draw.text((55, 26), "\ue000", fill=1, font=mediumIcon)
                        draw.text((0, 54), "Clickez pour réessayer.", fill=1, font=smallFont)
            elif ret == "Network unreachable":
                self.currentSetting = "UpdateEnded"
                device.clear()
                with canvas(device) as draw:
                    draw.text((0, 0), "Erreur réseau", fill=1, font=font)
                    draw.text((55, 26), "\ue000", fill=1, font=mediumIcon)
                    draw.text((0, 54), "Réessayez plus tard...", fill=1, font=smallFont)

        self.isDisplaying = False

    def displayOFF(self):
        self.isDisplaying = True
        with canvas(device) as draw:
            iconSize = bigIcon.getsize("\ue646")
            draw.text(((device.width - iconSize[0]) / 2, (device.height - iconSize[1]) / 2), "\ue646", fill=1, font=bigIcon)

    def putToSleep(self):
        if not self.isSleeping:
            device.hide()
            self.isSleeping = True


display = display()

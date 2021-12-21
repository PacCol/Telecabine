import gpiozero
from time import sleep

from gpiozero.internal_devices import CPUTemperature

google = gpiozero.PingServer("google.com")

while True:
    if google.is_active:
        break
    sleep(0.3)


from flask import Flask, redirect, send_from_directory, request
from datetime import datetime

app = Flask(__name__)

import sse, motor, lights

enabled = False
lightsEnabled = False
speed = 8
lastInteraction = datetime.now()

cpu = gpiozero.CPUTemperature()


@app.route("/")
def index():
    return redirect("/config/index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico")


@app.route("/config/<path:path>")
def webApp(path):
    return send_from_directory("static", path)


@app.route("/api/status", methods=["POST"])
def pingStatus():
    sendStatus()
    return "sended"


def sendStatus():

    if enabled:
        status = "enabled"
    else:
        status = "disabled"

    if lightsEnabled:
        ledStatus = "enabled"
    else:
        ledStatus= "disabled"

    msg = sse.format_sse(data="status:" + status + ",speed:" + str(speed) + ",ledStatus:" + ledStatus)
    sse.announcer.announce(msg=msg)


@app.route("/api/enable", methods=["POST"])
def enable():
    changeStatus(request.json["enable"], speed)
    return "enabled"


@app.route("/api/enablelights", methods=["POST"])
def enableLights():
    illuminatedButton.changeStatus(request.json["enable"])
    return "enabled"


@app.route("/api/speed", methods=["POST"])
def setSpeed():
    changeStatus(enabled, request.json["speed"])
    return "changed"

@app.route("/api/cpuTemp", methods=["GET"])
def getCPUTemp():
    return str(int(cpu.temperature)) + " °C"


def changeStatus(newState, newSpeed):
    global enabled, speed, lastInteraction
    enabled = newState
    speed = newSpeed
    motor.enable(enabled, speed)
    sendStatus()
    lastInteraction = datetime.now()
    display.showSpeed()


import rotary, display, illuminatedButton

app.run(host="0.0.0.0", port=80)

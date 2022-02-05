import gpiozero
from time import sleep
from flask import Flask, redirect, send_from_directory, request
from datetime import datetime


google = gpiozero.PingServer("google.com")

while True:
    if google.is_active:
        break
    sleep(0.3)


app = Flask(__name__)


lightsEnabled = False
speed = 0
sleeping = False
lastInteraction = datetime.now()

cpu = gpiozero.CPUTemperature()


import rotary, display.display as display, illuminatedButton, sse, motor


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

    if lightsEnabled:
        ledStatus = "enabled"
    else:
        ledStatus= "disabled"

    msg = sse.format_sse("speed:" + str(speed) + ",ledStatus:" + ledStatus)
    sse.announcer.announce(msg=msg)


@app.route("/api/enablelights", methods=["POST"])
def enableLights():
    illuminatedButton.changeStatus(request.json["enable"])
    return "enabled"


@app.route("/api/speed", methods=["POST"])
def setSpeed():
    changeStatus(request.json["speed"])
    return "changed"


@app.route("/api/cpuTemp", methods=["GET"])
def getCPUTemp():
    return str(int(cpu.temperature)) + " °C"


def changeStatus(newSpeed):
    global speed, lastInteraction, rotary
    speed = newSpeed
    rotary.rotor.steps = speed
    motor.enable(speed)
    sendStatus()
    lastInteraction = datetime.now()
    display.displayStatus()


app.run(host="0.0.0.0", port=80)

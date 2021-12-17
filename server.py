import time

time.sleep(0)

from flask import Flask, redirect, send_from_directory, request
from datetime import datetime

app = Flask(__name__)

import sse, motor

enabled = False
speed = 8
lastInteraction = datetime.now()


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
        msg = sse.format_sse(data="status:enabled,speed:" + str(speed))
    else:
        msg = sse.format_sse(data="status:disabled,speed:" + str(speed))

    sse.announcer.announce(msg=msg)


@app.route("/api/enable", methods=["POST"])
def enable():
    changeStatus(request.json["enable"], speed)
    return "enabled"


@app.route("/api/speed", methods=["POST"])
def setSpeed():
    changeStatus(enabled, request.json["speed"])
    return "changed"


def changeStatus(newState, newSpeed):
    global enabled, speed, lastInteraction
    enabled = newState
    speed = newSpeed
    motor.enable(enabled, speed)
    sendStatus()
    lastInteraction = datetime.now()
    display.showSpeed()


import rotary, display

app.run(host="0.0.0.0", port=80)

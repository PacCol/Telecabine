from flask import Flask, redirect, send_from_directory, request, Response
from datetime import datetime

from emulator import emulator
from status import *

if emulator:
    from emulator import gpiozero
else:
    import gpiozero

import hardware

app = Flask(__name__)

cpu = gpiozero.CPUTemperature()

import sse


@app.route("/")
def index():
    return redirect("/config/index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico")


@app.route("/config/<path:path>")
def webApp(path):
    return send_from_directory("static", path)


@app.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = sse.announcer.listen()
        while True:
            msg = messages.get()
            yield msg

    return Response(stream(), mimetype='text/event-stream')


@app.route("/api/status", methods=["POST"])
def pingStatus():
    sendStatus()
    return "sended"


def sendStatus():

    if hardware.lights.getStatus():
        ledStatus = "enabled"
    else:
        ledStatus= "disabled"

    msg = sse.format_sse("speed=" + str(hardware.motors.getSpeed()) + ",ledStatus=" + ledStatus + ",startTime=" + str(hardware.motors.getStartTime()))
    sse.announcer.announce(msg=msg)


@app.route("/api/enablelights", methods=["POST"])
def enableLights():
    hardware.setOutput(None, request.json["enable"])
    sendStatus()
    return "enabled"


@app.route("/api/speed", methods=["POST"])
def setSpeed():
    hardware.setOutput(request.json["speed"], None)
    sendStatus()
    return "changed"


@app.route("/api/cpuTemp", methods=["GET"])
def getCPUTemp():
    return str(int(cpu.temperature)) + " °C"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

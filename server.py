from flask import Flask, redirect, send_from_directory, request, Response
from datetime import datetime

from emulator import emulator
from status import *

if emulator:
    from emulator import gpiozero
else:
    import gpiozero

import sse
import hardware

app = Flask(__name__)

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
    sse.sendStatus(hardware.motors.getSpeed(), hardware.lights.getStatus(), hardware.motors.getStartTime())
    return "sended"


@app.route("/api/enablelights", methods=["POST"])
def enableLights():
    hardware.setOutput(None, request.json["enable"])
    return "enabled"


@app.route("/api/speed", methods=["POST"])
def setSpeed():
    hardware.setOutput(request.json["speed"], None)
    return "changed"


@app.route("/api/cpuTemp", methods=["GET"])
def getCPUTemp():
    return str(int(cpu.temperature)) + " °C"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

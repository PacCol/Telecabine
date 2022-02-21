import gpiozero
from time import sleep
from flask import Flask, redirect, send_from_directory, request, Response
from datetime import datetime

lastInteraction = datetime.now()
sleeping = False

from chairlift import motors, lights
import status
from inputDevices import illuminatedButton, rotary

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

    if lights.getStatus():
        ledStatus = "enabled"
    else:
        ledStatus= "disabled"

    msg = sse.format_sse("speed:" + str(motors.getSpeed()) + ",ledStatus:" + ledStatus)
    sse.announcer.announce(msg=msg)


@app.route("/api/enablelights", methods=["POST"])
def enableLights():
    status.setStatus(None, request.json["enable"])
    return "enabled"


@app.route("/api/speed", methods=["POST"])
def setSpeed():
    status.setStatus(request.json["speed"], None)
    return "changed"


@app.route("/api/cpuTemp", methods=["GET"])
def getCPUTemp():
    return str(int(cpu.temperature)) + " °C"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

from flask import Flask, Response, redirect, send_from_directory, request
import queue

app = Flask(__name__)

import sse


enabled = False
speed = 8


@app.route("/")
def index():
    return redirect("/config/index.html")


@app.route("/config/<path:path>")
def webApp(path):
    return send_from_directory("static", path)


@app.route("/api/status", methods=["POST"])
def pingStatus():
    sendStatus()
    return "sended"


def sendStatus():
    global enabled

    if enabled:
        msg = sse.format_sse(data="status:enabled,speed:" + str(speed))
    else:
        msg = sse.format_sse(data="status:disabled,speed:" + str(speed))

    sse.announcer.announce(msg=msg)


@app.route("/api/enable", methods=["POST"])
def enable():
    global enabled
    enabled = request.json["enable"]
    sendStatus()
    return "enabled"


@app.route("/api/speed", methods=["POST"])
def setSpeed():
    global speed
    speed = request.json["speed"]
    sendStatus()
    return "enabled"


app.run(host="0.0.0.0", port=5000)
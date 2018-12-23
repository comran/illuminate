from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import json
import math
import base64

import sys
sys.path.append('tools/cache/proto')
import messages_pb2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lettherebelight!'
socketio = SocketIO(app)

@socketio.on('connect')
def connect():
    print("someone connected")

@socketio.on('pixel_locations')
def set_lights(m):
    print(m)

    decoded = base64.b64decode(m)
    # print(decoded)

    pixels = messages_pb2.PixelLayout()
    pixels.ParseFromString(decoded)

    for pixel in pixels.pixel_locations:
        print(str(pixel.index) + ": " + str(pixel.x) + ", " + str(pixel.y))


if __name__ == '__main__':
    socketio.run(app)

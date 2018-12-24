from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import json
import math
import base64

import sys
sys.path.append('tools/cache/proto')
import messages_pb2
sys.dont_write_bytecode = True
sys.path.insert(0, 'lib')
import process_manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lettherebelight!'
socketio = SocketIO(app)
processes = process_manager.ProcessManager()

def run_and_die_if_error(command):
    if (processes.spawn_process_wait_for_code(command) != 0):
        processes.killall()
        sys.exit(1)

@socketio.on('connect')
def connect():
    print("someone connected")

@socketio.on('set_pixel_locations')
def set_pixel_locations(m):
    decoded = base64.b64decode(m)

    pixels = messages_pb2.PixelLayout()
    pixels.ParseFromString(decoded)

    # for pixel in pixels.pixel_locations:
    #     print(str(pixel.index) + ": " + str(pixel.x) + ", " + str(pixel.y))

    file = open("tools/cache/server/pixels.illp", "w") 
    file.write(m)
    file.close()

@socketio.on('get_pixel_locations')
def get_pixel_locations(data):
    csv_file = None
    try:
        csv_file = open("tools/cache/server/pixels.illp")
    except IOError:
        print("Cannot open pixel locations.")
        return

    read_file = str(csv_file.readlines()[0])

    return read_file


if __name__ == '__main__':
    run_and_die_if_error("mkdir -p tools/cache/server")

    socketio.run(app)

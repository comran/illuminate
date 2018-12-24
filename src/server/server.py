from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import json
import math
import base64
import hashlib
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

partial_routine_numberings = list()
partial_routines = dict()

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

    file = open("tools/cache/server/pixels.illp", "w") 
    file.write(m)
    file.close()

@socketio.on('set_partial_routine')
def set_partial_routine(m):
    partial_routine_numberings.append(m[0])
    partial_routines[m[0]] = m[1]

@socketio.on('set_routine')
def set_routine(hash):
    global partial_routine_numberings
    global partial_routines
    partial_routine_numberings.sort()

    reassembled_data = ""
    for partial_routine_numbering in partial_routine_numberings:
        reassembled_data += partial_routines[partial_routine_numbering]

    partial_routine_numberings = []
    partial_routines = dict()

    if(str(hashlib.md5(reassembled_data.encode('utf-8')).hexdigest()) != hash):
        print("Corrupted routines data from client.")
        return

    decoded = base64.b64decode(reassembled_data)
    routine = messages_pb2.Routine()
    try:
        routine.ParseFromString(decoded)
    except:
        print("Error parsing protobuf.")
        return

    file = open("tools/cache/server/routines/" + routine.name + ".illr", "w") 
    file.write(reassembled_data)
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
    run_and_die_if_error("mkdir -p tools/cache/server/routines")

    socketio.run(app)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from threading import Thread

import json
import math
import base64
import hashlib
import time
import os
import math
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
kToWrite = 10000


partial_routine_numberings = list()
partial_routines = dict()

routines = dict()
routines_encoded = dict()

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


@socketio.on('set_routine_start')
def set_routine_start():
    global partial_routine_numberings
    global partial_routines
    partial_routine_numberings = []
    partial_routines = dict()


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

    print("Successfully received routine: " + routine.name)

    file = open("tools/cache/server/routines/" + routine.name + ".illr", "w") 
    file.write(reassembled_data)
    file.close()

    routines[routine.name] = routine
    routines_encoded[routine.name] = reassembled_data


@socketio.on('get_routine_list')
def get_routine_list(m):
    routine_list = list(routines.keys())
    routine_dict = dict()

    count = 0
    for routine in routine_list:
        routine_dict[count] = routine
        count += 1

    return routine_dict


@socketio.on('get_partial_routine')
def get_partial_routine(m):
    routine_encoded = routines_encoded[m["name"]]
    print("size is " + str(len(routine_encoded)))

    written = 0
    global kToWrite
    count = 0
    while written < len(routine_encoded):
        msg = dict()
        end = min(written + kToWrite, len(routine_encoded))
        part = routine_encoded[written:end]

        count += 1

        msg["payload"] = str(part)
        msg["name"] = m["name"]
        msg["count"] = count

        socketio.emit(m["rx_identifier"], msg)
        written += kToWrite

@socketio.on('get_routine_number_of_partial_routines')
def get_routine_number_of_partial_routines(routine):
    global kToWrite
    return math.ceil(len(routines_encoded[routine]) / kToWrite)


if __name__ == '__main__':
    run_and_die_if_error("mkdir -p tools/cache/server")
    run_and_die_if_error("mkdir -p tools/cache/server/routines")

    for root, dirs, files in os.walk("tools/cache/server/routines"):  
        for filename in files:
            routine_filename = root + "/" + filename
            try:
                routine_file = open(routine_filename)
            except IOError:
                print("Cannot open saved routine: " + routine_filename)
                os.remove(routine_filename)
                continue
            
            lines = 0
            with open(routine_filename) as f:
                for i, l in enumerate(f):
                    lines += 1

            if lines < 1:
                print("Routine file does not contain any data: " + routine_filename)
                os.remove(routine_filename)
                continue

            read_file = str(routine_file.readlines()[0])
            decoded = base64.b64decode(read_file)
            routine = messages_pb2.Routine()
            try:
                routine.ParseFromString(decoded)
            except:
                print("Error parsing protobuf: " + routine_filename)
                os.remove(routine_filename)
                continue

            print("Opened saved routine file: " + routine.name + " with " + str(len(routine.frames)) + " frames")
            
            routines[routine.name] = routine
            routines_encoded[routine.name] = read_file

    socketio.run(app)

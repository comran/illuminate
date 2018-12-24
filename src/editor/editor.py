import cv2
import numpy as np
from requests.exceptions import ConnectionError
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import time
import argparse
import base64
import sys
sys.path.append('tools/cache/proto')
sys.dont_write_bytecode = True
import messages_pb2

args = None
socket = None

def on_connect():
    print('connected.')

    if args.mapping is not None:
        update_pixel_locations(args.mapping)

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')


def update_pixel_locations(mapping_file):
    csv_file = None

    try:
        csv_file = open(mapping_file)
    except IOError:
        print("Cannot open pixel location CSV file.")
        sys.exit(1)

    # Get max width and height of CSV data.
    width = 0
    height = 0
    for line in csv_file:
        line_split = line.split(",")
        width = max(width, len(line_split)) 
        height += 1

    csv_file = open(mapping_file)

    pixel_set = dict()

    pixel_layout = messages_pb2.PixelLayout()

    if width < height:
        if height > 0:
            pixel_layout.width = width / height
            pixel_layout.height = 1
        else:
            pixel_layout.width = 0
            pixel_layout.height = 0
    else:
        if width > 0:
            pixel_layout.height = height / width
            pixel_layout.width = 1
        else:
            pixel_layout.width = 0
            pixel_layout.height = 0

    y = 0
    for line in csv_file:
        x = 0

        line_split = line.split(",")
        seg = ""
        for pixel in line_split:
            if pixel.lstrip() == "":
                seg += " "
            else:
                # Check for duplicate pixels.
                if pixel in pixel_set:
                    print("Duplicate pixel index: " + pixel)
                    sys.exit(1)
                pixel_set[pixel] = True

                # Add pixel location to protobuf.
                pixel_location = pixel_layout.pixel_locations.add()
                pixel_location.x = x / width
                pixel_location.y = y / height
                pixel_location.index = int(pixel)

                print(str(pixel_location.index) + ": " + str(pixel_location.x))
            x += 1
        y = y + 1
    
    data = base64.b64encode(pixel_layout.SerializeToString()).decode("ascii")
    socket.emit("set_pixel_locations", data)

if __name__ == '__main__':
    print("connecting...")
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--mapping', action='store', required=True)

    args = parser.parse_args()

    socket = SocketIO('0.0.0.0', 5000)
    socket.on('connect', on_connect)
    socket.on('disconnect', on_disconnect)
    socket.on('reconnect', on_reconnect)

    connected_called = False

    while True:
        if socket.connected and not connected_called:
            on_connect()
            break

import cv2
import numpy as np
from requests.exceptions import ConnectionError
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import time
import argparse
import base64
import hashlib
import sys
sys.path.append('tools/cache/proto')
sys.dont_write_bytecode = True
import operator
import messages_pb2

socket = None

routine = None
minx = None
miny = None
maxx = None
maxy = None


class PixelLocationIndexed:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index


def on_connect():
    print('connected.')


def on_disconnect():
    print('disconnect')


def on_reconnect():
    print('reconnect')


def run_mapping(args):
    # Wait for connection to server.
    while True:
        if socket.connected:
            break

    csv_file = None

    try:
        csv_file = open(args.csv)
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

    csv_file = open(args.csv)

    pixel_set = dict()

    pixel_layout = messages_pb2.PixelLayout()
    pixel_locations = list()

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
                pixel_locations.append(PixelLocationIndexed( \
                    x / width, \
                    y / height, \
                    int(pixel)))
            x += 1
        y = y + 1

    pixel_locations.sort(key=operator.attrgetter('index'))

    i = 0
    for pixel_location in pixel_locations:
        pixel_location_proto = pixel_layout.pixel_locations.add()
        pixel_location_proto.x = pixel_locations[i].x
        pixel_location_proto.y = pixel_locations[i].y

        print(str(i) + ": " \
            + str(pixel_locations[i].x) \
            + ", " + str(pixel_locations[i].y))

        i += 1

    data = base64.b64encode(pixel_layout.SerializeToString()).decode("ascii")
    socket.emit("set_pixel_locations", data)


def run_routine(args):
    try:
        video = cv2.VideoCapture(args.video)
    except:
        print("problem opening input stream")
        sys.exit(1)

    if not video.isOpened():
        print("capture stream not open")
        sys.exit(1)

    global routine
    routine = messages_pb2.Routine()
    routine.name = args.id
    routine.fps = 30

    global minx, miny, maxx, maxy
    minx = int(args.minx)
    miny = int(args.miny)
    maxx = int(args.maxx)
    maxy = int(args.maxy)

    if minx > maxx or minx < 0:
        print("invalid x range: [" + str(minx) + ", " + str(maxx) + "]")

    if miny > maxy or miny < 0:
        print("invalid y range: [" + str(miny) + ", " + str(maxy) + "]")

    def extraction(pixel_layout_data):
        global routine

        socket.emit("set_routine_start")

        pixel_layout = messages_pb2.PixelLayout()
        pixel_layout.ParseFromString(base64.b64decode(pixel_layout_data))

        success, image = video.read()
        count = 0

        while success:
            success, image = video.read()
            if not success:
                break

            height, width = image.shape[:2]

            global minx, miny, maxx, maxy
            maxx = min(maxx, width)
            maxy = min(maxy, height)

            frame = routine.frames.add()
            for pixel_location in pixel_layout.pixel_locations:
                x = int(minx + (maxx - minx) * pixel_location.x)
                y = int(miny + (maxy - miny) * pixel_location.y)

                color_tuple = image[y, x]
                color = (color_tuple[0] << 16) + (color_tuple[1] << 8) + (
                    color_tuple[2])
                frame.pixel_colors.append(color)

            print('Read frame #', count)
            count += 1

        data = base64.b64encode(routine.SerializeToString()).decode("ascii")

        i = 0
        increment_size = 20000
        while i < len(data):
            print("sending " + str(i))
            subdata = data[i:min(len(data), i + increment_size)]
            to_send = [i, subdata]

            socket.emit("set_partial_routine", to_send)
            i += increment_size
            time.sleep(0.05)

        time.sleep(1)
        socket.emit("set_routine",
                    str(hashlib.md5(data.encode('utf-8')).hexdigest()))

    socket.emit("get_pixel_locations", "", extraction)
    print("Waiting for callback with pixel locations...")
    socket.wait_for_callbacks(10)


if __name__ == '__main__':
    print("connecting...")

    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers()
    mapping_parser = subparser.add_parser('mapping')
    mapping_parser.add_argument('--csv', action='store', required=True)
    mapping_parser.set_defaults(func=run_mapping)
    routine_parser = subparser.add_parser('routine')
    routine_parser.add_argument('--video', action='store', required=True)
    routine_parser.add_argument('--id', action='store', required=True)
    routine_parser.add_argument('--minx', action='store', required=True)
    routine_parser.add_argument('--miny', action='store', required=True)
    routine_parser.add_argument('--maxx', action='store', required=True)
    routine_parser.add_argument('--maxy', action='store', required=True)

    routine_parser.set_defaults(func=run_routine)

    socket = SocketIO('0.0.0.0', 5000)
    # socket = SocketIO('comran.org', 5000)
    socket.on('connect', on_connect)
    socket.on('disconnect', on_disconnect)
    socket.on('reconnect', on_reconnect)

    args = parser.parse_args()
    args.func(args)

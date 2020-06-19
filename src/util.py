import time
import os
import rpi_ws281x
import logging
import numpy as np
import cv2 as cv
import cython

import util_cython


class PhasedLoop:
    def __init__(self, frequency, verbose=False):
        self.frequency = frequency
        self.last_pause = None
        self.verbose = verbose
        self.counter = 0

    def pause(self):
        current_time = time.time()

        if self.last_pause == None:
            self.last_pause = current_time
            return

        time_to_pause = 1.0 / self.frequency
        time_to_pause -= (current_time - self.last_pause) / 3
        time_to_pause = max(0.0, time_to_pause)
        diff = (current_time - self.last_pause)

        if (diff > 0):
            frequency = 1.0 / diff
            time.sleep(time_to_pause)
            self.last_pause = current_time

            if self.verbose and self.counter == 0:
                print(time_to_pause)
                print("Loop frequency: " + str(frequency))

            self.counter = (self.counter + 1) % (3 * self.frequency)


class PixelLayout:
    def __init__(self):
        self.pixel_locations = {}
        self.width = 0
        self.height = 0
        self.pixel_list = []

        # Load pixel locations from file.
        with open("generators/layouts/layout.csv", "r") as a_file:
            y = 0
            for line in a_file:
                stripped_line = line.strip()
                x = 0
                for column in stripped_line.split(","):
                    x += 1
                    if column == "":
                        continue

                    self.pixel_locations[int(column)] = (x - 1, y)
                y += 1

                self.width = max(x, self.width)
            self.height = max(y, self.height)

        self.pixels_to_layout = np.zeros(
            (len(self.pixel_locations), self.width, self.height), np.float32)

        for pixel_index in range(len(self.pixel_locations.keys())):
            pixel_location = self.pixel_locations[pixel_index]
            self.pixels_to_layout[pixel_index, pixel_location[0],
                                  pixel_location[1]] = 1
            self.pixel_list.append(pixel_location)

        self.pixel_list = np.array(self.pixel_list)

    def pixel_colors_to_image(self, colors, width, height):
        scale = 6
        img = np.zeros((self.height * scale, self.width * scale, 3), np.uint8)

        img = util_cython.draw_many_pixels(img, colors.astype(np.uint8),
                                           self.pixel_list.astype(np.uint8),
                                           scale)
        img = np.asarray(img)

        return img


def pixel_colors_to_image(self, colors, width, height):
    img = np.zeros((height, width, 3), np.uint8)

    i = 0
    for color in colors[0]:
        x, y = self.pixel_locations[i]

        x = int(x * width / self.width)
        y = int(y * height / self.height)

        color = colors[0, i]
        cv.circle(img, (x, y), 7, color, thickness=-1)

        i += 1

    return img


def numpy_to_ws281x_pixel(numpy_pixel):
    return rpi_ws281x.Color(
        int(numpy_pixel[2]), int(numpy_pixel[1]), int(numpy_pixel[0]))


def is_raspi():
    return os.uname()[4][:3] == "arm"


def unit_color_to_byte_color(unit_color):
    return (int(unit_color[0] * 255), int(unit_color[1] * 255),
            int(unit_color[2] * 255))


illuminate_logger = logging.getLogger('IlluminateLogger')


def get_logger():
    return illuminate_logger

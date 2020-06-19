import numpy as np
import colorsys
import random

from src import constants
from src import util

DEFAULT_BARBERSHOP_LENGTH = 50


class BarbershopRoutine:
    def __init__(self):
        self.frame = np.zeros([1, constants.LED_COUNT, 3], np.uint8)

        self.color_generator = None
        self.color1 = np.array([0, 0, 0])
        self.color2 = np.array([255, 255, 255])
        self.offset = 0

        self.speed = 1.
        self.cycle_length = DEFAULT_BARBERSHOP_LENGTH

    def setup(self):
        h = random.uniform(0, 1)
        s = 1.
        v = 1.
        self.color1 = colorsys.hsv_to_rgb(h, s, v)
        self.color2 = colorsys.hsv_to_rgb(h, s, v * 0.2)

        self.color1 = util.unit_color_to_byte_color(self.color1)
        self.color2 = util.unit_color_to_byte_color(self.color2)

        self.speed = random.uniform(-1.5, 1.5)
        self.cycle_length = DEFAULT_BARBERSHOP_LENGTH * random.uniform(0.1, 1.)

    def get_frame(self):
        for i in range(constants.LED_COUNT):
            if (i + int(
                    self.offset)) % self.cycle_length < self.cycle_length / 2:
                color = self.color1
            else:
                color = self.color2

            self.frame[0, i] = color

        self.offset = (self.offset + self.speed) % self.cycle_length

        return self.frame

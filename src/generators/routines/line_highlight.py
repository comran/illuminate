import colorsys
import numpy as np
import random

from src import constants
from src import util

LINE_HIGHLIGHT_RAINBOW_CYCLE_TIME = 10


class LineHighlightRoutine:
    def __init__(self):
        self.frame_index = 0
        self.frame = np.zeros((1, constants.LED_COUNT, 3), dtype=np.uint8)
        self.color_generator = None
        self.black_color = np.zeros(3)

    def get_new_color(self):
        if self.color_generator is not None:
            self.color = np.array([self.color_generator.get_color()])
        else:
            self.color = colorsys.hsv_to_rgb(random.uniform(0, 1), 1.0, 1.0)
            self.color = util.unit_color_to_byte_color(self.color)

    def apply_theme(self, color_generator):
        self.color_generator = color_generator

    def get_frame(self):
        adjusted_index = self.frame_index % (constants.LED_COUNT * 2)
        if adjusted_index == 0:
            self.get_new_color()

        if self.frame_index % (constants.LED_COUNT * 2) < constants.LED_COUNT:
            adjusted_index = self.frame_index % constants.LED_COUNT
            self.frame[0, adjusted_index] = self.color
        else:
            adjusted_index -= constants.LED_COUNT
            self.frame[0, adjusted_index] = self.black_color

        self.frame_index += 1

        return self.frame

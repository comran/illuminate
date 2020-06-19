import numpy as np
import colorsys

from src import constants
from src import util

RAINBOW_HUE_TIME_TO_COMPLETE = 10


class RainbowHueRoutine:
    def __init__(self):
        self.frame = np.zeros((1, constants.LED_COUNT, 3), dtype=np.uint8)
        self.hue = 0
        self.color_generator = None

    def apply_theme(self, color_generator):
        self.color_generator = color_generator

    def get_frame(self):
        if self.color_generator is None:
            self.hue = self.hue + (
                1 / constants.FRAMES_PER_SECOND / RAINBOW_HUE_TIME_TO_COMPLETE)
            self.hue = self.hue % 1
            color = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
            color = np.flip(np.array(util.unit_color_to_byte_color(color)))
        else:
            color = np.flip(np.array(self.color_generator.get_color()))

        for i in range(constants.LED_COUNT):
            self.frame[0, i] = color

        return self.frame

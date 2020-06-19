import colorsys
import numpy as np

from src import constants
from src import util

RAINBOW_HUE_TIME_TO_COMPLETE = 10


class LineHighlightRainbowRoutine:
    def __init__(self):
        self.hue = 0

        self.frame_index = 0
        self.frame = np.zeros((1, constants.LED_COUNT, 3), dtype=np.uint8)
        self.black_color = np.zeros(3)
        self.color_generator = None

    def apply_theme(self, color_generator):
        self.color_generator = color_generator

    def get_frame(self):
        adjusted_index = self.frame_index % (constants.LED_COUNT * 2)

        color = self.black_color
        if self.color_generator is None:
            self.hue = self.hue + (
                1 / constants.FRAMES_PER_SECOND / RAINBOW_HUE_TIME_TO_COMPLETE)
            self.hue = self.hue % 1
            color = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
            color = np.flip(np.array(util.unit_color_to_byte_color(color)))
        else:
            color = np.flip(np.array(self.color_generator.get_color()))

        if self.frame_index % (constants.LED_COUNT * 2) < constants.LED_COUNT:
            adjusted_index = self.frame_index % constants.LED_COUNT
            self.frame[0, adjusted_index] = color
        else:
            adjusted_index -= constants.LED_COUNT
            self.frame[0, adjusted_index] = self.black_color

        self.frame_index += 1

        return self.frame

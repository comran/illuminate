import numpy as np
import random
import colorsys

import constants
import util

class LineHighlightRoutine:
    def __init__(self, number_of_leds):
        self.frame_index = 0
        self.frame = np.zeros(shape=(number_of_leds, 3), dtype=int)

    def get_new_color(self):
        self.color = colorsys.hsv_to_rgb(random.uniform(0, 1), 1.0, 0.3)
        self.color = util.unit_color_to_byte_color(self.color)

    def get_frame(self):
        adjusted_index = self.frame_index % (constants.LED_COUNT * 2)
        if adjusted_index == 0:
            self.get_new_color()

        if self.frame_index % (constants.LED_COUNT * 2) < constants.LED_COUNT:
            adjusted_index = self.frame_index % constants.LED_COUNT
            self.frame[adjusted_index][0] = self.color[0]
            self.frame[adjusted_index][1] = self.color[1]
            self.frame[adjusted_index][2] = self.color[2]
        else:
            adjusted_index -= constants.LED_COUNT
            self.frame[adjusted_index][0] = 0
            self.frame[adjusted_index][1] = 0
            self.frame[adjusted_index][2] = 0

        self.frame_index += 1

        return self.frame

LINE_HIGHLIGHT_RAINBOW_CYCLE_TIME = 10
class LineHighlightRainbowRoutine:
    def __init__(self, number_of_leds):
        self.hue = 0
        
        self.frame_index = 0
        self.frame = np.zeros(shape=(number_of_leds, 3), dtype=int)

    def get_frame(self):
        adjusted_index = self.frame_index % (constants.LED_COUNT * 2)

        self.hue = self.hue + (1 / constants.FRAMES_PER_SECOND
            / RAINBOW_HUE_TIME_TO_COMPLETE)
        self.hue = self.hue % 1
        color = colorsys.hsv_to_rgb(self.hue, 1.0, 0.3)
        color = util.unit_color_to_byte_color(color)

        if self.frame_index % (constants.LED_COUNT * 2) < constants.LED_COUNT:
            adjusted_index = self.frame_index % constants.LED_COUNT
            self.frame[adjusted_index][0] = color[0]
            self.frame[adjusted_index][1] = color[1]
            self.frame[adjusted_index][2] = color[2]
        else:
            adjusted_index -= constants.LED_COUNT
            self.frame[adjusted_index][0] = 0
            self.frame[adjusted_index][1] = 0
            self.frame[adjusted_index][2] = 0

        self.frame_index += 1

        return self.frame

RAINBOW_HUE_TIME_TO_COMPLETE = 10
class RainbowHueRoutine:
    def __init__(self, number_of_leds):
        self.frame = np.zeros(shape=(number_of_leds, 3), dtype=int)
        self.hue = 0

    def get_frame(self):
        self.hue = self.hue + (1 / constants.FRAMES_PER_SECOND
            / RAINBOW_HUE_TIME_TO_COMPLETE)
        self.hue = self.hue % 1
        color = colorsys.hsv_to_rgb(self.hue, 1.0, 0.3)
        color = util.unit_color_to_byte_color(color)

        for i in range(constants.LED_COUNT):
            self.frame[i][0] = color[0]
            self.frame[i][1] = color[1]
            self.frame[i][2] = color[2]

        return self.frame

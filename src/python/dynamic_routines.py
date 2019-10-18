import numpy as np
import random
import colorsys

import constants

class LineHighlightRoutine:
    def __init__(self, number_of_leds):
        self.frame_index = 0
        self.frame = np.zeros(shape=(number_of_leds, 3), dtype=int)

    def get_new_color(self):
        self.color = colorsys.hsv_to_rgb(random.uniform(0, 1), 1.0, 0.3)
        self.color = (int(self.color[0] * 255), int(self.color[1] * 255), int(self.color[2] * 255))
        print(self.color)

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


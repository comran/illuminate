import colorsys
import numpy as np
import random

from src import constants
from src import util

SPURT_WIDTH = 90


class SpurtRoutine:
    def __init__(self):
        self.frame = np.zeros((1, constants.LED_COUNT, 3), dtype=np.uint8)
        self.spurts = list()
        self.color_generator = None

    def add_spurt(self):
        if self.color_generator is not None:
            color = self.color_generator.get_color()
        else:
            color = util.unit_color_to_byte_color( \
                colorsys.hsv_to_rgb( \
                    random.uniform(0, 1), 1.0, 1.0))

        self.spurts.append([
            random.randint(0, constants.LED_COUNT), 1, color,
            random.uniform(0.9, 2.0)
        ])

    def apply_theme(self, color_generator):
        self.color_generator = color_generator

    def clear(self):
        self.frame.fill(0)

    def get_frame(self):
        index_adjust = 0
        self.clear()

        for spurt_index in range(len(self.spurts)):
            spurt_index -= index_adjust
            spurt = self.spurts[spurt_index]
            color_multiplier = max(0, (SPURT_WIDTH - spurt[1]) / SPURT_WIDTH)
            lower_bound = int(max(0, spurt[0] - spurt[1]))
            upper_bound = int(min(constants.LED_COUNT, spurt[0] + spurt[1]))

            for i in range(lower_bound, upper_bound):
                for j in range(3):
                    self.frame[0, i, 2 - j] = min(
                        255,
                        self.frame[0, i, j] + spurt[2][j] * color_multiplier)

            self.spurts[spurt_index][1] += spurt[3]

            if color_multiplier == 0:
                del self.spurts[spurt_index]
                index_adjust += 1

        if random.uniform(0, 1) > 0.90 and len(self.spurts) < 5:
            self.add_spurt()

        return self.frame

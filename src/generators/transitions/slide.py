import numpy as np
import random

from src import constants

import cv2 as cv


class SlideTransition:
    def __init__(self, flip=False):
        self.progress = 1
        self.flip = flip
        self.step = 0.008

    def reset(self):
        self.progress = 0
        self.step = 0.004 + random.uniform(0, 1) * 0.04

    def process(self, from_routine, to_routine):
        self.progress += self.step
        self.progress = max(0, min(1, self.progress))

        if self.progress == 1:
            return to_routine.get_frame()

        if self.flip:
            result = np.concatenate(
                [to_routine.get_frame(),
                 from_routine.get_frame()], axis=1)
            transition_frame = int(constants.LED_COUNT * (1 - self.progress))
            result = result[:, transition_frame:transition_frame +
                            constants.LED_COUNT]
        else:
            result = np.concatenate(
                [from_routine.get_frame(),
                 to_routine.get_frame()], axis=1)
            transition_frame = int(constants.LED_COUNT * self.progress)
            result = result[:, transition_frame:transition_frame +
                            constants.LED_COUNT]

        return result

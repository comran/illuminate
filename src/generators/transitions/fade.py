import numpy as np
import random


class FadeTransition:
    def __init__(self):
        self.progress = 1
        self.step = 0.008

    def reset(self):
        self.progress = 0
        self.step = 0.004 + random.uniform(0, 1) * 0.04

    def process(self, from_routine, to_routine):
        self.progress += self.step
        self.progress = max(0, min(1, self.progress))

        if self.progress == 1:
            return to_routine.get_frame()

        return np.clip(from_routine.get_frame() * (1 - self.progress) + \
            to_routine.get_frame() * self.progress, 0, 255)

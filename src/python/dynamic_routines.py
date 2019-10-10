import numpy as np

class LineHighlightRoutine:
    def __init__(self, number_of_leds):
        self.frame_index = 0
        self.frame = np.zeros(shape=(number_of_leds, 3), dtype=int)

    def get_frame(self):
        return self.frame


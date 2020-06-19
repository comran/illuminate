import numpy as np

from src import constants

TDX_ROUTINE_BLUE_LEDS_END = 210
TDX_ROUTINE_WHITE_LEDS_END = 384


class TdxRoutine:
    def __init__(self):
        self.frame = np.zeros((1, constants.LED_COUNT, 3), dtype=np.uint8)
        self.apply_theme(
            np.array([255, 0, 0]), np.array([255, 255, 255]),
            np.array([51, 51, 51]))

    def apply_theme(self, color1, color2, color3):
        for i in range(constants.LED_COUNT):
            if i <= TDX_ROUTINE_BLUE_LEDS_END:
                self.frame[0, i] = color1
            elif i <= TDX_ROUTINE_WHITE_LEDS_END:
                self.frame[0, i] = color2
            else:
                self.frame[0, i] = color3

    def get_frame(self):
        return self.frame

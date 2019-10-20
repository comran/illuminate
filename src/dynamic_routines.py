import numpy as np
import random
import colorsys

import constants
import util

class LineHighlightRoutine:
    def __init__(self):
        self.frame_index = 0
        self.frame = np.zeros(shape=(constants.LED_COUNT, 3), dtype=int)

    def get_new_color(self):
        self.color = colorsys.hsv_to_rgb(random.uniform(0, 1), 1.0, 1.0)
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
    def __init__(self):
        self.hue = 0

        self.frame_index = 0
        self.frame = np.zeros(shape=(constants.LED_COUNT, 3), dtype=int)

    def get_frame(self):
        adjusted_index = self.frame_index % (constants.LED_COUNT * 2)

        self.hue = self.hue + (1 / constants.FRAMES_PER_SECOND
            / RAINBOW_HUE_TIME_TO_COMPLETE)
        self.hue = self.hue % 1
        color = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
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
    def __init__(self):
        self.frame = np.zeros(shape=(constants.LED_COUNT, 3), dtype=int)
        self.hue = 0

    def get_frame(self):
        self.hue = self.hue + (1 / constants.FRAMES_PER_SECOND
            / RAINBOW_HUE_TIME_TO_COMPLETE)
        self.hue = self.hue % 1
        color = colorsys.hsv_to_rgb(self.hue, 1.0, 1.0)
        color = util.unit_color_to_byte_color(color)

        for i in range(constants.LED_COUNT):
            self.frame[i][0] = color[0]
            self.frame[i][1] = color[1]
            self.frame[i][2] = color[2]

        return self.frame

SPURT_WIDTH = 75
class SpurtRoutine:
    def __init__(self):
        self.frame = np.zeros(shape=(constants.LED_COUNT, 3), dtype=int)
        self.spurts = list()

    def add_spurt(self):
        self.spurts.append(
            [
                random.randint(0, constants.LED_COUNT),
                1,
                util.unit_color_to_byte_color(colorsys.hsv_to_rgb(random.uniform(0, 1), random.uniform(0.7, 1), 1.0)),
                random.uniform(0.3, 0.8)
            ]
        )

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
                    self.frame[i][j] = min(255, self.frame[i][j] + spurt[2][j] * color_multiplier)

            self.spurts[spurt_index][1] += spurt[3]

            if color_multiplier == 0:
                del self.spurts[spurt_index]
                index_adjust += 1

        if random.uniform(0, 1) > 0.95 and len(self.spurts) < 8:
            self.add_spurt()

        return self.frame

class ProtobufRoutine:
    def __init__(self):
        self.frame = np.zeros(shape=(constants.LED_COUNT, 3), dtype=int)
        self.routine_protobuf = None
        self.index = 0

    def set_routine_protobuf(self, routine_protobuf):
        self.routine_protobuf = routine_protobuf

    def get_frame(self):
        if self.routine_protobuf is None or \
            len(self.routine_protobuf.frames) == 0:

            return self.frame

        frame_protobuf = self.routine_protobuf.frames[self.index]
        for i in range(len(frame_protobuf.pixel_colors)):
            color = frame_protobuf.pixel_colors[i]
            self.frame[i][0] = color & 0xFF
            self.frame[i][1] = (color >> 8) & 0xFF
            self.frame[i][2] = (color >> 16) & 0xFF

        self.index = (self.index + 1) % len(self.routine_protobuf.frames)

        return self.frame

TDX_ROUTINE_BLUE_LEDS_END = 210
TDX_ROUTINE_WHITE_LEDS_END = 384
class TdxRoutine:
    def __init__(self):
        self.frame = np.zeros(shape=(constants.LED_COUNT, 3), dtype=int)

        for i in range(constants.LED_COUNT):
            if i <= TDX_ROUTINE_BLUE_LEDS_END:
                self.frame[i][0] = 0
                self.frame[i][1] = 0
                self.frame[i][2] = 255
            elif i <= TDX_ROUTINE_WHITE_LEDS_END:
                self.frame[i][0] = 255
                self.frame[i][1] = 255
                self.frame[i][2] = 255
            else:
                self.frame[i][0] = 51
                self.frame[i][1] = 51
                self.frame[i][2] = 51

    def get_frame(self):
        return self.frame

import numpy as np

from src import constants


class ProtobufRoutine:
    def __init__(self):
        self.frame = np.zeros((1, constants.LED_COUNT, 3), dtype=int)
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
            self.frame[0, i, 0] = (color >> 16) & 0xFF
            self.frame[0, i, 1] = (color >> 8) & 0xFF
            self.frame[0, i, 2] = color & 0xFF

        self.index = (self.index + 1) % len(self.routine_protobuf.frames)

        return self.frame

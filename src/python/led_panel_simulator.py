import cv2 as cv
import numpy as np
import base64
import time

import constants
import messages_pb2

class LedPanelSimulator:
    def __init__(self, count, pin, frequency, dma_channel, invert, brightness,
                    channel):

        self.pixel_layout = self.get_pixel_layout()

        self.width = int(constants.WINDOW_WIDTH * self.pixel_layout.width)
        self.height = int(constants.WINDOW_WIDTH *
            self.pixel_layout.height / self.pixel_layout.width)

        self.visualization = np.zeros((self.height, self.width, 3), np.uint8)

        self.last_render = None

    def clear(self):
        self.visualization = np.zeros((self.height, self.width, 3))

    def set_led(self, index, color):
        x = int(self.pixel_layout.pixel_locations[index].x * self.width)
        y = int(self.pixel_layout.pixel_locations[index].y * self.height)

        color_tuple = (color[2] / 255, color[1] / 255, color[0] / 255)
        cv.circle(self.visualization, (x, y), 7, color_tuple, thickness=-1)

    def render(self):
        current_time = time.time()
        
        if self.last_render == None:
            self.last_render = current_time
        else:
            fps = 1.0 / (current_time - self.last_render)
            fps_text = str(round(fps)) + " fps"
            cv.putText(self.visualization, fps_text, (5, 25),
                cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
            self.last_render = current_time

        cv.imshow("Illuminate", self.visualization)
        cv.waitKey(1)

    def get_pixel_layout(self):
        csv_file = None
        try:
            csv_file = open("../../routines/pixels.illp")
        except IOError:
            print("Cannot open pixel locations.")
            return

        read_file = str(csv_file.readlines()[0])

        pixel_layout = messages_pb2.PixelLayout()
        pixel_layout.ParseFromString(base64.b64decode(read_file))

        return pixel_layout


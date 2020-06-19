import sys
import os
import random
import time
import logging
import logging.handlers
import cv2 as cv

import led_panel
import library
import util
import constants
import player
import frame_filter

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)


def main():
    illuminate_logger = util.get_logger()
    illuminate_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    # logger_handler = logging.handlers.RotatingFileHandler(
    #     "illuminate.log", maxBytes=1024 * 1024 * 10, backupCount=5)

    # illuminate_logger.addHandler(logger_handler)

    stdout_handler = logging.StreamHandler(sys.stdout)
    illuminate_logger.addHandler(stdout_handler)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdout_handler.setFormatter(formatter)

    illuminate_logger.info("### Illuminate ###")

    sign_player = player.Player()
    sign_filter = frame_filter.Filter()

    panel = led_panel.LedPanel(constants.LED_COUNT, constants.LED_PIN,
                               constants.LED_FREQ_HZ, constants.LED_DMA,
                               constants.LED_INVERT, constants.LED_BRIGHTNESS,
                               constants.LED_CHANNEL)

    phased_loop = util.PhasedLoop(constants.FRAMES_PER_SECOND, verbose=False)

    while True:
        phased_loop.pause()
        panel.clear()
        frame = sign_player.get_frame()
        frame = sign_filter.process(frame)

        panel.set_leds(frame)
        panel.render()


if __name__ == '__main__':
    main()

import led_panel
import library
import dynamic_routines
import util
import constants
import transitions
import player
import frame_filter

import random
import time
import logging
import logging.handlers

def main():
    illuminate_logger = util.get_logger()
    illuminate_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    logger_handler = logging.handlers.RotatingFileHandler(
                "illuminate.log", maxBytes=1024 * 1024 * 10, backupCount=5)

    illuminate_logger.addHandler(logger_handler)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_handler.setFormatter(formatter)

    illuminate_logger.info("### Illuminate ###")

    sign_player = player.Player()
    sign_filter = frame_filter.Filter()

    panel = led_panel.LedPanel(
        constants.LED_COUNT,
        constants.LED_PIN,
        constants.LED_FREQ_HZ,
        constants.LED_DMA,
        constants.LED_INVERT,
        constants.LED_BRIGHTNESS,
        constants.LED_CHANNEL)

    phased_loop = util.PhasedLoop(constants.FRAMES_PER_SECOND, verbose=False)

    next_routine_time = None

    while True:
        phased_loop.pause()
        panel.clear()
        frame = sign_player.get_frame()
        frame = sign_filter.process(frame)

        for i in range(len(frame)):
            panel.set_led(i, frame[i])

        panel.render()

if __name__ == '__main__':
    main()

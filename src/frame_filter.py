import datetime

import constants
import util

class Filter:
    def __init__(self):
        self.last_logged_brightness = -1

    def process(self, frame):
        now = datetime.datetime.now()
        hour = now.hour + now.minute / 60

        # Make math a bit easier when dealing with midnight.
        if hour < constants.ANIMATED_START_HOUR:
            hour += 24

        dim_progress = (hour - constants.DIM_FADE_START_HOUR) / \
            (constants.DIM_FADE_END_HOUR - constants.DIM_FADE_START_HOUR)

        dim_progress = max(0, min(1, dim_progress))

        brightness = constants.DIM_MAX_BRIGHTNESS - \
            (constants.DIM_MAX_BRIGHTNESS - constants.DIM_MIN_BRIGHTNESS) \
                * dim_progress

        if abs(brightness - self.last_logged_brightness) > 0.05:
            util.get_logger().debug("Brightness is currently " +
                str(brightness) + " at " + str(now.hour) + ":" +
                str("%02d" % now.minute))

            self.last_logged_brightness = brightness

        frame = frame * brightness

        return frame

import datetime

import constants

class Filter:
    def __init__(self):
        self.printed_brightness = False

    def process(self, frame):
        now = datetime.datetime.now()
        hour = now.hour

        # Make math a bit easier when dealing with midnight.
        if hour < 10:
            hour += 24

        dim_progress = (hour - constants.DIM_FADE_START_HOUR) / \
            (constants.DIM_FADE_END_HOUR - constants.DIM_FADE_START_HOUR)

        dim_progress = max(0, min(1, dim_progress))

        brightness = constants.DIM_MAX_BRIGHTNESS - \
            (constants.DIM_MAX_BRIGHTNESS - constants.DIM_MIN_BRIGHTNESS) \
                * dim_progress

        if not self.printed_brightness:
            print("Brightness is currently " + str(brightness) + " at " +
                str(now.hour) + ":" + str("%02d" % now.minute))
            self.printed_brightness = True

        frame = frame * brightness

        return frame

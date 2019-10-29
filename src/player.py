import queue
import numpy as np
import random
import time
import datetime

import util
import library
import constants

class HalloweenColorGenerator:
    def __init__(self, random_choice=True):
        self.colors = list()
        self.colors.append((247, 95, 28))
        self.colors.append((255, 154, 0))
        self.colors.append((35, 35, 35))
        self.colors.append((255, 255, 255))
        self.colors.append((136, 30, 228))
        self.colors.append((133, 226, 31))
        self.last_color = self.get_random_color()
        self.current_color = self.get_random_color()
        self.fade = 0
        self.random_choice = random_choice

    def get_color(self):
        if self.random_choice:
            return random.choice(self.colors)
        else:
            if self.fade >= 1:
                self.last_color = self.current_color
                self.current_color = self.get_random_color()
                self.fade = 0

            self.fade += 1 / (4 * constants.FRAMES_PER_SECOND)

            return self.mix_color(self.fade, self.last_color, self.current_color)

    def get_random_color(self):
        return random.choice(self.colors)

    def mix_color(self, fade, color1, color2):
        r = color1[0] * (1 - fade) + color2[0] * fade
        g = color1[1] * (1 - fade) + color2[1] * fade
        b = color1[2] * (1 - fade) + color2[2] * fade
        return (r, g, b)


class Player:
    def __init__(self):
        self.library = library.Library()

        # Halloween theme.
        now = datetime.datetime.now()

        if now.month == 10 and (now.day > 27):
            self.library.get_routine(constants.DEFAULT_ROUTINE).apply_theme( \
                (247, 95, 28), (133, 226, 31), (255, 154, 0))
            self.library.get_routine("spurt_routine").apply_theme(HalloweenColorGenerator())
            self.library.get_routine("line_highlight_routine").apply_theme(HalloweenColorGenerator())
            self.library.get_routine("rainbow_hue_routine").apply_theme(HalloweenColorGenerator(random_choice=False))
            self.library.get_routine("line_highlight_rainbow_routine").apply_theme(HalloweenColorGenerator(random_choice=False))
            active_routines = list()
            active_routines.append(constants.DEFAULT_ROUTINE)
            active_routines.append("spurt_routine")
            active_routines.append("line_highlight_routine")
            active_routines.append("rainbow_hue_routine")
            active_routines.append("line_highlight_rainbow_routine")
            self.library.set_active_routines(active_routines)
        else:
            self.library.set_active_routines(self.library.get_all_routines())

        self.routine_queue = queue.Queue()
        self.transitions_queue = queue.Queue()

        self.next_transition_timestamp = self.get_next_transition_time()
        self.previous_routine = None
        self.current_routine = self.get_next_routine()
        self.current_transition = None

        self.start_transition()

        self.default_frame = np.zeros(shape=(constants.LED_COUNT, 3), dtype=int)


    def get_next_transition_time(self):
        now = datetime.datetime.now()

        clock_start = int(time.time()) - now.second
        multiplier = int(now.second / constants.CYCLE_TIME)
        return clock_start + constants.CYCLE_TIME * (multiplier + 1)


    def get_next_routine(self):
        now = datetime.datetime.now()

        # Check whether default routine should be displayed.
        adjusted_weekday = now.weekday()
        adjusted_hour = now.hour + now.minute / constants.MINUTES_IN_HOUR
        if adjusted_hour < constants.ANIMATED_START_HOUR:
            adjusted_hour += constants.HOURS_IN_DAY
            adjusted_weekday = (adjusted_weekday - 1) % constants.DAYS_IN_WEEK

        start_animating_hour = constants.HOURS_IN_DAY + constants.ANIMATED_START_HOUR

        stop_animating_hour = constants.ANIMATED_WEEKDAY_HOURS[adjusted_weekday]
        if stop_animating_hour < constants.ANIMATED_START_HOUR:
            stop_animating_hour += constants.HOURS_IN_DAY

        if adjusted_hour >= stop_animating_hour and \
            adjusted_hour <= start_animating_hour:
            routine_name = constants.DEFAULT_ROUTINE
        else:
            routine_name = self.library.get_time_based_routine(self.next_transition_timestamp)

        return self.library.get_routine(routine_name)


    def start_transition(self):
        # Add a new item to the queues.
        self.routine_queue.put(self.get_next_routine())
        self.transitions_queue.put(self.library.get_transition(
            self.library.get_random_transition()))

        # Update currently loaded items.
        self.previous_routine = self.current_routine
        self.current_routine = self.routine_queue.get()

        # Reset state.
        if self.current_transition is not None:
            if self.current_routine is self.previous_routine:
                # Aliasing case. Don't transition to the exact same routine.
                return
            else:
                util.get_logger().debug("Transitioning from " + \
                    str(type(self.previous_routine)) + " to " + \
                        str(type(self.current_routine)))

                self.current_transition.reset()

        self.current_transition = self.transitions_queue.get()


    def get_frame(self):
        if time.time() > self.next_transition_timestamp:
            self.start_transition()
            self.next_transition_timestamp = self.get_next_transition_time()

        frame = self.current_transition.process(
            self.previous_routine, self.current_routine)

        return frame

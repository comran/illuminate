import queue
import numpy as np
import random
import time
import datetime

import util
import library
import constants

class Player:
    def __init__(self):
        self.library = library.Library()

        self.routine_queue = queue.Queue()
        self.transitions_queue = queue.Queue()

        self.previous_routine = None
        self.current_routine = self.library.get_random_routine()
        self.current_transition = None

        self.next_transition_timestamp = time.time()

        self.default_frame = np.zeros(shape=(constants.LED_COUNT, 3), dtype=int)


    def get_next_routine(self):
        now = datetime.datetime.now()

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
            routine_name = self.library.get_random_routine()

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
            self.next_transition_timestamp = time.time() + constants.CYCLE_TIME

        frame = self.current_transition.process(
            self.previous_routine, self.current_routine)

        return frame

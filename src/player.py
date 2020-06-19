import queue
import numpy as np
import random
import time
import datetime
import copy

import util
import library
import constants


class Player:
    def __init__(self):
        self.library = library.Library()

        now = datetime.datetime.now()

        adjusted_weekday = now.weekday()
        adjusted_hour = now.hour + now.minute / constants.MINUTES_IN_HOUR
        if adjusted_hour < constants.ANIMATED_START_HOUR:
            adjusted_hour += constants.HOURS_IN_DAY
            adjusted_weekday = (adjusted_weekday - 1) % constants.DAYS_IN_WEEK

        print(adjusted_weekday)
        active_routines = list()

        if not self.override_routines():
            if adjusted_weekday > 3 or True:
                active_routines = self.library.get_all_routines()
            else:
                choice_routines = list()
                choice_routines.append("line_highlight_routine")
                choice_routines.append("line_highlight_rainbow_routine")
                choice_routines.append("red_blocks")
                choice_routines.append("spurt_routine")
                choice_routines.append("bricks")
                choice_routines.append("projector_visuals")
                choice_routines.append("hues")
                active_routines.append(random.choice(choice_routines))

            self.library.set_active_routines(active_routines)

        self.routine_queue = queue.Queue()
        self.transitions_queue = queue.Queue()

        self.next_transition_timestamp = self.get_next_transition_time()
        self.previous_routine = None
        self.current_routine = self.get_next_routine()
        self.current_transition = None

        self.start_transition()

        self.default_frame = np.zeros(
            shape=(constants.LED_COUNT, 3), dtype=int)

    def override_routines(self):
        now = datetime.datetime.now()
        print("month: " + str(now.month))
        print("day: " + str(now.day))

        # if (now.month == 11 and now.day == 11) or (now.month == 5
        #                                            and now.day == 25):
        #     # Veterans day
        #     self.library.get_routine(constants.DEFAULT_ROUTINE) \
        #         .apply_theme((255, 0, 0), (255, 255, 255), (0, 0, 255))

        #     self.library.set_active_routines(list())
        #     return True

        # elif now.month == 11 and (now.day >= 18 and now.day <= 21):
        #     # USC vs UCLA football game
        #     self.library.get_routine(constants.DEFAULT_ROUTINE) \
        #         .apply_theme((0, 85, 135), (255, 209, 0), (255, 255, 255))

        #     self.library.set_active_routines(self.library.get_all_routines())
        #     return True

        # elif now.month == 4 and (now.day == 20):
        #     # 4/20
        #     self.library.get_routine(constants.DEFAULT_ROUTINE) \
        #         .apply_theme((73, 155, 74), (73, 155, 74), (73, 155, 74))

        #     self.library.set_active_routines(list())
        #     return True

        # elif ((now.month == 11 and now.day >= 22) or now.month == 12 or False):
        #     # Christmas
        #     self.library.get_routine(constants.DEFAULT_ROUTINE) \
        #         .apply_theme((0, 255, 0), (255, 0, 0), (255, 0, 18))
        #     self.library.get_routine(
        #         "line_highlight_rainbow_routine").apply_theme(
        #             ChristmasColorGenerator(random_choice=False))
        #     self.library.get_routine("line_highlight_routine").apply_theme(
        #         ChristmasColorGenerator())
        #     self.library.get_routine("spurt_routine").apply_theme(
        #         ChristmasColorGenerator())
        #     self.library.get_routine("rainbow_hue_routine").apply_theme(
        #         ChristmasColorGenerator(random_choice=False))

        #     active_routines = list()
        #     #           active_routines.append("line_highlight_routine")
        #     #           active_routines.append("spurt_routine")
        #     #           active_routines.append("barbershop_routine")
        #     #           active_routines.append("line_highlight_rainbow_routine")
        #     #           active_routines.append("rainbow_hue_routine")
        #     #           active_routines.append("christmas_diagonals")
        #     #           active_routines.append("christmas_visuals")

        #     self.library.set_active_routines(active_routines)
        #     return True

        return False

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

        stop_animating_hour = constants.ANIMATED_WEEKDAY_HOURS[
            adjusted_weekday]
        if stop_animating_hour < constants.ANIMATED_START_HOUR:
            stop_animating_hour += constants.HOURS_IN_DAY

        if adjusted_hour >= stop_animating_hour and \
            adjusted_hour <= start_animating_hour:
            routine_name = constants.DEFAULT_ROUTINE
        else:
            routine_name = self.library.get_random_routine()

        print("Next routine is " + routine_name)

        return self.library.get_routine(routine_name)

    def start_transition(self):
        # Add a new item to the queues.
        self.routine_queue.put(self.get_next_routine())
        self.transitions_queue.put(
            self.library.get_transition(self.library.get_random_transition()))

        # Update currently loaded items.
        self.previous_routine = self.current_routine

        aliased = True
        next_routine = self.routine_queue.get()

        if hasattr(next_routine, 'setup'):
            self.current_routine = copy.deepcopy(next_routine)
            self.current_routine.setup()
            aliased = False
        else:
            self.current_routine = next_routine
            aliased = self.current_routine is self.previous_routine

        # Reset state.
        if self.current_transition is not None:
            if aliased:
                # Aliasing case. Don't transition to the exact same routine.
                return
            else:
                util.get_logger().debug("Transitioning from " + \
                    str(self.previous_routine) + " to " + \
                        str(self.current_routine))

                self.current_transition.reset()

        self.current_transition = self.transitions_queue.get()

    def get_frame(self):
        if time.time() > self.next_transition_timestamp:
            self.start_transition()
            self.next_transition_timestamp = self.get_next_transition_time()

        frame = self.current_transition.process(self.previous_routine,
                                                self.current_routine)

        return frame

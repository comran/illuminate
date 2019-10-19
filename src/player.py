import queue
import numpy as np
import random
import time

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

    def start_transition(self):
        # Add a new item to the queues.
        self.routine_queue.put(self.library.get_random_routine())
        self.transitions_queue.put(self.library.get_random_transition())

        # Update currently loaded items.
        self.previous_routine = self.current_routine
        self.current_routine = self.routine_queue.get()
        
        # Reset state.
        if self.current_transition is not None:
            if self.current_routine is self.previous_routine:
                # Aliasing case. Don't transition to the exact same routine.
                return
            else:
                self.current_transition.reset()

        self.current_transition = self.transitions_queue.get()


    def get_frame(self):
        if time.time() > self.next_transition_timestamp:
            self.start_transition()
            self.next_transition_timestamp = time.time() + constants.CYCLE_TIME

        frame = self.current_transition.process(
            self.previous_routine, self.current_routine)

        return frame
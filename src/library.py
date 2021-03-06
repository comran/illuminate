import os
import base64
import random
import ntpath

import constants
import messages_pb2
import util
from generators.transitions.slide import SlideTransition
from generators.transitions.fade import FadeTransition
from generators.routines.barbershop import BarbershopRoutine
from generators.routines.line_highlight import LineHighlightRoutine
from generators.routines.line_highlight_rainbow import LineHighlightRainbowRoutine
from generators.routines.protobuf import ProtobufRoutine
from generators.routines.rainbow_hue import RainbowHueRoutine
from generators.routines.spurt import SpurtRoutine
from generators.routines.tdx import TdxRoutine


class Library:
    def __init__(self):
        self.routines = dict()
        self.transitions = dict()

        self.active_routines = list()

        # Load in transitions.
        self.transitions["fade_transition"] = FadeTransition()
        self.transitions["slide_transition"] = SlideTransition()
        self.transitions["flipped_slide_transition"] = SlideTransition(
            flip=True)

        # Load in dynamic routines.
        # self.routines[
        #     "line_highlight_routine"] = LineHighlightRoutine(
        #     )
        # self.routines[
        #     "rainbow_hue_routine"] = RainbowHueRoutine()
        # self.routines[
        #     "line_highlight_rainbow_routine"] = LineHighlightRainbowRoutine()
        self.routines["spurt_routine"] = SpurtRoutine()
        # self.routines["barbershop_routine"] = BarbershopRoutine()
        self.routines[constants.DEFAULT_ROUTINE] = TdxRoutine()

        self.dynamic_routines = list(self.routines.keys())

        # Load transitions from files.
        # self.load_from_folder(constants.ROUTINES_FOLDER)

    def get_all_routines(self):
        return self.routines.keys()

    def get_dynamic_routines(self):
        return self.dynamic_routines

    def set_active_routines(self, active_routines):
        self.active_routines = active_routines

    def get_routine(self, routine_name):
        return self.routines[routine_name]

    def get_transition(self, transition_name):
        return self.transitions[transition_name]

    def get_time_based_routine(self, timestamp):
        nondefault_routines = self.get_nondefault_routines_list()
        index = (timestamp * 11) % len(nondefault_routines)
        return nondefault_routines[index]

    def get_nondefault_routines_list(self):
        nondefault_routines = list()
        for item in self.active_routines:
            if item is not constants.DEFAULT_ROUTINE:
                nondefault_routines.append(item)

        nondefault_routines.sort()

        if len(nondefault_routines) == 0:
            nondefault_routines.append(constants.DEFAULT_ROUTINE)

        return nondefault_routines

    def get_random_routine(self):
        random_routine = random.choice(self.get_nondefault_routines_list())

        return random_routine

    def get_random_transition(self):
        return random.choice(list(self.transitions.keys()))

    def load_from_folder(self, folder):
        for root, dirs, files in os.walk(folder):
            for filename in files:
                routine_filename = root + "/" + filename
                try:
                    routine_file = open(routine_filename)
                except IOError:
                    print("Cannot open saved routine: " + routine_filename)
                    os.remove(routine_filename)
                    continue

                filename, file_extension = os.path.splitext(routine_filename)
                if file_extension != ".illr":
                    continue

                head, tail = ntpath.split(filename)
                routine_name = tail

                lines = 0
                with open(routine_filename) as f:
                    for i, l in enumerate(f):
                        lines += 1

                if lines < 1:
                    print("Routine file does not contain any data: " \
                        + routine_filename)
                    os.remove(routine_filename)
                    continue

                read_file = str(routine_file.readlines()[0])
                decoded = base64.b64decode(read_file)
                routine = messages_pb2.Routine()
                try:
                    routine.ParseFromString(decoded)
                except:
                    print("Error parsing protobuf: " + routine_filename)
                    continue

                protobuf_routine = ProtobufRoutine()
                protobuf_routine.set_routine_protobuf(routine)

                util.get_logger().debug("Opened file \"" + routine_filename +
                                        "\" with " + str(len(routine.frames)) +
                                        " frames with name " + routine_name)

                self.routines[routine_name] = protobuf_routine

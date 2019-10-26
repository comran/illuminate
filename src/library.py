import constants
import dynamic_routines
import messages_pb2
import transitions
import util

import os
import base64
import random
import ntpath

class Library:
    def __init__(self):
        self.routines = dict()
        self.transitions = dict()

        # Load in transitions.
        self.transitions["fade_transition"] = transitions.FadeTransition()

        # Load in dynamic routines.
        self.routines["line_highlight"] = dynamic_routines.LineHighlightRoutine()
        self.routines["rainbow_hue_routine"] = dynamic_routines.RainbowHueRoutine()
        self.routines["line_highlight_rainbow_routine"] = dynamic_routines.LineHighlightRainbowRoutine()
        self.routines["spurt_routine"] = dynamic_routines.SpurtRoutine()
        self.routines[constants.DEFAULT_ROUTINE] = dynamic_routines.TdxRoutine()

        # Load transitions from files.
        self.load_from_folder(constants.ROUTINES_FOLDER)

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
        for item in self.routines.keys():
            if item is not constants.DEFAULT_ROUTINE:
                nondefault_routines.append(item)

        nondefault_routines.sort()

        return nondefault_routines

    def get_random_routine(self):
        while True:
            random_routine = random.choice(list(self.routines.keys()))
            if random_routine != constants.DEFAULT_ROUTINE or len(self.routines.keys()) == 1:
                break

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

                protobuf_routine = dynamic_routines.ProtobufRoutine()
                protobuf_routine.set_routine_protobuf(routine)

                util.get_logger().debug("Opened file \"" + routine_filename +
                    "\" with " + str(len(routine.frames)) +
                    " frames with name " + routine_name)

                self.routines[routine_name] = protobuf_routine

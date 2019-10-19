import constants
import dynamic_routines
import messages_pb2
import transitions

import os
import base64
import random

class Library:
    def __init__(self):
        self.routines = dict()
        self.transitions = dict()

        # Load in transitions.
        self.transitions["fade_transition"] = transitions.FadeTransition()

        # Load in dynamic routines.
        self.routines["line_highlight"] = \
            dynamic_routines.LineHighlightRoutine(constants.LED_COUNT)
        self.routines["rainbow_hue_routine"] = \
            dynamic_routines.RainbowHueRoutine(constants.LED_COUNT)
        self.routines["line_highlight_rainbow_routine"] = \
            dynamic_routines.LineHighlightRainbowRoutine(constants.LED_COUNT)

        # Load transitions from files.
        self.load_from_folder(constants.ROUTINES_FOLDER)

    def get_routine(self, routine_name):
        return self.routines[routine_name]

    def get_transition(self, transition_name):
        return self.transitions[transition_name]

    def get_random_routine(self):
        return self.get_routine(random.choice(list(self.routines.keys())))
    
    def get_random_transition(self):
        return self.get_transition(random.choice(list(self.transitions.keys())))

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
                    os.remove(routine_filename)
                    continue

                print("Opened file \"" + routine.name + "\" with " \
                    + str(len(routine.frames)) + " frames")
                

                protobuf_routine = dynamic_routines.ProtobufRoutine(constants.LED_COUNT)
                protobuf_routine.set_routine_protobuf(routine)

                self.routines[routine.name] = protobuf_routine

import os
import base64
import messages_pb2

class Library:
    def __init__(self):
        self.routines = dict()

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
                
                self.routines[routine.name] = routine

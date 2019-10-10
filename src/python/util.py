import time
import rpi_ws281x

class PhasedLoop:
    def __init__(self, frequency, verbose=False):
        self.frequency = frequency
        self.last_pause = None
        self.slowing_down = False
        self.verbose = verbose
        self.counter = 0

    def pause(self):
        current_time = time.time()

        if self.last_pause == None:
            self.last_pause = current_time
            return

        time_to_pause = 1.0 / self.frequency - (current_time - self.last_pause)
        time_to_pause = max(0.0, time_to_pause)
        if time_to_pause == 0.0 and not self.slowing_down:
            print("Phased loop is running slow!")
            self.slowing_down = True
        else:
            self.slowing_down = False

        time.sleep(time_to_pause)
        self.last_pause = time.time()

        if self.verbose and self.counter == 0:
            print("Loop frequency: " \
                    + str(round(1.0 / (self.last_pause - current_time), 1)))

        self.counter = (self.counter + 1) % self.frequency

def numpy_to_ws281x_pixel(numpy_pixel):
    return  rpi_ws281x.Color(
        int(numpy_pixel[0]),
        int(numpy_pixel[1]),
        int(numpy_pixel[2]))


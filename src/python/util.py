import time
import rpi_ws281x

class PhasedLoop:
    def __init__(self, frequency, verbose=False):
        self.frequency = frequency
        self.last_pause = None
        self.verbose = verbose
        self.counter = 0

    def pause(self):
        current_time = time.time()

        if self.last_pause == None:
            self.last_pause = current_time
            return

        time_to_pause = 1.0 / self.frequency - (current_time - self.last_pause)
        time_to_pause = max(0.0, time_to_pause)
        frequency = 1.0 / (current_time - self.last_pause)
        time.sleep(time_to_pause)
        self.last_pause = current_time + 1.0 / self.frequency

        if self.verbose and self.counter == 0:
            print(time_to_pause)
            print("Loop frequency: " + str(frequency))

        self.counter = (self.counter + 1) % (3 * self.frequency)


def numpy_to_ws281x_pixel(numpy_pixel):
    return  rpi_ws281x.Color(
        int(numpy_pixel[0]),
        int(numpy_pixel[1]),
        int(numpy_pixel[2]))


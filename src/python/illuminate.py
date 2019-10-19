import led_panel
import library
import dynamic_routines
import util
import constants

import random
import time

def main():
    print("### Illuminate ###")

    routine_library = library.Library()
    #routine_library.load_from_folder(ROUTINES_FOLDER)

    current_routine = None
    routines = list()

    routines.append(dynamic_routines.LineHighlightRoutine(constants.LED_COUNT))
    routines.append(dynamic_routines.RainbowHueRoutine(constants.LED_COUNT))
    routines.append(dynamic_routines.LineHighlightRainbowRoutine(constants.LED_COUNT))

    panel = led_panel.LedPanel(constants.LED_COUNT,
        constants.LED_PIN,
        constants.LED_FREQ_HZ,
        constants.LED_DMA,
        constants.LED_INVERT,
        constants.LED_BRIGHTNESS,
        constants.LED_CHANNEL)

    phased_loop = util.PhasedLoop(constants.FRAMES_PER_SECOND, verbose=False)

    next_routine_time = None

    while True:
        phased_loop.pause()

        panel.clear()

        if next_routine_time is None or time.time() > next_routine_time:
            current_routine = random.choice(routines)
            print(current_routine)
            next_routine_time = time.time() + constants.CYCLE_TIME
        
        frame = current_routine.get_frame()
        count = 0

        for color in frame:
            panel.set_led(count, color)
            count += 1

        panel.render()

if __name__ == '__main__':
    main()

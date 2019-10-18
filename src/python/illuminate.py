import led_panel
import library
import dynamic_routines
import util
import constants



def main():
    print("### Illuminate ###")

    routine_library = library.Library()
    #routine_library.load_from_folder(ROUTINES_FOLDER)

    line_highlight_routine = dynamic_routines.LineHighlightRoutine(constants.LED_COUNT)

    panel = led_panel.LedPanel(constants.LED_COUNT,
        constants.LED_PIN,
        constants.LED_FREQ_HZ,
        constants.LED_DMA,
        constants.LED_INVERT,
        constants.LED_BRIGHTNESS,
        constants.LED_CHANNEL)

    phased_loop = util.PhasedLoop(constants.FRAMES_PER_SECOND, verbose=False)

    while True:
        phased_loop.pause()

        frame = line_highlight_routine.get_frame()
        count = 0

        # print(frame)

        for pixel in frame:
            color = util.numpy_to_ws281x_pixel(pixel)

            panel.strip.setPixelColor(count, color)
            count += 1

        panel.render()

if __name__ == '__main__':
    main()

import led_panel
import library
import dynamic_routines
import util


# Constants
ROUTINES_FOLDER="routines"
FRAMES_PER_SECOND = 30
LED_COUNT = 551       # Number of LED pixels.
LED_PIN = 10          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def main():
    print("### Illuminate ###")
    routine_library = library.Library()
    #routine_library.load_from_folder(ROUTINES_FOLDER)

    line_highlight_routine = dynamic_routines.LineHighlightRoutine(LED_COUNT)

#   panel = led_panel.LedPanel(LED_COUNT,
#       LED_PIN,
#       LED_FREQ_HZ,
#       LED_DMA,
#       LED_INVERT,
#       LED_BRIGHTNESS,
#       LED_CHANNEL)

    phased_loop = util.PhasedLoop(FRAMES_PER_SECOND, verbose=True)

    while True:
        phased_loop.pause()

        frame = line_highlight_routine.get_frame()
        count = 0
        for pixel in frame:
            color = util.numpy_to_ws281x_pixel(pixel)

            #panel.strip.setPixelColor(count, color)
            count += 1

if __name__ == '__main__':
    main()

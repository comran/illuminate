import util

# Constants
ROUTINES_FOLDER = "generators/rendered"
FRAMES_PER_SECOND = 30
LED_COUNT = 551  # Number of LED pixels.
LED_PIN = 10  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

WINDOW_WIDTH = 1920
# CYCLE_TIME = 20
CYCLE_TIME = 5

MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24
DAYS_IN_WEEK = 7

DIM_FADE_START_HOUR = 12 + 7
DIM_FADE_END_HOUR = 12 + 11
DIM_MAX_BRIGHTNESS = 1.0

DIM_MIN_BRIGHTNESS = 1.0
if util.is_raspi():
    DIM_MIN_BRIGHTNESS = DIM_MAX_BRIGHTNESS * 0.5

DEFAULT_ROUTINE = "tdx_routine"

ANIMATED_START_HOUR = 9
ANIMATED_WEEKDAY_HOURS = (
    # Monday
    23,

    # Tuesday
    23,

    # Wednesday
    23,

    # Thursday
    3,

    # Friday
    3,

    # Saturday
    4,

    # Sunday
    0)

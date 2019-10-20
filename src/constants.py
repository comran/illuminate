import util

# Constants
ROUTINES_FOLDER="routines"
FRAMES_PER_SECOND = 40
LED_COUNT = 551       # Number of LED pixels.
LED_PIN = 10          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

WINDOW_WIDTH = 1920
CYCLE_TIME = 15

MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24
DAYS_IN_WEEK = 7

DIM_FADE_START_HOUR = 12 + 8
DIM_FADE_END_HOUR = 12 + 11
DIM_MAX_BRIGHTNESS = 0.8

if util.is_raspi():
    DIM_MIN_BRIGHTNESS = 0.3
else:
    DIM_MIN_BRIGHTNESS = 1.0

DEFAULT_ROUTINE = "tdx_routine"

ANIMATED_START_HOUR = 9
ANIMATED_WEEKDAY_HOURS = (
    # Monday
    22,

    # Tuesday
    22,

    # Wednesday
    22,

    # Thursday
    22,

    # Friday
    2,

    # Saturday
    2,

    # Sunday
    0,
)

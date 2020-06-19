import led_panel_simulator
import util
import constants

import rpi_ws281x
import os


class LedPanel:
    def __init__(self, count, pin, frequency, dma_channel, invert, brightness,
                 channel):

        if util.is_raspi():
            self.strip = rpi_ws281x.PixelStrip(count, pin, frequency,
                                               dma_channel, invert, brightness,
                                               channel)

            self.strip.begin()
        else:
            self.strip = None
            self.led_panel_simulator = led_panel_simulator.LedPanelSimulator(
                count, pin, frequency, dma_channel, invert, brightness,
                channel)

    def clear(self):
        if self.strip:
            pass
        else:
            self.led_panel_simulator.clear()

    def set_leds(self, leds):
        if self.strip is not None:
            for i in range(constants.LED_COUNT):
                color_ws281x = util.numpy_to_ws281x_pixel(leds[0, i])
                self.strip.setPixelColor(i, color_ws281x)
        else:
            self.led_panel_simulator.set_leds(leds)

    def render(self):
        if self.strip is not None:
            self.strip.show()
        else:
            self.led_panel_simulator.render()

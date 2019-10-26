import led_panel_simulator
import util

import rpi_ws281x
import os

class LedPanel:
    def __init__(self, count, pin, frequency, dma_channel, invert, brightness,
                    channel):

        if util.is_raspi():
            self.strip = rpi_ws281x.PixelStrip(
                count,
                pin,
                frequency,
                dma_channel,
                invert,
                brightness,
                channel)

            self.strip.begin()
        else:
            self.strip = None
            self.led_panel_simulator = led_panel_simulator.LedPanelSimulator(
                count, pin, frequency, dma_channel, invert, brightness, channel)

    def clear(self):
        if self.strip:
            pass
        else:
            self.led_panel_simulator.clear()

    def set_led(self, index, color):
        if self.strip is not None:
            color_ws281x = util.numpy_to_ws281x_pixel(color)
            self.strip.setPixelColor(index, color_ws281x)
        else:
            self.led_panel_simulator.set_led(index, color)

    def render(self):
        if self.strip is not None:
            self.strip.show()
        else:
            self.led_panel_simulator.render()

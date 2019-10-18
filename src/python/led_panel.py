import rpi_ws281x

class LedPanel:
    def __init__(self, count, pin, frequency, dma_channel, invert, brightness,
                    channel):

        self.strip = rpi_ws281x.PixelStrip(
            count,
            pin,
            frequency,
            dma_channel,
            invert,
            brightness,
            channel)

        self.strip.begin()
    
    def render(self):
        self.strip.show()
